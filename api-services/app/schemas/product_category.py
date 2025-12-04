from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ProductCategoryBase(BaseModel):
    """Base schema for product category."""
    name: str = Field(..., min_length=1, max_length=100, description="The name of the product category.")
    slug: str = Field(..., min_length=1, max_length=100, description="The slug for the product category.")
    description: Optional[str] = Field(None, description="A brief description of the product category.")


class ProductCategoryCreate(ProductCategoryBase):
    """Schema for creating a new product category."""
    pass


class ProductCategoryUpdate(BaseModel):
    """Schema for updating a product category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="The name of the product category.")
    slug: Optional[str] = Field(None, min_length=1, max_length=100, description="The slug for the product category.")
    description: Optional[str] = Field(None, description="A brief description of the product category.")


class ProductCategoryResponse(ProductCategoryBase):
    """Response schema for a product category, including metadata."""
    id: str = Field(..., description="The unique identifier of the product category.")
    created_at: datetime = Field(..., description="The timestamp when the product category was created.")
    updated_at: datetime = Field(..., description="The timestamp when the product category was last updated.")

    model_config = ConfigDict(from_attributes=True)