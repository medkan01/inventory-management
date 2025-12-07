"""
Endpoints pour la gestion des collections de produits.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db import get_db
from app.schemas import (
    ProductCollectionResponse,
    ProductCollectionCreate,
    ProductCollectionUpdate,
    User,
)
from app.services import product_collection_service
from app.core.constants import (
    DEFAULT_PRODUCT_COLLECTION_LIMIT,
    MAX_PRODUCT_COLLECTION_LIMIT,
)

router = APIRouter()


@router.get("/", response_model=List[ProductCollectionResponse])
def get_collections(
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_COLLECTION_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère la liste de toutes les collections de produits.

    Paramètres:
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre max d'éléments
      (défaut: DEFAULT_PRODUCT_COLLECTION_LIMIT,
      max: MAX_PRODUCT_COLLECTION_LIMIT)

    Retourne:
    - Liste des collections avec leurs informations complètes

    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_COLLECTION_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_COLLECTION_LIMIT} items.",
        )

    collections = product_collection_service.get_all_collections(
        db=db, skip=skip, limit=limit
    )
    return collections


@router.get("/{collection_slug}", response_model=ProductCollectionResponse)
def get_collection_by_slug(
    collection_slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les informations d'une collection par son slug.

    Paramètres:
    - **collection_slug**: Le slug unique de la collection à récupérer.

    Retourne:
    - Les informations complètes de la collection.

    Nécessite une authentification.
    """
    collection = product_collection_service.get_collection_by_slug(
        db=db, slug=collection_slug
    )

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Collection with slug '{collection_slug}' not found.",
        )

    return collection


@router.post(
    "/", response_model=ProductCollectionResponse, status_code=status.HTTP_201_CREATED
)
def create_collection(
    collection_in: ProductCollectionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Crée une nouvelle collection de produits.

    Paramètres:
    - **collection_in**: Données de la collection à créer.

    Retourne:
    - Les informations complètes de la collection créée.

    Nécessite une authentification.
    """
    try:
        collection = product_collection_service.create_collection(
            db=db, collection_in=collection_in
        )
        return collection
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{collection_slug}", response_model=ProductCollectionResponse)
def update_collection(
    collection_slug: str,
    collection_in: ProductCollectionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Met à jour une collection existante.

    Paramètres:
    - **collection_slug**: Le slug de la collection à mettre à jour.
    - **collection_in**: Données de la collection à mettre à jour.

    Retourne:
    - Les informations complètes de la collection mise à jour.

    Nécessite une authentification.
    """
    try:
        collection = product_collection_service.update_collection(
            db=db, slug=collection_slug, collection_in=collection_in
        )
        return collection
    except ValueError as e:
        # Convertir ValueError en HTTPException appropriée
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{collection_slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Supprime une collection existante.

    Paramètres:
    - **collection_slug**: Le slug de la collection à supprimer.

    Retourne:
    - Aucun contenu (204 No Content)

    Nécessite une authentification.
    """
    try:
        product_collection_service.delete_collection(db=db, slug=collection_slug)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
