"""
splitter.py
===========
Implementa la estrategia de chunking jerarquico Parent-Child con
segmentacion estructural basada en encabezados Markdown.

Estrategia:
-----------
  1. Se divide el documento por encabezados Markdown (H1, H2, H3).
     Cada bloque de texto entre encabezados se convierte en un CHUNK PADRE.
  2. Cada Chunk Padre se subdivide en CHUNKS HIJOS de tamano fijo con
     solapamiento (sliding window).
  3. Los Chunks Hijos llevan un puntero al ID de su Chunk Padre, lo que
     permite recuperar el contexto completo en el momento de la inferencia.

Estructura de datos:
--------------------
  - ParentChunk : Fragmento grande (seccion completa del documento)
  - ChildChunk  : Fragmento pequeno listo para ser indexado en el VectorStore
  - ChunkPair   : Par (parent, children) que sale del splitter
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ---------------------------------------------------------------------------
# Constantes de segmentacion por defecto
# ---------------------------------------------------------------------------

DEFAULT_PARENT_SIZE: int = 1500   # caracteres maximos por chunk padre
DEFAULT_PARENT_OVERLAP: int = 150  # solapamiento entre chunks padre consecutivos
DEFAULT_CHILD_SIZE: int = 300     # caracteres maximos por chunk hijo
DEFAULT_CHILD_OVERLAP: int = 50   # solapamiento entre chunks hijo consecutivos

# Patron para detectar encabezados Markdown (H1, H2, H3)
_HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Tipos de datos
# ---------------------------------------------------------------------------

@dataclass
class ParentChunk:
    """Fragmento grande que representa una seccion del documento."""
    id: str
    content: str
    heading: Optional[str]          # Titulo de la seccion (si existe)
    heading_level: Optional[int]    # Nivel del encabezado (1, 2 o 3)
    metadata: Dict[str, Any]


@dataclass
class ChildChunk:
    """Fragmento pequeno derivado de un ParentChunk, indexable en VectorStore."""
    id: str
    parent_id: str                  # Puntero al chunk padre
    content: str
    chunk_index: int                # Posicion dentro de los hijos del padre
    metadata: Dict[str, Any]


@dataclass
class ChunkPair:
    """Agrupacion de un chunk padre con todos sus chunks hijos."""
    parent: ParentChunk
    children: List[ChildChunk] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Splitter principal
# ---------------------------------------------------------------------------

class ParentChildSplitter:
    """
    Divide un documento en chunks jerarquicos Parent-Child.

    Parametros
    ----------
    parent_size : int
        Numero maximo de caracteres por chunk padre.
    parent_overlap : int
        Numero de caracteres compartidos entre chunks padre consecutivos.
    child_size : int
        Numero maximo de caracteres por chunk hijo.
    child_overlap : int
        Numero de caracteres compartidos entre chunks hijo consecutivos.
    split_by_headings : bool
        Si True (por defecto), divide primero por encabezados Markdown.
        Si False, aplica directamente la sliding window sobre todo el texto.
    """

    def __init__(
        self,
        parent_size: int = DEFAULT_PARENT_SIZE,
        parent_overlap: int = DEFAULT_PARENT_OVERLAP,
        child_size: int = DEFAULT_CHILD_SIZE,
        child_overlap: int = DEFAULT_CHILD_OVERLAP,
        split_by_headings: bool = True,
    ) -> None:
        if parent_size <= 0 or child_size <= 0:
            raise ValueError("Los tamanos de chunk deben ser mayores que cero.")
        if child_size >= parent_size:
            raise ValueError("child_size debe ser menor que parent_size.")

        self.parent_size = parent_size
        self.parent_overlap = parent_overlap
        self.child_size = child_size
        self.child_overlap = child_overlap
        self.split_by_headings = split_by_headings

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------

    def split_document(
        self, text: str, document_metadata: Dict[str, Any]
    ) -> List[ChunkPair]:
        """
        Divide el texto completo de un documento en pares Parent-Child.

        Parametros
        ----------
        text : str
            Texto completo o Markdown del documento parseado.
        document_metadata : dict
            Metadatos base del documento (nombre de fichero, fuente, etc.)

        Returns
        -------
        List[ChunkPair]
            Lista ordenada de pares (padre, [hijos]) con IDs enlazados.
        """
        if not text or not text.strip():
            return []

        # Paso 1: Segmentacion estructural en secciones (chunks padre)
        sections = (
            self._split_by_markdown_headings(text)
            if self.split_by_headings
            else [{"heading": None, "level": None, "content": text}]
        )

        # Paso 2: Para cada seccion grande, aplicar sliding window de padre
        raw_parents: List[Dict[str, Any]] = []
        for section in sections:
            content = section["content"].strip()
            if not content:
                continue
            if len(content) <= self.parent_size:
                raw_parents.append(section)
            else:
                # Seccion muy larga: dividirla en sub-padres con overlap
                sub_blocks = self._sliding_window(
                    content, self.parent_size, self.parent_overlap
                )
                for block in sub_blocks:
                    raw_parents.append(
                        {
                            "heading": section["heading"],
                            "level": section["level"],
                            "content": block,
                        }
                    )

        # Paso 3: Construir ChunkPairs con sus hijos
        pairs: List[ChunkPair] = []
        for idx, raw in enumerate(raw_parents):
            parent_id = self._generate_id("P", document_metadata, idx)
            parent_meta = {
                **document_metadata,
                "chunk_type": "parent",
                "section_heading": raw["heading"],
                "heading_level": raw["level"],
                "parent_index": idx,
            }

            parent = ParentChunk(
                id=parent_id,
                content=raw["content"],
                heading=raw["heading"],
                heading_level=raw["level"],
                metadata=parent_meta,
            )

            # Paso 4: Crear los hijos de este padre
            child_blocks = self._sliding_window(
                raw["content"], self.child_size, self.child_overlap
            )
            children: List[ChildChunk] = []
            for c_idx, c_content in enumerate(child_blocks):
                child_id = self._generate_id("C", document_metadata, idx, c_idx)
                child_meta = {
                    **document_metadata,
                    "chunk_type": "child",
                    "parent_id": parent_id,
                    "section_heading": raw["heading"],
                    "heading_level": raw["level"],
                    "parent_index": idx,
                    "child_index": c_idx,
                }
                children.append(
                    ChildChunk(
                        id=child_id,
                        parent_id=parent_id,
                        content=c_content,
                        chunk_index=c_idx,
                        metadata=child_meta,
                    )
                )

            pairs.append(ChunkPair(parent=parent, children=children))

        return pairs

    # ------------------------------------------------------------------
    # Metodos privados
    # ------------------------------------------------------------------

    def _split_by_markdown_headings(self, text: str) -> List[Dict[str, Any]]:
        """
        Divide el texto Markdown en secciones basandose en encabezados H1-H3.

        Cada seccion incluye el encabezado y el cuerpo de texto que le sigue
        hasta el proximo encabezado del mismo nivel o superior.

        Returns
        -------
        List[dict] con claves: heading, level, content
        """
        sections: List[Dict[str, Any]] = []
        matches = list(_HEADING_PATTERN.finditer(text))

        if not matches:
            # Sin encabezados: el documento entero es una sola seccion
            return [{"heading": None, "level": None, "content": text}]

        # Texto antes del primer encabezado (preambulo)
        preamble = text[: matches[0].start()].strip()
        if preamble:
            sections.append({"heading": None, "level": None, "content": preamble})

        # Iterar sobre los encabezados encontrados
        for i, match in enumerate(matches):
            level = len(match.group(1))   # Numero de '#'
            heading = match.group(2).strip()

            # Contenido: desde el fin del encabezado hasta el inicio del siguiente
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()

            # Incluir el propio encabezado dentro del contenido del chunk
            content = f"{'#' * level} {heading}\n\n{body}" if body else f"{'#' * level} {heading}"

            sections.append({"heading": heading, "level": level, "content": content})

        return sections

    def _sliding_window(
        self, text: str, window_size: int, overlap: int
    ) -> List[str]:
        """
        Aplica una ventana deslizante de longitud fija con solapamiento sobre
        el texto, respetando los limites de palabra para no cortar palabras.

        Parametros
        ----------
        text : str
            Texto sobre el que aplicar la ventana.
        window_size : int
            Tamano maximo de la ventana en caracteres.
        overlap : int
            Numero de caracteres solapados entre ventanas consecutivas.

        Returns
        -------
        List[str] con los bloques de texto generados.
        """
        if not text:
            return []

        step = max(1, window_size - overlap)
        blocks: List[str] = []
        start = 0

        while start < len(text):
            end = min(start + window_size, len(text))

            # Ajustar el final al limite de palabra mas cercano (si no es el fin)
            if end < len(text):
                # Buscar el ultimo espacio dentro de la ventana
                last_space = text.rfind(" ", start, end)
                if last_space > start:
                    end = last_space

            block = text[start:end].strip()
            if block:
                blocks.append(block)

            start += step

        return blocks

    @staticmethod
    def _generate_id(*args) -> str:
        """
        Genera un identificador unico determinista basado en los argumentos
        combinado con un UUID v4 para garantizar unicidad entre ejecuciones.
        """
        # Formato: <prefijo>-<uuid_corto>
        # Ejemplo: P-3f2a1b7c  /  C-9d8e0a4f
        prefix = str(args[0]) if args else "CHUNK"
        return f"{prefix}-{uuid.uuid4().hex[:8]}"
