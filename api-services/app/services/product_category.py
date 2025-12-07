"""
Service pour la gestion des catégories de produits.
Contient la logique métier et les validations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud import product_category as crud_category
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate
from app.models import ProductCategory


class ProductCategoryService:
    """Service pour gérer la logique métier des catégories de produits."""

    def get_all_categories(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ProductCategory]:
        """
        Récupère toutes les catégories avec pagination.

        Args:
            db: Session de base de données
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner

        Returns:
            Liste des catégories
        """
        return crud_category.get_multi(db=db, skip=skip, limit=limit)

    def get_category_by_slug(self, db: Session, slug: str) -> Optional[ProductCategory]:
        """
        Récupère une catégorie par son slug.

        Args:
            db: Session de base de données
            slug: Slug de la catégorie

        Returns:
            Catégorie si trouvée, None sinon
        """
        return crud_category.get_by_slug(db=db, slug=slug)

    def create_category(
        self, db: Session, category_in: ProductCategoryCreate
    ) -> ProductCategory:
        """
        Crée une nouvelle catégorie avec validations métier.

        Args:
            db: Session de base de données
            category_in: Données de la catégorie à créer

        Returns:
            Catégorie créée

        Raises:
            ValueError: Si le slug ou le nom existe déjà
        """
        # Validation : slug unique
        self._validate_slug_uniqueness(db, category_in.slug)

        # Validation : nom unique
        self._validate_name_uniqueness(db, category_in.name)

        # Création de la catégorie
        return crud_category.create(db=db, obj_in=category_in)

    def update_category(
        self,
        db: Session,
        slug: str,
        category_in: ProductCategoryUpdate,
    ) -> ProductCategory:
        """
        Met à jour une catégorie existante avec validations métier.

        Args:
            db: Session de base de données
            slug: Slug de la catégorie à mettre à jour
            category_in: Nouvelles données de la catégorie

        Returns:
            Catégorie mise à jour

        Raises:
            ValueError: Si la catégorie n'existe pas ou si les validations échouent
        """
        # Récupérer la catégorie existante
        category = self.get_category_by_slug(db, slug)
        if not category:
            raise ValueError(f"Category with slug '{slug}' not found")

        # Si le slug est modifié, vérifier qu'il n'existe pas déjà
        if category_in.slug and category_in.slug != slug:
            self._validate_slug_uniqueness(db, category_in.slug)

        # Si le nom est modifié, vérifier qu'il n'existe pas déjà
        if category_in.name and category_in.name != category.name:
            self._validate_name_uniqueness(db, category_in.name)

        # Mise à jour de la catégorie
        return crud_category.update(db=db, db_obj=category, obj_in=category_in)

    def delete_category(self, db: Session, slug: str) -> None:
        """
        Supprime une catégorie existante.

        Args:
            db: Session de base de données
            slug: Slug de la catégorie à supprimer

        Raises:
            ValueError: Si la catégorie n'existe pas
        """
        category = self.get_category_by_slug(db, slug)
        if not category:
            raise ValueError(f"Category with slug '{slug}' not found")

        crud_category.delete(db=db, id=category.id)

    def _validate_slug_uniqueness(self, db: Session, slug: str) -> None:
        """
        Valide que le slug n'existe pas déjà.

        Args:
            db: Session de base de données
            slug: Slug à valider

        Raises:
            ValueError: Si le slug existe déjà
        """
        existing_category = crud_category.get_by_slug(db=db, slug=slug)
        if existing_category:
            raise ValueError(f"Category with slug '{slug}' already exists")

    def _validate_name_uniqueness(self, db: Session, name: str) -> None:
        """
        Valide que le nom n'existe pas déjà.

        Args:
            db: Session de base de données
            name: Nom à valider

        Raises:
            ValueError: Si le nom existe déjà
        """
        existing_category = crud_category.get_by_name(db=db, name=name)
        if existing_category:
            raise ValueError(f"Category with name '{name}' already exists")


# Instance globale du service
product_category_service = ProductCategoryService()
