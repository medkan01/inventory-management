"""
Factories pour créer des données de test.
Simplifie la création d'objets de test avec des valeurs par défaut cohérentes.
"""

from typing import Optional
from sqlalchemy.orm import Session
import uuid

from app.models.product import Product, ProductCategory, ProductCollection


class ProductCategoryFactory:
    """Factory pour créer des catégories de produits de test."""

    @staticmethod
    def create(
        db: Session,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        commit: bool = True,
    ) -> ProductCategory:
        """
        Crée une catégorie de produits de test.

        Args:
            db: Session de base de données
            name: Nom de la catégorie (génère un nom unique si non fourni)
            slug: Slug de la catégorie (génère depuis le nom si non fourni)
            description: Description de la catégorie
            commit: Si True, commit la transaction

        Returns:
            ProductCategory: Catégorie créée
        """
        if name is None:
            # Générer un nom unique basé sur UUID
            unique_id = uuid.uuid4().hex[:12]
            name = f"Category-{unique_id}"

        if slug is None:
            slug = name.lower().replace(" ", "-")

        category = ProductCategory(
            name=name,
            slug=slug,
            description=description or f"Description for {name}",
        )

        db.add(category)
        if commit:
            db.commit()
            db.refresh(category)

        return category

    @staticmethod
    def create_batch(
        db: Session,
        count: int = 3,
        commit: bool = True,
    ) -> list[ProductCategory]:
        """
        Crée plusieurs catégories de test.

        Args:
            db: Session de base de données
            count: Nombre de catégories à créer
            commit: Si True, commit la transaction

        Returns:
            list[ProductCategory]: Liste des catégories créées
        """
        categories = []
        for i in range(count):
            unique_id = uuid.uuid4().hex[:12]
            category = ProductCategoryFactory.create(
                db=db,
                name=f"Category-{unique_id}-{i}",
                commit=False,
            )
            categories.append(category)

        if commit:
            db.commit()
            for category in categories:
                db.refresh(category)

        return categories


class ProductCollectionFactory:
    """Factory pour créer des collections de produits de test."""

    @staticmethod
    def create(
        db: Session,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        commit: bool = True,
    ) -> ProductCollection:
        """
        Crée une collection de produits de test.

        Args:
            db: Session de base de données
            name: Nom de la collection (génère un nom unique si non fourni)
            slug: Slug de la collection (génère depuis le nom si non fourni)
            description: Description de la collection
            commit: Si True, commit la transaction

        Returns:
            ProductCollection: Collection créée
        """
        if name is None:
            unique_id = uuid.uuid4().hex[:12]
            name = f"Collection-{unique_id}"

        if slug is None:
            slug = name.lower().replace(" ", "-")

        collection = ProductCollection(
            name=name,
            slug=slug,
            description=description or f"Description for {name}",
        )

        db.add(collection)
        if commit:
            db.commit()
            db.refresh(collection)

        return collection

    @staticmethod
    def create_batch(
        db: Session,
        count: int = 3,
        commit: bool = True,
    ) -> list[ProductCollection]:
        """
        Crée plusieurs collections de test.

        Args:
            db: Session de base de données
            count: Nombre de collections à créer
            commit: Si True, commit la transaction

        Returns:
            list[ProductCollection]: Liste des collections créées
        """
        collections = []
        for i in range(count):
            unique_id = uuid.uuid4().hex[:12]
            collection = ProductCollectionFactory.create(
                db=db,
                name=f"Collection-{unique_id}-{i}",
                commit=False,
            )
            collections.append(collection)

        if commit:
            db.commit()
            for collection in collections:
                db.refresh(collection)

        return collections


class ProductFactory:
    """Factory pour créer des produits de test."""

    @staticmethod
    def create(
        db: Session,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[ProductCategory] = None,
        collection: Optional[ProductCollection] = None,
        commit: bool = True,
    ) -> Product:
        """
        Crée un produit de test.

        Args:
            db: Session de base de données
            name: Nom du produit (génère un nom unique si non fourni)
            description: Description du produit
            category: Catégorie du produit (crée une nouvelle si non fournie)
            collection: Collection du produit (optionnelle)
            commit: Si True, commit la transaction

        Returns:
            Product: Produit créé
        """
        if name is None:
            unique_id = uuid.uuid4().hex[:12]
            name = f"Product-{unique_id}"

        # Créer une catégorie si non fournie
        if category is None:
            category = ProductCategoryFactory.create(db=db, commit=commit)

        # Générer le slug depuis le nom
        slug = name.lower().replace(" ", "-")

        product = Product(
            name=name,
            slug=slug,
            description=description or f"Description for {name}",
            category_id=category.id,
            collection_id=collection.id if collection else None,
        )

        db.add(product)
        if commit:
            db.commit()
            db.refresh(product)

        return product

    @staticmethod
    def create_batch(
        db: Session,
        count: int = 5,
        category: Optional[ProductCategory] = None,
        collection: Optional[ProductCollection] = None,
        commit: bool = True,
    ) -> list[Product]:
        """
        Crée plusieurs produits de test.

        Args:
            db: Session de base de données
            count: Nombre de produits à créer
            category: Catégorie commune (crée une nouvelle si non fournie)
            collection: Collection commune (optionnelle)
            commit: Si True, commit la transaction

        Returns:
            list[Product]: Liste des produits créés
        """
        # Créer une catégorie commune si non fournie
        if category is None:
            category = ProductCategoryFactory.create(db=db, commit=False)

        products = []
        for i in range(count):
            unique_id = uuid.uuid4().hex[:12]
            product = ProductFactory.create(
                db=db,
                name=f"Product-{unique_id}-{i}",
                category=category,
                collection=collection,
                commit=False,
            )
            products.append(product)

        if commit:
            db.commit()
            for product in products:
                db.refresh(product)

        return products


# Fixtures utilisant les factories (à ajouter dans conftest.py si nécessaire)
def create_test_category(db: Session, **kwargs) -> ProductCategory:
    """Helper pour créer une catégorie de test avec des valeurs par défaut."""
    return ProductCategoryFactory.create(db=db, **kwargs)


def create_test_collection(db: Session, **kwargs) -> ProductCollection:
    """Helper pour créer une collection de test avec des valeurs par défaut."""
    return ProductCollectionFactory.create(db=db, **kwargs)


def create_test_product(db: Session, **kwargs) -> Product:
    """Helper pour créer un produit de test avec des valeurs par défaut."""
    return ProductFactory.create(db=db, **kwargs)
