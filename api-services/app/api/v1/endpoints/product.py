"""
Endpoints pour la gestion des produits.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db import get_db
from app.schemas import ProductResponse, User, ProductCreate, ProductUpdate
from app.services import product_service
from app.core.constants import DEFAULT_PRODUCT_LIMIT, MAX_PRODUCT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère la liste de tous les produits.
    
    Paramètres:
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre maximum d'éléments à retourner (défaut: DEFAULT_PRODUCT_LIMIT, max: MAX_PRODUCT_LIMIT)
    
    Retourne:
    - Liste des produits avec leurs informations complètes
    
    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_LIMIT} items."
        )
    
    products = product_service.get_all_products(db=db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les informations d'un produit par son ID.
    
    Paramètres:
    - **product_id**: L'ID unique du produit à récupérer.
    
    Retourne:
    - Les informations complètes du produit.
    
    Nécessite une authentification.
    """
    product = product_service.get_product_by_id(db=db, product_id=product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    
    return product

@router.get("/{product_slug}", response_model=ProductResponse)
def get_product_by_slug(
    product_slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les informations d'un produit par son slug.
    
    Paramètres:
    - **product_slug**: Le slug unique du produit à récupérer.
    
    Retourne:
    - Les informations complètes du produit.
    
    Nécessite une authentification.
    """
    product = product_service.get_product_by_slug(db=db, slug=product_slug)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    
    return product

@router.get("/category/{category_id}", response_model=List[ProductResponse])
def get_products_by_category_id(
    category_id: int,
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les produits par ID de catégorie.
    
    Paramètres:
    - **category_id**: L'ID de la catégorie.
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre maximum d'éléments à retourner (défaut: DEFAULT_PRODUCT_LIMIT, max: MAX_PRODUCT_LIMIT)
    
    Retourne:
    - Liste des produits appartenant à la catégorie spécifiée.
    
    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_LIMIT} items."
        )
    
    products = product_service.get_products_by_category_id(
        db=db, category_id=category_id, skip=skip, limit=limit
    )
    return products

@router.get("/collection/{collection_id}", response_model=List[ProductResponse])
def get_products_by_collection_id(
    collection_id: int,
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les produits par ID de collection.
    
    Paramètres:
    - **collection_id**: L'ID de la collection.
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre maximum d'éléments à retourner (défaut: DEFAULT_PRODUCT_LIMIT, max: MAX_PRODUCT_LIMIT)
    
    Retourne:
    - Liste des produits appartenant à la collection spécifiée.
    
    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_LIMIT} items."
        )
    
    products = product_service.get_products_by_collection_id(
        db=db, collection_id=collection_id, skip=skip, limit=limit
    )
    return products

@router.get("/category/slug/{category_slug}", response_model=List[ProductResponse])
def get_products_by_category_slug(
    category_slug: str,
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les produits par slug de catégorie.
    
    Paramètres:
    - **category_slug**: Le slug de la catégorie.
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre maximum d'éléments à retourner (défaut: DEFAULT_PRODUCT_LIMIT, max: MAX_PRODUCT_LIMIT)
    
    Retourne:
    - Liste des produits appartenant à la catégorie spécifiée.
    
    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_LIMIT} items."
        )
    
    products = product_service.get_products_by_category_slug(
        db=db, category_slug=category_slug, skip=skip, limit=limit
    )
    return products

@router.get("/collection/slug/{collection_slug}", response_model=List[ProductResponse])
def get_products_by_collection_slug(
    collection_slug: str,
    skip: int = 0,
    limit: int = DEFAULT_PRODUCT_LIMIT,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Récupère les produits par slug de collection.
    
    Paramètres:
    - **collection_slug**: Le slug de la collection.
    - **skip**: Nombre d'éléments à sauter pour la pagination (défaut: 0)
    - **limit**: Nombre maximum d'éléments à retourner (défaut: DEFAULT_PRODUCT_LIMIT, max: MAX_PRODUCT_LIMIT)
    
    Retourne:
    - Liste des produits appartenant à la collection spécifiée.
    
    Nécessite une authentification.
    """
    if limit > MAX_PRODUCT_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit cannot exceed {MAX_PRODUCT_LIMIT} items."
        )
    
    products = product_service.get_products_by_collection_slug(
        db=db, collection_slug=collection_slug, skip=skip, limit=limit
    )
    return products

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Crée un nouveau produit.
    
    Paramètres:
    - **product_in**: Données du produit à créer.
    
    Retourne:
    - Les informations complètes du produit créé.
    
    Nécessite une authentification.
    """
    try:
        product = product_service.create_product(db=db, product_in=product_in)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Met à jour un produit existant.
    
    Paramètres:
    - **product_id**: L'ID du produit à mettre à jour.
    - **product_in**: Données du produit à mettre à jour.
    
    Retourne:
    - Les informations complètes du produit mis à jour.
    
    Nécessite une authentification.
    """
    try:
        product = product_service.update_product(db=db, product_id=product_id, product_in=product_in)
        return product
    except ValueError as e:
        # Convertir ValueError en HTTPException appropriée
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Supprime un produit existant.
    
    Paramètres:
    - **product_id**: L'ID du produit à supprimer.
    
    Retourne:
    - Aucun contenu (204 No Content)
    
    Nécessite une authentification.
    """
    try:
        product_service.delete_product(db=db, product_id=product_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

