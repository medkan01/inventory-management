"""
Service pour la gestion des collections de produits.
Contient la logique métier et les validations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud import product_collection as crud_collection
from app.schemas import ProductCollectionCreate, ProductCollectionUpdate
from app.models import ProductCollection


class ProductCollectionService:
    """Service pour gérer la logique métier des collections de produits."""

    def get_all_collections(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ProductCollection]:
        """
        Récupère toutes les collections avec pagination.
        
        Args:
            db: Session de base de données
            skip: Nombre d'éléments à sauter
            limit: Nombre maximum d'éléments à retourner
            
        Returns:
            Liste des collections
        """
        return crud_collection.get_multi(db=db, skip=skip, limit=limit)

    def get_collection_by_slug(
        self, db: Session, slug: str
    ) -> Optional[ProductCollection]:
        """
        Récupère une collection par son slug.
        
        Args:
            db: Session de base de données
            slug: Slug de la collection
            
        Returns:
            Collection si trouvée, None sinon
        """
        return crud_collection.get_by_slug(db=db, slug=slug)

    def create_collection(
        self, db: Session, collection_in: ProductCollectionCreate
    ) -> ProductCollection:
        """
        Crée une nouvelle collection avec validations métier.
        
        Args:
            db: Session de base de données
            collection_in: Données de la collection à créer
            
        Returns:
            Collection créée
            
        Raises:
            ValueError: Si le slug ou le titre existe déjà
        """
        # Validation : slug unique
        self._validate_slug_uniqueness(db, collection_in.slug)
        
        # Validation : nom unique
        self._validate_name_uniqueness(db, collection_in.name)
        
        # Création de la collection
        return crud_collection.create(db=db, obj_in=collection_in)

    def update_collection(
        self,
        db: Session,
        slug: str,
        collection_in: ProductCollectionUpdate,
    ) -> ProductCollection:
        """
        Met à jour une collection existante avec validations métier.
        
        Args:
            db: Session de base de données
            slug: Slug de la collection à mettre à jour
            collection_in: Nouvelles données de la collection
            
        Returns:
            Collection mise à jour
            
        Raises:
            ValueError: Si la collection n'existe pas ou si les validations échouent
        """
        # Récupérer la collection existante
        collection = self.get_collection_by_slug(db, slug)
        if not collection:
            raise ValueError(f"Collection with slug '{slug}' not found")
        
        # Si le slug est modifié, vérifier qu'il n'existe pas déjà
        if collection_in.slug and collection_in.slug != slug:
            self._validate_slug_uniqueness(db, collection_in.slug)
        
        # Si le nom est modifié, vérifier qu'il n'existe pas déjà
        if collection_in.name and collection_in.name != collection.name:
            self._validate_name_uniqueness(db, collection_in.name)
        
        # Mise à jour de la collection
        return crud_collection.update(db=db, db_obj=collection, obj_in=collection_in)

    def delete_collection(self, db: Session, slug: str) -> None:
        """
        Supprime une collection existante.
        
        Args:
            db: Session de base de données
            slug: Slug de la collection à supprimer
            
        Raises:
            ValueError: Si la collection n'existe pas
        """
        collection = self.get_collection_by_slug(db, slug)
        if not collection:
            raise ValueError(f"Collection with slug '{slug}' not found")
        
        crud_collection.delete(db=db, id=collection.id)

    def _validate_slug_uniqueness(self, db: Session, slug: str) -> None:
        """
        Valide que le slug n'existe pas déjà.
        
        Args:
            db: Session de base de données
            slug: Slug à valider
            
        Raises:
            ValueError: Si le slug existe déjà
        """
        existing_collection = crud_collection.get_by_slug(db=db, slug=slug)
        if existing_collection:
            raise ValueError(f"Collection with slug '{slug}' already exists")

    def _validate_name_uniqueness(self, db: Session, name: str) -> None:
        """
        Valide que le nom n'existe pas déjà.
        
        Args:
            db: Session de base de données
            name: Nom à valider
            
        Raises:
            ValueError: Si le nom existe déjà
        """
        existing_collection = crud_collection.get_by_name(db=db, name=name)
        if existing_collection:
            raise ValueError(f"Collection with name '{name}' already exists")


# Instance globale du service
product_collection_service = ProductCollectionService()
