# Plan de Implementación: Pipeline de Actualización Incremental (Fase 5 - Parte 2)

Este documento detalla el diseño técnico para implementar el **Pipeline de Ingestión Incremental** utilizando un ledger relacional local en SQLite. El sistema detectará automáticamente archivos nuevos, modificados y eliminados en un directorio compartido de ingeniería, actualizando la base de datos vectorial y el almacén documental sin tener que re-indexar todo desde cero.

---

## User Review Required

> [!IMPORTANT]
> **Eliminación y Desuscripción de Vectores (Tombstoning):**
> Al modificar o eliminar un archivo, es crucial purgar todos sus vectores huérfanos de Qdrant. Qdrant permite eliminar puntos mediante filtros basados en metadatos. Proponemos añadir a `VectorStoreManager` una función que elimine todos los puntos cuyo campo de metadatos `source` (ruta del archivo) coincida con la del documento borrado. Esto garantiza una sincronización 100% limpia.

---

## Open Questions

> [!WARNING]
> 1. **Detección de Archivos Huérfanos:**
>    Si un archivo se elimina físicamente del disco local del servidor de ingeniería, la sincronización debe detectarlo. Proponemos realizar una verificación bidireccional (verificar si las rutas registradas en la base de datos SQLite del ledger siguen existiendo en el disco físico). ¿Es este el comportamiento esperado para la purga automática?
> 2. **Ruta por Defecto de la DB de Ledger:**
>    Proponemos ubicar la base de datos SQLite del ledger en `data_store/ledger.db` para que se guarde de manera segura junto con los chunks padres indexados y no se pierda al reiniciar.

---

## Proposed Changes

### 1. Motor de Sincronización y Ledger SQLite
Implementaremos el ledger relacional local utilizando la biblioteca estándar `sqlite3` de Python (evitando añadir dependencias externas pesadas).

#### [MODIFY] [ledger.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/sync/ledger.py)
- Reemplazar la clase `IngestionLedger` con una implementación real en SQLite:
  - Crear la tabla `document_ledger` en `data_store/ledger.db` si no existe.
  - Campos: `file_path` (TEXT Primary Key), `file_hash` (TEXT, SHA-256), `last_modified` (REAL), `parent_ids` (TEXT, lista separada por comas).
  - Implementar [`calculate_hash(file_path)`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/sync/ledger.py#L9) leyendo bloques binarios del archivo de manera eficiente en memoria.
  - Implementar [`detect_changes(file_paths)`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/sync/ledger.py#L14) para contrastar el estado actual del disco físico contra la base de datos SQLite y retornar los conjuntos de archivos `new`, `modified` y `deleted`.
  - Implementar métodos de inserción, actualización y borrado del ledger.

### 2. Soporte de Eliminación en Almacenes e Ingestión Eficiente

#### [MODIFY] [pdf_parser.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/parsers/pdf_parser.py)
- Optimizar [`MarkerPDFParser.parse(file_path)`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/parsers/pdf_parser.py#L43):
  - Verificar si existe un archivo `.md` homónimo en el mismo directorio (ej. si recibe `AD4086_Datasheet.pdf`, busca `AD4086_Datasheet.md`).
  - Si existe, leerlo directamente y omitir la carga en memoria e inferencia de los modelos neuronales de `Marker`, acelerando el procesamiento en máquinas con baja RAM.

#### [MODIFY] [vector_store.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/storage/vector_store.py)
- Añadir el método `delete_by_source(source_path: str) -> int`:
  - Utiliza `client.delete()` de Qdrant con un selector de filtros que busque todos los vectores donde `"source" == source_path`.
  - Retorna la cantidad de puntos eliminados.

### 3. Orquestador de Ingestión Incremental
#### [NEW] [orchestrator.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/sync/orchestrator.py)
- Clase `IncrementalSyncOrchestrator`:
  - `sync_directory(directory_path: str) -> dict`:
    1. Escanea el directorio en busca de documentos soportados (`.pdf`, `.docx`).
    2. Ejecuta `detect_changes` en el ledger.
    3. Para cada archivo **eliminado**:
       - Recupera sus `parent_ids` del ledger y los elimina de `DocStoreManager`.
       - Llama a `delete_by_source` en `VectorStoreManager` para borrar sus vectores.
       - Elimina el archivo de la DB de ledger.
    4. Para cada archivo **modificado**:
       - Recupera y elimina todos sus `parent_ids` anteriores y vectores (igual que en los eliminados).
       - Llama a `pipeline.process_file()` para extraer los nuevos chunks padre/hijo.
       - Guarda los nuevos chunks en vector store y doc store.
       - Registra los nuevos hashes y los nuevos `parent_ids` en el ledger.
    5. Para cada archivo **nuevo**:
       - Ejecuta `pipeline.process_file()`.
       - Registra en el ledger con su hash y lista de `parent_ids`.
    6. Retorna un reporte con el resumen de la sincronización: `{'added': X, 'updated': Y, 'deleted': Z, 'skipped': W}`.

### 4. Modificaciones en el Pipeline Principal
#### [MODIFY] [pipeline.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/pipeline.py)
- En [`process_file`](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/ingestion/pipeline.py#L123), cambiar el retorno del método para que además de estadísticas, devuelva la lista de `parent_ids` generados. Esto permitirá al orquestador registrar qué chunks corresponden a cada archivo físico.

### 5. Rutas FastAPI
#### [MODIFY] [routes.py](file:///d:/PropuestaCanalYoutube/2026-06-16-RAG-Industrial/app/api/routes.py)
- Añadir endpoint `POST /api/v1/ingest/sync_dir`:
  - Espera un JSON con la ruta del directorio local.
  - Instancia el orquestador y ejecuta la sincronización en segundo plano mediante un background task de FastAPI.
  - Devuelve un ticket inmediato de proceso iniciado.

---

## Verification Plan

### Manual Verification
1. **Verificación de Ingestión Inicial**:
   - Ejecutar la sincronización sobre una carpeta con 2 archivos PDF de prueba.
   - Validar que se indexan en Qdrant y se registra en SQLite ledger con hashes correctos.
2. **Verificación de Modificación**:
   - Editar uno de los PDFs de prueba (ej. añadir un párrafo o cambiar algún número) y volver a ejecutar la sincronización.
   - Validar que el ledger detecta que está modificado, elimina los chunks anteriores y sube los nuevos.
3. **Verificación de Eliminación**:
   - Borrar uno de los archivos PDF del disco y volver a ejecutar la sincronización.
   - Validar que se borran de Qdrant los vectores de ese archivo (y que disminuye el recuento en `/health`), y que el ledger purga el registro de la DB.
