import os
import sys
import time
import shutil
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para consola Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from fastapi.testclient import TestClient
from app.api.main import app

def test_incremental_sync():
    print("======================================================================")
    print("INICIANDO PRUEBA DE PIPELINE DE ACTUALIZACIÓN INCREMENTAL")
    print("======================================================================\n")
    
    # 1. Rutas locales
    temp_dir = ROOT / "playground" / "temp_test_sync"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    src_pdf = ROOT / "data" / "ad9446.pdf"
    src_md = ROOT / "data" / "ad9446.md"
    
    dest_pdf = temp_dir / "test_doc.pdf"
    dest_md = temp_dir / "test_doc.md"
    
    # Copiar documentos de prueba
    shutil.copy2(src_pdf, dest_pdf)
    shutil.copy2(src_md, dest_md)
    
    # Base de datos del ledger para pruebas
    ledger_db = ROOT / "data_store" / "ledger.db"
    
    # Asegurarnos de que iniciamos limpios para el archivo de prueba
    try:
        if ledger_db.exists():
            conn = sqlite3.connect(str(ledger_db))
            conn.execute("DELETE FROM document_ledger WHERE file_path LIKE '%test_doc.pdf%'")
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error al limpiar base de datos ledger (harmless): {e}")

    with TestClient(app) as client:
        # Verificar cantidad inicial de vectores
        print("Obteniendo estado inicial de la base de datos...")
        health_resp = client.get("/api/v1/health")
        initial_vector_count = health_resp.json()["vector_count"]
        print(f"Vectores iniciales en Qdrant: {initial_vector_count}\n")
        
        # ------------------------------------------------------------------
        # FASE A: NUEVO ARCHIVO
        # ------------------------------------------------------------------
        print(f"--- PASO A: Ingesta de nuevo archivo ('{dest_pdf.name}') ---")
        payload = {
            "directory_path": str(temp_dir),
            "project_id": "PRJ-TEST-INC",
            "doc_type": "datasheet",
            "confidentiality": "INTERNAL"
        }
        
        start = time.perf_counter()
        response = client.post("/api/v1/ingest/sync_dir", json=payload)
        duration = time.perf_counter() - start
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            res_data = response.json()
            print(f"Tiempo empleado: {duration:.4f}s (Optimizado mediante lectura de .md)")
            print(f"Añadidos: {res_data['added_count']}, Actualizados: {res_data['updated_count']}, Eliminados: {res_data['deleted_count']}, Omitidos: {res_data['skipped_count']}")
            
            assert res_data["added_count"] == 1, "¡Error! Debió añadir 1 archivo."
            assert res_data["updated_count"] == 0
            assert res_data["deleted_count"] == 0
        else:
            print(f"Error en Ingesta A: {response.text}")
            cleanup(temp_dir)
            return
            
        # Comprobar el incremento de vectores
        health_resp = client.get("/api/v1/health")
        after_add_count = health_resp.json()["vector_count"]
        print(f"Vectores en Qdrant después del Paso A: {after_add_count} (Incremento: {after_add_count - initial_vector_count})\n")
        
        # ------------------------------------------------------------------
        # FASE B: ARCHIVO OMITIDO (Sin cambios)
        # ------------------------------------------------------------------
        print(f"--- PASO B: Segunda sincronización sin modificar nada (Esperado: Omitido) ---")
        response = client.post("/api/v1/ingest/sync_dir", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            res_data = response.json()
            print(f"Añadidos: {res_data['added_count']}, Actualizados: {res_data['updated_count']}, Eliminados: {res_data['deleted_count']}, Omitidos: {res_data['skipped_count']}")
            assert res_data["added_count"] == 0
            assert res_data["updated_count"] == 0
            assert res_data["deleted_count"] == 0
            assert res_data["skipped_count"] == 1, "¡Error! El archivo debió ser omitido."
        else:
            print(f"Error en Sincronización B: {response.text}")
            cleanup(temp_dir)
            return
            
        # ------------------------------------------------------------------
        # FASE C: ARCHIVO MODIFICADO
        # ------------------------------------------------------------------
        print(f"--- PASO C: Modificación del archivo (Esperado: Actualizado / Re-indexación) ---")
        # Simular modificación física cambiando la fecha del sistema y agregando datos al archivo PDF
        # Para que cambie el hash SHA-256, añadimos un byte al final del PDF.
        with open(dest_pdf, "ab") as f:
            f.write(b"\n")
            
        # Actualizamos también el Markdown para simular un cambio de contenido
        with open(dest_md, "a", encoding="utf-8") as f:
            f.write("\n\nNuevas especificaciones añadidas en el proceso de modificación de prueba.")
            
        response = client.post("/api/v1/ingest/sync_dir", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            res_data = response.json()
            print(f"Añadidos: {res_data['added_count']}, Actualizados: {res_data['updated_count']}, Eliminados: {res_data['deleted_count']}, Omitidos: {res_data['skipped_count']}")
            assert res_data["added_count"] == 0
            assert res_data["updated_count"] == 1, "¡Error! El archivo debió ser detectado como modificado/actualizado."
            assert res_data["deleted_count"] == 0
        else:
            print(f"Error en Sincronización C: {response.text}")
            cleanup(temp_dir)
            return

        # ------------------------------------------------------------------
        # FASE D: ARCHIVO ELIMINADO
        # ------------------------------------------------------------------
        print(f"--- PASO D: Eliminación del archivo en el disco (Esperado: Eliminado / Purgado de vectores) ---")
        dest_pdf.unlink()
        dest_md.unlink()
        
        response = client.post("/api/v1/ingest/sync_dir", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            res_data = response.json()
            print(f"Añadidos: {res_data['added_count']}, Actualizados: {res_data['updated_count']}, Eliminados: {res_data['deleted_count']}, Omitidos: {res_data['skipped_count']}")
            assert res_data["added_count"] == 0
            assert res_data["updated_count"] == 0
            assert res_data["deleted_count"] == 1, "¡Error! El archivo debió ser purgado (eliminado)."
        else:
            print(f"Error en Sincronización D: {response.text}")
            cleanup(temp_dir)
            return
            
        # Comprobar que los vectores se redujeron al número inicial
        health_resp = client.get("/api/v1/health")
        final_vector_count = health_resp.json()["vector_count"]
        print(f"Vectores en Qdrant al finalizar: {final_vector_count} (Esperados: {initial_vector_count})")
        assert final_vector_count == initial_vector_count, "¡Error! Los vectores del archivo borrado no se purgaron correctamente."
        
    cleanup(temp_dir)
    print("\n======================================================================")
    print("¡TODAS LAS PRUEBAS DE PIPELINE INCREMENTAL PASARON CORRECTAMENTE!")
    print("======================================================================")

def cleanup(directory: Path):
    if directory.exists():
        shutil.rmtree(directory)

if __name__ == "__main__":
    test_incremental_sync()
