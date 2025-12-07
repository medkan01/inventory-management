"""
Service pour la gestion des produits.
Contient la logique métier et les validations.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud import (
    product as crud_product,
    product_category as crud_category,
    product_collection as crud_collection,
)
from app.schemas import ProductCreate, ProductUpdate
from app.models import Product


class ProductService:
    """Service pour gérer la logique métier des produits."""

    def get_all_products(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Récupère tous les produits avec pagination.

        Args:
            db: Session de base de données
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner

        Returns:
            Liste des produits
        """
        return crud_product.get_multi(db=db, skip=skip, limit=limit)

    def get_product_by_id(self, db: Session, product_id: UUID) -> Optional[Product]:
        """
        Récupère un produit par son ID.

        Args:
            db: Session de base de données
            product_id: ID du produit

        Returns:
            Produit si trouvé, None sinon
        """
        return crud_product.get(db=db, id=product_id)

    def get_product_by_slug(self, db: Session, slug: str) -> Optional[Product]:
        """
        Récupère un produit par son slug.

        Args:
            db: Session de base de données
            slug: Slug du produit

        Returns:
            Produit si trouvé, None sinon
        """
        return crud_product.get_by_slug(db=db, slug=slug)

    def get_products_by_category_id(
        self, db: Session, category_id: UUID, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Récupère les produits par ID de catégorie.

        Args:
            db: Session de base de données
            category_id: ID de la catégorie
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner

        Returns:
            Liste des produits de la catégorie
        """
        return crud_product.get_by_category_id(
            db=db, category_id=category_id, skip=skip, limit=limit
        )

    def get_products_by_category_slug(
        self, db: Session, category_slug: str, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Récupère les produits par slug de catégorie.

        Args:
            db: Session de base de données
            category_slug: Slug de la catégorie
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner

        Returns:
            Liste des produits de la catégorie
        """
        return crud_product.get_by_category_slug(
            db=db, category_slug=category_slug, skip=skip, limit=limit
        )

    def get_products_by_collection_id(
        self, db: Session, collection_id: UUID, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Récupère les produits par ID de collection.

        Args:
            db: Session de base de données
            collection_id: ID de la collection
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner

        Returns:
            Liste des produits de la collection
        """
        return crud_product.get_by_collection_id(
            db=db, collection_id=collection_id, skip=skip, limit=limit
        )

    def get_products_by_collection_slug(
        self, db: Session, collection_slug: str, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Récupère les produits par slug de collection.

        Args:
            db: Session de base de données
            collection_slug: Slug de la collection
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner

        Returns:
            Liste des produits de la collection
        """
        return crud_product.get_by_collection_slug(
            db=db, collection_slug=collection_slug, skip=skip, limit=limit
        )

    def create_product(self, db: Session, product_in: ProductCreate) -> Product:
        """
        Crée un nouveau produit avec validations métier.

        Args:
            db: Session de base de données
            product_in: Données du produit à créer

        Returns:
            Produit créé

        Raises:
            ValueError: Si les validations échouent
        """
        # Validation : slug unique
        existing_product = crud_product.get_by_slug(db=db, slug=product_in.slug)
        if existing_product:
            raise ValueError(f"Product with slug '{product_in.slug}' already exists")

        # Validation : catégorie existe
        self._validate_category_exists(db, product_in.category_id)

        # Validation : collection existe (si fournie)
        if product_in.collection_id:
            self._validate_collection_exists(db, product_in.collection_id)

        # Création du produit
        return crud_product.create(db=db, obj_in=product_in)

    def update_product(
        self, db: Session, product_id: UUID, product_in: ProductUpdate
    ) -> Product:
        """
        Met à jour un produit existant avec validations métier.

        Args:
            db: Session de base de données
            product_id: ID du produit à mettre à jour
            product_in: Nouvelles données du produit

        Returns:
            Produit mis à jour

        Raises:
            ValueError: Si le produit n'existe pas ou si les validations échouent
        """
        # Récupérer le produit existant
        product = self.get_product_by_id(db, product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        # Validation : slug unique (si fourni et différent de l'actuel)
        if product_in.slug and product_in.slug != product.slug:
            existing_product = crud_product.get_by_slug(db=db, slug=product_in.slug)
            if existing_product:
                raise ValueError(
                    f"Product with slug '{product_in.slug}' already exists"
                )

        # Validation : catégorie existe (si fournie)
        if product_in.category_id:
            self._validate_category_exists(db, product_in.category_id)

        # Validation : collection existe (si fournie)
        if product_in.collection_id:
            self._validate_collection_exists(db, product_in.collection_id)

        # Mise à jour du produit
        return crud_product.update(db=db, db_obj=product, obj_in=product_in)

    def delete_product(self, db: Session, product_id: UUID) -> None:
        """
        Supprime un produit existant.

        Args:
            db: Session de base de données
            product_id: ID du produit à supprimer

        Raises:
            ValueError: Si le produit n'existe pas
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        crud_product.delete(db=db, id=product_id)

    def _validate_category_exists(self, db: Session, category_id: UUID) -> None:
        """
        Valide que la catégorie existe.

        Args:
            db: Session de base de données
            category_id: ID de la catégorie à valider

        Raises:
            ValueError: Si la catégorie n'existe pas
        """
        category = crud_category.get(db=db, id=category_id)
        if not category:
            raise ValueError(f"Category with ID '{category_id}' does not exist")

    def _validate_collection_exists(self, db: Session, collection_id: UUID) -> None:
        """
        Valide que la collection existe.

        Args:
            db: Session de base de données
            collection_id: ID de la collection à valider

        Raises:
            ValueError: Si la collection n'existe pas
        """
        collection = crud_collection.get(db=db, id=collection_id)
        if not collection:
            raise ValueError(f"Collection with ID '{collection_id}' does not exist")


# Instance globale du service
product_service = ProductService()
