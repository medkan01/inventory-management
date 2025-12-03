"""
Point d'entrée principal de l'application FastAPI.
Configure l'application, les middlewares et inclut les routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.router import api_router

# Configuration du logging
setup_logging(settings.log_level)
logger = get_logger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title=settings.project_name,
    description="API for inventory management with Supabase authentication",
    version=settings.version,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Événement exécuté au démarrage de l'application."""
    logger.info(f"Starting {settings.project_name} v{settings.version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API documentation: /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Événement exécuté à l'arrêt de l'application."""
    logger.info(f"Shutting down {settings.project_name}")


@app.get("/")
async def root():
    """Route racine publique."""
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": settings.version,
        "docs": "/docs",
        "api": settings.api_v1_str
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint pour Docker et monitoring.
    
    Utilisé par Docker HEALTHCHECK et les outils de monitoring.
    """
    return {
        "status": "healthy",
        "service": settings.project_name,
        "version": settings.version
    }


# Inclusion du router API v1
app.include_router(api_router, prefix=settings.api_v1_str)