import logging
from pathlib import Path
from typing import Any, Dict, Optional

from app.ingestion.pipeline import IngestionPipeline

logger = logging.getLogger("app.ingestion.sync.orchestrator")

_SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc"}

class IncrementalSyncOrchestrator:
    """
    Orquesta el flujo de sincronización e ingesta incremental de directorios.
    Detecta cambios en los archivos usando el ledger SQLite y aplica inserciones,
    actualizaciones o purgas (tombstoning) sobre Qdrant y el almacén documental.
    """

    def __init__(self, pipeline: IngestionPipeline):
        self.pipeline = pipeline
        self.ledger = pipeline.ledger
        self.doc_store = pipeline.doc_store
        self.vector_store = pipeline.vector_store

    def sync_directory(
        self,
        directory_path: str,
        base_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Escanea un directorio local y sincroniza sus archivos incrementalmente.
        """
        path = Path(directory_path)
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Directorio no encontrado o inválido: {directory_path}")

        # 1. Encontrar todos los archivos válidos
        all_files = []
        for file in path.rglob("*"):
            if file.is_file() and file.suffix.lower() in _SUPPORTED_EXTENSIONS:
                all_files.append(str(file.resolve()))

        # 2. Detectar cambios
        changes = self.ledger.detect_changes(all_files)
        
        new_set = changes["new"]
        modified_set = changes["modified"]
        deleted_set = changes["deleted"]
        
        logger.info(
            f"Resultados de escaneo en '{directory_path}': "
            f"Nuevos={len(new_set)}, Modificados={len(modified_set)}, Eliminados={len(deleted_set)}"
        )

        report = {
            "directory": str(path.resolve()),
            "added": [],
            "updated": [],
            "deleted": [],
            "skipped_count": len(all_files) - len(new_set) - len(modified_set),
            "status": "success"
        }

        # 3. Procesar Eliminaciones
        for f_path in deleted_set:
            try:
                logger.info(f"Purgando documento eliminado: {f_path}")
                parent_ids = self.ledger.get_parent_ids(f_path)
                
                # Borrar del DocStore
                deleted_parents_count = 0
                for pid in parent_ids:
                    if self.doc_store.delete_parent(pid):
                        deleted_parents_count += 1
                        
                # Borrar de Qdrant
                self.vector_store.delete_by_source(f_path)
                
                # Borrar de la base de datos de auditoría (ledger)
                self.ledger.remove_from_ledger(f_path)
                
                report["deleted"].append({
                    "file_path": f_path,
                    "deleted_parents": deleted_parents_count
                })
            except Exception as e:
                logger.error(f"Error al eliminar '{f_path}': {e}", exc_info=True)
                report["status"] = "partial_errors"

        # 4. Procesar Modificaciones (Eliminar antiguo + Ingestar nuevo)
        for f_path in modified_set:
            try:
                logger.info(f"Actualizando documento modificado: {f_path}")
                
                # Obtener y eliminar relación anterior
                old_parent_ids = self.ledger.get_parent_ids(f_path)
                for pid in old_parent_ids:
                    self.doc_store.delete_parent(pid)
                self.vector_store.delete_by_source(f_path)
                
                # Procesar archivo con los datos nuevos
                stats = self.pipeline.process_file(f_path, base_metadata=base_metadata)
                
                # Actualizar Ledger
                new_hash = self.ledger.calculate_hash(f_path)
                new_parent_ids = stats.get("parent_ids", [])
                self.ledger.update_ledger(f_path, new_hash, new_parent_ids)
                
                report["updated"].append({
                    "file_path": f_path,
                    "n_parents": stats["n_parents"],
                    "n_children": stats["n_children"]
                })
            except Exception as e:
                logger.error(f"Error al actualizar '{f_path}': {e}", exc_info=True)
                report["status"] = "partial_errors"

        # 5. Procesar Archivos Nuevos
        for f_path in new_set:
            try:
                logger.info(f"Ingestando nuevo documento: {f_path}")
                stats = self.pipeline.process_file(f_path, base_metadata=base_metadata)
                
                # Registrar en Ledger
                file_hash = self.ledger.calculate_hash(f_path)
                parent_ids = stats.get("parent_ids", [])
                self.ledger.update_ledger(f_path, file_hash, parent_ids)
                
                report["added"].append({
                    "file_path": f_path,
                    "n_parents": stats["n_parents"],
                    "n_children": stats["n_children"]
                })
            except Exception as e:
                logger.error(f"Error al ingestar '{f_path}': {e}", exc_info=True)
                report["status"] = "partial_errors"

        return report
