from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


class ProductCollectionBase(BaseModel):
    """Base schema for product collection."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The name of the product collection.",
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The slug for the product collection.",
    )
    description: Optional[str] = Field(
        None, description="A brief description of the product collection."
    )


class ProductCollectionCreate(ProductCollectionBase):
    """Schema for creating a new product collection."""

    pass


class ProductCollectionUpdate(BaseModel):
    """Schema for updating a product collection."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="The name of the product collection.",
    )
    slug: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="The slug for the product collection.",
    )
    description: Optional[str] = Field(
        None, description="A brief description of the product collection."
    )


class ProductCollectionResponse(ProductCollectionBase):
    """Response schema for a product collection, including metadata."""

    id: UUID = Field(
        ..., description="The unique identifier of the product collection."
    )
    created_at: datetime = Field(
        ..., description="The timestamp when the product collection was created."
    )
    updated_at: datetime = Field(
        ..., description="The timestamp when the product collection was last updated."
    )

    model_config = ConfigDict(from_attributes=True)
