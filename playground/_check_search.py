import sys
sys.path.append('.')
from app.ingestion.pipeline import IngestionPipeline

STORE_PATH = './data_store'
QDRANT_PATH = './qdrant_db'
COLLECTION = 'industrial_chunks_test'

pipeline = IngestionPipeline(
    storage_path=STORE_PATH,
    qdrant_path=QDRANT_PATH,
    collection_name=COLLECTION,
    embedding_model='sentence-transformers/all-MiniLM-L6-v2',
)

QUERIES = [
    'ADC resolution noise performance',
    'power consumption low power mode',
    'input voltage range specifications',
]
REQUIRED_KEYS = {'project_id', 'doc_type', 'confidentiality', 'parent_id', 'chunk_type', 'source', 'document_name'}

all_results = []
errors = []

print('[4/6] Busquedas semanticas...')
for q in QUERIES:
    results = pipeline.vector_store.search_similar(q, limit=3)
    print(f'  Query: {repr(q)}')
    if not results:
        print('  [FAIL] Sin resultados')
        sys.exit(1)
    for i, r in enumerate(results[:2]):
        heading = (r.payload.get('section_heading') or 'sin encabezado')[:55]
        print(f'    [{i+1}] score={r.score:.4f}  seccion={repr(heading)}')
    all_results.extend(results)

best = max(all_results, key=lambda r: r.score)
print(f'\n[5/6] Recuperando padre del mejor hit (score={best.score:.4f})...')
parent_id = best.payload.get('parent_id')
parent = pipeline.retrieve_parent(parent_id)
if parent is None:
    print(f'  [FAIL] No se encontro padre {parent_id}')
    sys.exit(1)
heading_str = parent.heading if parent.heading else 'sin encabezado'
print(f'  parent_id = {parent_id}')
print(f'  heading   = {heading_str}')
print(f'  len       = {len(parent.content)} chars')
print(f'  inicio    = {repr(parent.content[:100].strip())}')

print('\n[6/6] Verificando metadatos en payload...')
for r in all_results:
    missing = REQUIRED_KEYS - set(r.payload.keys())
    if missing:
        errors.append(f'Hit {r.id}: faltan {missing}')
if errors:
    for e in errors:
        print(f'  [FAIL] {e}')
    sys.exit(1)
print(f'  [OK] Todos los campos presentes en {len(all_results)} resultados')

info = pipeline.get_collection_info()
print('\nINFO COLECCION QDRANT:')
for k, v in info.items():
    print(f'  {k:<22}: {v}')

print('\n[OK] TODAS LAS VALIDACIONES PASARON - FASE 2 COMPLETA')
