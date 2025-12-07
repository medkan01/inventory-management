"""
Tests pour les routes principales de l'application.
"""

from fastapi import status


def test_root_endpoint(client):
    """Test de la route racine /"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "api" in data
    assert data["api"] == "/api/v1"


def test_health_endpoint(client):
    """Test de la route /health"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_docs_endpoint(client):
    """Test que la documentation Swagger est accessible"""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]


def test_openapi_schema(client):
    """Test que le schéma OpenAPI est accessible"""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
