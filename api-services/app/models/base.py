from sqlalchemy import Column, DateTime, UUID, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin:
    """A mixin that adds created_at and updated_at timestamp fields to a model."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class BaseModel(Base, TimestampMixin):
    """Base model that includes an auto-generated UUID primary key and timestamps."""
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), nullable=False, index=True, unique=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)