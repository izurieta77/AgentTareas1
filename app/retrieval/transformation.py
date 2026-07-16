"""
transformation.py
================
Módulo de transformación de consultas (Query Transformation) para RAG.

Métodos implementados
---------------------
1. Multi-Query:
   Genera variantes semánticas y terminológicas de la consulta del usuario utilizando un LLM.
   Esto mitiga problemas de consultas mal redactadas o sesgadas y mejora la cobertura (Recall).

2. HyDE (Hypothetical Document Embeddings):
   Genera un documento o fragmento de respuesta hipotético. El embedding de esta respuesta ficticia
   suele estar alineado en el espacio vectorial con los documentos reales (datasheets, manuales, etc.)
   en lugar de alinearse con el espacio vectorial de las preguntas directas.

Robustez y Fallback
-------------------
Si no se configuran variables de entorno de LLM (ej. sin internet o sin API Key), el módulo
captura la excepción y realiza un fallback elegante devolviendo la consulta original sin alterar.
"""

import os
from typing import List, Optional
from google import genai
from google.genai import types


class QueryTransformer:
    """
    Clase para aplicar transformaciones a consultas de usuario usando un modelo LLM.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-3.5-flash",
    ) -> None:
        self.model = model
        
        # Recuperar credenciales (prioriza constructor, luego env)
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        self._client: Optional[genai.Client] = None
        self._enabled = False

        if self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
                self._enabled = True
            except Exception:
                self._client = None
                self._enabled = False

    def generate_hyde_document(self, query: str) -> str:
        """
        Genera un fragmento de respuesta hipotético a la consulta técnica.
        
        Fallback: Devuelve la query original si no hay LLM activo o si hay error.
        """
        if not self._enabled or not self._client:
            return query

        system_prompt = (
            "Eres un ingeniero experto en sistemas de control, electrónica y software industrial.\n"
            "Dada la pregunta del usuario, escribe un fragmento técnico hipotético que responda "
            "directamente a la pregunta. Este fragmento se usará para buscar pasajes similares en "
            "un manual técnico. Escribe únicamente la respuesta técnica directa, de forma objetiva "
            "y concisa (máximo 150 palabras). No agregues introducciones, saludos ni advertencias."
        )

        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=f"Pregunta: {query}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                    max_output_tokens=300
                )
            )
            hyde_doc = response.text
            return hyde_doc.strip() if hyde_doc else query
        except Exception as e:
            # Fallback seguro
            print(f"[QueryTransformer WARNING] Error en generación HyDE: {e}. Usando consulta original.")
            return query

    def generate_alternative_queries(self, query: str, n: int = 3) -> List[str]:
        """
        Genera N variantes de la consulta original para ampliar el Recall técnico.
        
        Fallback: Devuelve una lista con la consulta original si hay error o no hay LLM.
        """
        fallback_result = [query]
        if not self._enabled or not self._client:
            return fallback_result

        system_prompt = (
            "Eres un asistente de recuperación de información técnica para manuales de ingeniería.\n"
            f"Tu tarea es generar exactamente {n} variaciones o formas alternativas de formular la "
            "pregunta del usuario para realizar búsquedas semánticas más completas en el corpus.\n"
            "Reglas críticas:\n"
            "1. Agrega sinónimos técnicos alternativos (ej. 'power consumption' -> 'current draw', 'low power mode').\n"
            "2. Devuelve únicamente las variaciones, una por línea. No enumeres, no añadas explicaciones.\n"
            "3. Mantén el idioma original de la consulta."
        )

        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=f"Consulta original: {query}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.5,
                    max_output_tokens=200
                )
            )
            content = response.text
            if not content:
                return fallback_result

            # Limpiar líneas de salida
            queries = [
                line.strip().lstrip("1234567890.- ")
                for line in content.split("\n")
                if line.strip()
            ]
            
            # Garantizar que al menos incluyamos la original y no devuelva lista vacía
            valid_queries = [q for q in queries if q]
            if not valid_queries:
                return fallback_result
                
            # Agregar la original si no está y devolver
            if query not in valid_queries:
                valid_queries.append(query)
            return valid_queries[:n+1]
            
        except Exception as e:
            # Fallback seguro
            print(f"[QueryTransformer WARNING] Error en Multi-Query: {e}. Usando consulta original.")
            return fallback_result
