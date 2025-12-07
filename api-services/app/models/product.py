from app.models.base import BaseModel
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship


class ProductCategory(BaseModel):
    """
    Represents a category for products in the application.
    """

    __tablename__ = "product_categories"

    # Core fields
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    products = relationship("Product", back_populates="category")


class ProductCollection(BaseModel):
    """
    Represents a collection of products in the application.
    """

    __tablename__ = "product_collections"

    # Core fields
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    products = relationship("Product", back_populates="collection")


class Product(BaseModel):
    """
    Represents a product in the application.
    """

    __tablename__ = "products"

    # Core fields
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Foreign keys
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=False, index=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("product_collections.id"), nullable=True, index=True)

    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    collection = relationship("ProductCollection", back_populates="products")