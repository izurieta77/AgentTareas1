# Plan de Implementación — Fase 3: Canalización de Retrieval Avanzado e Híbrido

## Objetivo

Implementar un motor de búsqueda y recuperación avanzado (`RetrievalEngine`) para nuestro sistema RAG Industrial. Este motor optimizará las consultas de los usuarios y combinará la precisión semántica con la exactitud léxica antes de devolver los resultados finales.

El motor de búsqueda constará de:
1. **Query Transformation**: Generación de consultas alternativas (Multi-Query) y respuestas hipotéticas (HyDE) utilizando un cliente LLM configurable (compatible con OpenAI y Ollama local).
2. **Búsqueda Híbrida (Dense + Sparse)**:
   - *Dense*: Búsqueda por similitud vectorial en Qdrant (usando `all-MiniLM-L6-v2`).
   - *Sparse*: Búsqueda léxica mediante una implementación propia de **BM25 en Python puro** (sin dependencias de compiladores de Windows ni paquetes externos).
3. **Fusión de Rankings (RRF)**: Combinación de los rankings de la búsqueda densa y dispersa mediante *Reciprocal Rank Fusion*.
4. **Re-ranking con Cross-Encoder**: Reordenación de los mejores candidatos utilizando el modelo local ultra-ligero `cross-encoder/ms-marco-MiniLM-L-6-v2` (90 MB, ejecutado localmente con `sentence-transformers`).
5. **Hidratación**: Recuperación de los chunks padre correspondientes del `DocStore` local.

---

## Contexto actual

- Los chunks hijos están indexados vectorialmente en Qdrant (`points_count = 1622`).
- Los chunks padres están guardados en JSON local (`data_store/parents/`).
- Tenemos `openai` y `sentence-transformers` instalados y listos.
- No tenemos dependencias adicionales instaladas para BM25 o enrutamiento.

---

## User Review Required

> [!IMPORTANT]
> **Implementación de BM25**: Para evitar dependencias externas como `rank_bm25` (que pueden causar conflictos de versiones o problemas de compilación en Windows), se propone escribir una clase `BM25Retriever` en Python puro. Esta clase se inicializará escaneando la colección de Qdrant (método `scroll`) para extraer el contenido de los chunks hijos e indexarlos en memoria. Debido a que el tamaño de los datos locales es de miles de chunks, la indexación y búsqueda tardarán <10ms en memoria. ¿Es aceptable este enfoque?

> [!IMPORTANT]
> **Modelo Cross-Encoder para Re-ranking**: Se propone usar **`cross-encoder/ms-marco-MiniLM-L-6-v2`** que pesa solo 90 MB, es sumamente rápido en CPU y tiene un excelente rendimiento. La alternativa es `BAAI/bge-reranker-base` (270 millones de parámetros, ~1.1 GB). ¿Confirmamos el uso del modelo ligero de 90 MB para mantener la agilidad local?

> [!NOTE]
> **Compatibilidad de la API de LLM (Ollama/OpenAI)**: El módulo de transformación de consultas soportará de forma nativa la API de OpenAI. Si el usuario desea ejecutarlo 100% local, podrá configurar el endpoint a Ollama (`http://localhost:11434/v1`) mediante variables de entorno (`OPENAI_API_BASE` o `LLM_BASE_URL`).

---

## Proposed Changes

### Componente 1: BM25 Retriever

#### [NEW] [bm25.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/bm25.py)
Clase `BM25Retriever` escrita en Python puro para búsqueda de palabras clave:
- Tokenizador simple (minúsculas, remoción de caracteres no alfanuméricos).
- Cálculo de IDF clásico de BM25.
- Método `score_documents(query: str, limit: int)` que devuelve los IDs de los chunks hijos y sus puntuaciones BM25.
- Caching opcional: Posibilidad de guardar/cargar la estructura del índice en `data_store/bm25_index.json` para evitar reconstruirlo desde Qdrant en cada inicio.

---

### Componente 2: Re-ranking con Cross-Encoder

#### [NEW] [reranker.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/reranker.py)
Clase `CrossEncoderReranker`:
- Inicialización diferida (Lazy initialization) del modelo `SentenceTransformer.CrossEncoder`.
- Método `rerank(query: str, candidates: List[ParentChunk | ChildChunk], top_n: int) -> List[Tuple[Any, float]]`.
- Permite calcular la relevancia real entre la consulta del usuario y el contenido extendido de los fragmentos.

---

### Componente 3: Transformación de Consultas (HyDE & Multi-Query)

#### [NEW] [transformation.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/transformation.py)
Clase `QueryTransformer` que expone:
- **`generate_hyde_document(query: str) -> str`**: Llama a un LLM para generar una respuesta hipotética.
- **`generate_alternative_queries(query: str, n: int = 3) -> List[str]`**: Genera variantes con sinónimos técnicos.
- **Manejo de Fallback**: Si no hay API key configurada o falla la llamada al LLM, el módulo devuelve la query original sin alterar, evitando caídas del sistema.

---

### Componente 4: Orquestador de Retrieval (RetrievalEngine)

#### [NEW] [engine.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/engine.py)
La clase central `RetrievalEngine` que conecta todo:
```
RetrievalEngine(pipeline: IngestionPipeline, llm_config: Optional[dict])
  │
  ├── retrieve(query: str, filter_rules: dict, top_k: int) -> List[Dict[str, Any]]
  │     1. QUERY TRANSFORMATION:
  │        - Si HyDE está activo, obtiene query_hyde.
  │        - Si Multi-Query está activo, genera query_variants.
  │     2. SEARCH STAGE:
  │        - Ejecuta búsqueda densa en Qdrant (para query o query_hyde).
  │        - Ejecuta búsqueda dispersa en BM25.
  │     3. RANK FUSION (RRF):
  │        - Combina los rankings usando Reciprocal Rank Fusion.
  │        - Obtiene el Top-N de chunks hijos candidatos.
  │     4. HYDRATE:
  │        - Recupera los ParentChunks correspondientes del DocStore.
  │        - Elimina duplicados de padres (si varios hijos apuntan al mismo).
  │     5. RE-RANKING:
  │        - Pasa los ParentChunks (o ChildChunks) y la query por el Cross-Encoder.
  │        - Ordena por score final y devuelve el Top-K definitivo.
```

---

### Componente 5: Tests y Playground

#### [NEW] [playground/test_retrieval.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_retrieval.py)
Script interactivo y de test para la Fase 3 que valida:
1. **BM25**: Búsqueda por palabras clave exactas (`"AD4086"` o `"55 Nm"`).
2. **Dense vs. Hybrid**: Comparar qué recupera la búsqueda densa vs. la híbrida.
3. **Reranker**: Validar que el reordenamiento posiciona mejor los fragmentos con mayor correspondencia real.
4. **Query Transformation**: Comprobar la generación de variantes (si se proporciona una API key simulada o real).

---

## Verification Plan

### Automated Tests
- Ejecutar `playground/test_retrieval.py` sin API Key (valida el flujo híbrido + rerank con fallback).
- Ejecutar `playground/test_retrieval.py` simulando respuestas del LLM para HyDE/Multi-Query.

### Criterios de Éxito
- **Exactitud léxica**: Una búsqueda de `"AD4086"` debe devolver el datasheet correspondiente en el top-3 mediante BM25/Híbrida.
- **Reranker Latency**: El paso de re-ranking por Cross-Encoder sobre 10 candidatos debe demorar `< 150ms` en CPU/GPU.
- **No duplicados**: Chunks padres devueltos no deben estar duplicados tras la hidratación.
- **Integridad de metadatos**: Los resultados finales deben incluir las citas correctas (`source`, `page/heading`).
