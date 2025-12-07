"""
Tests pour les endpoints de ProductCategory.
Teste les routes HTTP, l'authentification, les status codes.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.fixtures.factories import ProductCategoryFactory


class TestProductCategoryGetAll:
    """Tests pour GET /api/v1/categories/"""

    def test_get_categories_success(self, client: TestClient, db: Session):
        """Test de récupération de toutes les catégories."""
        ProductCategoryFactory.create_batch(db=db, count=3)

        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in cat for cat in data)
        assert all("name" in cat for cat in data)
        assert all("slug" in cat for cat in data)

    def test_get_categories_with_pagination(self, client: TestClient, db: Session):
        """Test de pagination."""
        ProductCategoryFactory.create_batch(db=db, count=10)

        response = client.get("/api/v1/categories/?skip=0&limit=5")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_get_categories_limit_exceeds_max(self, client: TestClient, db: Session):
        """Test qu'une limite trop élevée retourne une erreur."""
        response = client.get("/api/v1/categories/?limit=10000")

        assert response.status_code == 400
        assert "exceed" in response.json()["detail"].lower()

    def test_get_categories_empty(self, client: TestClient, db: Session):
        """Test avec une base vide."""
        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        assert response.json() == []


class TestProductCategoryGetBySlug:
    """Tests pour GET /api/v1/categories/{slug}"""

    def test_get_category_by_slug_success(self, client: TestClient, db: Session):
        """Test de récupération d'une catégorie par slug."""
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics"
        )

        response = client.get(f"/api/v1/categories/{category.slug}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Electronics"
        assert data["slug"] == "electronics"

    def test_get_category_by_slug_not_found(self, client: TestClient, db: Session):
        """Test qu'un slug inexistant retourne 404."""
        response = client.get("/api/v1/categories/nonexistent")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestProductCategoryCreate:
    """Tests pour POST /api/v1/categories/"""

    def test_create_category_success(self, client: TestClient, db: Session):
        """Test de création d'une catégorie."""
        category_data = {
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic devices",
        }

        response = client.post("/api/v1/categories/", json=category_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Electronics"
        assert data["slug"] == "electronics"
        assert "id" in data

    def test_create_category_duplicate_slug_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'un slug dupliqué retourne une erreur."""
        ProductCategoryFactory.create(db=db, slug="electronics")

        category_data = {
            "name": "New Category",
            "slug": "electronics",
            "description": "Test",
        }

        response = client.post("/api/v1/categories/", json=category_data)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_category_invalid_data_fails(self, client: TestClient, db: Session):
        """Test qu'une donnée invalide retourne une erreur."""
        category_data = {
            "slug": "electronics"
            # name manquant (requis)
        }

        response = client.post("/api/v1/categories/", json=category_data)

        assert response.status_code == 422


class TestProductCategoryUpdate:
    """Tests pour PUT /api/v1/categories/{slug}"""

    def test_update_category_success(self, client: TestClient, db: Session):
        """Test de mise à jour d'une catégorie."""
        category = ProductCategoryFactory.create(
            db=db, name="Old Name", slug="old-name"
        )

        update_data = {"name": "New Name"}
        response = client.put(f"/api/v1/categories/{category.slug}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["slug"] == "old-name"

    def test_update_category_not_found(self, client: TestClient, db: Session):
        """Test qu'une catégorie inexistante retourne 404."""
        update_data = {"name": "New Name"}
        response = client.put("/api/v1/categories/nonexistent", json=update_data)

        assert response.status_code == 404

    def test_update_category_duplicate_slug_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'un slug dupliqué retourne une erreur."""
        ProductCategoryFactory.create(db=db, slug="existing-slug")
        category = ProductCategoryFactory.create(db=db, slug="my-slug")

        update_data = {"slug": "existing-slug"}
        response = client.put(f"/api/v1/categories/{category.slug}", json=update_data)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


class TestProductCategoryDelete:
    """Tests pour DELETE /api/v1/categories/{slug}"""

    def test_delete_category_success(self, client: TestClient, db: Session):
        """Test de suppression d'une catégorie."""
        category = ProductCategoryFactory.create(db=db, slug="to-delete")

        response = client.delete(f"/api/v1/categories/{category.slug}")

        assert response.status_code == 204

        # Vérifier que la catégorie est bien supprimée
        get_response = client.get(f"/api/v1/categories/{category.slug}")
        assert get_response.status_code == 404

    def test_delete_category_not_found(self, client: TestClient, db: Session):
        """Test qu'une catégorie inexistante retourne 404."""
        response = client.delete("/api/v1/categories/nonexistent")

        assert response.status_code == 404
