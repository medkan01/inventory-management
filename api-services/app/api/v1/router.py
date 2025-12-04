"""
Router principal pour l'API v1.
Regroupe tous les endpoints sous /api/v1.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, product, product_category, product_collection

api_router = APIRouter()

# Inclusion des différents routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(product.router, prefix="/products", tags=["Products"])
api_router.include_router(product_category.router, prefix="/categories", tags=["Product Categories"])
api_router.include_router(product_collection.router, prefix="/collections", tags=["Product Collections"])
