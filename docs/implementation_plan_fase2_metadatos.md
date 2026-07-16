# Plan de Implementación — Fase 2: Enriquecimiento de Metadatos e Índice Vectorial

## Objetivo

Implementar la capa de **metadatos estructurados + almacenamiento** que conecta los `ChunkPair` generados por el `ParentChildSplitter` con:
- **Qdrant** (VectorDB): índice de chunks hijos con payload de metadatos para pre-filtrado.
- **DocStore local** (JSON file): almacén KV de chunks padre recuperable por `parent_id`.
- **MetadataExtractor**: enriquecimiento heurístico del esquema de metadatos industriales.

Al final de esta fase, el comando `IngestionPipeline.process_file()` estará completamente operativo de extremo a extremo.

---

## Contexto actual

| Módulo | Estado |
|---|---|
| `chunking/splitter.py` | ✅ Completo — genera `ChunkPair` con `ParentChunk` / `ChildChunk` |
| `metadata/extractor.py` | ⚠️ Stub — devuelve `base_metadata` sin enriquecimiento |
| `storage/vector_store.py` | ⚠️ Stub — sin cliente Qdrant real |
| `storage/doc_store.py` | ⚠️ Stub — sin persistencia real |
| `ingestion/pipeline.py` | ⚠️ Stub — `process_file()` vacío con `pass` |
| `sync/ledger.py` | ⚠️ Stub — sin implementar |

---

## User Review Required

> [!IMPORTANT]
> **Embeddings locales vs. API**: Para vectorizar los chunks hijos necesitamos un modelo de embeddings.
> Se propone usar **`BAAI/bge-m3`** ejecutado localmente con `sentence-transformers` (aprox. 2.2 GB, soporta español e inglés, 1024 dimensiones). Es gratuito, funciona en GPU y es el estándar Open-Source para RAG multilingüe.
> La alternativa es `OpenAIEmbeddings` (`text-embedding-3-large`, 3072d) — de pago por llamada. ¿Confirmamos el modelo local?

> [!IMPORTANT]
> **DocStore backend para PoC**: Para la fase de desarrollo se propone un **JSON file store local** (sin Redis ni PostgreSQL) que persiste los chunks padre en `./data_store/parents/`. Es upgradeable a Redis en producción sin cambiar la interfaz. ¿Es aceptable para avanzar?

> [!NOTE]
> **Qdrant en modo local (sin Docker)**: Qdrant tiene un modo embebido (`QdrantClient(path="./qdrant_db")`) que crea una base de datos vectorial local en disco sin necesidad de levantar ningún servidor. Se usará este modo para el PoC. En producción se apunta a `QdrantClient(url="http://qdrant:6333")`.

---

## Open Questions

> [!WARNING]
> El `IngestionLedger` (control de hashes SHA-256 para indexación incremental) es la Fase 5 de la guía. **No se implementará en esta fase** para no mezclar complejidades. El `process_file()` del pipeline asumirá que todos los documentos son nuevos. ¿Confirmas este alcance?

---

## Proposed Changes

### Bloque 1: Esquema de Metadatos

#### [MODIFY] [extractor.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/metadata/extractor.py)

Reemplazar el stub con:

1. **`IndustrialMetadata`** — TypedDict completo con todos los campos de la guía + campos de posición de chunk:

```
project_id         str        # "PRJ-HELIOS-2025"
product_line       str        # "EXTRUDER-LINE-3"
doc_type           Literal    # PRD | SOP | MAINTENANCE_LOG | DATASHEET | PATENT | OTHER
confidentiality    Literal    # PUBLIC | INTERNAL | RESTRICTED | TOP_SECRET
version            str        # "2.1.0"
creation_timestamp int        # Unix epoch
language           str        # "es" | "en" | "mixed"
section_heading    str        # Del ParentChunk
heading_level      int | None # 1, 2, 3 o None
chunk_type         Literal    # "parent" | "child"
parent_id          str | None # Solo en chunks hijo
source             str        # Ruta del archivo origen
document_name      str        # Nombre del documento sin extensión
```

2. **`MetadataExtractor.extract()`** con dos modos:
   - **Modo heurístico** (`use_llm=False`, por defecto): Detecta `language` con `langdetect`, infiere `doc_type` por palabras clave en el nombre del fichero (ej: si contiene "SOP" → `SOP`, si contiene "Datasheet" → `DATASHEET`), y hereda el resto de `base_metadata`.
   - **Modo LLM** (`use_llm=True`): Reservado para fases futuras (Fase 2 avanzada de la guía). Diseñado pero no implementado todavía.

---

### Bloque 2: DocStore (KV Store de Chunks Padre)

#### [MODIFY] [doc_store.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/storage/doc_store.py)

Implementar un **JSON File Store** con la siguiente interfaz:

```
DocStoreManager(storage_path: str)
  ├── save_parents(pairs: List[ChunkPair]) → None
  │     Serializa cada ParentChunk a JSON y lo persiste en:
  │     storage_path/parents/{parent_id}.json
  │
  ├── get_parent(parent_id: str) → ParentChunk | None
  │     Deserializa y devuelve el ParentChunk por su ID.
  │
  └── exists(parent_id: str) → bool
        Comprueba si el fichero existe (base para el ledger futuro).
```

**Formato de serialización por fichero:**
```json
{
  "id": "P-3f2a1b7c",
  "content": "## Sección 4.2: Calibración...",
  "heading": "Calibración de la Válvula Principal",
  "heading_level": 2,
  "metadata": { "project_id": "...", "doc_type": "DATASHEET", ... }
}
```

---

### Bloque 3: VectorStore (Qdrant)

#### [MODIFY] [vector_store.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/storage/vector_store.py)

Implementar `VectorStoreManager` con cliente **Qdrant en modo embebido local**:

```
VectorStoreManager(collection_name, embedding_model, qdrant_path)
  │
  ├── __init__()
  │     Inicializa QdrantClient(path=qdrant_path) con lazy init.
  │     Crea la colección si no existe con:
  │       - VectorParams(size=1024, distance=Distance.COSINE)
  │       - HNSW: m=16, ef_construct=100
  │       - Payload indexes: project_id, doc_type, confidentiality (keyword)
  │
  ├── add_child_chunks(children: List[ChildChunk]) → int
  │     Vectoriza los textos en batch con SentenceTransformer.
  │     Genera PointStruct con:
  │       - id: UUID derivado del child.id
  │       - vector: embedding del child.content
  │       - payload: child.metadata completo (incluyendo parent_id)
  │     Hace upsert en Qdrant.
  │     Devuelve número de puntos indexados.
  │
  └── search_similar(query, filter_rules, limit=5) → List[ScoredPoint]
        Vectoriza la query y ejecuta similarity search con pre-filtrado
        usando qdrant_client.models.Filter.
```

**Configuración HNSW elegida:**
- `m=16`: 16 conexiones por nodo — equilibrio calidad/memoria para colecciones de miles de chunks.
- `ef_construct=100`: Exploración amplia durante construcción del grafo — mayor recall.

**Payload indexes** — permiten el pre-filtrado eficiente sin escaneo total:
- `project_id` → `KeywordIndex` (filtrar por proyecto I+D)
- `doc_type` → `KeywordIndex` (filtrar por tipo de documento)
- `confidentiality` → `KeywordIndex` (soporte RBAC)

---

### Bloque 4: Orquestador del Pipeline

#### [MODIFY] [pipeline.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/pipeline.py)

Implementar `IngestionPipeline.process_file()` con el flujo completo:

```
process_file(file_path, base_metadata)
  │
  ├─ 1. PARSE
  │     Detectar extensión → elegir parser (MarkerPDFParser o PandocDocxParser)
  │     → raw_text: str
  │
  ├─ 2. SPLIT
  │     splitter.split_document(raw_text, base_metadata)
  │     → pairs: List[ChunkPair]
  │
  ├─ 3. ENRICH METADATA
  │     Para cada pair, extractor.extract(chunk.content, base_metadata)
  │     → Fusionar metadatos estructurales del chunk con IndustrialMetadata
  │
  ├─ 4. STORE PARENTS (DocStore)
  │     doc_store.save_parents(pairs)
  │
  └─ 5. INDEX CHILDREN (VectorStore)
        vector_store.add_child_chunks([child for pair in pairs for child in pair.children])
        → Retornar estadísticas: n_parents, n_children
```

#### [NEW] [playground/test_phase2.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_phase2.py)

Script de test end-to-end que:
1. Ejecuta `pipeline.process_file()` con el datasheet `AD4086_Datasheet.pdf`.
2. Verifica que los padres existen en el DocStore (lectura por `parent_id`).
3. Lanza una búsqueda semántica de prueba y recupera el chunk padre del resultado.
4. Muestra las estadísticas completas de la indexación.

---

## Dependencias a instalar

```bash
pip install qdrant-client sentence-transformers langdetect
```

| Paquete | Versión aprox. | Uso |
|---|---|---|
| `qdrant-client` | 1.9.x | Cliente Qdrant (modo embebido + servidor) |
| `sentence-transformers` | 3.x | Modelo BAAI/bge-m3 para embeddings locales |
| `langdetect` | 1.0.9 | Detección de idioma en modo heurístico |

---

## Verification Plan

### Automated — `playground/test_phase2.py`

```
[1/5] Instalación de dependencias ................. pip check
[2/5] Ingestión completa del datasheet ............ process_file()
[3/5] Verificar padres en DocStore ................ get_parent(pair.parent.id) != None
[4/5] Búsqueda semántica de prueba ................ search_similar("ADC resolution")
[5/5] Recuperar padre del resultado ............... get_parent(hit.payload["parent_id"])
```

### Criterios de éxito

| Criterio | Umbral |
|---|---|
| Chunks padre persistidos | = n_parents del splitter |
| Chunks hijo indexados en Qdrant | = n_children del splitter |
| Búsqueda semántica devuelve resultados | score > 0.5 |
| Recuperación de padre del hit | `parent_id` válido y contenido no vacío |
| Tiempo total de ingestión (91 págs) | < 120 segundos (GPU) |
