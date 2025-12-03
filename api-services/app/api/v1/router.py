"""
Router principal pour l'API v1.
Regroupe tous les endpoints sous /api/v1.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Inclusion des différents routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# TODO: Ajouter d'autres routers ici
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
