import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para consola Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from fastapi.testclient import TestClient
from app.api.main import app

def test_api_locally():
    print("Iniciando TestClient de FastAPI (esto disparará el evento lifespan)...")
    
    # Usar el TestClient con manejador de contexto 'with' para asegurar
    # que los eventos de lifespan (inicialización de RAG) se disparen.
    try:
        with TestClient(app) as client:
            print("\n--- TEST: GET /health ---")
            response = client.get("/api/v1/health")
            print(f"Status Code: {response.status_code}")
            print(f"Response JSON: {response.json()}")
            
            print("\n--- TEST: GET / (root) ---")
            response = client.get("/")
            print(f"Status Code: {response.status_code}")
            print(f"Response JSON: {response.json()}")
            
            print("\n--- TEST: POST /api/v1/query ---")
            payload = {
                "query": "funcionalidad de los pines B4, B5 del AD4086",
                "filters": None
            }
            start_time = os.times().elapsed
            response = client.post("/api/v1/query", json=payload)
            end_time = os.times().elapsed
            
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                res_data = response.json()
                print(f"Categoría RAG: {res_data['category']}")
                print(f"Respuesta:\n{res_data['answer']}")
                print("\nFuentes Citadas:")
                for src in res_data['sources']:
                    print(f"  - Documento: {src['document']} | Sección: {src['heading']} | ID: {src['id']}")
                print(f"Trazabilidad: {res_data['pipeline_trace']}")
            else:
                print(f"Error en consulta: {response.text}")
                
    except Exception as e:
        print(f"Error durante la ejecución del test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_locally()
