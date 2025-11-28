"""
Authentication dependencies for FastAPI routes.

This module provides dependency functions to validate JWT tokens from Supabase
and extract user information.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os

# Configuration Supabase
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")

# Security scheme for Bearer token
security = HTTPBearer()


class User:
    """Represents an authenticated user."""
    
    def __init__(self, user_id: str, email: str, role: Optional[str] = None):
        self.user_id = user_id
        self.email = email
        self.role = role


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token from Supabase.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: JWT secret not configured"
        )
    
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}  # Supabase doesn't use aud claim
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency to get the current authenticated user.
    
    Use this in route parameters to require authentication:
    ```python
    @app.get("/protected")
    async def protected_route(user: User = Depends(get_current_user)):
        return {"message": f"Hello {user.email}"}
    ```
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        User object with user information
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    # Extract user information from JWT payload
    user_id = payload.get("sub")
    email = payload.get("email")
    role = payload.get("role")
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return User(user_id=user_id, email=email, role=role)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[User]:
    """
    Dependency to get the current user if authenticated, None otherwise.
    
    Use this for routes that can work both authenticated and unauthenticated:
    ```python
    @app.get("/optional-auth")
    async def optional_route(user: Optional[User] = Depends(get_current_user_optional)):
        if user:
            return {"message": f"Hello {user.email}"}
        return {"message": "Hello guest"}
    ```
    
    Args:
        credentials: Bearer token from Authorization header (optional)
        
    Returns:
        User object if authenticated, None otherwise
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
        
        return User(user_id=user_id, email=email, role=role)
    except HTTPException:
        return None
