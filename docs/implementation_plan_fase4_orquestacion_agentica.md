# Plan de Implementación — Fase 4: Orquestación Agéntica y Generación Grounded

## Objetivo

Implementar la capa de orquestación y generación del sistema RAG Industrial. Esta fase permitirá responder de forma precisa y fundamentada a las consultas del usuario utilizando los fragmentos recuperados en la Fase 3, garantizando la total ausencia de alucinaciones y obligando al modelo a citar la fuente exacta de su respuesta.

El pipeline agéntico constará de:
1. **Agentic Router (`AgenticRouter`)**: Clasifica la consulta en tres categorías (`LINEA_PRODUCCION`, `I_D_PATENTES`, `ESPECIFICACIONES`) para optimizar el camino de búsqueda y la latencia.
2. **Compresor Contextual (`ContextCompressor`)**: Reduce el tamaño del contexto para mitigar el efecto *Lost in the Middle*. Se implementará una compresión heurística avanzada basada en la puntuación de oraciones del Cross-Encoder para conservar únicamente las oraciones más relevantes de los chunks padres.
3. **Generador Grounded (`GroundedGenerator`)**: Genera la respuesta técnica final a través del LLM, formateando el contexto con identificadores únicos y forzando citaciones estrictas en formato `[DocName, pág. X]` o `[parent_id]`.

---

## Contexto actual

- El motor de recuperación avanzado (`RetrievalEngine`) funciona de extremo a extremo, retornando el Top-K de chunks padres ordenados semánticamente.
- Las dependencias de LLM (`openai` SDK) están instaladas.
- Existe un fallback seguro que permite probar la lógica incluso si no hay conexión a APIs de LLM externas.

---

## User Review Required

> [!IMPORTANT]
> **Compresión Contextual Local vs. LLMLingua**: Para evitar descargar otro modelo masivo de lenguaje en local (que requeriría entre 3 y 7 GB de RAM para medir perplejidad con LLMLingua), proponemos una **compresión semántica por oraciones utilizando el Cross-Encoder ya cargado** (`ms-marco-MiniLM-L-6-v2`). El compresor dividirá el chunk padre en oraciones, calculará el score de relevancia de cada oración contra la pregunta del usuario y mantendrá solo las $N$ oraciones con mayor relevancia. Esto reduce el contexto un 60% de forma ultra-rápida en CPU/GPU sin modelos adicionales. ¿Aprobamos este enfoque heurístico?

> [!IMPORTANT]
> **Políticas de Mitigación de Alucinaciones**: El sistema utilizará un prompt con reglas negativas estrictas: si el contexto no contiene la respuesta, el LLM retornará obligatoriamente `"INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD"`. Cualquier intento de deducción creativa será penalizado con temperatura cero absoluta (`temperature=0.0`).

---

## Proposed Changes

### Componente 1: Enrutamiento Inteligente

#### [NEW] [router.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/router.py)
Clase `AgenticRouter`:
- Método `route_query(query: str) -> str`: Clasifica la consulta en:
  - `LINEA_PRODUCCION`: Consultas operativas rápidas (ej: alarmas, fallos mecánicos directos). Búsqueda híbrida básica, sin HyDE, latencia mínima.
  - `I_D_PATENTES`: Consultas conceptuales complejas de diseño. Requiere HyDE y reranking profundo.
  - `ESPECIFICACIONES`: Datos exactos de dimensiones, límites y torques. Sin HyDE (para evitar alucinaciones en cifras), pre-filtrado estricto por proyecto.
- Fallback determinista: Si no hay LLM activo, analiza por palabras clave (ej: si contiene "alarma", "error", "line" -> `LINEA_PRODUCCION`).

---

### Componente 2: Compresión Contextual Semántica

#### [NEW] [compressor.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/compressor.py)
Clase `ContextCompressor`:
- Toma un `ParentChunk` o texto, lo segmenta en oraciones (usando expresiones regulares).
- Utiliza la instancia del `CrossEncoderReranker` para evaluar el score de cada pareja `(query, oración)`.
- Reconstruye el chunk conservando únicamente las oraciones con puntuación superior a un umbral (o el Top-N oraciones), manteniendo su orden físico de aparición en el documento para no destruir la estructura del texto.

---

### Componente 3: Generador Grounded con Citas Estrictas

#### [NEW] [generator.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/generator.py)
Clase `GroundedGenerator`:
- Construcción y renderizado del prompt de ingeniería con el contexto hidratado y comprimido.
- Reglas inquebrantables de generación:
  - Prohibido suponer o inventar.
  - Formato estricto de citas inline: `[NombreDocumento, Sección]` o `[parent_id]`.
  - Retorno unívoco de no disponibilidad de información.
- Método `generate_response(query: str, contexts: List[ParentChunk]) -> Dict[str, Any]` que retorna `{"answer": str, "used_contexts": list, "sources": list}`.

---

### Componente 4: Orquestador Agéntico Completo (AgenticRAGPipeline)

#### [NEW] [agentic_pipeline.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/agentic_pipeline.py)
La clase central `AgenticRAGPipeline` (o método integrado en `RetrievalEngine`):
- Integra el Router, el RetrievalEngine, el Compresor y el Generador Grounded en un único flujo:
```
Usuario Query ──► Router (Clasifica) 
                 ├── LINEA_PRODUCCION ──► Retrieval Rápido (Top-5) ──► Compresión ──► Generación
                 └── I+D / PATENTES   ──► HyDE + Retrieval Profundo ──► Compresión ──► Generación
```

---

### Componente 5: Tests y Playground

#### [NEW] [playground/test_agentic.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/test_agentic.py)
Script interactivo y de test para la Fase 4 que valida:
1. **Router**: Clasificación correcta de consultas de prueba.
2. **Compressor**: Reducción efectiva del tamaño del texto de entrada conservando la respuesta clave.
3. **Generator**: Generación correcta sin API key (fallback a mock) y con API key (OpenAI/Ollama).
4. **Citas e Integridad**: Validación de que el output del LLM contiene cadenas de citación correctas.

---

## Verification Plan

### Automated Tests
- Ejecutar `playground/test_agentic.py` con mock de LLM (valida lógica del router, compresor y formateador de prompts).
- Ejecutar `playground/test_agentic.py` con OpenAI/Ollama (si hay credenciales) validando la concordancia y la no alucinación.

### Criterios de Éxito
- **Tasa de compresión**: El compresor contextual debe reducir la longitud en caracteres del contexto en al menos un **40%**.
- **Preservación semántica**: La respuesta de la pregunta clave debe seguir estando presente en las oraciones seleccionadas por el compresor.
- **Citación estricta**: El 100% de las respuestas generadas con éxito deben contener al menos una cita en formato de corchetes.
- **Comportamiento seguro**: Al preguntar algo fuera del datasheet (ej. *"¿Cuál es la órbita de Júpiter?"*), el sistema debe responder exactamente: `"INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD"`.
