"""
Configuration globale pour pytest.
Fixtures partagées pour tous les tests.
"""

import os
import pytest
from datetime import datetime, timedelta
from jose import jwt
from fastapi.testclient import TestClient

# Charger les variables d'environnement de test AVANT d'importer l'app
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("NEXT_PUBLIC_SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_JWT_SECRET", "test-jwt-secret-for-testing")

from app.main import app
from app.core.config import settings
from app.schemas.user import User


@pytest.fixture
def client():
    """
    Fixture pour le client de test FastAPI.
    
    Usage:
        def test_something(client):
            response = client.get("/")
            assert response.status_code == 200
    """
    return TestClient(app)


@pytest.fixture
def test_user():
    """
    Fixture pour un utilisateur de test.
    
    Returns:
        User: Objet utilisateur avec des données de test
    """
    return User(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        email="test@example.com",
        role="user"
    )


@pytest.fixture
def admin_user():
    """
    Fixture pour un utilisateur administrateur de test.
    
    Returns:
        User: Objet utilisateur admin avec des données de test
    """
    return User(
        user_id="987e6543-e21b-98d7-a654-321987654321",
        email="admin@example.com",
        role="admin"
    )


@pytest.fixture
def valid_jwt_token(test_user):
    """
    Génère un JWT valide pour les tests.
    
    Le token est signé avec le même secret que l'application
    et contient les claims standards de Supabase.
    
    Args:
        test_user: Fixture de l'utilisateur de test
        
    Returns:
        str: Token JWT valide
    """
    payload = {
        "sub": test_user.user_id,
        "email": test_user.email,
        "role": test_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def admin_jwt_token(admin_user):
    """
    Génère un JWT valide pour un utilisateur admin.
    
    Args:
        admin_user: Fixture de l'utilisateur admin
        
    Returns:
        str: Token JWT valide pour admin
    """
    payload = {
        "sub": admin_user.user_id,
        "email": admin_user.email,
        "role": admin_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def expired_jwt_token(test_user):
    """
    Génère un JWT expiré pour tester la validation.
    
    Args:
        test_user: Fixture de l'utilisateur de test
        
    Returns:
        str: Token JWT expiré
    """
    payload = {
        "sub": test_user.user_id,
        "email": test_user.email,
        "role": test_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() - timedelta(hours=1),  # Expiré il y a 1h
        "iat": datetime.utcnow() - timedelta(hours=2)
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def invalid_signature_token(test_user):
    """
    Génère un JWT avec une signature invalide.
    
    Args:
        test_user: Fixture de l'utilisateur de test
        
    Returns:
        str: Token JWT avec signature invalide
    """
    payload = {
        "sub": test_user.user_id,
        "email": test_user.email,
        "role": test_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, "wrong-secret-key", algorithm="HS256")


@pytest.fixture
def auth_headers(valid_jwt_token):
    """
    Fixture pour les headers d'authentification avec un token JWT valide.
    
    Args:
        valid_jwt_token: Fixture du token JWT valide
        
    Returns:
        dict: Headers avec Authorization Bearer
    """
    return {
        "Authorization": f"Bearer {valid_jwt_token}"
    }
