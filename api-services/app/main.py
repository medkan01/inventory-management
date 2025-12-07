"""
Point d'entrée principal de l'application FastAPI.
Configure l'application, les middlewares et inclut les routes.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.router import api_router

# Configuration du logging
setup_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie de l'application.
    Remplace les anciens @app.on_event("startup") et @app.on_event("shutdown").
    """
    # Startup
    logger.info("Starting %s v%s", settings.project_name, settings.version)
    logger.info("Debug mode: %s", settings.debug)
    logger.info("API documentation: /docs")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.project_name}")


# Création de l'application FastAPI
app = FastAPI(
    title=settings.project_name,
    description="API for inventory management with Supabase authentication",
    version=settings.version,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Route racine publique."""
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": settings.version,
        "docs": "/docs",
        "api": settings.api_v1_str,
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
        "version": settings.version,
    }


# Inclusion du router API v1
app.include_router(api_router, prefix=settings.api_v1_str)
