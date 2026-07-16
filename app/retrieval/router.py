"""
router.py
=========
Enrutador inteligente para clasificar consultas y optimizar el pipeline de recuperación.
"""

import re
from enum import Enum
from typing import Optional
from google import genai
from google.genai import types

class RouteCategory(str, Enum):
    LINEA_PRODUCCION = "LINEA_PRODUCCION"
    I_D_PATENTES = "I_D_PATENTES"
    ESPECIFICACIONES = "ESPECIFICACIONES"

class AgenticRouter:
    """
    Clasifica la consulta del usuario en diferentes categorías para 
    decidir la estrategia de recuperación (top_k, hyde, rrf, etc.).
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-3.5-flash"
    ):
        self.api_key = api_key
        self.model = model
        
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def route_query(self, query: str) -> RouteCategory:
        """
        Clasifica la consulta en LINEA_PRODUCCION, I_D_PATENTES o ESPECIFICACIONES.
        Si no hay API key de OpenAI, utiliza un fallback determinista basado en palabras clave.
        """
        if not self.client:
            return self._deterministic_fallback(query)

        try:
            prompt = (
                "Eres un enrutador inteligente para un sistema de RAG Industrial.\n"
                "Clasifica la siguiente consulta en UNA de las tres categorías exactas:\n"
                "- LINEA_PRODUCCION: Consultas operativas rápidas, alarmas, fallos mecánicos directos, mantenimiento.\n"
                "- I_D_PATENTES: Consultas conceptuales complejas, diseño, patentes, arquitecturas.\n"
                "- ESPECIFICACIONES: Datos exactos de dimensiones, límites, torques, especificaciones técnicas, temperaturas.\n\n"
                f"Consulta: '{query}'\n\n"
                "Responde SOLO con el nombre exacto de la categoría correspondiente."
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=f"Consulta: '{query}'\n\nResponde SOLO con el nombre exacto de la categoría correspondiente.",
                config=types.GenerateContentConfig(
                    system_instruction=prompt.replace(f"Consulta: '{query}'\n\nResponde SOLO con el nombre exacto de la categoría correspondiente.", "").strip(),
                    temperature=0.0,
                    max_output_tokens=10
                )
            )

            result = response.text.strip().upper()

            # Validar y castear a Enum
            for category in RouteCategory:
                if category.value in result:
                    return category
            
            # Fallback a LINEA_PRODUCCION por defecto si LLM devuelve basura
            return RouteCategory.LINEA_PRODUCCION

        except Exception:
            # Fallback si falla la API
            return self._deterministic_fallback(query)

    def _deterministic_fallback(self, query: str) -> RouteCategory:
        """Fallback determinista mediante regex/palabras clave cuando no hay LLM."""
        q = query.lower()
        
        # Palabras clave de línea de producción
        if re.search(r'\b(alarma|error|falla|fallo|rompió|parada|linea|línea|operativo|mantenimiento|reparar|roto)\b', q):
            return RouteCategory.LINEA_PRODUCCION
            
        # Palabras clave de especificaciones
        if re.search(r'\b(dimensiones|límite|limite|torque|peso|medida|tamaño|cuánto|cuanto|velocidad|temperatura|especificaci(?:ón|ones)|metros|kilos)\b', q):
            return RouteCategory.ESPECIFICACIONES
            
        # Si no encaja en las anteriores, asignamos a I_D / Patentes (investigación/conceptos)
        return RouteCategory.I_D_PATENTES
