"""
pipeline.py
===========
Orquestador central del flujo de ingesta de documentos técnicos e industriales.

Flujo de process_file()
------------------------
  1. PARSE   → Detecta la extensión del fichero y selecciona el parser adecuado.
               Extrae el texto completo en formato Markdown.

  2. SPLIT   → ParentChildSplitter divide el texto en ChunkPairs jerárquicos
               (chunks padre por sección Markdown + chunks hijo por ventana deslizante).

  3. ENRICH  → MetadataExtractor enriquece cada chunk con el payload estructurado:
               idioma, doc_type, project_id, confidentiality, etc.

  4. STORE   → DocStoreManager persiste los ParentChunks en disco (JSON files).

  5. INDEX   → VectorStoreManager vectoriza e indexa los ChildChunks en Qdrant.

  6. REPORT  → Devuelve un diccionario con las estadísticas de la ingesta.

Configuración por defecto
--------------------------
  - Embeddings  : BAAI/bge-m3 (local, ~2.2 GB)
  - VectorDB    : Qdrant en modo embebido local (./qdrant_db)
  - DocStore    : JSON files en disco (./data_store/parents/)
  - Chunking    : parent_size=1500 / child_size=300 / split_by_headings=True
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.ingestion.parsers.pdf_parser import MarkerPDFParser
from app.ingestion.parsers.docx_parser import PandocDocxParser
from app.ingestion.chunking.splitter import ParentChildSplitter, ChunkPair
from app.ingestion.metadata.extractor import MetadataExtractor
from app.ingestion.storage.vector_store import VectorStoreManager
from app.ingestion.storage.doc_store import DocStoreManager
from app.ingestion.sync.ledger import IngestionLedger


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

_SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx",
}


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class IngestionPipeline:
    """
    Orquestador completo del flujo de ingesta de documentos técnicos e industriales.

    Parámetros
    ----------
    storage_path : str
        Directorio raíz para el DocStore (chunks padre en JSON).
    qdrant_path : str
        Directorio para la base de datos Qdrant embebida.
    collection_name : str
        Nombre de la colección Qdrant para los chunks hijos.
    embedding_model : str
        Modelo SentenceTransformer para vectorización.
    parent_size : int
        Tamaño máximo del chunk padre en caracteres.
    child_size : int
        Tamaño máximo del chunk hijo en caracteres.
    """

    def __init__(
        self,
        storage_path: str = "./data_store",
        qdrant_path: str = "./qdrant_db",
        collection_name: str = "industrial_chunks",
        embedding_model: str = "BAAI/bge-m3",
        parent_size: int = 1500,
        parent_overlap: int = 150,
        child_size: int = 300,
        child_overlap: int = 50,
    ) -> None:
        # Parsers (lazy initialization dentro de cada clase)
        self.pdf_parser = MarkerPDFParser()
        self.docx_parser = PandocDocxParser()

        # Splitter jerárquico
        self.splitter = ParentChildSplitter(
            parent_size=parent_size,
            parent_overlap=parent_overlap,
            child_size=child_size,
            child_overlap=child_overlap,
            split_by_headings=True,
        )

        # Enriquecimiento de metadatos (modo heurístico)
        self.extractor = MetadataExtractor(use_llm=False)

        # Almacenamiento
        self.vector_store = VectorStoreManager(
            collection_name=collection_name,
            qdrant_path=qdrant_path,
            embedding_model=embedding_model,
        )
        self.doc_store = DocStoreManager(storage_path=storage_path)

        # Ledger de indexación incremental (stub — Fase 5)
        self.ledger = IngestionLedger()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def process_file(
        self,
        file_path: str,
        base_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Procesa un fichero completo por el flujo de ingesta.

        Parámetros
        ----------
        file_path : str
            Ruta absoluta o relativa al fichero a ingestar.
        base_metadata : dict | None
            Metadatos base del documento. Campos reconocidos:
              project_id, product_line, doc_type, confidentiality,
              version, creation_timestamp.

        Returns
        -------
        dict
            Estadísticas de la ingesta:
              file_path, n_parents, n_children, duration_seconds, status.

        Raises
        ------
        ValueError
            Si el formato del fichero no está soportado.
        FileNotFoundError
            Si el fichero no existe en la ruta indicada.
        """
        start_time = time.perf_counter()
        path = Path(file_path)

        # ---- Validaciones previas ----
        if not path.exists():
            raise FileNotFoundError(f"Fichero no encontrado: {file_path}")

        ext = path.suffix.lower()
        if ext not in _SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Formato '{ext}' no soportado. "
                f"Formatos válidos: {list(_SUPPORTED_EXTENSIONS.keys())}"
            )

        if base_metadata is None:
            base_metadata = {}

        # Enriquecer base_metadata con información del fichero si no viene ya
        base_metadata.setdefault("source", str(path.resolve()))
        base_metadata.setdefault("document_name", path.stem)
        base_metadata.setdefault("file_type", _SUPPORTED_EXTENSIONS[ext])

        # ----------------------------------------------------------------
        # PASO 1: PARSE
        # ----------------------------------------------------------------
        fmt = _SUPPORTED_EXTENSIONS[ext]
        if fmt == "pdf":
            raw_text = self.pdf_parser.parse(str(path))
        else:
            raw_text = self.docx_parser.parse(str(path))

        if not raw_text or not raw_text.strip():
            return {
                "file_path": str(path),
                "n_parents": 0,
                "n_children": 0,
                "duration_seconds": round(time.perf_counter() - start_time, 2),
                "status": "empty_document",
                "parent_ids": [],
            }

        # Detección del idioma a nivel de documento para optimizar llamadas redundantes
        if "language" not in base_metadata:
            from app.ingestion.metadata.extractor import _detect_language
            base_metadata["language"] = _detect_language(raw_text)


        # ----------------------------------------------------------------
        # PASO 2: SPLIT
        # ----------------------------------------------------------------
        pairs: List[ChunkPair] = self.splitter.split_document(raw_text, base_metadata)

        if not pairs:
            return {
                "file_path": str(path),
                "n_parents": 0,
                "n_children": 0,
                "duration_seconds": round(time.perf_counter() - start_time, 2),
                "status": "no_chunks_generated",
                "parent_ids": [],
            }

        # ----------------------------------------------------------------
        # PASO 3: ENRICH METADATA
        # ----------------------------------------------------------------
        # Enriquecer los metadatos de cada chunk (padre e hijo)
        # con el payload de metadatos industriales.
        for pair in pairs:
            # Enriquecer metadatos del padre
            enriched_parent = self.extractor.enrich_chunk(
                chunk_metadata=pair.parent.metadata,
                base_metadata=base_metadata,
                text_sample=pair.parent.content,
            )
            pair.parent.metadata.update(enriched_parent)

            # Enriquecer metadatos de cada hijo
            for child in pair.children:
                enriched_child = self.extractor.enrich_chunk(
                    chunk_metadata=child.metadata,
                    base_metadata=base_metadata,
                    text_sample=child.content,
                )
                child.metadata.update(enriched_child)

        # ----------------------------------------------------------------
        # PASO 4: STORE PARENTS (DocStore)
        # ----------------------------------------------------------------
        n_parents = self.doc_store.save_parents(pairs)

        # ----------------------------------------------------------------
        # PASO 5: INDEX CHILDREN (VectorStore)
        # ----------------------------------------------------------------
        all_children = [child for pair in pairs for child in pair.children]
        n_children = self.vector_store.add_child_chunks(all_children)

        # ----------------------------------------------------------------
        # PASO 6: REPORT
        # ----------------------------------------------------------------
        duration = round(time.perf_counter() - start_time, 2)
        return {
            "file_path": str(path),
            "n_parents": n_parents,
            "n_children": n_children,
            "duration_seconds": duration,
            "status": "ok",
            "parent_ids": [pair.parent.id for pair in pairs],
        }

    def get_collection_info(self) -> Dict[str, Any]:
        """Información sobre el estado actual de la colección Qdrant."""
        return self.vector_store.collection_info()

    def retrieve_parent(self, parent_id: str):
        """Recupera un chunk padre del DocStore por su ID."""
        return self.doc_store.get_parent(parent_id)
