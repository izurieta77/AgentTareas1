"""
engine.py
=========
Orquestador central de búsqueda y recuperación (Retrieval Engine) del RAG Industrial.

Flujo de ejecución de retrieve()
--------------------------------
  1. TRANSFORMACIÓN: Aplica Multi-Query o HyDE si se configuran (a través de QueryTransformer).
  2. BÚSQUEDA DENSA: Busca en Qdrant (usando vectores cosine de all-MiniLM-L6-v2).
  3. BÚSQUEDA LÉXICA: Busca con la clase propia BM25 (en memoria, cargando desde Qdrant scroll).
  4. FUSIÓN (RRF): Combina los rankings de Dense y Sparse mediante Reciprocal Rank Fusion.
  5. HIDRATACIÓN: Traduce los IDs de chunks hijos al chunk padre correspondiente de DocStore.
  6. RE-ORDERING: Pasa los chunks padres e inyecta la consulta al Cross-Encoder local.
  7. RETORNO: Devuelve el Top-K ordenado de chunks padres con su score semántico final.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.chunking.splitter import ParentChunk
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.reranker import CrossEncoderReranker
from app.retrieval.transformation import QueryTransformer

logger = logging.getLogger(__name__)


class RetrievalEngine:
    """
    Motor de búsqueda avanzada que orquesta Multi-Query, HyDE, Búsqueda Híbrida,
    RRF, Hidratación de Padres y Re-ranking.
    """

    def __init__(
        self,
        pipeline: IngestionPipeline,
        api_key: Optional[str] = None,
        llm_model: str = "gemini-3.5-flash",
        reranker_model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        bm25_k1: float = 1.5,
        bm25_b: float = 0.75,
    ) -> None:
        self.pipeline = pipeline
        
        # Inicializar componentes
        self.transformer = QueryTransformer(
            api_key=api_key,
            model=llm_model,
        )
        self.reranker = CrossEncoderReranker(model_name=reranker_model_name)
        self.bm25 = BM25Retriever(k1=bm25_k1, b=bm25_b)
        
        self._bm25_indexed = False

    def _ensure_bm25_index(self, force: bool = False) -> None:
        """
        Garantiza que el índice BM25 en memoria esté construido.
        Hace scroll de todos los puntos de la colección de Qdrant.
        """
        if self._bm25_indexed and not force:
            return

        client = self.pipeline.vector_store._get_client()
        collection_name = self.pipeline.vector_store.collection_name

        try:
            # Obtener todos los puntos almacenados (limit=10000 para PoC)
            points, _ = client.scroll(
                collection_name=collection_name,
                limit=10000,
                with_payload=True,
                with_vectors=False,
            )

            documents = []
            for p in points:
                payload = p.payload or {}
                child_id = payload.get("child_id") or str(p.id)
                content = payload.get("content", "")
                documents.append({"id": child_id, "content": content})

            self.bm25.index_documents(documents)
            self._bm25_indexed = True
            logger.info(f"Índice BM25 inicializado con {len(documents)} fragmentos hijo de Qdrant.")
        except Exception as e:
            logger.error(f"Error al inicializar el índice BM25 desde Qdrant: {e}")
            # Inicializar con lista vacía para no romper el flujo
            self.bm25.index_documents([])
            self._bm25_indexed = False

    def retrieve(
        self,
        query: str,
        filter_rules: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        use_hyde: bool = False,
        use_multiquery: bool = False,
        rrf_k: int = 60,
        candidates_limit: int = 20,
    ) -> List[Tuple[ParentChunk, float]]:
        """
        Realiza la recuperación avanzada de chunks padres aplicando todo el pipeline.
        
        Parámetros
        ----------
        query : str
            Pregunta original del usuario.
        filter_rules : dict | None
            Filtros para Qdrant (RBAC, project_id, etc.).
        top_k : int
            Número final de chunks padres a devolver.
        use_hyde : bool
            Si True, genera un documento hipotético para realizar la búsqueda vectorial.
        use_multiquery : bool
            Si True, expande la consulta a variantes antes de buscar.
        rrf_k : int
            Constante para el cálculo de RRF (por defecto 60).
        candidates_limit : int
            Número de candidatos a extraer en la primera fase para fusionar y reordenar.
            
        Returns
        -------
        List[Tuple[ParentChunk, float]]
            Lista de parejas (ParentChunk, score) ordenadas de mejor a peor por el Reranker.
        """
        # Asegurar índice BM25 cargado
        self._ensure_bm25_index()

        # ------------------------------------------------------------------
        # 1. QUERY TRANSFORMATION
        # ------------------------------------------------------------------
        queries_dense = [query]
        
        if use_hyde:
            hyde_doc = self.transformer.generate_hyde_document(query)
            queries_dense = [hyde_doc]
        elif use_multiquery:
            queries_dense = self.transformer.generate_alternative_queries(query)

        # ------------------------------------------------------------------
        # 2. DENSE RETRIEVAL (Búsqueda Vectorial)
        # ------------------------------------------------------------------
        # Agrupar resultados densos combinando puntuaciones si hay Multi-Query
        dense_hits_map: Dict[str, Tuple[Any, float]] = {}  # child_id -> (hit_point, max_score)
        
        for q_dense in queries_dense:
            try:
                # Buscamos en Qdrant
                hits = self.pipeline.vector_store.search_similar(
                    query=q_dense,
                    filter_rules=filter_rules,
                    limit=candidates_limit,
                )
                for h in hits:
                    child_id = h.payload.get("child_id")
                    if not child_id:
                        continue
                    # Si ya existe, guardamos el score máximo encontrado
                    if child_id in dense_hits_map:
                        dense_hits_map[child_id] = (
                            dense_hits_map[child_id][0],
                            max(dense_hits_map[child_id][1], h.score),
                        )
                    else:
                        dense_hits_map[child_id] = (h, h.score)
            except Exception as e:
                logger.error(f"Error en búsqueda densa para query '{q_dense}': {e}")

        # Ordenar lista combinada densa por score de mayor a menor
        dense_rank = sorted(
            dense_hits_map.values(),
            key=lambda x: x[1],
            reverse=True,
        )
        # Convertir a lista de IDs para el RRF
        dense_ordered_ids = [h[0].payload["child_id"] for h in dense_rank]

        # ------------------------------------------------------------------
        # 3. SPARSE RETRIEVAL (Búsqueda Léxica BM25)
        # ------------------------------------------------------------------
        # La búsqueda léxica siempre se hace sobre la consulta original
        sparse_hits = self.bm25.search(query, top_k=candidates_limit)
        sparse_ordered_ids = [doc_id for doc_id, _ in sparse_hits]

        # ------------------------------------------------------------------
        # 4. RANK FUSION (RRF)
        # ------------------------------------------------------------------
        rrf_scores: Dict[str, float] = {}
        
        # Procesar posiciones de la búsqueda densa
        for rank, child_id in enumerate(dense_ordered_ids, start=1):
            rrf_scores[child_id] = rrf_scores.get(child_id, 0.0) + 1.0 / (rrf_k + rank)
            
        # Procesar posiciones de la búsqueda léxica
        for rank, child_id in enumerate(sparse_ordered_ids, start=1):
            rrf_scores[child_id] = rrf_scores.get(child_id, 0.0) + 1.0 / (rrf_k + rank)

        # Ordenar candidatos fusionados
        fused_candidates = sorted(
            rrf_scores.keys(),
            key=lambda x: rrf_scores[x],
            reverse=True,
        )[:candidates_limit]

        # ------------------------------------------------------------------
        # 5. HIDRATACIÓN (Recuperar Chunks Padre y eliminar duplicados)
        # ------------------------------------------------------------------
        parent_chunks: List[ParentChunk] = []
        seen_parents: Set[str] = set()

        # Necesitamos el mapeo de child_id -> parent_id
        # Lo podemos sacar del payload de los hits densos acumulados,
        # o consultarlo a Qdrant si no lo tenemos en memoria.
        child_to_parent: Dict[str, str] = {}
        for child_id, (h, _) in dense_hits_map.items():
            parent_id = h.payload.get("parent_id")
            if parent_id:
                child_to_parent[child_id] = parent_id

        # Si faltan mapeos (ej. chunks que solo aparecieron en BM25),
        # los consultamos rápido a Qdrant por scroll/ID
        missing_ids = [cid for cid in fused_candidates if cid not in child_to_parent]
        if missing_ids:
            try:
                client = self.pipeline.vector_store._get_client()
                collection_name = self.pipeline.vector_store.collection_name
                
                # Consultamos por ID en Qdrant
                for cid in missing_ids:
                    # En vector_store.py el UUID de Qdrant es derivado por uuid5 de child_id
                    import uuid
                    point_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, cid))
                    points_retrieved = client.retrieve(
                        collection_name=collection_name,
                        ids=[point_uuid],
                        with_payload=True,
                        with_vectors=False,
                    )
                    if points_retrieved:
                        parent_id = points_retrieved[0].payload.get("parent_id")
                        if parent_id:
                            child_to_parent[cid] = parent_id
            except Exception as e:
                logger.error(f"Error al recuperar parent_ids faltantes de Qdrant: {e}")

        # Hidratar padres usando DocStore
        for child_id in fused_candidates:
            parent_id = child_to_parent.get(child_id)
            if not parent_id or parent_id in seen_parents:
                continue

            parent = self.pipeline.retrieve_parent(parent_id)
            if parent:
                parent_chunks.append(parent)
                seen_parents.add(parent_id)

        # ------------------------------------------------------------------
        # 6. RE-RANKING CON CROSS-ENCODER LOCAL
        # ------------------------------------------------------------------
        # Pasamos la consulta original y los chunks padres al reranker
        if not parent_chunks:
            return []

        reranked_results = self.reranker.rerank(
            query=query,
            candidates=parent_chunks,
            top_n=top_k,
        )

        return reranked_results
