import os
import sys
from pathlib import Path

# Agregar el directorio raiz del proyecto al path (un nivel superior a playground)
sys.path.append(str(Path(__file__).parent.parent))

from app.ingestion.parsers.pdf_parser import MarkerPDFParser

def main():
    # El archivo PDF se ubica en el directorio data del proyecto (un nivel superior a playground)
    pdf_path = Path(__file__).parent.parent / "data" / "AD4086_Datasheet.pdf"
    
    if not pdf_path.exists():
        print(f"[ERROR] No se encuentra el archivo PDF en: {pdf_path}")
        return

    print(f"Iniciando el parseo de {pdf_path.name} con Marker...")
    
    try:
        parser = MarkerPDFParser()
        markdown_text = parser.parse(str(pdf_path))
        
        # Guardar el resultado en la misma carpeta data
        output_path = pdf_path.with_suffix(".md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)
            
        print(f"\n[OK] Parseo exitoso!")
        print(f"Archivo guardado en: {output_path}")
        print("\nPrimeras 20 lineas del contenido extraido:")
        print("-" * 60)
        lines = markdown_text.splitlines()
        # Imprimimos de forma segura para evitar fallos de codificacion en consolas Windows
        for line in lines[:20]:
            try:
                print(line)
            except UnicodeEncodeError:
                # Reemplazamos caracteres incompatibles en consolas antiguas
                print(line.encode("ascii", "replace").decode("ascii"))
        print("-" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Ocurrio un fallo durante el parseo:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
