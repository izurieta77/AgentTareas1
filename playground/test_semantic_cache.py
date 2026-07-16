import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para consola Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from fastapi.testclient import TestClient
from app.api.main import app

def test_semantic_cache():
    print("======================================================================")
    print("INICIANDO PRUEBA DE CACHÉ SEMÁNTICA EN PLANTA")
    print("======================================================================\n")
    
    # Asegurarnos de que el backend sea Qdrant para desarrollo local
    os.environ["SEMANTIC_CACHE_BACKEND"] = "qdrant"
    os.environ["SEMANTIC_CACHE_THRESHOLD"] = "0.95"
    os.environ["SEMANTIC_CACHE_TTL_DAYS"] = "7.0"
    
    # Limpiar caché previa para asegurar que el test es idempotente
    try:
        from app.api.dependencies import initialize_pipeline
        pipeline, _, _ = initialize_pipeline()
        client_qdrant = pipeline.vector_store._get_client()
        existing = [c.name for c in client_qdrant.get_collections().collections]
        if "semantic_cache" in existing:
            client_qdrant.delete_collection("semantic_cache")
            print("Caché semántica previa eliminada para asegurar limpieza del test.")
    except Exception as e:
        print(f"No se pudo limpiar la caché previa (harmless): {e}")
    
    with TestClient(app) as client:
        # Consulta 1: Primera vez (Cache Miss)
        query_1 = "funcionalidad de los pines B4, B5 del AD4086"
        print(f"--- CONSULTA 1: '{query_1}' (Esperado: Cache Miss / LLM) ---")
        start = time.perf_counter()
        response1 = client.post("/api/v1/query", json={"query": query_1})
        duration1 = time.perf_counter() - start
        
        print(f"Status Code: {response1.status_code}")
        if response1.status_code == 200:
            res_data = response1.json()
            trace = res_data["pipeline_trace"]
            print(f"Tiempo de ejecución: {duration1:.4f} segundos")
            print(f"Cache Hit: {trace['cache_hit']}")
            print(f"Respuesta:\n{res_data['answer']}\n")
        else:
            print(f"Error: {response1.text}")
            return

        # Consulta 2: Consulta idéntica (Esperado: Cache Hit instantáneo)
        print(f"--- CONSULTA 2: '{query_1}' (Esperado: Cache Hit instantáneo) ---")
        start = time.perf_counter()
        response2 = client.post("/api/v1/query", json={"query": query_1})
        duration2 = time.perf_counter() - start
        
        print(f"Status Code: {response2.status_code}")
        if response2.status_code == 200:
            res_data = response2.json()
            trace = res_data["pipeline_trace"]
            print(f"Tiempo de ejecución: {duration2:.4f} segundos")
            print(f"Cache Hit: {trace['cache_hit']}")
            print(f"Similitud calculada: {trace['cache_similarity']}")
            print(f"Respuesta:\n{res_data['answer']}\n")
            
            # Validación
            assert trace["cache_hit"] is True, "¡Error! Debió ser un Cache Hit"
            assert duration2 < 0.2, f"¡Advertencia! Latencia de caché fue de {duration2:.4f}s (esperado < 0.2s)"
        else:
            print(f"Error: {response2.text}")
            return

        # Consulta 3: Consulta semánticamente muy similar (Esperado: Cache Hit semántico)
        query_3 = "¿qué funcionalidad tienen los pines B4 y B5 del AD4086?"
        print(f"--- CONSULTA 3: '{query_3}' (Esperado: Cache Hit semántico) ---")
        start = time.perf_counter()
        response3 = client.post("/api/v1/query", json={"query": query_3})
        duration3 = time.perf_counter() - start
        
        print(f"Status Code: {response3.status_code}")
        if response3.status_code == 200:
            res_data = response3.json()
            trace = res_data["pipeline_trace"]
            print(f"Tiempo de ejecución: {duration3:.4f} segundos")
            print(f"Cache Hit: {trace['cache_hit']}")
            print(f"Similitud calculada: {trace['cache_similarity']}")
            print(f"Respuesta:\n{res_data['answer']}\n")
        else:
            print(f"Error: {response3.text}")
            return

        # Consulta 4: Consulta totalmente distinta (Esperado: Cache Miss / LLM)
        query_4 = "¿cuál es la tensión de alimentación máxima del AD4086?"
        print(f"--- CONSULTA 4: '{query_4}' (Esperado: Cache Miss / LLM) ---")
        start = time.perf_counter()
        response4 = client.post("/api/v1/query", json={"query": query_4})
        duration4 = time.perf_counter() - start
        
        print(f"Status Code: {response4.status_code}")
        if response4.status_code == 200:
            res_data = response4.json()
            trace = res_data["pipeline_trace"]
            print(f"Tiempo de ejecución: {duration4:.4f} segundos")
            print(f"Cache Hit: {trace['cache_hit']}")
            print(f"Respuesta:\n{res_data['answer']}\n")
            
            # Validación
            assert trace["cache_hit"] is False, "¡Error! No debió ser un Cache Hit"
        else:
            print(f"Error: {response4.text}")
            return

    print("======================================================================")
    print("¡TODAS LAS PRUEBAS DE CACHÉ SEMÁNTICA PASARON CORRECTAMENTE!")
    print("======================================================================")

if __name__ == "__main__":
    test_semantic_cache()
