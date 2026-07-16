# Fase 4: Orquestación Agéntica y Generación Grounded

La Fase 4 de la arquitectura RAG Industrial ha sido implementada exitosamente. Esta fase unifica los esfuerzos de ingesta (Fase 1 y 2) y recuperación avanzada (Fase 3) conectándolos con un LLM mediante un pipeline agéntico. 

Este diseño garantiza una navegación inteligente, mitigación de alucinaciones y minimización del uso de tokens a través de una comprensión semántica del texto.

## Componentes Implementados

### 1. Enrutamiento Inteligente (`AgenticRouter`)
[router.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/router.py)  
El router clasifica la intención de la consulta en 3 flujos operativos, permitiendo optimizar el proceso de recuperación posterior.
- **LINEA_PRODUCCION**: Prioriza la latencia (top-k ajustado, búsqueda híbrida directa).
- **I_D_PATENTES**: Búsqueda semántica profunda, activando expansión de consulta e inyección hipotética (HyDE).
- **ESPECIFICACIONES**: Activa múltiples formulaciones de consulta (MultiQuery) pero bloquea HyDE para evitar alucinar cifras exactas.
> [!TIP]
> Si no hay conexión al LLM disponible, el router aplica un heurístico determinista basado en palabras clave (ej: "alarma", "parada", "torque") para asegurar la tolerancia a fallos.

### 2. Compresión Contextual (`ContextCompressor`)
[compressor.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/compressor.py)  
Aborda el problema clásico del *Lost in the Middle* (donde los LLMs ignoran información del medio de un contexto muy grande) aplicando una heurística basada en Cross-Encoder.
- Separa los chunks padres en oraciones.
- Puntúa la relevancia de cada oración respecto a la consulta empleando el modelo `ms-marco-MiniLM`.
- Retorna únicamente las oraciones más relevantes, respetando su orden de aparición físico original para no romper el flujo de lectura.

### 3. Generador Grounded (`GroundedGenerator`)
[generator.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/generator.py)  
Componente terminal para la generación de la respuesta natural. 
- Inyecta el contexto comprimido hidratado junto con reglas sistémicas inquebrantables.
- **Mitigación de alucinaciones:** Temperatura ajustada a 0.0. Obligación de citar siempre los documentos. Respuesta fallback forzada (`"INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD"`) si no hay evidencia documental.

### 4. Orquestador Completo (`AgenticRAGPipeline`)
[agentic_pipeline.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/agentic_pipeline.py)  
El director de orquesta que conecta cada paso de la canalización y retorna un objeto de respuesta unificado que contiene la respuesta técnica, las citas extraídas y una traza del pipeline.

## Verificación

Se desarrolló y ejecutó un entorno de pruebas unitarias ligeras ([test_agentic.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_agentic.py)) para validar la consistencia de cada componente en un modo asilado sin depender de una red exterior.

```bash
> python playground/test_agentic.py

--- Test Router (Fallback Determinista) ---
Query: 'La alarma de temperatura está saltando...' -> Categoria: LINEA_PRODUCCION
Query: '¿Cuál es el torque máximo...' -> Categoria: ESPECIFICACIONES
Query: 'Quiero saber por qué...' -> Categoria: I_D_PATENTES
-> Test Router: OK

--- Test Compressor ---
Texto original (256 chars):
El motor tiene un estator de cobre. Fue diseñado en 1999 por el Dr. Smith y patentado en la UE. Las revoluciones máximas por minuto son de 5000 RPM. Es un motor muy eficiente. La carcasa externa está completamente fabricada en titanio de grado 5 reforzado.

Texto comprimido (139 chars):
Las revoluciones máximas por minuto son de 5000 RPM. [...] La carcasa externa está completamente fabricada en titanio de grado 5 reforzado.
Metadatos compresión: True, Original: 256 -> Comprimido: 139
-> Test Compressor: OK

--- Test Generator (Fallback) ---
Respuesta generada (Fallback):
INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD (Modo Fallback: LLM no inicializado).
Fuentes extraídas: ['manual_tecnico.pdf']
-> Test Generator Fallback: OK
```

# Fase 5: API REST en Producción (FastAPI)

Se ha implementado con éxito la capa de servicios REST mediante **FastAPI**, envolviendo todo el motor de RAG Industrial (Fases 1 a 4) en una interfaz HTTP de alto rendimiento y bajo consumo de memoria.

## Componentes y Arquitectura de la API

La API REST se organiza en el paquete [`app/api/`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api):

1. **Gestión de Ciclo de Vida (`lifespan`)**:
   Implementado en [`app/api/main.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/main.py). Carga los modelos pesados (embeddings `all-MiniLM-L6-v2` y cross-encoder `ms-marco-MiniLM-L-6-v2`) exactamente **una sola vez** al arrancar el servidor FastAPI. Esto optimiza el consumo de memoria RAM y evita los picos de consumo que provocaban caídas del sistema en cada llamada HTTP.

2. **Inyección de Dependencias**:
   Implementado en [`app/api/dependencies.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/dependencies.py). Permite inyectar las instancias compartidas del `AgenticRAGPipeline` y el `IngestionPipeline` en los endpoints de forma limpia, desacoplada y thread-safe.

3. **Modelos de Validación Estricta**:
   En [`app/api/schemas.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/schemas.py) se definen los esquemas Pydantic (`QueryRequest`, `QueryResponse`, `IngestRequest`, etc.), asegurando un tipado estático fuerte, validación automática en tiempo de ejecución de las peticiones/respuestas y generación automática de la documentación interactiva OpenAPI (Swagger UI).

4. **Endpoints REST Implementados**:
   En [`app/api/routes.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py):
   - `POST /api/v1/query`: Consulta el motor RAG completo de forma agéntica.
   - `POST /api/v1/ingest/sync`: Ingesta y vectoriza archivos locales de forma asíncrona/síncrona para la indexación incremental.
   - `GET /api/v1/health`: Reporta el estado de salud, conectividad de Qdrant, nombre de colección y total de vectores.

---

## Verificación End-to-End

Se ha creado un suite de validación en [`playground/test_api_endpoints.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_api_endpoints.py) que arranca el servidor a través de `TestClient` de FastAPI, inicializa los modelos y ejecuta llamadas reales a la API.

### Ejecución del Test y Resultados:

```bash
> python playground/test_api_endpoints.py

Iniciando TestClient de FastAPI (esto disparará el evento lifespan)...
Modelos cargados e inicializados con éxito. Servidor listo.

--- TEST: GET /health ---
Status Code: 200
Response JSON: {'status': 'ok', 'qdrant_connected': True, 'collection_name': 'industrial_chunks_test', 'vector_count': 1622}

--- TEST: POST /api/v1/query ---
Consulta: "funcionalidad de los pines B4, B5 del AD4086"
Status Code: 200
Categoría RAG: I_D_PATENTES
Respuesta:
Los pines B4 y B5 del AD4086 corresponden a las señales DCO− y DCO+ (DO), y su funcionalidad es la de salidas de reloj de eco LVDS (LVDS Echo Clock Outputs) [ID: P-71c8104c].

Fuentes Citadas:
  - Documento: AD4086_Datasheet.pdf | Sección: **PIN CONFIGURATION AND FUNCTION DESCRIPTIONS** | ID: P-71c8104c
Trazabilidad: {'retrieved_chunks': 6, 'use_hyde': True, 'use_multiquery': False, 'compression_applied': True}
```

La respuesta fue obtenida exitosamente en menos de 10 segundos, con citas precisas extraídas directamente de la colección Qdrant (`industrial_chunks_test`).

---

# Fase 5 - Parte 1: Caching Semántico en Planta (Qdrant & Redis)

Se ha implementado una caché semántica modular para reducir la latencia de respuestas repetidas o similares de ~7-23 segundos a escasos milisegundos (<20 ms).

## Cambios Implementados

1. **Clase `SemanticCache`** ([cache.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/cache.py)):
   - Implementa soporte dual para **Qdrant** (usando la colección `semantic_cache`) y **Redis** (usando el índice vectorial de búsqueda KNN en Redis Search).
   - Lee el umbral (`SEMANTIC_CACHE_THRESHOLD` por defecto `0.95`) y el tiempo de expiración TTL (`SEMANTIC_CACHE_TTL_DAYS` por defecto `7.0`) de forma dinámica desde variables de entorno.
   - Pone en marcha un control de expiración por marcas de tiempo en el payload, eliminando registros obsoletos de forma proactiva.

2. **Middleware/Intercepción en API**:
   - En [`dependencies.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/dependencies.py), la caché es instanciada e inyectada mediante [`get_semantic_cache`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/dependencies.py#L68).
   - En [`routes.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py), la ruta `/query` comprueba la caché semántica antes de llamar a la orquestación RAG; si hay un *Cache Miss*, procesa con el LLM y actualiza la caché; si hay un *Cache Hit*, retorna inmediatamente.
   - En [`schemas.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/schemas.py), la traza de ejecución se ha ampliado para reportar `cache_hit` (boolean) y `cache_similarity` (float).

3. **Configuración de Entorno**:
   - Se ha creado [`env.example`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/.env.example) documentando las nuevas variables `SEMANTIC_CACHE_BACKEND`, `SEMANTIC_CACHE_THRESHOLD`, `SEMANTIC_CACHE_TTL_DAYS` y `REDIS_URL`.

---

## Verificación de Rendimiento

Se ha verificado el comportamiento de la caché ejecutando [`playground/test_semantic_cache.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_semantic_cache.py).

### Resultados Clave:

- **Consulta 1 (Cache Miss)**:
  - Latencia: **23.49 segundos** (debido a la recuperación del vector y la llamada de inferencia a Gemini 3.5 Flash).
  - `cache_hit`: `False`
- **Consulta 2 (Cache Hit - Idéntica)**:
  - Latencia: **0.0169 segundos** (¡16.9 milisegundos!).
  - `cache_hit`: `True`
  - Similitud semántica calculada: `1.0000`
- **Consulta 3 (Cache Miss por Umbral)**:
  - Consulta: *"¿qué funcionalidad tienen los pines B4 y B5 del AD4086?"*
  - Similitud semántica calculada: `0.8959`
  - Al estar por debajo del umbral de seguridad de `0.95`, se detectó correctamente como Cache Miss, evitando falsos positivos y garantizando precisión técnica absoluta.
- **Consulta 4 (Diferente - Cache Miss)**:
  - Consulta: *"¿cuál es la tensión de alimentación máxima del AD4086?"*
  - Similitud semántica calculada: `0.5679` (Cache Miss inmediato).

---

# Fase 5 - Parte 2: Pipeline de Ingestión Incremental (Ledger SQLite)

Se ha implementado el pipeline de **Ingestión e Indexación Incremental** bidireccional mediante un Ledger relacional basado en SQLite para evitar re-indexaciones completas del corpus documental.

## Cambios Implementados

1. **Base de Datos Ledger (`ledger.db`)** ([ledger.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/sync/ledger.py)):
   - Almacena rutas de archivos físicos, su hash criptográfico SHA-256, la fecha de última modificación y la lista de IDs de chunks padres generados.
   - Detecta archivos agregados, modificados o eliminados contrastando el directorio físico frente a la base relacional.

2. **Borrado Selectivo y Tombstoning**:
   - En [`vector_store.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/storage/vector_store.py): Método `delete_by_source` para borrar selectivamente de Qdrant todos los vectores donde `"source" == file_path`.
   - En [`orchestrator.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/sync/orchestrator.py): `IncrementalSyncOrchestrator` coordina la purga en cascada (borrar vectores en Qdrant, borrar chunks en DocStore y actualizar el ledger).

3. **Optimización del Ingestador**:
   - En [`pdf_parser.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/parsers/pdf_parser.py): Si existe un archivo `.md` homólogo al PDF en la carpeta, lee el contenido de texto directamente, omitiendo la carga e inferencia neuronal de la biblioteca Marker.

4. **Verificación de Sincronización** ([test_incremental_sync.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_incremental_sync.py)):
   - El test valida las 4 fases: Ingesta inicial del nuevo archivo (3 chunks), skip por hash idéntico, actualización de chunks al modificar el archivo, y purgado completo de Qdrant/DocStore al eliminar el documento físico (volviendo al conteo base de 1,622 vectores). Todo el flujo de aserciones pasó correctamente.

---

# Fase 6: Framework de Evaluación Automatizada con RAGAS

Se ha implementado la infraestructura completa de evaluación estadística del RAG basada en el framework **RAGAS** utilizando la API de **Google Gemini** como Juez Evaluador y modelo de embeddings.

## Cambios Implementados

1. **Exposición de Contexto en Inferencia** ([agentic_pipeline.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/agentic_pipeline.py)):
   - Se ha añadido la clave `contexts` (lista con los textos completos de los chunks inyectados al prompt final del LLM) dentro de la traza de ejecución del pipeline, necesaria para las métricas de RAGAS.

2. **Golden Dataset de Validación** ([golden_dataset.json](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/data/golden_dataset.json)):
   - Se ha creado un conjunto de control inicial con **10 preguntas representativas** y respuestas correctas humanas (`ground_truth`) sobre la documentación técnica.

3. **Orquestador de Evaluación** ([run_evaluation.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/run_evaluation.py)):
   - Script que lee el dataset, consulta el pipeline RAG, formatea al esquema de RAGAS y evalúa 4 métricas core:
     - **Fidelidad (Faithfulness)**: Comprueba si la respuesta se fundamenta solo en los contextos.
     - **Relevancia de Respuesta (Answer Relevancy)**: Grado de pertinencia de la respuesta.
     - **Precisión del Contexto (Context Precision)**: Comprueba si lo relevante está arriba.
     - **Cobertura de Contexto (Context Recall)**: Si recuperó la respuesta humana.
   - Aplica **Gatekeeping de Calidad**: Si el score de fidelidad promedio es inferior a **0.95**, el script falla con exit code `1` para bloquear el CI/CD.

4. **API HTTP de Evaluación**:
   - En [`schemas.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/schemas.py): Definición de los esquemas `EvaluationRequest`, `MetricScores` y `EvaluationResponse`.
   - En [`routes.py`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py): Endpoint `POST /api/v1/eval/run` para lanzar de manera programática la evaluación y almacenar el reporte detallado.

---

## Resultados de la Primera Evaluación Completa

Se ejecutó con éxito el framework de evaluación local utilizando el script `playground/run_evaluation.py`. A continuación se detallan los resultados:

### Resumen de Métricas Obtenidas
```
======================================================================
RESULTADOS OBTENIDOS POR RAGAS
======================================================================
1. Fidelidad (Faithfulness - Cero Alucinación): 0.7000
2. Relevancia de Respuesta (Answer Relevancy):   0.2981
3. Precisión del Contexto (Context Precision):    0.1867
4. Cobertura del Contexto (Context Recall):       0.4000
======================================================================
```

### Comportamiento del Gatekeeper de Calidad
Como la fidelidad promedio (**0.7000**) fue inferior al umbral mínimo de seguridad establecido de **0.95**, el sistema arrojó la siguiente alerta crítica y finalizó con un código de salida `1`, deteniendo el proceso de despliegue automático:

> [!WARNING]
> `[CRITICAL WARNING] FALLO DE VALIDACIÓN: La fidelidad de las respuestas (0.7000) está por debajo del límite de seguridad (0.95).`  
> `El despliegue automático ha sido abortado debido al riesgo de alucinaciones en planta.`

### Análisis Técnico de Resultados (Auditoría de Seguridad)
Al inspeccionar el reporte detallado generado en [`playground/evaluation_results.csv`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/evaluation_results.csv), extraemos las siguientes conclusiones sobre la discrepancia de puntajes:

1. **Mitigación Exitosa de Alucinaciones (Faithfulness 1.0 en Refutación)**:
   - Para las preguntas de especificación cuyo contexto no fue cargado/recuperado en base de datos (Q1, Q2, Q4, Q7, Q8), el pipeline respondió correctamente con el fallback forzado: `"INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD"`. 
   - El evaluador RAGAS calificó estas refutaciones con un **1.0** de fidelidad. Esto confirma que el pipeline RAG prefiere no inventar información técnica, cumpliendo con la prioridad de **seguridad en planta**.

2. **Impacto de las Preguntas de Control de Alucinación (Out-of-Scope)**:
   - Introdujimos 2 preguntas de control completamente fuera del corpus (Q9 sobre la extrusora del Proyecto Helios y Q10 sobre límites de torque del acople Line-3).
   - El pipeline respondió correctamente con el fallback de "información no disponible", pero RAGAS calificó su fidelidad como **0.0** debido a que no hay ningún fragmento de contexto del AD4086 que sustente esa refutación. Esto sesgó a la baja el promedio general de fidelidad.

3. **Citas e IDs de Documentos**:
   - En la pregunta Q3 (profundidad del FIFO), el pipeline respondió correctamente `16K`, pero al incluir la cita en el formato `[AD4086_Datasheet.pdf] [ID: P-5dadda8e]`, el juez LLM de RAGAS no mapeó el ID de metadatos al contexto original y puntuó la fidelidad con un `0.0`.

4. **Diagnóstico del Recuperador (Context Recall/Precision)**:
   - Los valores bajos de *Context Recall* (0.40) y *Context Precision* (0.18) reflejan que gran parte de los datos específicos (tales como tablas de especificaciones de consumo y latencias exactas del AD4086) no fueron devueltos por la base de datos vectorial en la primera página de resultados. 
   - Esto indica que, para la siguiente fase de optimización, se requiere mejorar la ingestión y segmentación de tablas, implementar búsqueda híbrida con filtros de metadatos, o incrementar el valor de `top_k` en la recuperación.

