import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Request

from app.ingestion.pipeline import IngestionPipeline
from app.retrieval.engine import RetrievalEngine
from app.retrieval.agentic_pipeline import AgenticRAGPipeline
from app.retrieval.cache import SemanticCache

ROOT = Path(__file__).parent.parent.parent

def initialize_pipeline() -> tuple[IngestionPipeline, AgenticRAGPipeline, SemanticCache]:
    """
    Inicializa una única vez los modelos, la base de datos (Qdrant + SQLite + SQLite FTS/BM25)
    y la caché semántica, retornando las instancias del pipeline, orquestador y caché.
    """
    # Cargar variables de entorno
    load_dotenv(dotenv_path=ROOT / ".env")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no configurada en el archivo .env")

    STORE_PATH = ROOT / "data_store"
    QDRANT_PATH = ROOT / "qdrant_db"
    COLLECTION = "industrial_chunks"
    
    # 1. Instanciar el pipeline de ingesta (carga el SentenceTransformer all-MiniLM-L6-v2)
    pipeline = IngestionPipeline(
        storage_path=str(STORE_PATH),
        qdrant_path=str(QDRANT_PATH),
        collection_name=COLLECTION,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    )
    
    # 2. Verificar colección Qdrant y aplicar fallback si está vacía
    try:
        client = pipeline.vector_store._get_client()
        collections_info = client.get_collections()
        existing_collections = [c.name for c in collections_info.collections]
        
        if COLLECTION not in existing_collections:
            if "industrial_chunks_test" in existing_collections:
                COLLECTION = "industrial_chunks_test"
                pipeline.vector_store.collection_name = COLLECTION
        
        # Verificar cantidad de registros para fallback inteligente
        count = client.count(collection_name=COLLECTION).count
        if count == 0 and COLLECTION == "industrial_chunks" and "industrial_chunks_test" in existing_collections:
            COLLECTION = "industrial_chunks_test"
            pipeline.vector_store.collection_name = COLLECTION
            
    except Exception:
        # Fallback por seguridad
        COLLECTION = "industrial_chunks_test"
        pipeline.vector_store.collection_name = COLLECTION
        
    # 3. Instanciar el motor de recuperación y el pipeline agéntico (carga el Cross-Encoder)
    engine = RetrievalEngine(pipeline=pipeline, api_key=api_key)
    rag = AgenticRAGPipeline(retrieval_engine=engine, api_key=api_key)
    
    # 4. Inicializar la Caché Semántica
    cache = SemanticCache(pipeline=pipeline)
    
    return pipeline, rag, cache

def get_rag_pipeline(request: Request) -> AgenticRAGPipeline:
    """Dependency provider para el orquestador RAG."""
    return request.app.state.rag_pipeline

def get_ingestion_pipeline(request: Request) -> IngestionPipeline:
    """Dependency provider para el pipeline de ingesta."""
    return request.app.state.ingestion_pipeline

def get_semantic_cache(request: Request) -> SemanticCache:
    """Dependency provider para la caché semántica."""
    return request.app.state.semantic_cache

