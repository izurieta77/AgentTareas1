from app.ingestion.parsers.base import BaseParser

class DoclingPDFParser(BaseParser):
    """Implementacion de parser de PDF utilizando IBM Docling de manera local."""

    def parse(self, file_path: str) -> str:
        # TODO: Implementar analisis e integracion real con docling
        return f"Contenido parseado de PDF (Docling): {file_path}"

class LlamaParsePDFParser(BaseParser):
    """Implementacion de parser de PDF utilizando la API de LlamaParse."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def parse(self, file_path: str) -> str:
        # TODO: Implementar llamada a LlamaParse API
        return f"Contenido parseado de PDF (LlamaParse): {file_path}"


class MarkerPDFParser(BaseParser):
    """Implementacion de parser de PDF utilizando la libreria local Marker."""

    def __init__(self):
        self._converter = None

    def _get_converter(self):
        if self._converter is None:
            try:
                from marker.converters.pdf import PdfConverter
                from marker.models import create_model_dict
                
                # Inicializacion diferida de los modelos neuronales de Marker
                self._converter = PdfConverter(
                    artifact_dict=create_model_dict(),
                )
            except ImportError as e:
                raise ImportError(
                    "Falta la libreria marker-pdf. Ejecuta: pip install marker-pdf"
                ) from e
        return self._converter

    def parse(self, file_path: str) -> str:
        import logging
        logger = logging.getLogger("app.ingestion.parsers.pdf_parser")
        
        from pathlib import Path
        pdf_path = Path(file_path)
        md_path = pdf_path.with_suffix(".md")
        
        # Si existe el archivo Markdown homónimo, omitimos la inicialización y uso de Marker.
        if md_path.exists():
            logger.info(f"Detectado archivo pre-parseado '{md_path.name}'. Leyendo contenido directamente del disco.")
            return md_path.read_text(encoding="utf-8")
            
        logger.info(f"No se detectó pre-parseo para '{pdf_path.name}'. Ejecutando Marker converter (este paso requiere GPU/RAM y puede demorar)...")
        converter = self._get_converter()
        rendered = converter(file_path)
        return rendered.markdown


