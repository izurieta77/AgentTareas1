import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.api.dependencies import initialize_pipeline

# Configurar logs básicos
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app.api.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Inicializa los recursos pesados de RAG al iniciar el servidor FastAPI.
    """
    logger.info("Iniciando carga de modelos RAG y conexiones en memoria...")
    try:
        pipeline, rag, cache = initialize_pipeline()
        app.state.ingestion_pipeline = pipeline
        app.state.rag_pipeline = rag
        app.state.semantic_cache = cache
        logger.info("Modelos cargados e inicializados con éxito. Servidor listo.")
    except Exception as e:
        logger.critical(f"Fallo crítico al inicializar el RAG Pipeline en startup: {e}", exc_info=True)
        # Opcional: Impedir que la API inicie si el core de RAG falla
        raise e
        
    yield
    
    logger.info("Apagando API y liberando recursos...")

# Crear instancia de la app FastAPI
app = FastAPI(
    title="RAG Industrial REST API",
    description="API REST de alta disponibilidad para consultas técnicas de ingeniería y mantenimiento industrial mediante RAG Agéntico.",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar middleware de CORS para permitir conexiones externas (Frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador global de excepciones no controladas para evitar caídas y retornar JSON limpio
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error global detectado en la API: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Error interno del servidor: {str(exc)}"}
    )

# Incluir las rutas con prefijo de versión v1
app.include_router(api_router, prefix="/api/v1", tags=["RAG Core"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de RAG Industrial",
        "docs_url": "/docs",
        "status": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    # Arranque por defecto
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
