"""
Tests pour les endpoints de ProductCollection.
Teste les routes HTTP, l'authentification, les status codes.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.fixtures.factories import ProductCollectionFactory


class TestProductCollectionGetAll:
    """Tests pour GET /api/v1/collections/"""

    def test_get_collections_success(self, client: TestClient, db: Session):
        """Test de récupération de toutes les collections."""
        ProductCollectionFactory.create_batch(db=db, count=3)

        response = client.get("/api/v1/collections/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in col for col in data)
        assert all("name" in col for col in data)
        assert all("slug" in col for col in data)

    def test_get_collections_with_pagination(self, client: TestClient, db: Session):
        """Test de pagination."""
        ProductCollectionFactory.create_batch(db=db, count=10)

        response = client.get("/api/v1/collections/?skip=0&limit=5")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_get_collections_limit_exceeds_max(self, client: TestClient, db: Session):
        """Test qu'une limite trop élevée retourne une erreur."""
        response = client.get("/api/v1/collections/?limit=10000")

        assert response.status_code == 400
        assert "exceed" in response.json()["detail"].lower()

    def test_get_collections_empty(self, client: TestClient, db: Session):
        """Test avec une base vide."""
        response = client.get("/api/v1/collections/")

        assert response.status_code == 200
        assert response.json() == []


class TestProductCollectionGetBySlug:
    """Tests pour GET /api/v1/collections/{slug}"""

    def test_get_collection_by_slug_success(self, client: TestClient, db: Session):
        """Test de récupération d'une collection par slug."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer Sale", slug="summer-sale"
        )

        response = client.get(f"/api/v1/collections/{collection.slug}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Summer Sale"
        assert data["slug"] == "summer-sale"

    def test_get_collection_by_slug_not_found(self, client: TestClient, db: Session):
        """Test qu'un slug inexistant retourne 404."""
        response = client.get("/api/v1/collections/nonexistent")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestProductCollectionCreate:
    """Tests pour POST /api/v1/collections/"""

    def test_create_collection_success(self, client: TestClient, db: Session):
        """Test de création d'une collection."""
        collection_data = {
            "name": "Summer Sale",
            "slug": "summer-sale",
            "description": "Summer products",
        }

        response = client.post("/api/v1/collections/", json=collection_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Summer Sale"
        assert data["slug"] == "summer-sale"
        assert "id" in data

    def test_create_collection_duplicate_slug_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'un slug dupliqué retourne une erreur."""
        ProductCollectionFactory.create(db=db, slug="summer-sale")

        collection_data = {
            "name": "New Collection",
            "slug": "summer-sale",
            "description": "Test",
        }

        response = client.post("/api/v1/collections/", json=collection_data)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_collection_invalid_data_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'une donnée invalide retourne une erreur."""
        collection_data = {
            "slug": "summer-sale"
            # name manquant (requis)
        }

        response = client.post("/api/v1/collections/", json=collection_data)

        assert response.status_code == 422


class TestProductCollectionUpdate:
    """Tests pour PUT /api/v1/collections/{slug}"""

    def test_update_collection_success(self, client: TestClient, db: Session):
        """Test de mise à jour d'une collection."""
        collection = ProductCollectionFactory.create(
            db=db, name="Old Name", slug="old-name"
        )

        update_data = {"name": "New Name"}
        response = client.put(
            f"/api/v1/collections/{collection.slug}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["slug"] == "old-name"

    def test_update_collection_not_found(self, client: TestClient, db: Session):
        """Test qu'une collection inexistante retourne 404."""
        update_data = {"name": "New Name"}
        response = client.put("/api/v1/collections/nonexistent", json=update_data)

        assert response.status_code == 404

    def test_update_collection_duplicate_slug_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'un slug dupliqué retourne une erreur."""
        ProductCollectionFactory.create(db=db, slug="existing-slug")
        collection = ProductCollectionFactory.create(db=db, slug="my-slug")

        update_data = {"slug": "existing-slug"}
        response = client.put(
            f"/api/v1/collections/{collection.slug}", json=update_data
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


class TestProductCollectionDelete:
    """Tests pour DELETE /api/v1/collections/{slug}"""

    def test_delete_collection_success(self, client: TestClient, db: Session):
        """Test de suppression d'une collection."""
        collection = ProductCollectionFactory.create(db=db, slug="to-delete")

        response = client.delete(f"/api/v1/collections/{collection.slug}")

        assert response.status_code == 204

        # Vérifier que la collection est bien supprimée
        get_response = client.get(f"/api/v1/collections/{collection.slug}")
        assert get_response.status_code == 404

    def test_delete_collection_not_found(self, client: TestClient, db: Session):
        """Test qu'une collection inexistante retourne 404."""
        response = client.delete("/api/v1/collections/nonexistent")

        assert response.status_code == 404
