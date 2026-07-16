from abc import ABC, abstractmethod

class BaseParser(ABC):
    """Interfaz abstracta base para todos los parsers de documentos tecnicos."""

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Parsea el archivo dado y extrae el texto en formato estructurado (usualmente Markdown).

        Args:
            file_path: Ruta absoluta o relativa al archivo local.

        Returns:
            Contenido de texto estructurado.
        """
        pass
