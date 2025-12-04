from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import ProductCategory
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryUpdate


class CRUDProductCategory(CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate]):
    """CRUD operations for the ProductCategory model."""
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[ProductCategory]:
        """Retrieve a product category by its name."""
        return db.query(ProductCategory).filter(ProductCategory.name == name).first()
    
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[ProductCategory]:
        """Retrieve a product category by its slug."""
        return db.query(ProductCategory).filter(ProductCategory.slug == slug).first()