# Plan de Implementación: Framework de Evaluación Automatizada con RAGAS (Fase 6)

Este documento detalla el diseño técnico para implementar el **Framework de Evaluación Automatizada** de nuestro pipeline RAG utilizando la librería **RAGAS** y la API de **Google Gemini** de forma nativa como juez evaluador y modelo de embeddings.

---

## User Review Required

> [!IMPORTANT]
> **Modelo Evaluador y Embeddings de RAGAS:**
> RAGAS tradicionalmente depende de OpenAI por defecto. Proponemos configurarlo para usar de forma nativa la API de **Google Gemini** (`google-genai` SDK) que ya está integrada en el proyecto. 
> - Usaremos `gemini-3.5-flash` como modelo LLM de evaluación (juez).
> - Usaremos `text-embedding-004` (el estándar recomendado de Google GenAI) para las métricas que requieren distancias vectoriales de embedding, como `answer_relevancy`.
> Esto evita añadir dependencias de OpenAI y reutiliza la API activa de Google.

---

## Open Questions

> [!WARNING]
> 1. **Instalación de Dependencias**:
>    Para ejecutar la evaluación necesitaremos instalar los paquetes `ragas`, `datasets` y `pandas`. ¿Se permite la ejecución automática de la instalación de estas librerías en el entorno virtual de Python durante la fase de ejecución?
> 2. **Tamaño del Golden Dataset de Validación**:
>    La guía en producción propone un conjunto fijo de **120 preguntas críticas**. Para esta fase y PoC, proponemos crear un **Golden Dataset inicial de 10 preguntas y respuestas de referencia (Ground Truth)** clave basadas en los dos datasheets indexados (`AD4086` y `ad9446`). Esto permite una ejecución de pruebas rápida en CI/CD. ¿Es aceptable este tamaño de PoC?

---

## Proposed Changes

### 1. Actualización del Pipeline para Retener Contextos Completos
Para que RAGAS pueda calcular las métricas de fidelidad y cobertura de contexto, necesita la lista de textos de contexto completo que se inyectaron al prompt del LLM.

#### [MODIFY] [agentic_pipeline.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/retrieval/agentic_pipeline.py)
- Añadir el campo `contexts` en el diccionario retornado por `query()`:
  - `"contexts": [chunk.content for chunk in compressed_parents]` dentro de la clave `pipeline_trace`.
  - Esto proporcionará la lista de strings con los fragmentos de contexto reales.

---

### 2. Creación del Golden Dataset de Referencia

#### [NEW] [golden_dataset.json](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/data/golden_dataset.json)
- Crear un archivo JSON estructurado con preguntas técnicas y respuestas definitivas escritas por expertos (Ground Truth):
```json
[
  {
    "question": "¿Cuál es la resolución y la velocidad de muestreo del AD4086 según su hoja de especificaciones?",
    "ground_truth": "El AD4086 es un ADC de alto rendimiento con una resolución de 16 bits y una velocidad de muestreo de hasta 80 MSPS."
  },
  {
    "question": "¿Cuál es el límite absoluto de torque admisible para el acople de la extrusora Line-3 en el manual V2?",
    "ground_truth": "INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD"
  },
  {
    "question": "¿Cuál es la frecuencia de muestreo máxima del convertidor AD9446?",
    "ground_truth": "La frecuencia de muestreo del AD9446 es de hasta 80 MSPS / 100 MSPS."
  }
]
```

---

### 3. Script Orquestador de Evaluación

#### [NEW] [run_evaluation.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/playground/run_evaluation.py)
- Un script independiente en Python que ejecute la evaluación y aplique políticas de gatekeeping:
  1. Cargar el `golden_dataset.json`.
  2. Inicializar `AgenticRAGPipeline` utilizando la base de datos local Qdrant activa.
  3. Ejecutar las preguntas del dataset recolectando la respuesta generada (`answer`) y los contextos (`contexts`) de `pipeline_trace`.
  4. Dar formato de Dataset de Hugging Face (`Dataset.from_dict(...)`).
  5. Configurar RAGAS para usar Gemini como evaluador y embeddings:
     - Utilizar `llm_factory` de RAGAS con el proveedor `"google"`.
     - Utilizar `GoogleEmbeddings` de RAGAS para `text-embedding-004`.
  6. Lanzar `evaluate` con las métricas de: `faithfulness`, `answer_relevancy`, `context_precision`, y `context_recall`.
  7. Guardar los resultados en `playground/evaluation_results.csv`.
  8. **Gatekeeping de CI/CD**: Validar que el promedio del score de `faithfulness` sea `>= 0.95`. Si no se cumple, imprimir advertencia y finalizar el script con código de salida `1` (fail), de lo contrario con `0` (success).

---

### 4. API Endpoints para Evaluación HTTP
Agregaremos esquemas y endpoints para poder disparar y monitorizar la evaluación del RAG de manera programática a través del servidor FastAPI.

#### [MODIFY] [schemas.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/schemas.py)
- Definir las clases `EvaluationRequest`, `MetricScores` y `EvaluationResponse` para tipar la respuesta de la evaluación.

#### [MODIFY] [routes.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py)
- Crear el endpoint `POST /api/v1/eval/run` que invoque la lógica del script de evaluación en segundo plano (FastAPI Background Tasks) y almacene el reporte de la última ejecución.

---

## Verification Plan

### Automated Tests
1. **Instalación de Dependencias**:
   - Ejecutar la instalación de Ragas en el entorno virtual.
2. **Ejecución del Pipeline RAGAS**:
   - Correr `python playground/run_evaluation.py` en local y verificar que:
     - Loguea la llamada a cada consulta del golden dataset.
     - Inicializa correctamente el evaluador y los embeddings de Google Gemini.
     - Ejecuta la evaluación e imprime la tabla de puntuación (Fidelidad, Relevancia, Cobertura, Precisión).
     - Genera y escribe con éxito el archivo de resultados CSV en la carpeta `playground/`.
     - Retorna código de salida `0` si el score de fidelidad supera el 95%.
3. **Validación del Endpoint de API**:
   - Iniciar la API localmente y llamar a `POST /api/v1/eval/run` usando `TestClient` o `Postman`.
   - Validar que responde con el estado de inicio de la tarea y devuelve las métricas correspondientes al completarse.
