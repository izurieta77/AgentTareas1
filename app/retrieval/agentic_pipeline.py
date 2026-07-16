"""
agentic_pipeline.py
===================
Orquestador de alto nivel (Agentic RAG) que unifica el Enrutador, el Motor de
Búsqueda, el Compresor Contextual y el Generador Grounded.
"""

from typing import Any, Dict, Optional

from app.retrieval.engine import RetrievalEngine
from app.retrieval.router import AgenticRouter, RouteCategory
from app.retrieval.compressor import ContextCompressor
from app.retrieval.generator import GroundedGenerator

class AgenticRAGPipeline:
    """
    Pipeline completo que recibe la consulta del usuario y devuelve
    la respuesta final junto con la trazabilidad del proceso.
    """
    
    def __init__(
        self,
        retrieval_engine: RetrievalEngine,
        api_key: Optional[str] = None,
        llm_model: str = "gemini-3.5-flash"
    ):
        self.engine = retrieval_engine
        
        # Inicializar componentes agénticos
        self.router = AgenticRouter(
            api_key=api_key,
            model=llm_model
        )
        
        # Reutilizamos el reranker local del engine para no cargar múltiples modelos
        self.compressor = ContextCompressor(reranker=self.engine.reranker)
        
        self.generator = GroundedGenerator(
            api_key=api_key,
            model=llm_model,
            temperature=0.0  # Temperatura 0 para evitar alucinaciones
        )
        
    def query(self, user_query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo de RAG Agéntico.
        
        Parámetros
        ----------
        user_query : str
            La consulta original del usuario.
        filters : dict | None
            Filtros para Qdrant (ej. project_id).
            
        Returns
        -------
        dict
            Respuesta generada, fuentes y metadatos de trazabilidad.
        """
        # 1. Enrutamiento Inteligente
        category = self.router.route_query(user_query)
        
        # 2. Configurar parámetros de Retrieval según categoría
        top_k = 5
        use_hyde = False
        use_multiquery = False
        
        if category == RouteCategory.LINEA_PRODUCCION:
            # Latencia mínima, búsqueda directa y rápida. 
            # Los fallos en línea son urgentes.
            top_k = 4
            use_hyde = False
            use_multiquery = False
            top_n_sentences = 3
        elif category == RouteCategory.I_D_PATENTES:
            # Búsqueda profunda conceptual
            top_k = 6
            use_hyde = True
            top_n_sentences = 6
        elif category == RouteCategory.ESPECIFICACIONES:
            # Búsqueda exacta sin alterar la query (HyDE alucina o modifica cifras en la expansión)
            top_k = 5
            use_hyde = False
            use_multiquery = True
            top_n_sentences = 5
        else:
            top_n_sentences = 5
            
        # 3. Retrieval Avanzado Híbrido (Denso + Sparse BM25 + RRF + CrossEncoder)
        retrieved_results = self.engine.retrieve(
            query=user_query,
            filter_rules=filters,
            top_k=top_k,
            use_hyde=use_hyde,
            use_multiquery=use_multiquery
        )
        
        # Extraemos solo los objetos ParentChunk descartando el score del RRF/CrossEncoder 
        # (ya vienen ordenados)
        parents = [chunk for chunk, score in retrieved_results]
        
        # 4. Compresión Contextual (Mitigación Lost in the Middle)
        compressed_parents = self.compressor.compress_list(
            query=user_query,
            parents=parents,
            top_n_sentences_per_chunk=top_n_sentences
        )
        
        # 5. Generación Grounded (Llamada final al LLM)
        generation_result = self.generator.generate_response(
            query=user_query,
            contexts=compressed_parents
        )
        
        # Ensamblar traza final
        return {
            "query": user_query,
            "category": category.value,
            "answer": generation_result["answer"],
            "sources": generation_result["sources"],
            "pipeline_trace": {
                "retrieved_chunks": len(parents),
                "use_hyde": use_hyde,
                "use_multiquery": use_multiquery,
                "compression_applied": True,
                "contexts": [chunk.content for chunk in compressed_parents]
            }
        }
