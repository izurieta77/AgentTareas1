"""
compressor.py
=============
Compresión contextual basada en Cross-Encoder para mitigar el problema de "Lost in the Middle".
"""

import re
from typing import List
from app.ingestion.chunking.splitter import ParentChunk
from app.retrieval.reranker import CrossEncoderReranker

class ContextCompressor:
    """
    Reduce el tamaño de un ParentChunk manteniendo únicamente las oraciones
    que resultan más relevantes para la consulta del usuario, ahorrando tokens
    en la generación y mejorando la precisión del LLM.
    """

    def __init__(self, reranker: CrossEncoderReranker):
        self.reranker = reranker

    def compress(
        self, 
        query: str, 
        parent_chunk: ParentChunk, 
        top_n_sentences: int = 5,
        min_score: float = -10.0
    ) -> ParentChunk:
        """
        Divide el contenido del ParentChunk en oraciones, las puntúa con el
        CrossEncoder, y devuelve un nuevo ParentChunk modificado que solo
        contiene las oraciones más relevantes, respetando su orden original.
        """
        # Extraer oraciones manteniendo cierta lógica de párrafos
        paragraphs = parent_chunk.content.split('\n')
        
        sentences = []
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            # Separar por puntos seguidos de espacio para detectar oraciones.
            # Esta regex heurística es rápida y suficientemente buena para texto técnico.
            sents = re.split(r'(?<=[.!?])\s+', p)
            for s in sents:
                if s.strip():
                    sentences.append(s.strip())
                    
        if not sentences:
            return parent_chunk

        # Preparamos las oraciones como candidatos para el Reranker
        # Usamos dicts porque reranker.py soporta diccionarios con la key "content"
        candidates = [{"content": s, "original_index": i} for i, s in enumerate(sentences)]
        
        # Puntuamos todas las oraciones
        ranked_results = self.reranker.rerank(
            query=query,
            candidates=candidates,
            top_n=len(sentences)
        )
        
        # Filtrar por score mínimo (opcional) para quitar ruido total
        best_sentences = [
            (cand, score) for cand, score in ranked_results if score >= min_score
        ]
        
        # Tomamos solo el top N oraciones más relevantes
        best_sentences = best_sentences[:top_n_sentences]
        
        # Si todo se descartó, devolver texto original por seguridad
        if not best_sentences:
            return parent_chunk
            
        # Reordenar las oraciones ganadoras según su índice de aparición físico
        best_sentences.sort(key=lambda x: x[0]["original_index"])
        
        # Ensamblar el texto comprimido indicando elipsis
        compressed_text = " [...] ".join(cand["content"] for cand, _ in best_sentences)
        
        # Metadatos actualizados
        new_meta = parent_chunk.metadata.copy()
        new_meta["compressed"] = True
        new_meta["original_length"] = len(parent_chunk.content)
        new_meta["compressed_length"] = len(compressed_text)
        
        # Devolver nuevo chunk modificado
        return ParentChunk(
            id=parent_chunk.id,
            content=compressed_text,
            heading=parent_chunk.heading,
            heading_level=parent_chunk.heading_level,
            metadata=new_meta
        )

    def compress_list(
        self,
        query: str,
        parents: List[ParentChunk],
        top_n_sentences_per_chunk: int = 5
    ) -> List[ParentChunk]:
        """Aplica la compresión a una lista de ParentChunks de forma independiente."""
        return [
            self.compress(query, p, top_n_sentences=top_n_sentences_per_chunk) 
            for p in parents
        ]
