from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import ProductCategory
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryUpdate


class CRUDProductCategory(CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate]):
    """CRUD operations for the ProductCategory model."""
    
    def get_by_name(self, db: Session, *, name: str, skip: int = 0, limit: int = 100) -> List[ProductCategory]:
        """Retrieve product categories by their name with pagination."""
        return db.query(ProductCategory).filter(ProductCategory.name == name).offset(skip).limit(limit).all()
    
    def get_active_categories(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ProductCategory]:
        """Retrieve all active product categories with pagination."""
        return db.query(ProductCategory).filter(ProductCategory.is_active == True).offset(skip).limit(limit).all()
    
    def get_inactive_categories(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ProductCategory]:
        """Retrieve all inactive product categories with pagination."""
        return db.query(ProductCategory).filter(ProductCategory.is_active == False).offset(skip).limit(limit).all()
    
    def deactivate_category(self, db: Session, *, category_id: str) -> Optional[ProductCategory]:
        """Deactivate a product category by setting its is_active field to False."""
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if category:
            category.is_active = False
            db.add(category)
            db.commit()
            db.refresh(category)
        return category
    
    def activate_category(self, db: Session, *, category_id: str) -> Optional[ProductCategory]:
        """Activate a product category by setting its is_active field to True."""
        category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
        if category:
            category.is_active = True
            db.add(category)
            db.commit()
            db.refresh(category)
        return category
    
    def search_by_name(self, db: Session, *, name_substring: str, skip: int = 0, limit: int = 100) -> List[ProductCategory]:
        """Search for product categories whose names contain the given substring."""
        return db.query(ProductCategory).filter(ProductCategory.name.ilike(f"%{name_substring}%")).offset(skip).limit(limit).all()