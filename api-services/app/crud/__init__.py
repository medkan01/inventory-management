"""CRUD instances for application models."""

from app.crud.base import CRUDBase
from app.crud.product import CRUDProduct
from app.crud.product_category import CRUDProductCategory
from app.crud.product_collection import CRUDProductCollection
from app.models import Product
from app.models.product import ProductCategory, ProductCollection

# Instances globales pour les opérations CRUD
product = CRUDProduct(Product)
product_category = CRUDProductCategory(ProductCategory)
product_collection = CRUDProductCollection(ProductCollection)

__all__ = ["CRUDBase", "CRUDProduct", "product", "product_category", "product_collection"]