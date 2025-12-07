from app.models.base import BaseModel as Base
from pydantic import BaseModel
from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic CRUD operations for a given SQLAlchemy model."""
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUD object with the given model.
        
        :param model: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Retrieve a single record by its ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Retrieve multiple records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)  # type: ignore

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        """Update an existing record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def delete(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """Delete a record by its ID."""
        obj = db.query(self.model).filter(self.model.id == id).first()

        if obj:
            db.delete(obj)
            db.commit()

        return obj