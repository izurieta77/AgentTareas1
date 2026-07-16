"""
test_agentic.py
===============
Playground y Tests para la Fase 4: Orquestación Agéntica.
Valida el comportamiento de Router, Compressor y Generator mediante mocks/fallbacks.
"""

import sys
import os
from pathlib import Path

# Asegurar que importamos desde la raiz del proyecto
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.retrieval.router import AgenticRouter, RouteCategory
from app.ingestion.chunking.splitter import ParentChunk
from app.retrieval.compressor import ContextCompressor
from app.retrieval.generator import GroundedGenerator

class MockReranker:
    """Mock de CrossEncoderReranker para no cargar el modelo real en los tests unitarios."""
    def rerank(self, query, candidates, top_n):
        # Devuelve las oraciones usando la longitud del texto como score ficticio
        # (Para probar que el compresor sabe ordenar y recortar correctamente)
        res = []
        for cand in candidates:
            # Score ficticio: favorecemos textos largos por simplicidad en el mock
            score = len(cand["content"])
            res.append((cand, score))
        # Orden de mayor a menor score
        res.sort(key=lambda x: x[1], reverse=True)
        return res[:top_n]


def test_router_fallback():
    print("\n--- Test Router (Fallback Determinista) ---")
    router = AgenticRouter()
    
    # Pruebas de reglas deterministas
    cat1 = router.route_query("La alarma de temperatura está saltando, la linea se paró.")
    print(f"Query: 'La alarma de temperatura está saltando...' -> Categoria: {cat1.value}")
    assert cat1 == RouteCategory.LINEA_PRODUCCION, "Fallo en LINEA_PRODUCCION"
    
    cat2 = router.route_query("¿Cuál es el torque máximo y las dimensiones del rotor?")
    print(f"Query: '¿Cuál es el torque máximo...' -> Categoria: {cat2.value}")
    assert cat2 == RouteCategory.ESPECIFICACIONES, "Fallo en ESPECIFICACIONES"
    
    cat3 = router.route_query("Quiero saber por qué decidieron usar este diseño en la patente.")
    print(f"Query: 'Quiero saber por qué...' -> Categoria: {cat3.value}")
    assert cat3 == RouteCategory.I_D_PATENTES, "Fallo en I_D_PATENTES"
    
    print("-> Test Router: OK")


def test_compressor():
    print("\n--- Test Compressor ---")
    reranker = MockReranker()
    compressor = ContextCompressor(reranker)
    
    content = (
        "El motor tiene un estator de cobre. "
        "Fue diseñado en 1999 por el Dr. Smith y patentado en la UE. "
        "Las revoluciones máximas por minuto son de 5000 RPM. "
        "Es un motor muy eficiente. "
        "La carcasa externa está completamente fabricada en titanio de grado 5 reforzado."
    )
    
    chunk = ParentChunk(
        id="chunk_123",
        content=content,
        heading="Motor Principal",
        heading_level=1,
        metadata={"source": "manual.pdf"}
    )
    
    # Extraer las 2 oraciones (simulado que sean las más largas)
    compressed = compressor.compress(query="¿De qué material es la carcasa?", parent_chunk=chunk, top_n_sentences=2)
    
    print(f"Texto original ({len(content)} chars):\n{content}\n")
    print(f"Texto comprimido ({len(compressed.content)} chars):\n{compressed.content}\n")
    print(f"Metadatos compresión: {compressed.metadata.get('compressed')}, Original: {compressed.metadata.get('original_length')} -> Comprimido: {compressed.metadata.get('compressed_length')}")
    
    assert compressed.metadata.get("compressed") is True, "El flag 'compressed' debe ser True"
    assert len(compressed.content) < len(content), "El texto comprimido debe ser menor al original"
    # Debe mantener el orden original de las oraciones en el documento
    assert compressed.content.find("Fue diseñado") < compressed.content.find("La carcasa externa"), "Las oraciones deben mantener su orden físico"
    
    print("-> Test Compressor: OK")


def test_generator_fallback():
    print("\n--- Test Generator (Fallback) ---")
    generator = GroundedGenerator()
    
    chunk = ParentChunk(
        id="chunk_123",
        content="Las revoluciones máximas por minuto son de 5000 RPM. La carcasa está hecha de titanio reforzado.",
        heading="Motor Principal",
        heading_level=1,
        metadata={"source": "manual_tecnico.pdf"}
    )
    
    res = generator.generate_response("¿De qué material es la carcasa?", [chunk])
    print(f"Respuesta generada (Fallback):\n{res['answer']}")
    print(f"Fuentes extraídas: {[s['document'] for s in res['sources']]}")
    
    assert "INFORMACIÓN NO DISPONIBLE" in res["answer"], "El fallback debe rechazar responder al no haber LLM"
    assert res["sources"][0]["document"] == "manual_tecnico.pdf", "Debe parsear correctamente el source en la metadata"
    
    print("-> Test Generator Fallback: OK")

if __name__ == "__main__":
    print("Iniciando pruebas de validación de componentes de Fase 4...")
    test_router_fallback()
    test_compressor()
    test_generator_fallback()
    print("\n==============================================")
    print("Todas las pruebas base completadas con éxito.")
    print("==============================================")
