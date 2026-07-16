"""
reranker.py
===========
Reordenación (Re-ranking) semántica local utilizando modelos Cross-Encoder.

¿Por qué usar un Cross-Encoder?
--------------------------------
Los modelos de embeddings (Bi-Encoders) vectorizan las preguntas y los fragmentos por separado,
calculando la similitud de forma rápida pero sin interacción directa palabra-palabra.
Un Cross-Encoder toma la consulta y el fragmento juntos y utiliza las cabezas de atención del
Transformer para cruzar de manera profunda cada palabra de la consulta con cada palabra del texto.
Esto nos da un score de relevancia de precisión quirúrgica (Precision@5 alta), ideal para filtrar
el Top-N final antes de entregárselo al LLM.

Modelo por defecto:
------------------
  - `cross-encoder/ms-marco-MiniLM-L-6-v2` (~90 MB): Extremadamente rápido en CPU y GPU, muy sensible.
"""

from typing import Any, Dict, List, Tuple, Union
from app.ingestion.chunking.splitter import ParentChunk, ChildChunk


class CrossEncoderReranker:
    """
    Reranker semántico local que carga un modelo CrossEncoder para ordenar candidatos.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ) -> None:
        self.model_name = model_name
        self._model = None  # Lazy initialization

    def _get_model(self):
        """
        Carga diferida (lazy init) de la clase CrossEncoder de sentence-transformers.
        """
        if self._model is None:
            import os
            # Configurar entorno seguro frente a Hugging Face
            os.environ.setdefault("SAFETENSORS_FAST_GPU", "1")
            os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
            
            from sentence_transformers import CrossEncoder
            
            # Carga del modelo CrossEncoder
            self._model = CrossEncoder(self.model_name)
            
        return self._model

    def rerank(
        self,
        query: str,
        candidates: List[Union[ParentChunk, ChildChunk, Dict[str, Any], Any]],
        top_n: int = 5,
    ) -> List[Tuple[Any, float]]:
        """
        Ordena los candidatos en base a la relevancia evaluada por el Cross-Encoder.
        
        Parámetros
        ----------
        query : str
            Consulta del usuario en lenguaje natural.
        candidates : List[Union[ParentChunk, ChildChunk, dict, Any]]
            Lista de fragmentos candidatos recuperados en la fase de búsqueda.
            Pueden ser objetos ParentChunk, ChildChunk, diccionarios de hits de Qdrant, o texto puro.
        top_n : int
            Número máximo de candidatos a devolver una vez ordenados.

        Returns
        -------
        List[Tuple[Any, float]]
            Lista de tuplas (candidato, score) ordenadas de mayor a menor relevancia.
        """
        if not candidates:
            return []

        model = self._get_model()

        # Extraer el contenido textual de cada candidato para la inferencia
        pairs: List[Tuple[str, str]] = []
        for c in candidates:
            text = ""
            if hasattr(c, "content"):
                text = c.content
            elif isinstance(c, dict):
                # Caso de diccionario (ej. hit de Qdrant o similar)
                text = c.get("content") or c.get("payload", {}).get("content", "")
            else:
                # Fallback a conversión a string
                text = str(c)
            pairs.append((query, text))

        # Ejecutar inferencia en batch
        # Los scores para ms-marco suelen estar en escala sigmoide (valores reales)
        scores = model.predict(pairs, show_progress_bar=False).tolist()

        # Emparejar candidatos originales con sus puntuaciones
        ranked_results = list(zip(candidates, scores))
        # Ordenar de mayor a menor puntuación
        ranked_results.sort(key=lambda x: x[1], reverse=True)

        return ranked_results[:top_n]
