"""
Dépendances communes pour les routes API.
Contient les dependencies d'authentification, de base de données, etc.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.user import User

logger = get_logger(__name__)

# Security scheme for Bearer token
security = HTTPBearer()


class AuthenticationError(HTTPException):
    """Exception levée lors d'une erreur d'authentification."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


def decode_token(token: str) -> dict:
    """
    Décode et valide un JWT token de Supabase.
    
    Args:
        token: JWT token string
        
    Returns:
        Payload du token décodé
        
    Raises:
        AuthenticationError: Si le token est invalide ou expiré
    """
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False}  # Supabase doesn't use aud claim
        )
        logger.debug(f"Token decoded successfully for user: {payload.get('email')}")
        return payload
        
    except JWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise AuthenticationError(f"Invalid authentication token: {str(e)}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency pour obtenir l'utilisateur authentifié actuel.
    
    Utilisation dans une route:
    ```python
    @router.get("/protected")
    async def protected_route(user: User = Depends(get_current_user)):
        return {"message": f"Hello {user.email}"}
    ```
    
    Args:
        credentials: Bearer token depuis le header Authorization
        
    Returns:
        Objet User avec les informations de l'utilisateur
        
    Raises:
        AuthenticationError: Si l'authentification échoue
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    # Extraire les informations utilisateur du JWT
    user_id = payload.get("sub")
    email = payload.get("email")
    role = payload.get("role")
    
    if not user_id or not email:
        logger.error("Token payload missing required fields")
        raise AuthenticationError("Invalid token payload")
    
    logger.info(f"User authenticated: {email}")
    return User(user_id=user_id, email=email, role=role)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[User]:
    """
    Dependency pour obtenir l'utilisateur si authentifié, None sinon.
    
    Utilisé pour les routes qui fonctionnent avec ou sans authentification:
    ```python
    @router.get("/optional")
    async def optional_route(user: Optional[User] = Depends(get_current_user_optional)):
        if user:
            return {"message": f"Hello {user.email}"}
        return {"message": "Hello guest"}
    ```
    
    Args:
        credentials: Bearer token optionnel depuis le header Authorization
        
    Returns:
        Objet User si authentifié, None sinon
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = decode_token(token)
        
        user_id = payload.get("sub")
        email = payload.get("email")
        role = payload.get("role")
        
        if not user_id or not email:
            return None
        
        logger.info(f"Optional auth - User authenticated: {email}")
        return User(user_id=user_id, email=email, role=role)
        
    except AuthenticationError:
        logger.debug("Optional auth - Invalid token, returning None")
        return None
