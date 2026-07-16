"""
bm25.py
=======
Implementación de búsqueda léxica (Sparse Search) utilizando BM25 en Python puro.

Diseño
------
Para garantizar que el sistema funcione en cualquier plataforma (especialmente Windows)
sin depender de compiladores de C++ o librerías externas propensas a romper compatibilidades
(como rank_bm25), implementamos el algoritmo clásico BM25 de manera nativa y optimizada.

Fórmula BM25 utilizada:
-----------------------
  IDF(q) = ln((N - n(q) + 0.5) / (n(q) + 0.5) + 1.0)
  Score(D, Q) = Sum_q( IDF(q) * (f(q, D) * (k1 + 1)) / (f(q, D) + k1 * (1 - b + b * (dl / avgdl))) )

Dónde:
  - N: Número total de documentos (chunks hijo)
  - n(q): Número de documentos que contienen el término q
  - f(q, D): Frecuencia de q en el documento D
  - dl: Longitud del documento D en tokens
  - avgdl: Longitud promedio de todos los documentos del corpus
  - k1: Parámetro de saturación del término (por defecto 1.5)
  - b: Parámetro de normalización de la longitud (por defecto 0.75)
"""

import math
import re
import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


class BM25Retriever:
    """
    Retriever léxico que implementa BM25 en memoria sobre los chunks hijo.
    """

    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        self.k1 = k1
        self.b = b
        
        # Estado del índice
        self.corpus_size: int = 0
        self.avg_doc_len: float = 0.0
        self.doc_ids: List[str] = []         # IDs de los chunks correspondientes
        self.doc_lengths: List[int] = []     # Longitud de cada documento en tokens
        self.doc_freqs: List[Dict[str, int]] = []  # Frecuencias de términos por documento
        self.term_doc_freqs: Dict[str, int] = {}  # nd: Número de documentos con el término q
        self.vocab: Set[str] = set()

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenizador simple alfanumérico en minúsculas.
        """
        if not text:
            return []
        # Extrae palabras/códigos (ej. "AD4086", "55", "Nm") y los pasa a minúsculas
        return re.findall(r"\w+", text.lower())

    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Indexa una lista de documentos en memoria.
        
        Parámetros
        ----------
        documents : List[Dict[str, Any]]
            Lista de diccionarios, cada uno con al menos:
            {"id": str, "content": str}
        """
        self.doc_ids = []
        self.doc_lengths = []
        self.doc_freqs = []
        self.term_doc_freqs = {}
        self.vocab = set()
        
        total_len = 0
        for doc in documents:
            doc_id = doc["id"]
            content = doc["content"]
            
            tokens = self._tokenize(content)
            doc_len = len(tokens)
            total_len += doc_len
            
            # Frecuencia de términos en este documento
            freqs: Dict[str, int] = {}
            for t in tokens:
                freqs[t] = freqs.get(t, 0) + 1
            
            # Actualizar frecuencias globales de documentos (nd)
            for t in freqs.keys():
                self.term_doc_freqs[t] = self.term_doc_freqs.get(t, 0) + 1
                self.vocab.add(t)
                
            self.doc_ids.append(doc_id)
            self.doc_lengths.append(doc_len)
            self.doc_freqs.append(freqs)
            
        self.corpus_size = len(documents)
        self.avg_doc_len = total_len / self.corpus_size if self.corpus_size > 0 else 0.0

    def get_scores(self, query: str) -> List[float]:
        """
        Calcula las puntuaciones BM25 de todos los documentos para la query.
        """
        query_tokens = self._tokenize(query)
        scores = [0.0] * self.corpus_size
        
        if self.corpus_size == 0 or not query_tokens:
            return scores
            
        for i in range(self.corpus_size):
            score = 0.0
            freqs = self.doc_freqs[i]
            dl = self.doc_lengths[i]
            
            for q in query_tokens:
                if q not in self.vocab:
                    continue
                
                n_q = self.term_doc_freqs[q]
                # Cálculo de IDF
                idf = math.log((self.corpus_size - n_q + 0.5) / (n_q + 0.5) + 1.0)
                
                # Frecuencia del término en el documento actual
                f = freqs.get(q, 0)
                
                # Puntuación BM25 para este término
                numerator = f * (self.k1 + 1)
                denominator = f + self.k1 * (1.0 - self.b + self.b * (dl / self.avg_doc_len))
                
                score += idf * (numerator / denominator)
                
            scores[i] = score
            
        return scores

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Busca los documentos más relevantes para una consulta.
        
        Returns
        -------
        List[Tuple[str, float]]
            Lista de tuplas (doc_id, score) ordenadas de mayor a menor.
        """
        scores = self.get_scores(query)
        
        # Emparejar IDs y puntuaciones y ordenar
        results = [
            (self.doc_ids[i], scores[i])
            for i in range(self.corpus_size)
            if scores[i] > 0.0
        ]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # Persistencia de caché en disco
    # ------------------------------------------------------------------

    def save_index(self, filepath: str) -> None:
        """
        Guarda el estado del índice en un archivo JSON.
        """
        data = {
            "k1": self.k1,
            "b": self.b,
            "corpus_size": self.corpus_size,
            "avg_doc_len": self.avg_doc_len,
            "doc_ids": self.doc_ids,
            "doc_lengths": self.doc_lengths,
            "doc_freqs": self.doc_freqs,
            "term_doc_freqs": self.term_doc_freqs,
        }
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_index(self, filepath: str) -> bool:
        """
        Carga el estado del índice desde un archivo JSON.
        
        Returns
        -------
        bool
            True si se cargó correctamente, False si el archivo no existe o es corrupto.
        """
        path = Path(filepath)
        if not path.exists():
            return False
            
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.k1 = data["k1"]
            self.b = data["b"]
            self.corpus_size = data["corpus_size"]
            self.avg_doc_len = data["avg_doc_len"]
            self.doc_ids = data["doc_ids"]
            self.doc_lengths = data["doc_lengths"]
            self.doc_freqs = data["doc_freqs"]
            self.term_doc_freqs = data["term_doc_freqs"]
            self.vocab = set(self.term_doc_freqs.keys())
            return True
        except Exception:
            return False
