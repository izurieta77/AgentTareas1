"""
generator.py
============
Generador Grounded con Citas Estrictas para RAG Industrial.
"""

from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from app.ingestion.chunking.splitter import ParentChunk

class GroundedGenerator:
    """
    Se encarga de generar la respuesta final basándose EXCLUSIVAMENTE
    en el contexto proporcionado, forzando la inclusión de citas y
    mitigando alucinaciones a través de reglas estrictas.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-3.5-flash",
        temperature: float = 0.0
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            
    def generate_response(self, query: str, contexts: List[ParentChunk]) -> Dict[str, Any]:
        """
        Construye el prompt con los contextos proporcionados y genera la respuesta.
        Retorna la respuesta generada y las fuentes utilizadas.
        """
        # Preparar fuentes y formatear el contexto para el prompt
        formatted_contexts = []
        sources = []
        
        for idx, chunk in enumerate(contexts):
            # Obtener nombre del documento de los metadatos o usar un ID por defecto
            doc_name = chunk.metadata.get("source_file") or chunk.metadata.get("source", "Documento_Desconocido")
            # Extraer solo el nombre base sin rutas enteras
            doc_name = doc_name.split("/")[-1].split("\\")[-1]
            
            # Formatear la sección de contexto
            context_text = f"--- INICIO CONTEXTO [{doc_name}] (ID: {chunk.id}) ---\n"
            context_text += f"{chunk.content}\n"
            context_text += f"--- FIN CONTEXTO [{doc_name}] ---\n"
            
            formatted_contexts.append(context_text)
            
            # Guardar en la metadata de respuesta
            sources.append({
                "id": chunk.id,
                "document": doc_name,
                "heading": chunk.heading,
                "content_snippet": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                "compressed": chunk.metadata.get("compressed", False)
            })
            
        context_block = "\n".join(formatted_contexts)
        
        system_prompt = (
            "Eres un asistente técnico experto operando en un sistema de RAG para una planta industrial.\n"
            "Tu única tarea es responder a la consulta del usuario basándote EXCLUSIVAMENTE en el contexto proporcionado.\n\n"
            "REGLAS INQUEBRANTABLES:\n"
            "1. NO INVENTES NI SUPONGAS NADA. Si el contexto no contiene la respuesta exacta a la pregunta, DEBES responder ÚNICAMENTE con la frase: \"INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD\". No añadas nada más.\n"
            "2. DEBES citar la fuente de cada afirmación usando el formato estricto: [NombreDocumento] o [ID: chunk_id] basándote en las cabeceras de contexto.\n"
            "3. Prohibido usar conocimientos externos a los contextos proveídos.\n"
            "4. Sé directo, técnico y conciso."
        )
        
        user_prompt = f"CONTEXTOS RECUPERADOS:\n{context_block}\n\nPREGUNTA DEL USUARIO:\n{query}"
        
        if not self.client:
            # Fallback determinista si no hay LLM configurado (para testing en CI o entorno sin GPU/APIs)
            # Retornamos las fuentes pero avisamos que no hay generación.
            return {
                "answer": "INFORMACIÓN NO DISPONIBLE EN EL CORPUS DE SEGURIDAD (Modo Fallback: LLM no inicializado).",
                "used_contexts": [c.id for c in contexts],
                "sources": sources
            }
            
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=self.temperature
                )
            )
            
            answer = response.text.strip()
            
            return {
                "answer": answer,
                "used_contexts": [c.id for c in contexts],
                "sources": sources
            }
            
        except Exception as e:
            return {
                "answer": f"Error crítico al generar la respuesta mediante el LLM: {str(e)}",
                "used_contexts": [c.id for c in contexts],
                "sources": sources
            }
