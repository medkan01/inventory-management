from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import ProductCollection
from app.schemas.product_collection import (
    ProductCollectionCreate,
    ProductCollectionUpdate,
)


class CRUDProductCollection(
    CRUDBase[ProductCollection, ProductCollectionCreate, ProductCollectionUpdate]
):
    """CRUD operations for the ProductCollection model."""

    def get_by_name(self, db: Session, *, name: str) -> Optional[ProductCollection]:
        """Retrieve a product collection by its name."""
        return (
            db.query(ProductCollection).filter(ProductCollection.name == name).first()
        )

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[ProductCollection]:
        """Retrieve a product collection by its slug."""
        return (
            db.query(ProductCollection).filter(ProductCollection.slug == slug).first()
        )
