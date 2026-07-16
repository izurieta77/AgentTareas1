"""
doc_store.py
============
Persistencia KV de chunks padre (ParentChunk) en disco local.

Estrategia de almacenamiento
-----------------------------
Cada ParentChunk se serializa como un fichero JSON independiente en:

    storage_path/
    └── parents/
        ├── P-3f2a1b7c.json
        ├── P-ae173d95.json
        └── ...

Este diseño:
  - No requiere ninguna dependencia extra (solo stdlib).
  - Permite acceso O(1) por parent_id (lookup directo por nombre de fichero).
  - Es upgradeable a Redis/PostgreSQL sin cambiar la interfaz pública:
    save_parents(), get_parent(), exists(), delete_parent(), list_all_ids().

Upgrade path a producción
--------------------------
  Redis:     Reemplazar las operaciones de fichero por redis.set() / redis.get()
  PostgreSQL: INSERT INTO parents (id, data JSONB) ... / SELECT data FROM parents WHERE id=...
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from app.ingestion.chunking.splitter import ChunkPair, ParentChunk


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

_PARENTS_DIR = "parents"


# ---------------------------------------------------------------------------
# DocStoreManager
# ---------------------------------------------------------------------------

class DocStoreManager:
    """
    Almacén KV de chunks padre (ParentChunk) en disco local (JSON file store).

    Parámetros
    ----------
    storage_path : str
        Directorio raíz del almacén. Se crea automáticamente si no existe.
    """

    def __init__(self, storage_path: str = "./data_store") -> None:
        self._root = Path(storage_path) / _PARENTS_DIR
        self._root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def save_parents(self, pairs: List[ChunkPair]) -> int:
        """
        Persiste en disco todos los ParentChunk de la lista de ChunkPairs.

        Parámetros
        ----------
        pairs : List[ChunkPair]
            Lista de pares generados por ParentChildSplitter.split_document().

        Returns
        -------
        int
            Número de chunks padre escritos en disco.
        """
        count = 0
        for pair in pairs:
            self._write_parent(pair.parent)
            count += 1
        return count

    def get_parent(self, parent_id: str) -> Optional[ParentChunk]:
        """
        Recupera un ParentChunk por su ID.

        Parámetros
        ----------
        parent_id : str
            ID del chunk padre (ej. "P-3f2a1b7c").

        Returns
        -------
        ParentChunk | None
            El chunk padre deserializado, o None si no existe.
        """
        path = self._path_for(parent_id)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return ParentChunk(
                id=data["id"],
                content=data["content"],
                heading=data.get("heading"),
                heading_level=data.get("heading_level"),
                metadata=data.get("metadata", {}),
            )
        except (json.JSONDecodeError, KeyError):
            return None

    def exists(self, parent_id: str) -> bool:
        """Comprueba si un chunk padre ya está persistido en disco."""
        return self._path_for(parent_id).exists()

    def delete_parent(self, parent_id: str) -> bool:
        """
        Elimina el fichero de un chunk padre del disco.
        Útil para el ledger de indexación incremental (Fase 5).

        Returns
        -------
        bool
            True si el fichero existía y fue eliminado, False si no existía.
        """
        path = self._path_for(parent_id)
        if path.exists():
            path.unlink()
            return True
        return False

    def list_all_ids(self) -> List[str]:
        """Devuelve todos los parent_id actualmente persistidos en disco."""
        return [p.stem for p in self._root.glob("*.json")]

    def count(self) -> int:
        """Número total de chunks padre almacenados."""
        return len(list(self._root.glob("*.json")))

    # ------------------------------------------------------------------
    # Métodos privados
    # ------------------------------------------------------------------

    def _path_for(self, parent_id: str) -> Path:
        """Devuelve la ruta de fichero para un parent_id dado."""
        # Sanitizar el ID para que sea un nombre de fichero válido
        safe_id = parent_id.replace("/", "_").replace("\\", "_")
        return self._root / f"{safe_id}.json"

    def _write_parent(self, parent: ParentChunk) -> None:
        """Serializa y escribe un ParentChunk en disco."""
        payload = {
            "id": parent.id,
            "content": parent.content,
            "heading": parent.heading,
            "heading_level": parent.heading_level,
            "metadata": parent.metadata,
        }
        path = self._path_for(parent.id)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
