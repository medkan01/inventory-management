from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """CRUD operations for the Product model."""

    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        """Retrieve a product by its name."""
        return db.query(Product).filter(Product.name == name).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Product]:
        """Retrieve a product by its slug."""
        return db.query(Product).filter(Product.slug == slug).first()

    def get_by_category_id(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """Retrieve products by category ID with pagination."""
        return (
            db.query(Product)
            .filter(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_collection_id(
        self, db: Session, *, collection_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """Retrieve products by collection ID with pagination."""
        return (
            db.query(Product)
            .filter(Product.collection_id == collection_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_category_slug(
        self, db: Session, *, category_slug: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """Retrieve products by category slug with pagination."""
        return (
            db.query(Product)
            .join(Product.category)
            .filter(Product.category.has(slug=category_slug))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_collection_slug(
        self, db: Session, *, collection_slug: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """Retrieve products by collection slug with pagination."""
        return (
            db.query(Product)
            .join(Product.collection)
            .filter(Product.collection.has(slug=collection_slug))
            .offset(skip)
            .limit(limit)
            .all()
        )
