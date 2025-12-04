from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    """Base schema for product."""
    name: str = Field(..., min_length=1, max_length=200, description="The name of the product.")
    description: Optional[str] = Field(None, description="A brief description of the product.")
    category_id: str = Field(..., description="The unique identifier of the product category.")
    collection_id: str = Field(..., description="The unique identifier of the product collection.")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="The name of the product.")
    description: Optional[str] = Field(None, description="A brief description of the product.")
    category_id: Optional[str] = Field(None, description="The unique identifier of the product category.")
    collection_id: Optional[str] = Field(None, description="The unique identifier of the product collection.")


class ProductResponse(ProductBase):
    """Response schema for a product, including metadata."""
    id: str = Field(..., description="The unique identifier of the product.")
    created_at: datetime = Field(..., description="The timestamp when the product was created.")
    updated_at: datetime = Field(..., description="The timestamp when the product was last updated.")

    model_config = ConfigDict(from_attributes=True)