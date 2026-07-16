"""
extractor.py
============
Extrae y enriquece los ChunkPairs con un payload de metadatos estructurado
y estrictamente tipado, listo para ser almacenado como payload en Qdrant.

Modos de operación
------------------
  - Heurístico (use_llm=False, por defecto):
      Detecta el idioma con langdetect, infiere doc_type por nombre de
      fichero y hereda el resto de base_metadata. Sin coste externo, sin
      dependencias de red.

  - LLM estructurado (use_llm=True):
      Reservado para fases futuras. Llamará a un modelo local (ej. Ollama
      con structured output) para inferir project_id, product_line y
      version directamente del texto del chunk.

Campos del esquema IndustrialMetadata
--------------------------------------
  project_id         — Identificador del proyecto de I+D (RBAC)
  product_line       — Línea de producto o maquinaria específica
  doc_type           — Tipo documental (enum)
  confidentiality    — Nivel de acceso (enum, base para RBAC)
  version            — Versión del documento
  creation_timestamp — Unix epoch (para ordenación y obsolescencia)
  language           — Idioma detectado automáticamente
  source             — Ruta absoluta del fichero origen
  document_name      — Nombre del documento sin extensión
  section_heading    — Título de la sección (del ChunkPair.parent)
  heading_level      — Nivel del encabezado (1, 2, 3 o None)
  chunk_type         — "parent" | "child"
  parent_id          — ID del chunk padre (solo para chunks hijo)
  parent_index       — Posición del padre dentro del documento
  child_index        — Posición del hijo dentro de su padre (solo child)
"""

from __future__ import annotations

import re
import time
from typing import Literal, Optional
from typing_extensions import TypedDict

# langdetect es opcional: si no está instalado, el campo language = "unknown"
try:
    from langdetect import detect as _langdetect_detect
    _LANGDETECT_AVAILABLE = True
except ImportError:
    _LANGDETECT_AVAILABLE = False


# ---------------------------------------------------------------------------
# Esquema de metadatos industriales
# ---------------------------------------------------------------------------

DocType = Literal["PRD", "SOP", "MAINTENANCE_LOG", "DATASHEET", "PATENT", "OTHER"]
ConfidentialityLevel = Literal["PUBLIC", "INTERNAL", "RESTRICTED", "TOP_SECRET"]


class IndustrialMetadata(TypedDict, total=False):
    # Campos de identificación del documento
    project_id: str
    product_line: str
    doc_type: DocType
    confidentiality: ConfidentialityLevel
    version: str
    creation_timestamp: int
    language: str
    source: str
    document_name: str

    # Campos de posición estructural (del ChunkPair)
    section_heading: Optional[str]
    heading_level: Optional[int]
    chunk_type: Literal["parent", "child"]
    parent_id: Optional[str]
    parent_index: int
    child_index: Optional[int]


# ---------------------------------------------------------------------------
# Reglas heurísticas de inferencia de doc_type
# ---------------------------------------------------------------------------

# Cada entrada: (patrón regex sobre el nombre del fichero en minúsculas, doc_type resultante)
# Se evalúan en orden; la primera coincidencia gana.
_DOCTYPE_RULES: list[tuple[str, DocType]] = [
    (r"datasheet|data.?sheet|ds\d|spec", "DATASHEET"),
    (r"sop|standard.?operating|procedure", "SOP"),
    (r"mainten|mantenim|servic|repair", "MAINTENANCE_LOG"),
    (r"patent|ip\d|invention", "PATENT"),
    (r"prd|product.?requirement|product.?spec", "PRD"),
]


def _infer_doc_type(document_name: str) -> DocType:
    """Infiere el tipo documental a partir del nombre del fichero."""
    name_lower = document_name.lower()
    for pattern, dtype in _DOCTYPE_RULES:
        if re.search(pattern, name_lower):
            return dtype
    return "OTHER"


def _detect_language(text: str) -> str:
    """Detecta el idioma del fragmento de texto (primeros 500 chars)."""
    if not _LANGDETECT_AVAILABLE or not text or not text.strip():
        return "unknown"
    try:
        sample = text[:500]
        return _langdetect_detect(sample)
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Extractor principal
# ---------------------------------------------------------------------------

class MetadataExtractor:
    """
    Enriquece los chunks con un payload de metadatos estructurado.

    Parámetros
    ----------
    use_llm : bool
        Si True, activa el modo LLM (no implementado en esta fase).
        Si False (por defecto), usa reglas heurísticas deterministas.
    """

    def __init__(self, use_llm: bool = False) -> None:
        self.use_llm = use_llm
        if use_llm:
            raise NotImplementedError(
                "El modo LLM del MetadataExtractor está reservado para fases futuras. "
                "Usa use_llm=False para el modo heurístico determinista."
            )

    def enrich_chunk(
        self,
        chunk_metadata: dict,
        base_metadata: dict,
        text_sample: str = "",
    ) -> IndustrialMetadata:
        """
        Enriquece los metadatos de un chunk individual (padre o hijo).

        Combina:
          1. Los metadatos estructurales del chunk (section_heading, chunk_type, etc.)
          2. Los metadatos base del documento (project_id, confidentiality, etc.)
          3. Los metadatos inferidos heurísticamente (language, doc_type)

        Parámetros
        ----------
        chunk_metadata : dict
            Metadatos ya incluidos en el ChunkPair (del splitter).
        base_metadata : dict
            Metadatos base del documento proporcionados en la llamada al pipeline.
        text_sample : str
            Texto del chunk para detección de idioma.

        Returns
        -------
        IndustrialMetadata
            Payload completo listo para indexar en Qdrant.
        """
        document_name = base_metadata.get("document_name", "")

        # --- Campos inferidos heurísticamente ---
        doc_type: DocType = base_metadata.get(
            "doc_type", _infer_doc_type(document_name)
        )
        language = base_metadata.get("language") or _detect_language(text_sample)


        # --- Construcción del payload final ---
        enriched: IndustrialMetadata = {
            # Identificación del documento
            "project_id": base_metadata.get("project_id", "common"),
            "product_line": base_metadata.get("product_line", "unknown"),
            "doc_type": doc_type,
            "confidentiality": base_metadata.get("confidentiality", "INTERNAL"),
            "version": base_metadata.get("version", "1.0.0"),
            "creation_timestamp": base_metadata.get(
                "creation_timestamp", int(time.time())
            ),
            "language": language,
            "source": base_metadata.get("source", ""),
            "document_name": document_name,

            # Posición estructural (heredada del chunk)
            "section_heading": chunk_metadata.get("section_heading"),
            "heading_level": chunk_metadata.get("heading_level"),
            "chunk_type": chunk_metadata.get("chunk_type", "child"),
            "parent_id": chunk_metadata.get("parent_id"),
            "parent_index": chunk_metadata.get("parent_index", 0),
            "child_index": chunk_metadata.get("child_index"),
        }

        return enriched
