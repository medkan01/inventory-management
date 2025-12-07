"""
Endpoints d'authentification.
Routes pour tester l'authentification et obtenir les informations utilisateur.
"""

from typing import Optional
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_current_user_optional
from app.schemas import User, UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur authentifié actuel.

    Nécessite un token JWT valide dans le header Authorization.
    """
    return UserResponse(
        user_id=current_user.user_id, email=current_user.email, role=current_user.role
    )


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """
    Route protégée - authentification obligatoire.

    Exemple de route nécessitant une authentification.
    """
    return {
        "message": f"Hello {current_user.email}!",
        "user_id": current_user.user_id,
        "email": current_user.email,
        "role": current_user.role,
        "authentication": "required",
    }


@router.get("/optional")
async def optional_auth_route(
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Route avec authentification optionnelle.

    Fonctionne avec ou sans token JWT.
    """
    if current_user:
        return {
            "message": f"Welcome back, {current_user.email}!",
            "user_id": current_user.user_id,
            "authenticated": True,
        }
    return {"message": "Welcome, guest!", "authenticated": False}
