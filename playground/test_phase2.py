"""
test_phase2.py
==============
Test end-to-end de la Fase 2: Metadatos + VectorStore + DocStore + Pipeline.

Que valida este test
---------------------
  [1/6] Importaciones y dependencias disponibles
  [2/6] Ingestión completa del datasheet AD4086_Datasheet.pdf
        → process_file() ejecuta Parse→Split→Enrich→DocStore→Qdrant
  [3/6] Verificación del DocStore
        → Al menos el 95% de los padres están persistidos en disco
  [4/6] Búsqueda semántica en Qdrant
        → search_similar("ADC resolution noise") devuelve resultados con score > 0.3
  [5/6] Recuperación de padre desde hit
        → El parent_id del mejor resultado existe en el DocStore
  [6/6] Integridad de metadatos
        → Cada resultado de búsqueda tiene los campos obligatorios en el payload

Ejecución
---------
  cd d:\\PropuestaCanalYoutube\\2026-06-16-RAG-Industrial
  python playground/test_phase2.py

Nota: La primera ejecución descargará el modelo BAAI/bge-m3 (~2.2 GB).
Las ejecuciones siguientes son instantáneas (modelo cacheado por HuggingFace).
"""

import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from app.ingestion.pipeline import IngestionPipeline


# ---------------------------------------------------------------------------
# Helpers de consola (seguros en Windows cp1252)
# ---------------------------------------------------------------------------

def safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def sep(char: str = "-", w: int = 70) -> None:
    safe_print(char * w)


def ok(msg: str) -> None:
    safe_print(f"  [OK] {msg}")


def fail(msg: str) -> None:
    safe_print(f"  [FAIL] {msg}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Configuración del test
# ---------------------------------------------------------------------------

PDF_PATH = ROOT / "data" / "AD4086_Datasheet.pdf"
STORE_PATH = ROOT / "data_store"
QDRANT_PATH = ROOT / "qdrant_db"
COLLECTION = "industrial_chunks_test"

BASE_METADATA = {
    "project_id": "PRJ-ADC-TEST-2026",
    "product_line": "ADC-EVALUATION",
    "confidentiality": "INTERNAL",
    "version": "1.0.0",
}

SEARCH_QUERIES = [
    "ADC resolution noise performance",
    "power consumption low power mode",
    "input voltage range specifications",
]

PAYLOAD_REQUIRED_KEYS = {
    "project_id", "doc_type", "confidentiality",
    "parent_id", "chunk_type", "source", "document_name",
}


# ---------------------------------------------------------------------------
# TEST
# ---------------------------------------------------------------------------

def main() -> None:
    sep("=")
    safe_print("TEST FASE 2: Pipeline End-to-End (Metadatos + Qdrant + DocStore)")
    sep("=")

    # Limpiar state anterior para tener un test limpio
    if STORE_PATH.exists():
        shutil.rmtree(STORE_PATH)
    if QDRANT_PATH.exists():
        shutil.rmtree(QDRANT_PATH)

    # ------------------------------------------------------------------
    # [1/6] Importaciones y fichero de entrada
    # ------------------------------------------------------------------
    sep()
    safe_print("[1/6] Verificando dependencias y fichero de entrada...")
    if not PDF_PATH.exists():
        fail(f"PDF no encontrado en {PDF_PATH}. Ejecuta primero: playground/test_parse_pdf.py")
    ok(f"PDF encontrado: {PDF_PATH.name} ({PDF_PATH.stat().st_size / 1024 / 1024:.1f} MB)")

    try:
        from qdrant_client import QdrantClient
        from sentence_transformers import SentenceTransformer
        from langdetect import detect
        ok("Dependencias: qdrant-client, sentence-transformers, langdetect — todas disponibles")
    except ImportError as e:
        fail(f"Dependencia no disponible: {e}")

    # ------------------------------------------------------------------
    # [2/6] Ingestión completa
    # ------------------------------------------------------------------
    sep()
    safe_print("[2/6] Ejecutando IngestionPipeline.process_file()...")
    safe_print("      (La primera ejecucion descargara BAAI/bge-m3 ~2.2 GB si no esta en cache)")
    safe_print("      Esto puede tardar varios minutos...")

    pipeline = IngestionPipeline(
        storage_path=str(STORE_PATH),
        qdrant_path=str(QDRANT_PATH),
        collection_name=COLLECTION,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        parent_size=1500,
        parent_overlap=150,
        child_size=300,
        child_overlap=50,
    )

    stats = pipeline.process_file(str(PDF_PATH), BASE_METADATA.copy())

    sep()
    safe_print("ESTADISTICAS DE INGESTA:")
    sep()
    safe_print(f"  Fichero procesado : {Path(stats['file_path']).name}")
    safe_print(f"  Chunks PADRE      : {stats['n_parents']}")
    safe_print(f"  Chunks HIJO       : {stats['n_children']}")
    safe_print(f"  Tiempo total      : {stats['duration_seconds']} segundos")
    safe_print(f"  Estado            : {stats['status']}")
    sep()

    if stats["status"] != "ok":
        fail(f"El pipeline terminó con estado inesperado: {stats['status']}")
    if stats["n_parents"] == 0 or stats["n_children"] == 0:
        fail("El pipeline no generó chunks. Revisar el parser o el splitter.")

    ok(f"Ingestión completada: {stats['n_parents']} padres, {stats['n_children']} hijos")

    # ------------------------------------------------------------------
    # [3/6] Verificación del DocStore
    # ------------------------------------------------------------------
    sep()
    safe_print("[3/6] Verificando persistencia en DocStore...")
    total_stored = pipeline.doc_store.count()
    expected = stats["n_parents"]
    coverage = total_stored / expected if expected > 0 else 0

    safe_print(f"  Padres esperados  : {expected}")
    safe_print(f"  Padres en disco   : {total_stored}")
    safe_print(f"  Cobertura         : {coverage * 100:.1f}%")

    if coverage < 0.95:
        fail(f"Cobertura del DocStore insuficiente: {coverage * 100:.1f}% < 95%")
    ok(f"DocStore verificado: {total_stored}/{expected} chunks padre persistidos")

    # ------------------------------------------------------------------
    # [4/6] Búsqueda semántica
    # ------------------------------------------------------------------
    sep()
    safe_print("[4/6] Ejecutando busquedas semanticas de prueba...")

    all_results = []
    for query in SEARCH_QUERIES:
        results = pipeline.vector_store.search_similar(query, limit=3)
        safe_print(f"\n  Query: '{query}'")
        if not results:
            fail(f"La búsqueda no devolvió resultados para: '{query}'")
        for i, r in enumerate(results):
            heading = r.payload.get("section_heading") or "(sin encabezado)"
            safe_print(f"    [{i+1}] score={r.score:.4f}  seccion='{heading[:60]}'")
        all_results.extend(results)

    best_score = max(r.score for r in all_results) if all_results else 0
    if best_score < 0.3:
        fail(f"Score máximo demasiado bajo: {best_score:.4f} < 0.3")
    ok(f"Búsqueda semántica OK — mejor score: {best_score:.4f}")

    # ------------------------------------------------------------------
    # [5/6] Recuperación de padre desde hit de búsqueda
    # ------------------------------------------------------------------
    sep()
    safe_print("[5/6] Verificando recuperacion de chunk padre desde hit...")

    best_hit = max(all_results, key=lambda r: r.score)
    parent_id = best_hit.payload.get("parent_id")

    if not parent_id:
        fail("El mejor resultado no tiene 'parent_id' en su payload.")

    parent_chunk = pipeline.retrieve_parent(parent_id)
    if parent_chunk is None:
        fail(f"No se encontró el padre '{parent_id}' en el DocStore.")

    safe_print(f"  Mejor hit score   : {best_hit.score:.4f}")
    safe_print(f"  parent_id         : {parent_id}")
    safe_print(f"  Sección del padre : {parent_chunk.heading or '(sin encabezado)'}")
    safe_print(f"  Long. del padre   : {len(parent_chunk.content)} chars")
    safe_print(f"  Inicio del padre  : {parent_chunk.content[:120].strip()!r} ...")
    ok("Recuperación de padre verificada correctamente")

    # ------------------------------------------------------------------
    # [6/6] Integridad de metadatos en el payload de Qdrant
    # ------------------------------------------------------------------
    sep()
    safe_print("[6/6] Verificando integridad de metadatos en los resultados...")

    errors = []
    for r in all_results:
        missing = PAYLOAD_REQUIRED_KEYS - set(r.payload.keys())
        if missing:
            errors.append(f"Hit {r.id}: faltan campos {missing}")

    if errors:
        for e in errors:
            safe_print(f"  [ERROR] {e}")
        fail(f"Se encontraron {len(errors)} errores de metadatos.")

    ok(f"Todos los campos requeridos presentes en {len(all_results)} resultados")

    # ------------------------------------------------------------------
    # Info de la colección Qdrant
    # ------------------------------------------------------------------
    sep()
    info = pipeline.get_collection_info()
    safe_print("INFO DE LA COLECCION QDRANT:")
    for k, v in info.items():
        safe_print(f"  {k:<22}: {v}")

    # ------------------------------------------------------------------
    # Resultado final
    # ------------------------------------------------------------------
    sep("=")
    safe_print("[OK] TODAS LAS VALIDACIONES PASARON CORRECTAMENTE")
    safe_print(f"     Pipeline funcional: {stats['n_parents']} padres en DocStore,")
    safe_print(f"     {stats['n_children']} hijos indexados en Qdrant '{COLLECTION}'.")
    sep("=")


if __name__ == "__main__":
    main()
