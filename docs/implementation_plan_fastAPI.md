# Implementación Fase 5: API REST en Producción (FastAPI)

Este documento detalla el plan para envolver el motor de RAG Industrial (Fases 1 a 4) en una API robusta usando FastAPI, sentando las bases para el despliegue en producción.

## Contexto y Justificación (¿Por qué ahora?)

La guía original titula la Fase 5 como **"Despliegue en Producción, Caching Semántico e Indexación Incremental"**. Aunque no menciona explícitamente "FastAPI", el despliegue en producción *exige* una capa de interfaz que comunique el backend (nuestro motor de Python) con los clientes (dashboards de operarios, sistemas SCADA, frontends web).

**Es el momento perfecto para hacerlo antes de que el proyecto siga creciendo por las siguientes razones:**
1. **Punto de Inyección (Dependency Injection):** Antes de añadir el "Caching Semántico" de la Fase 5, es mejor tener FastAPI montado, ya que el caché funcionará idealmente como un *middleware* de la API.
2. **Gestión de Memoria:** Evitará que recarguemos los pesados modelos de IA (embeddings, cross-encoder) en cada consulta. FastAPI nos permitirá cargarlos una sola vez en memoria (`lifespan events`) y servir cientos de consultas asíncronas.
3. **Desacoplamiento:** Mantendremos la lógica core del RAG (en `app/retrieval` y `app/ingestion`) completamente aislada y limpia, mientras que la lógica web y de seguridad HTTP vivirá en `app/api`.

---

## Cambios Propuestos

Vamos a crear un nuevo módulo dentro del proyecto llamado `app/api/` que contendrá toda la capa de servicio web.

### 1. Estructura de Datos (Pydantic)
Definiremos los esquemas estrictos de entrada y salida para que la API tenga tipado fuerte y documentación autogenerada (Swagger/OpenAPI).

#### [NEW] [schemas.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/schemas.py)
- `QueryRequest`: Esperará un campo `query` (string) y opcionalmente filtros de `project_id` o `doc_type`.
- `SourceNode`: Representación de un documento fuente (documento, encabezado).
- `QueryResponse`: Devolverá la respuesta del LLM, la categoría enrutada, y una lista de `SourceNode`.

### 2. Ciclo de Vida y Dependencias
Para no saturar la memoria (ya hemos visto que los modelos son pesados), cargaremos el pipeline de RAG una sola vez al arrancar el servidor.

#### [NEW] [dependencies.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/dependencies.py)
- Instanciación centralizada de `IngestionPipeline`, `RetrievalEngine` y `AgenticRAGPipeline`.
- Funciones `get_rag_pipeline()` para inyectar el motor en los endpoints sin duplicar recursos.

### 3. Rutas y Endpoints
Crearemos los puntos de acceso para interactuar con el sistema.

#### [NEW] [routes.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py)
- `POST /api/v1/query`: Endpoint principal. Recibe la pregunta del usuario, la procesa por nuestro pipeline agéntico y devuelve la respuesta.
- `POST /api/v1/ingest/sync`: Endpoint administrativo (preparación para la indexación incremental).
- `GET /health`: Para verificar que los modelos están cargados en la memoria y la API está viva.

### 4. Orquestador de la Aplicación
#### [NEW] [main.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/main.py)
- Inicialización de FastAPI.
- Configuración de CORS (Cross-Origin Resource Sharing) para permitir que aplicaciones Frontend llamen a esta API.
- Manejadores globales de excepciones para evitar que un fallo en el RAG tumbe el servidor web.

#### [MODIFY] [requirements.txt](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/requirements.txt)
- Añadir dependencias web: `fastapi` y `uvicorn`.

---

## Plan de Verificación

Una vez implementado, verificaremos el despliegue realizando:
1. **Prueba de Arranque:** Ejecutar `uvicorn app.api.main:app --reload` y validar que los modelos se alojan correctamente en la memoria sin colapsar el sistema.
2. **Prueba de Interfaz:** Acceder a la documentación autogenerada en `http://localhost:8000/docs`.
3. **Prueba End-to-End por HTTP:** Enviar un `POST` desde un script cliente o Postman a `/api/v1/query` preguntando por los pines del AD4086 y confirmar que devuelve el JSON estructurado correctamente.
