import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimestampMixin:
    """A mixin that adds created_at and updated_at timestamp fields to a model."""

    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """Base model that includes an auto-generated UUID primary key and timestamps."""

    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
        unique=True,
    )
