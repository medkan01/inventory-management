from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """CRUD operations for the Product model."""
    
    def get_by_name(self, db: Session, *, name: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve products by their name with pagination."""
        return db.query(Product).filter(Product.name == name).offset(skip).limit(limit).all()
    
    def get_active_products(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve all active products with pagination."""
        return db.query(Product).filter(Product.is_active == True).offset(skip).limit(limit).all()
    
    def get_inactive_products(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve all inactive products with pagination."""
        return db.query(Product).filter(Product.is_active == False).offset(skip).limit(limit).all()
    
    def deactivate_product(self, db: Session, *, product_id: str) -> Optional[Product]:
        """Deactivate a product by setting its is_active field to False."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.is_active = False
            db.add(product)
            db.commit()
            db.refresh(product)
        return product
    
    def activate_product(self, db: Session, *, product_id: str) -> Optional[Product]:
        """Activate a product by setting its is_active field to True."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.is_active = True
            db.add(product)
            db.commit()
            db.refresh(product)
        return product
    
    def search_by_name(self, db: Session, *, name_substring: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search for products whose names contain the given substring."""
        return db.query(Product).filter(Product.name.ilike(f"%{name_substring}%")).offset(skip).limit(limit).all()
    
    def search_by_description(self, db: Session, *, description_substring: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search for products whose descriptions contain the given substring."""
        return db.query(Product).filter(Product.description.ilike(f"%{description_substring}%")).offset(skip).limit(limit).all()
    
    def search_by_category(self, db: Session, *, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search for products by their category."""
        return db.query(Product).filter(Product.category == category).offset(skip).limit(limit).all()
    
    def search_by_collection(self, db: Session, *, collection: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search for products by their collection."""
        return db.query(Product).filter(Product.collection == collection).offset(skip).limit(limit).all()