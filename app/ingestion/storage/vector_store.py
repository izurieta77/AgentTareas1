"""
vector_store.py
===============
Gestiona la indexación y búsqueda de chunks hijos en Qdrant (modo embebido local).

Arquitectura de la colección
-----------------------------
  - Nombre         : configurable (por defecto "industrial_chunks")
  - Distancia      : Cosine (estándar para embeddings de texto)
  - Dimensiones    : 1024 (BAAI/bge-m3)
  - Índice HNSW    : m=16, ef_construct=100 (calidad/memoria equilibrada)
  - Payload indexes:
      project_id      → KeywordIndex  (pre-filtrado RBAC por proyecto)
      doc_type        → KeywordIndex  (pre-filtrado por tipo documental)
      confidentiality → KeywordIndex  (pre-filtrado por nivel de acceso)

Modelo de embeddings
---------------------
  BAAI/bge-m3 (sentence-transformers):
  - 1024 dimensiones
  - Soporte nativo español + inglés (multilingüe)
  - ~2.2 GB en disco, se descarga automáticamente la primera vez
  - Inicialización perezosa (lazy) para no bloquear el arranque del sistema

Upgrade path a producción
--------------------------
  Para apuntar al servidor Qdrant en producción, basta con cambiar:
    QdrantClient(path="./qdrant_db")
  por:
    QdrantClient(url="http://qdrant:6333", api_key="...")
  sin modificar ningún otro código.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.ingestion.chunking.splitter import ChildChunk


# ---------------------------------------------------------------------------
# Constantes de configuración
# ---------------------------------------------------------------------------

# Modelo de desarrollo (384 dims, nativo safetensors, funciona en Windows sin permisos especiales)
_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_VECTOR_SIZE = 384
# Modelo de producción recomendado (1024 dims, multilingüe ES+EN):
#   BAAI/bge-m3 — requiere Windows Developer Mode habilitado para symlinks de HuggingFace
#   En Linux/Mac no tiene restricciones. Para cambiar, actualiza _EMBEDDING_MODEL y _VECTOR_SIZE=1024.
_HNSW_M = 16
_HNSW_EF_CONSTRUCT = 100
_BATCH_SIZE = 64  # Número de chunks a vectorizar y subir en cada batch


# ---------------------------------------------------------------------------
# VectorStoreManager
# ---------------------------------------------------------------------------

class VectorStoreManager:
    """
    Gestiona la conexión, indexación y búsqueda semántica en Qdrant.

    Parámetros
    ----------
    collection_name : str
        Nombre de la colección Qdrant.
    qdrant_path : str
        Ruta local para Qdrant en modo embebido. Si se pasa ``qdrant_url``,
        este parámetro se ignora.
    qdrant_url : str | None
        URL del servidor Qdrant en producción (ej. "http://qdrant:6333").
    embedding_model : str
        Nombre del modelo de SentenceTransformer a usar.
    """

    def __init__(
        self,
        collection_name: str = "industrial_chunks",
        qdrant_path: str = "./qdrant_db",
        qdrant_url: Optional[str] = None,
        embedding_model: str = _EMBEDDING_MODEL,
        vector_size: int = _VECTOR_SIZE,
    ) -> None:
        self.collection_name = collection_name
        self.qdrant_path = qdrant_path
        self.qdrant_url = qdrant_url
        self.embedding_model_name = embedding_model
        self.vector_size = vector_size

        # Lazy initialization — los modelos pesan ~2.2 GB, no los cargamos
        # hasta que se necesiten por primera vez.
        self._client: Optional[QdrantClient] = None
        self._embedder = None  # SentenceTransformer

    # ------------------------------------------------------------------
    # Lazy init helpers
    # ------------------------------------------------------------------

    def _get_client(self) -> QdrantClient:
        if self._client is None:
            if self.qdrant_url:
                self._client = QdrantClient(url=self.qdrant_url)
            else:
                self._client = QdrantClient(path=self.qdrant_path)
            self._ensure_collection()
        return self._client

    def _get_embedder(self):
        if self._embedder is None:
            import os
            # CVE-2025-32434: transformers >= 4.51 bloquea torch.load en torch < 2.6.
            # La excepción se aplica solo a archivos .bin; safetensors no tiene restricción.
            # Forzamos la carga exclusiva de safetensors via variable de entorno.
            os.environ.setdefault("SAFETENSORS_FAST_GPU", "1")
            os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

            from sentence_transformers import SentenceTransformer

            # Intentamos primero con use_safetensors (sentence-transformers >= 3.x)
            self._embedder = SentenceTransformer(self.embedding_model_name)

        return self._embedder

    def _ensure_collection(self) -> None:
        """Crea la colección si no existe, con la configuración HNSW correcta."""
        client = self._client
        existing = [c.name for c in client.get_collections().collections]

        if self.collection_name not in existing:
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self.vector_size,
                    distance=qmodels.Distance.COSINE,
                ),
                hnsw_config=qmodels.HnswConfigDiff(
                    m=_HNSW_M,
                    ef_construct=_HNSW_EF_CONSTRUCT,
                ),
            )

            # Crear índices de payload para pre-filtrado eficiente
            for field_name in ("project_id", "doc_type", "confidentiality"):
                client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field_name,
                    field_schema=qmodels.PayloadSchemaType.KEYWORD,
                )

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def add_child_chunks(self, children: List[ChildChunk]) -> int:
        """
        Vectoriza e indexa los chunks hijos en Qdrant en lotes.

        Parámetros
        ----------
        children : List[ChildChunk]
            Lista de chunks hijos generados por el splitter.

        Returns
        -------
        int
            Número de puntos indexados correctamente.
        """
        if not children:
            return 0

        client = self._get_client()
        embedder = self._get_embedder()
        all_points: List[qmodels.PointStruct] = []

        # Procesar en batches para no saturar la GPU/RAM
        for batch_start in range(0, len(children), _BATCH_SIZE):
            batch = children[batch_start: batch_start + _BATCH_SIZE]
            texts = [c.content for c in batch]

            # Vectorizar el batch completo
            vectors = embedder.encode(
                texts,
                batch_size=_BATCH_SIZE,
                show_progress_bar=False,
                normalize_embeddings=True,  # Normalización para distancia coseno
            ).tolist()

            # Construir los PointStruct para Qdrant
            for child, vector in zip(batch, vectors):
                # Qdrant necesita UUIDs como IDs de punto
                point_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, child.id))
                all_points.append(
                    qmodels.PointStruct(
                        id=point_uuid,
                        vector=vector,
                        payload={
                            **child.metadata,
                            "child_id": child.id,      # ID original del chunk
                            "content": child.content,  # Texto para recuperación directa
                        },
                    )
                )

        # Upsert único de todos los puntos en Qdrant (un solo commit en disco)
        if all_points:
            client.upsert(
                collection_name=self.collection_name,
                points=all_points,
            )

        return len(all_points)


    def search_similar(
        self,
        query: str,
        filter_rules: Optional[Dict[str, Any]] = None,
        limit: int = 5,
        score_threshold: float = 0.0,
    ) -> List[qmodels.ScoredPoint]:
        """
        Busca los chunks hijos más similares a la query con pre-filtrado.

        Parámetros
        ----------
        query : str
            Consulta del usuario en lenguaje natural.
        filter_rules : dict | None
            Diccionario de filtros {campo: valor} para pre-filtrado en Qdrant.
            Ejemplo: {"project_id": "PRJ-HELIOS", "doc_type": "DATASHEET"}
        limit : int
            Número máximo de resultados a devolver.
        score_threshold : float
            Umbral mínimo de similitud (0.0 = sin umbral).

        Returns
        -------
        List[ScoredPoint]
            Lista de puntos Qdrant con score y payload completo.
        """
        client = self._get_client()
        embedder = self._get_embedder()

        query_vector = embedder.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        # Construir el filtro de Qdrant si se proporcionaron reglas
        qdrant_filter = None
        if filter_rules:
            conditions = [
                qmodels.FieldCondition(
                    key=field,
                    match=qmodels.MatchValue(value=value),
                )
                for field, value in filter_rules.items()
            ]
            qdrant_filter = qmodels.Filter(must=conditions)

        # qdrant-client >= 1.7.0: usar query_points() en lugar del deprecado search()
        response = client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=qdrant_filter,
            limit=limit,
            score_threshold=score_threshold if score_threshold > 0 else None,
        )

        return response.points


    def delete_by_source(self, source_path: str) -> int:
        """
        Elimina todos los vectores asociados a un documento origen.
        
        Parámetros
        ----------
        source_path : str
            Ruta del archivo original tal como se guardó en metadatos ('source').
            
        Returns
        -------
        int
            1 si la operación fue exitosa, 0 si falló.
        """
        client = self._get_client()
        try:
            delete_filter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="source",
                        match=qmodels.MatchValue(value=source_path)
                    )
                ]
            )
            client.delete(
                collection_name=self.collection_name,
                points_selector=delete_filter
            )
            return 1
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error al eliminar vectores de '{source_path}': {e}")
            return 0


    def collection_info(self) -> Dict[str, Any]:
        """Devuelve información de la colección (puntos indexados, estado, etc.)."""
        client = self._get_client()
        info = client.get_collection(self.collection_name)
        # qdrant-client >= 1.7: vectors_count fue renombrado a points_count en CollectionInfo
        points = getattr(info, "points_count", None) or getattr(info, "vectors_count", 0)
        return {
            "collection_name": self.collection_name,
            "points_count": points,
            "status": str(info.status),
            "vector_size": self.vector_size,
            "embedding_model": self.embedding_model_name,
        }

