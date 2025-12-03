"""
Schémas Pydantic pour les utilisateurs.
Utilisés pour la validation des données et la sérialisation API.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """Schéma de base pour un utilisateur."""

    email: EmailStr


class User(UserBase):
    """
    Schéma représentant un utilisateur authentifié.
    Utilisé par les dependencies d'authentification.
    """

    user_id: str = Field(..., description="UUID de l'utilisateur")
    role: Optional[str] = Field(None, description="Rôle de l'utilisateur")

    model_config = {"from_attributes": True}


class UserResponse(UserBase):
    """Schéma pour les réponses API contenant des informations utilisateur."""

    user_id: str
    role: Optional[str] = None

    model_config = {"from_attributes": True}
