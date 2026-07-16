import os
import time
import logging
import uuid
from typing import Any, Dict, Optional

# Configuración de logs
logger = logging.getLogger("app.retrieval.cache")

class SemanticCache:
    """
    Caché Semántica para consultas de RAG Industrial.
    Soporta almacenamiento modular en Qdrant (por defecto) o Redis.
    El umbral de similitud y el tiempo de vida (TTL) se configuran por env.
    """
    
    def __init__(self, pipeline, threshold: Optional[float] = None, ttl_days: Optional[float] = None):
        self.pipeline = pipeline
        
        # Leer variables de entorno con fallbacks configurados por el usuario
        self.backend_type = os.environ.get("SEMANTIC_CACHE_BACKEND", "qdrant").lower()
        
        if threshold is None:
            try:
                self.threshold = float(os.environ.get("SEMANTIC_CACHE_THRESHOLD", "0.95"))
            except ValueError:
                self.threshold = 0.95
        else:
            self.threshold = threshold
            
        if ttl_days is None:
            try:
                self.ttl_seconds = float(os.environ.get("SEMANTIC_CACHE_TTL_DAYS", "7.0")) * 86400.0
            except ValueError:
                self.ttl_seconds = 7.0 * 86400.0
        else:
            self.ttl_seconds = ttl_days * 86400.0
            
        self.collection_name = "semantic_cache"
        self.vector_size = self.pipeline.vector_store.vector_size
        
        # Inicializar backends de manera lazy
        self._qdrant_client = None
        self._redis_client = None
        
        logger.info(
            f"Inicializando Caché Semántica: backend={self.backend_type}, "
            f"threshold={self.threshold}, TTL={self.ttl_seconds / 86400.0} días"
        )
        
        if self.backend_type == "qdrant":
            self._init_qdrant()
        elif self.backend_type == "redis":
            self._init_redis()
            
    def _init_qdrant(self):
        """Inicializa la colección de caché en Qdrant si no existe."""
        self._qdrant_client = self.pipeline.vector_store._get_client()
        from qdrant_client.http import models as qmodels
        
        existing = [c.name for c in self._qdrant_client.get_collections().collections]
        if self.collection_name not in existing:
            logger.info(f"Creando colección de caché semántica '{self.collection_name}' en Qdrant...")
            self._qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(
                    size=self.vector_size,
                    distance=qmodels.Distance.COSINE
                )
            )

    def _init_redis(self):
        """Inicializa la conexión y el índice vectorial de Redis."""
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        try:
            import redis
            from redis.commands.search.field import TextField, VectorField
            from redis.commands.search.indexDefinition import IndexDefinition, IndexType
            
            self._redis_client = redis.from_url(redis_url)
            # Verificar conexión
            self._redis_client.ping()
            
            # Crear índice vectorial si no existe
            self.index_name = "idx:semantic_cache"
            try:
                self._redis_client.ft(self.index_name).info()
                logger.info("Índice de caché semántica en Redis ya existe.")
            except Exception:
                logger.info(f"Creando índice vectorial '{self.index_name}' en Redis...")
                schema = (
                    TextField("query_text"),
                    TextField("response_json"),
                    TextField("timestamp"),
                    VectorField(
                        "query_vector",
                        "HNSW",
                        {
                            "TYPE": "FLOAT32",
                            "DIM": self.vector_size,
                            "DISTANCE_METRIC": "COSINE"
                        }
                    )
                )
                self._redis_client.ft(self.index_name).create_index(
                    fields=schema,
                    definition=IndexDefinition(prefix=["cache:"], index_type=IndexType.HASH)
                )
        except ImportError:
            raise ImportError(
                "La librería 'redis' no está instalada. "
                "Ejecuta 'pip install redis' para usar el backend de Redis."
            )
        except Exception as e:
            logger.error(f"No se pudo conectar a Redis en '{redis_url}': {e}. Fallback temporal a Qdrant.")
            self.backend_type = "qdrant"
            self._init_qdrant()

    def check(self, query_text: str) -> Optional[Dict[str, Any]]:
        """
        Busca si existe una respuesta cacheada semánticamente similar a la consulta.
        Retorna la respuesta si existe un hit y no ha expirado; de lo contrario, None.
        """
        # Generar el embedding de la pregunta
        embedder = self.pipeline.vector_store._get_embedder()
        query_vector = embedder.encode(query_text, normalize_embeddings=True).tolist()
        
        if self.backend_type == "qdrant":
            return self._check_qdrant(query_text, query_vector)
        elif self.backend_type == "redis":
            return self._check_redis(query_text, query_vector)
        return None

    def update(self, query_text: str, response: Dict[str, Any]) -> None:
        """
        Almacena una respuesta en la caché semántica con un vector de la consulta.
        """
        embedder = self.pipeline.vector_store._get_embedder()
        query_vector = embedder.encode(query_text, normalize_embeddings=True).tolist()
        
        if self.backend_type == "qdrant":
            self._update_qdrant(query_text, query_vector, response)
        elif self.backend_type == "redis":
            self._update_redis(query_text, query_vector, response)

    # ------------------------------------------------------------------
    # Backend Qdrant
    # ------------------------------------------------------------------
    
    def _check_qdrant(self, query_text: str, query_vector: list) -> Optional[Dict[str, Any]]:
        try:
            response = self._qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=1
            )
            
            if not response.points:
                return None
                
            hit = response.points[0]
            score = hit.score
            
            # Validar umbral de similitud
            if score < self.threshold:
                logger.info(f"[Cache Miss] Similitud más cercana {score:.4f} por debajo del umbral {self.threshold}")
                return None
                
            payload = hit.payload
            cached_time = payload.get("timestamp", 0.0)
            
            # Verificar expiración (TTL)
            if time.time() - cached_time > self.ttl_seconds:
                logger.info("[Cache Expired] Hit expirado para la consulta. Purgando punto.")
                # Borrado asíncrono/síncrono simple del punto expirado
                self._qdrant_client.delete(
                    collection_name=self.collection_name,
                    points_selector=[hit.id]
                )
                return None
                
            logger.info(f"[Cache Hit Qdrant] Similitud: {score:.4f}")
            
            # Retornar respuesta enriquecida con metadatos del hit
            cached_response = payload.get("response", {})
            return {
                "response": cached_response,
                "similarity": score
            }
        except Exception as e:
            logger.error(f"Error al consultar caché en Qdrant: {e}")
            return None

    def _update_qdrant(self, query_text: str, query_vector: list, response: Dict[str, Any]) -> None:
        try:
            from qdrant_client.http import models as qmodels
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, query_text))
            
            self._qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    qmodels.PointStruct(
                        id=point_id,
                        vector=query_vector,
                        payload={
                            "query_text": query_text,
                            "response": response,
                            "timestamp": time.time()
                        }
                    )
                ]
            )
            logger.info(f"[Cache Update Qdrant] Consulta guardada con ID: {point_id}")
        except Exception as e:
            logger.error(f"Error al escribir en caché de Qdrant: {e}")

    # ------------------------------------------------------------------
    # Backend Redis
    # ------------------------------------------------------------------
    
    def _check_redis(self, query_text: str, query_vector: list) -> Optional[Dict[str, Any]]:
        try:
            import numpy as np
            from redis.commands.search.query import Query
            
            # Convertir vector a bytes para Redis
            vector_bytes = np.array(query_vector, dtype=np.float32).tobytes()
            
            # Query de Redis Vector Search
            q = Query("*=>[KNN 1 @query_vector ($vec_param) AS vector_score]").return_fields(
                "query_text", "response_json", "timestamp", "vector_score"
            ).sort_by("vector_score").dialect(2)
            
            res = self._redis_client.ft(self.index_name).search(q, query_params={"vec_param": vector_bytes})
            
            if res.total == 0:
                return None
                
            doc = res.docs[0]
            # La distancia en Redis coseno suele ir de 0 (idénticos) a 2 (opuestos).
            # Para pasarlo a similitud coseno: similitud = 1.0 - distancia
            distancia = float(doc.vector_score)
            score = 1.0 - distancia
            
            # Validar umbral
            if score < self.threshold:
                logger.info(f"[Cache Miss Redis] Similitud {score:.4f} inferior al umbral {self.threshold}")
                return None
                
            cached_time = float(doc.timestamp)
            # Verificar expiración (TTL)
            if time.time() - cached_time > self.ttl_seconds:
                logger.info("[Cache Expired Redis] Purgando clave expuesta.")
                self._redis_client.delete(doc.id)
                return None
                
            logger.info(f"[Cache Hit Redis] Similitud: {score:.4f}")
            
            import json
            cached_response = json.loads(doc.response_json)
            return {
                "response": cached_response,
                "similarity": score
            }
        except Exception as e:
            logger.error(f"Error al consultar caché en Redis: {e}")
            return None

    def _update_redis(self, query_text: str, query_vector: list, response: Dict[str, Any]) -> None:
        try:
            import json
            import numpy as np
            
            # Crear ID determinista
            cache_key = f"cache:{str(uuid.uuid5(uuid.NAMESPACE_DNS, query_text))}"
            vector_bytes = np.array(query_vector, dtype=np.float32).tobytes()
            
            payload = {
                "query_text": query_text,
                "response_json": json.dumps(response),
                "timestamp": str(time.time()),
                "query_vector": vector_bytes
            }
            
            self._redis_client.hset(cache_key, mapping=payload)
            logger.info(f"[Cache Update Redis] Guardado en clave: {cache_key}")
        except Exception as e:
            logger.error(f"Error al escribir en caché de Redis: {e}")
