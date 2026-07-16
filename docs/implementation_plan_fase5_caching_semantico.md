# Plan de Implementación: Caching Semántico en Planta (Fase 5 - Parte 1)

Este documento detalla el diseño técnico para implementar un sistema de **Caché Semántica** para el motor de RAG Industrial, reduciendo la latencia de respuesta para consultas repetidas o semánticamente similares a menos de 150 ms y minimizando el coste de llamadas al LLM.

---

## User Review Required

> [!IMPORTANT]
> **Consumo de Recursos (RAM/VRAM):**
> Dado que el sistema tiene restricciones estrictas de RAM, se propone **usar Qdrant** (creando una colección dedicada `semantic_cache` dentro de la base de datos vectorial existente) como la opción por defecto. Esto evita la necesidad de levantar un servicio de Redis adicional, ahorrando unos ~500 MB de memoria en la planta. No obstante, el diseño será modular para que se pueda habilitar Redis mediante una variable de entorno.

---

## Open Questions

> [!WARNING]
> 1. **Umbral de Similitud Semántica (Threshold):**
>    ¿Es adecuado un umbral inicial de **0.95** para considerar dos preguntas como idénticas? Un umbral demasiado bajo podría retornar respuestas incorrectas (falsos positivos), y uno muy alto causaría fallos de caché (cache misses) innecesarios.
> 2. **Política de Expiración (TTL):**
>    ¿Cuánto tiempo deben considerarse válidas las respuestas en caché? Proponemos un tiempo de vida (TTL) de **7 días**, después del cual la consulta debe refrescarse ejecutando el RAG completo.

---

## Proposed Changes

### 1. Motor de Caché Semántica
Crearemos un módulo genérico de caché que interactúa con la base de datos vectorial para guardar y consultar embeddings de preguntas previas.

#### [NEW] [cache.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/cache.py)
- Clase `SemanticCache`:
  - `check(query_text: str) -> Optional[dict]`: Obtiene el embedding de la pregunta y busca en la colección `semantic_cache`. Si la similitud supera el umbral, retorna la respuesta almacenada en el payload.
  - `update(query_text: str, response: dict) -> None`: Almacena el par (pregunta, respuesta) en la colección de caché junto con su vector y un timestamp de creación.

### 2. Modificaciones de API (FastAPI)
Actualizaremos los endpoints para interceptar las consultas entrantes y retornar respuestas de la caché si existen.

#### [MODIFY] [dependencies.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/dependencies.py)
- Añadir la inicialización de la colección `semantic_cache` en Qdrant al arrancar la app.
- Crear el provider de dependencias `get_semantic_cache()`.

#### [MODIFY] [routes.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py)
- Modificar el endpoint `/query`:
  - Antes de llamar a `rag.query()`, consultar `cache.check(request.query)`.
  - Si hay un *Cache Hit*, retornar la respuesta directamente con la traza marcada como `cache_hit: true` y el score de similitud.
  - Si hay un *Cache Miss*, procesar con el LLM y luego registrar el resultado llamando a `cache.update(request.query, result)`.

#### [MODIFY] [schemas.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/schemas.py)
- Añadir campos en `PipelineTrace` para auditoría de la caché:
  - `cache_hit`: bool (si la respuesta provino de la caché semántica).
  - `cache_similarity`: Optional[float] (score de similitud del hit).

---

## Verification Plan

### Manual Verification
1. **Script de Prueba (`playground/test_semantic_cache.py`)**:
   - Realizar una primera consulta: `"¿Cuál es la función de los pines B4 y B5?"` (Medir tiempo: esperado ~5-15s).
   - Realizar la misma consulta de forma idéntica (Medir tiempo: esperado <50ms, `cache_hit: true`).
   - Realizar una consulta semánticamente muy parecida: `"¿qué hacen los pines B4 y B5 del ad4086?"` (Medir tiempo: esperado <100ms, `cache_hit: true`, score >= 0.95).
   - Realizar una consulta distinta: `"¿cuál es la temperatura máxima de operación?"` (Debe ser un Miss y procesar por LLM).
