"""
Endpoints pour la gestion des catégories de produits.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db import get_db
from app.schemas import (
    ProductCategoryResponse,
    ProductCategoryCreate,
    ProductCategoryUpdate,
    User,
)
from app.services import product_category_service
from app.core.constants import (
    DEFAULT_PRODUCT_CATEGORY_LIMIT,
    MAX_PRODUCT_CATEGORY_LIMIT,
)

router = APIRouter()


@router.get("/", response_model=List[ProductCategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_CATEGORY_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère la liste de toutes les catégories de produits.

    Paramètres:
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre max d'éléments (défaut: DEFAULT_PRODUCT_CATEGORY_LIMIT,
      max: MAX_PRODUCT_CATEGORY_LIMIT)

    Retourne:
    - Liste des catégories avec leurs informations complètes

    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_CATEGORY_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_CATEGORY_LIMIT} items.",
        )

    categories = product_category_service.get_all_categories(
        db=db, skip=skip, limit=limit
    )
    return categories


@router.get("/{category_slug}", response_model=ProductCategoryResponse)
def get_category_by_slug(
    category_slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les informations d'une catégorie par son slug.

    Paramètres:
    - **category_slug**: Le slug unique de la catégorie à récupérer.

    Retourne:
    - Les informations complètes de la catégorie.

    Nécessite une authentification.
    """
    category = product_category_service.get_category_by_slug(db=db, slug=category_slug)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with slug '{category_slug}' not found.",
        )

    return category


@router.post(
    "/", response_model=ProductCategoryResponse, status_code=status.HTTP_201_CREATED
)
def create_category(
    category_in: ProductCategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Crée une nouvelle catégorie de produits.

    Paramètres:
    - **category_in**: Données de la catégorie à créer.

    Retourne:
    - Les informations complètes de la catégorie créée.

    Nécessite une authentification.
    """
    try:
        category = product_category_service.create_category(
            db=db, category_in=category_in
        )
        return category
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{category_slug}", response_model=ProductCategoryResponse)
def update_category(
    category_slug: str,
    category_in: ProductCategoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Met à jour une catégorie existante.

    Paramètres:
    - **category_slug**: Le slug de la catégorie à mettre à jour.
    - **category_in**: Données de la catégorie à mettre à jour.

    Retourne:
    - Les informations complètes de la catégorie mise à jour.

    Nécessite une authentification.
    """
    try:
        category = product_category_service.update_category(
            db=db, slug=category_slug, category_in=category_in
        )
        return category
    except ValueError as e:
        # Convertir ValueError en HTTPException appropriée
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{category_slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Supprime une catégorie existante.

    Paramètres:
    - **category_slug**: Le slug de la catégorie à supprimer.

    Retourne:
    - Aucun contenu (204 No Content)

    Nécessite une authentification.
    """
    try:
        product_category_service.delete_category(db=db, slug=category_slug)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
