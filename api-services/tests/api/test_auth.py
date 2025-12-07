"""
Tests pour les endpoints d'authentification.
"""

from fastapi import status


def test_optional_auth_without_token(client_no_auth):
    """Test de la route /api/v1/auth/optional sans token"""
    response = client_no_auth.get("/api/v1/auth/optional")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["message"] == "Welcome, guest!"
    assert data["authenticated"] is False


def test_protected_route_without_token(client_no_auth):
    """Test de la route protégée sans token - doit retourner 403"""
    response = client_no_auth.get("/api/v1/auth/protected")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_me_route_without_token(client_no_auth):
    """Test de la route /me sans token - doit retourner 403"""
    response = client_no_auth.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_protected_route_with_valid_token(client_no_auth, auth_headers, test_user):
    """Test de la route protégée avec un token JWT valide"""
    response = client_no_auth.get("/api/v1/auth/protected", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert data["user_id"] == test_user.user_id
    assert data["email"] == test_user.email


def test_me_route_with_valid_token(client_no_auth, auth_headers, test_user):
    """Test de la route /me avec un token JWT valide"""
    response = client_no_auth.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["user_id"] == test_user.user_id
    assert data["email"] == test_user.email
    assert data["role"] == test_user.role


def test_protected_route_with_expired_token(client_no_auth, expired_jwt_token):
    """Test de la route protégée avec un token expiré - doit retourner 401"""
    headers = {"Authorization": f"Bearer {expired_jwt_token}"}
    response = client_no_auth.get("/api/v1/auth/protected", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_route_with_invalid_signature(client_no_auth, invalid_signature_token):
    """Test de la route protégée avec une signature invalide - doit retourner 401"""
    headers = {"Authorization": f"Bearer {invalid_signature_token}"}
    response = client_no_auth.get("/api/v1/auth/protected", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_route_with_malformed_token(client_no_auth):
    """Test de la route protégée avec un token malformé - doit retourner 401"""
    headers = {"Authorization": "Bearer not-a-valid-jwt-token"}
    response = client_no_auth.get("/api/v1/auth/protected", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_optional_auth_with_valid_token(client_no_auth, auth_headers, test_user):
    """Test de la route /api/v1/auth/optional avec un token valide"""
    response = client_no_auth.get("/api/v1/auth/optional", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["authenticated"] is True
    assert data["user_id"] == test_user.user_id
    assert "Welcome back" in data["message"]


def test_admin_route_with_admin_token(client_no_auth, admin_jwt_token, admin_user):
    """Test d'une route avec un token admin"""
    headers = {"Authorization": f"Bearer {admin_jwt_token}"}
    response = client_no_auth.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["role"] == "admin"
    assert data["email"] == admin_user.email
