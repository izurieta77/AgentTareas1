import os
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from app.ingestion.pipeline import IngestionPipeline
from app.retrieval.engine import RetrievalEngine
from app.retrieval.agentic_pipeline import AgenticRAGPipeline

def test_query():
    # Fix for Windows console encoding
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: No se encontró GEMINI_API_KEY en .env")
        return
        
    STORE_PATH = ROOT / "data_store"
    QDRANT_PATH = ROOT / "qdrant_db"
    COLLECTION = "industrial_chunks" # Nombre real en producción, probamos fallback a test si no existe
    
    # Asumimos que si no está "industrial_chunks", puede que se haya ingerido en "industrial_chunks_test"
    # El test real de la fase 2 usó "industrial_chunks_test", veamos cuál tiene documentos
    
    pipeline = IngestionPipeline(
        storage_path=str(STORE_PATH),
        qdrant_path=str(QDRANT_PATH),
        collection_name=COLLECTION,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    )
    
    # Verificamos rápidamente si la colección existe o usamos la de test
    try:
        client = pipeline.vector_store._get_client()
        count = client.count(collection_name=COLLECTION).count
        if count == 0:
            COLLECTION = "industrial_chunks_test"
            pipeline.vector_store.collection_name = COLLECTION
            print(f"Cambiando a colección de prueba '{COLLECTION}'")
        else:
            print(f"Usando colección '{COLLECTION}' con {count} vectores.")
    except Exception:
        COLLECTION = "industrial_chunks_test"
        pipeline.vector_store.collection_name = COLLECTION
        print(f"Cambiando a colección de prueba '{COLLECTION}' (la principal no existe)")
    
    print("\nInicializando motor de recuperación (BM25 + Dense + Reranker)...")
    engine = RetrievalEngine(pipeline=pipeline, api_key=api_key)
    
    print("Inicializando Pipeline Agéntico (Gemini 1.5 Flash)...")
    rag = AgenticRAGPipeline(retrieval_engine=engine, api_key=api_key)
    
    query = "funcionalidad de los pines B4, B5 del AD4086"
    print(f"\n==============================================")
    print(f"Realizando consulta: '{query}'")
    print(f"==============================================\n")
    
    result = rag.query(query)
    
    print(f"Categoría asignada: {result['category']}")
    print(f"Traza del pipeline: {result['pipeline_trace']}")
    print(f"\nRespuesta generada:\n------------------\n{result['answer']}\n------------------")
    print("\nFuentes recuperadas y utilizadas para el contexto:")
    for i, s in enumerate(result['sources']):
        print(f"  [{i+1}] Documento: {s.get('document', 'Desconocido')} | Sección: {s.get('heading', 'Sin sección')}")

if __name__ == "__main__":
    test_query()
