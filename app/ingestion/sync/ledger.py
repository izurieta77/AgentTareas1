import os
import time
import hashlib
import sqlite3
from typing import List, Dict, Set
from pathlib import Path

class IngestionLedger:
    """
    Administra el control de cambios de documentos mediante hashes SHA-256
    y almacena las relaciones con los chunks padre persistidos en disco.
    """

    def __init__(self, db_url: str = "./data_store/ledger.db"):
        # Extraer la ruta del archivo SQLite a partir del string de conexión
        if db_url.startswith("sqlite:///"):
            path_str = db_url.replace("sqlite:///", "")
        else:
            path_str = db_url
        
        self.db_path = Path(path_str)
        # Asegurar directorio de la base de datos
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(str(self.db_path))

    def _init_db(self):
        """Inicializa la tabla de control de cambios."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_ledger (
                    file_path TEXT PRIMARY KEY,
                    file_hash TEXT NOT NULL,
                    last_modified REAL NOT NULL,
                    parent_ids TEXT NOT NULL
                )
            """)
            conn.commit()

    def calculate_hash(self, file_path: str) -> str:
        """Calcula el hash SHA-256 de un archivo físico local de forma eficiente."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return ""

    def detect_changes(self, file_paths: List[str]) -> Dict[str, Set[str]]:
        """
        Compara la lista actual de archivos y hashes con el ledger histórico.

        Returns:
            Diccionario clasificado con conjuntos de paths:
            {
               'new': {path1, path2},
               'modified': {path3},
               'deleted': {path4}
            }
        """
        # Convertir a paths absolutos normalizados para consistencia
        current_paths = {str(Path(p).resolve()) for p in file_paths}
        
        new_files = set()
        modified_files = set()
        deleted_files = set()
        
        # 1. Obtener estado de los archivos en disco
        current_state = {}
        for p in current_paths:
            if os.path.exists(p):
                file_hash = self.calculate_hash(p)
                mtime = os.path.getmtime(p)
                current_state[p] = (file_hash, mtime)

        # 2. Consultar el estado del ledger en la base de datos
        ledger_state = {}
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path, file_hash, last_modified FROM document_ledger")
            for row in cursor.fetchall():
                ledger_state[row[0]] = (row[1], row[2])

        # 3. Detectar eliminaciones: archivos en ledger que ya no están en la lista actual
        for db_path in ledger_state:
            if db_path not in current_paths or not os.path.exists(db_path):
                deleted_files.add(db_path)

        # 4. Detectar novedades y modificaciones
        for curr_path, (curr_hash, _) in current_state.items():
            if curr_path not in ledger_state:
                new_files.add(curr_path)
            else:
                db_hash, _ = ledger_state[curr_path]
                if curr_hash != db_hash:
                    modified_files.add(curr_path)

        return {
            "new": new_files,
            "modified": modified_files,
            "deleted": deleted_files
        }

    def update_ledger(self, file_path: str, file_hash: str, parent_ids: List[str]) -> None:
        """Registra o actualiza el hash de un documento en el ledger."""
        abs_path = str(Path(file_path).resolve())
        mtime = os.path.getmtime(abs_path) if os.path.exists(abs_path) else time.time()
        parent_ids_str = ",".join(parent_ids)
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO document_ledger (file_path, file_hash, last_modified, parent_ids)
                VALUES (?, ?, ?, ?)
            """, (abs_path, file_hash, mtime, parent_ids_str))
            conn.commit()

    def remove_from_ledger(self, file_path: str) -> None:
        """Elimina un documento del ledger."""
        abs_path = str(Path(file_path).resolve())
        with self._get_connection() as conn:
            conn.execute("DELETE FROM document_ledger WHERE file_path = ?", (abs_path,))
            conn.commit()

    def get_parent_ids(self, file_path: str) -> List[str]:
        """Recupera la lista de parent_ids asociada a un archivo."""
        abs_path = str(Path(file_path).resolve())
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT parent_ids FROM document_ledger WHERE file_path = ?", (abs_path,))
            row = cursor.fetchone()
            if row and row[0]:
                return row[0].split(",")
            return []
