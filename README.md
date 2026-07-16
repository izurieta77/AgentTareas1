# RAG Industrial — Framework de Retrieval-Augmented Generation para Entornos Industriales

Sistema RAG de alta precisión orientado a documentación técnica industrial (datasheets, manuales de ingeniería, documentos de I+D), con pipeline de Integración Continua (CI).

Portado del proyecto [elproximoframework/2026-06-16-RAG-Industrial](https://github.com/elproximoframework/2026-06-16-RAG-Industrial), construido originalmente siguiendo la guía `docs/Guia_Paso_a_Paso_RAG_Industrial.md`.

## Arquitectura: Agentic RAG Modular en 6 fases

| Fase | Componente | Módulos clave |
|------|------------|---------------|
| 1 | **Ingestión avanzada y chunking jerárquico** (parent-child) | `app/ingestion/parsers/`, `app/ingestion/chunking/splitter.py`, `app/ingestion/storage/` |
| 2 | **Enriquecimiento de metadatos** e índice vectorial (Qdrant) | `app/ingestion/metadata/extractor.py`, `app/ingestion/storage/vector_store.py` |
| 3 | **Retrieval híbrido** (denso + BM25), transformación de queries (HyDE / Multi-Query) y re-ranking con Cross-Encoder | `app/retrieval/engine.py`, `app/retrieval/bm25.py`, `app/retrieval/transformation.py`, `app/retrieval/reranker.py` |
| 4 | **Orquestación agéntica**: enrutamiento inteligente, compresión contextual y generación grounded con citas | `app/retrieval/router.py`, `app/retrieval/compressor.py`, `app/retrieval/generator.py`, `app/retrieval/agentic_pipeline.py` |
| 5 | **Producción**: API REST (FastAPI), caching semántico (Qdrant/Redis) e ingestión incremental con ledger SQLite | `app/api/`, `app/retrieval/cache.py`, `app/ingestion/sync/` |
| 6 | **Evaluación automatizada con RAGAS** sobre un golden dataset | `playground/run_evaluation.py`, `data/golden_dataset.json` |

El diagrama interactivo del proyecto está en `docs/diagrama_proyecto_rag.html`, y los planes de implementación de cada fase en `docs/implementation_plan_*.md`.

## Estructura del proyecto

```
app/
├── api/                # FastAPI: rutas, esquemas, dependencias
├── ingestion/          # Parsers (PDF/DOCX), chunking jerárquico, metadatos,
│                       # almacenamiento (Qdrant + DocStore) y sync incremental
└── retrieval/          # Motor híbrido, transformación de queries, re-ranker,
                        # router agéntico, compresor, generador y caché semántica
data/                   # Datasheets de ejemplo (AD4086, AD9446) y golden dataset
playground/             # Scripts de prueba manual de cada fase
tests/                  # Tests unitarios (pytest)
docs/                   # Guía paso a paso, walkthrough, planes y diagrama
.github/workflows/      # Pipeline CI (ruff + pytest)
```

## Puesta en marcha

```bash
# 1. Dependencias
pip install -r requirements.txt      # runtime (google-genai, qdrant-client, fastapi, ...)
pip install -r requirements-dev.txt  # desarrollo (pytest, ruff)

# 2. Configuración
cp .env.example .env                 # añadir GEMINI_API_KEY y ajustar la caché semántica

# 3. Levantar la API
uvicorn app.api.main:app --reload
```

### Endpoints (prefijo `/api/v1`)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/query` | Consulta al motor RAG agéntico (enrutamiento + retrieval híbrido + citas) |
| POST | `/api/v1/ingest/sync` | Ingesta en caliente de un archivo local (`.pdf`, `.docx`) |
| POST | `/api/v1/ingest/sync_dir` | Sincronización incremental de un directorio (ledger SQLite) |
| POST | `/api/v1/eval/run` | Ejecuta la evaluación RAGAS contra el golden dataset |
| GET | `/api/v1/health` | Salud del sistema y conectividad con Qdrant |

Documentación OpenAPI interactiva en `http://localhost:8000/docs`.

## Tests y CI

```bash
ruff check ./app ./tests   # lint
pytest tests/ -v           # tests unitarios
```

El workflow `.github/workflows/ci.yml` ejecuta lint y tests en cada pull request hacia `dev` o `main`.
