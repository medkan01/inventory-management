from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import ProductCollection
from app.schemas.product_collection import ProductCollectionCreate, ProductCollectionUpdate


class CRUDProductCollection(CRUDBase[ProductCollection, ProductCollectionCreate, ProductCollectionUpdate]):
    """CRUD operations for the ProductCollection model."""

    def get_by_name(self, db: Session, *, name: str, skip: int = 0, limit: int = 100) -> List[ProductCollection]:
        """Retrieve product collections by their name with pagination."""
        return db.query(ProductCollection).filter(ProductCollection.name == name).offset(skip).limit(limit).all()
    
    def get_active_collections(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ProductCollection]:
        """Retrieve all active product collections with pagination."""
        return db.query(ProductCollection).filter(ProductCollection.is_active == True).offset(skip).limit(limit).all()
    
    def get_inactive_collections(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ProductCollection]:
        """Retrieve all inactive product collections with pagination."""
        return db.query(ProductCollection).filter(ProductCollection.is_active == False).offset(skip).limit(limit).all()
    
    def deactivate_collection(self, db: Session, *, collection_id: str) -> Optional[ProductCollection]:
        """Deactivate a product collection by setting its is_active field to False."""
        collection = db.query(ProductCollection).filter(ProductCollection.id == collection_id).first()
        if collection:
            collection.is_active = False
            db.add(collection)
            db.commit()
            db.refresh(collection)
        return collection
    
    def activate_collection(self, db: Session, *, collection_id: str) -> Optional[ProductCollection]:
        """Activate a product collection by setting its is_active field to True."""
        collection = db.query(ProductCollection).filter(ProductCollection.id == collection_id).first()
        if collection:
            collection.is_active = True
            db.add(collection)
            db.commit()
            db.refresh(collection)
        return collection
    
    def search_by_name(self, db: Session, *, name_substring: str, skip: int = 0, limit: int = 100) -> List[ProductCollection]:
        """Search for product collections whose names contain the given substring."""
        return db.query(ProductCollection).filter(ProductCollection.name.ilike(f"%{name_substring}%")).offset(skip).limit(limit).all()