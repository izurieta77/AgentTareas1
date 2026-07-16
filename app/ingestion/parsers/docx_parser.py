from app.ingestion.parsers.base import BaseParser

class PandocDocxParser(BaseParser):
    """Implementacion de parser de Word (.docx) utilizando Pandoc."""

    def parse(self, file_path: str) -> str:
        # TODO: Implementar conversion usando subprocess llamando a pandoc
        return f"Contenido parseado de Word (Pandoc): {file_path}"

class DoclingDocxParser(BaseParser):
    """Implementacion de parser de Word (.docx) utilizando IBM Docling."""

    def parse(self, file_path: str) -> str:
        # TODO: Implementar integracion real con docling
        return f"Contenido parseado de Word (Docling): {file_path}"
