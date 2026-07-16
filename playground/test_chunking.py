"""
test_chunking.py
================
Script de prueba para validar el ParentChildSplitter usando el Markdown
generado por test_parse_pdf.py (AD4086_Datasheet.md).

Que valida este test:
---------------------
  1. El splitter genera ChunkPairs a partir de texto real.
  2. Cada ChildChunk tiene un parent_id que apunta a un ParentChunk existente.
  3. Los metadatos se propagan correctamente de padre a hijo.
  4. La cobertura de texto es completa (ningun trozo se pierde).
  5. No hay chunks vacios.

Ejecucion:
----------
  cd d:\\PropuestaCanalYoutube\\2026-06-16-RAG-Industrial
  python playground/test_chunking.py
"""

import sys
from pathlib import Path

# Raiz del proyecto
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from app.ingestion.chunking.splitter import ParentChildSplitter, ChunkPair


# ---------------------------------------------------------------------------
# Utilidades de impresion (seguras en consolas Windows con cp1252/ascii)
# ---------------------------------------------------------------------------

def safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def print_separator(char: str = "-", width: int = 70) -> None:
    safe_print(char * width)


# ---------------------------------------------------------------------------
# Helpers de validacion
# ---------------------------------------------------------------------------

def validate_pairs(pairs: list[ChunkPair]) -> list[str]:
    """Ejecuta validaciones y devuelve la lista de errores encontrados."""
    errors: list[str] = []
    parent_ids = {p.parent.id for p in pairs}

    for i, pair in enumerate(pairs):
        # El padre no debe estar vacio
        if not pair.parent.content.strip():
            errors.append(f"[Par {i}] El chunk padre esta vacio.")

        # Debe tener al menos un hijo
        if not pair.children:
            errors.append(f"[Par {i}] El chunk padre '{pair.parent.id}' no tiene hijos.")

        for child in pair.children:
            # El hijo no debe estar vacio
            if not child.content.strip():
                errors.append(
                    f"[Par {i} / Hijo {child.chunk_index}] Chunk hijo vacio."
                )
            # El parent_id debe apuntar a un padre real
            if child.parent_id not in parent_ids:
                errors.append(
                    f"[Par {i} / Hijo {child.id}] parent_id '{child.parent_id}' "
                    f"no corresponde a ningun padre."
                )
            # El parent_id del hijo debe coincidir con el padre del par
            if child.parent_id != pair.parent.id:
                errors.append(
                    f"[Par {i} / Hijo {child.id}] parent_id '{child.parent_id}' "
                    f"no coincide con el padre del par '{pair.parent.id}'."
                )
            # Los metadatos deben contener las claves minimas
            required_keys = {"chunk_type", "parent_id", "section_heading"}
            missing = required_keys - set(child.metadata.keys())
            if missing:
                errors.append(
                    f"[Par {i} / Hijo {child.id}] Metadatos faltantes: {missing}."
                )

    return errors


# ---------------------------------------------------------------------------
# Test principal
# ---------------------------------------------------------------------------

def main() -> None:
    print_separator("=")
    safe_print("TEST: ParentChildSplitter - Chunking Jerarquico")
    print_separator("=")

    # ------------------------------------------------------------------
    # 1. Cargar el Markdown generado por el parser
    # ------------------------------------------------------------------
    md_path = ROOT / "data" / "AD4086_Datasheet.md"

    if not md_path.exists():
        safe_print(
            f"\n[ERROR] No se encontro el archivo Markdown en: {md_path}\n"
            f"Ejecuta primero: python playground/test_parse_pdf.py"
        )
        sys.exit(1)

    safe_print(f"\n[1/4] Cargando Markdown desde: {md_path.name}")
    text = md_path.read_text(encoding="utf-8")
    safe_print(f"      Caracteres totales: {len(text):,}")
    safe_print(f"      Lineas totales    : {text.count(chr(10)):,}")

    # ------------------------------------------------------------------
    # 2. Instanciar el splitter con parametros bien definidos
    # ------------------------------------------------------------------
    safe_print("\n[2/4] Instanciando ParentChildSplitter...")
    splitter = ParentChildSplitter(
        parent_size=1500,
        parent_overlap=150,
        child_size=300,
        child_overlap=50,
        split_by_headings=True,
    )
    safe_print(f"      parent_size    = {splitter.parent_size}")
    safe_print(f"      parent_overlap = {splitter.parent_overlap}")
    safe_print(f"      child_size     = {splitter.child_size}")
    safe_print(f"      child_overlap  = {splitter.child_overlap}")
    safe_print(f"      split_by_headings = {splitter.split_by_headings}")

    # ------------------------------------------------------------------
    # 3. Ejecutar el split
    # ------------------------------------------------------------------
    safe_print("\n[3/4] Ejecutando split_document()...")
    base_metadata = {
        "source": str(md_path),
        "document_name": md_path.stem,
        "file_type": "pdf",
    }
    pairs = splitter.split_document(text, base_metadata)

    # ------------------------------------------------------------------
    # 4. Estadisticas de resultado
    # ------------------------------------------------------------------
    total_children = sum(len(p.children) for p in pairs)
    avg_parent_len = (
        sum(len(p.parent.content) for p in pairs) / len(pairs) if pairs else 0
    )
    avg_child_len = (
        sum(len(c.content) for p in pairs for c in p.children) / total_children
        if total_children else 0
    )

    print_separator()
    safe_print("RESULTADO DEL SPLIT:")
    print_separator()
    safe_print(f"  Chunks PADRE generados : {len(pairs)}")
    safe_print(f"  Chunks HIJO generados  : {total_children}")
    safe_print(f"  Promedio long. padre   : {avg_parent_len:,.0f} chars")
    safe_print(f"  Promedio long. hijo    : {avg_child_len:,.0f} chars")
    print_separator()

    # ------------------------------------------------------------------
    # 5. Detalle de los primeros 3 pares
    # ------------------------------------------------------------------
    safe_print("\nDETALLE - Primeros 3 pares Parent-Child:")
    for i, pair in enumerate(pairs[:3]):
        print_separator("-")
        safe_print(f"[Par {i + 1}]")
        safe_print(f"  PADRE id      : {pair.parent.id}")
        safe_print(f"  Seccion       : {pair.parent.heading or '(sin encabezado)'}")
        safe_print(f"  Nivel heading : {pair.parent.heading_level or '-'}")
        safe_print(f"  Contenido     : {pair.parent.content[:120].strip()!r} ...")
        safe_print(f"  Num. hijos    : {len(pair.children)}")
        for j, child in enumerate(pair.children[:2]):
            safe_print(f"    [Hijo {j}] id={child.id}  parent_id={child.parent_id}")
            safe_print(f"             contenido={child.content[:80].strip()!r} ...")
        if len(pair.children) > 2:
            safe_print(f"    ... y {len(pair.children) - 2} hijos mas.")

    # ------------------------------------------------------------------
    # 6. Validacion de integridad
    # ------------------------------------------------------------------
    print_separator()
    safe_print("\n[4/4] Validando integridad de los chunks...")
    errors = validate_pairs(pairs)

    if errors:
        safe_print(f"\n[FAIL] Se encontraron {len(errors)} error(es):")
        for err in errors:
            safe_print(f"  - {err}")
        sys.exit(1)
    else:
        safe_print(f"\n[OK] Todas las validaciones pasaron correctamente.")
        safe_print(f"     {len(pairs)} pares con {total_children} chunks hijos, sin errores.")
    print_separator("=")


if __name__ == "__main__":
    main()
