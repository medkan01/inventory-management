"""
Tests pour les endpoints de Product.
Teste les routes HTTP, l'authentification, les status codes.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.fixtures.factories import (
    ProductFactory,
    ProductCategoryFactory,
    ProductCollectionFactory,
)


class TestProductGetAll:
    """Tests pour GET /api/v1/products/"""

    def test_get_products_success(self, client: TestClient, db: Session):
        """Test de récupération de tous les produits."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=3, category=category)

        response = client.get("/api/v1/products/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in prod for prod in data)
        assert all("name" in prod for prod in data)

    def test_get_products_with_pagination(self, client: TestClient, db: Session):
        """Test de pagination."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=10, category=category)

        response = client.get("/api/v1/products/?skip=0&limit=5")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_get_products_limit_exceeds_max(self, client: TestClient, db: Session):
        """Test qu'une limite trop élevée retourne une erreur."""
        response = client.get("/api/v1/products/?limit=10000")

        assert response.status_code == 400
        assert "exceed" in response.json()["detail"].lower()

    def test_get_products_empty(self, client: TestClient, db: Session):
        """Test avec une base vide."""
        response = client.get("/api/v1/products/")

        assert response.status_code == 200
        assert response.json() == []


class TestProductGetById:
    """Tests pour GET /api/v1/products/{id}"""

    def test_get_product_by_id_success(self, client: TestClient, db: Session):
        """Test de récupération d'un produit par ID."""
        product = ProductFactory.create(db=db, name="Test Product")

        response = client.get(f"/api/v1/products/{product.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Product"
        assert data["id"] == str(product.id)

    def test_get_product_by_id_not_found(self, client: TestClient, db: Session):
        """Test qu'un ID inexistant retourne 404."""
        from uuid import uuid4

        nonexistent_id = uuid4()

        response = client.get(f"/api/v1/products/{nonexistent_id}")

        assert response.status_code == 404


class TestProductGetByCategory:
    """Tests pour GET /api/v1/products/category/{id} et /category/slug/{slug}"""

    def test_get_products_by_category_id(self, client: TestClient, db: Session):
        """Test de récupération par ID de catégorie."""
        category1 = ProductCategoryFactory.create(db=db, name="Category 1")
        category2 = ProductCategoryFactory.create(db=db, name="Category 2")
        ProductFactory.create_batch(db=db, count=3, category=category1)
        ProductFactory.create_batch(db=db, count=2, category=category2)

        response = client.get(f"/api/v1/products/category/{category1.id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_get_products_by_category_slug(self, client: TestClient, db: Session):
        """Test de récupération par slug de catégorie."""
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics"
        )
        ProductFactory.create_batch(db=db, count=4, category=category)

        response = client.get(f"/api/v1/products/category/slug/{category.slug}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4


class TestProductGetByCollection:
    """Tests pour GET /api/v1/products/collection/{id} et /collection/slug/{slug}"""

    def test_get_products_by_collection_id(self, client: TestClient, db: Session):
        """Test de récupération par ID de collection."""
        category = ProductCategoryFactory.create(db=db)
        collection1 = ProductCollectionFactory.create(db=db, name="Collection 1")
        collection2 = ProductCollectionFactory.create(db=db, name="Collection 2")
        ProductFactory.create_batch(
            db=db, count=3, category=category, collection=collection1
        )
        ProductFactory.create_batch(
            db=db, count=2, category=category, collection=collection2
        )

        response = client.get(f"/api/v1/products/collection/{collection1.id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_get_products_by_collection_slug(self, client: TestClient, db: Session):
        """Test de récupération par slug de collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(
            db=db, name="Summer Sale", slug="summer-sale"
        )
        ProductFactory.create_batch(
            db=db, count=4, category=category, collection=collection
        )

        response = client.get(f"/api/v1/products/collection/slug/{collection.slug}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4


class TestProductCreate:
    """Tests pour POST /api/v1/products/"""

    def test_create_product_success(self, client: TestClient, db: Session):
        """Test de création d'un produit."""
        category = ProductCategoryFactory.create(db=db)

        product_data = {
            "name": "Laptop Dell XPS 13",
            "slug": "laptop-dell-xps-13",
            "description": "High-performance laptop",
            "category_id": str(category.id),
        }

        response = client.post("/api/v1/products/", json=product_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Laptop Dell XPS 13"
        assert "id" in data

    def test_create_product_with_collection(self, client: TestClient, db: Session):
        """Test de création avec une collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db)

        product_data = {
            "name": "Product",
            "slug": "product-with-collection",
            "category_id": str(category.id),
            "collection_id": str(collection.id),
        }

        response = client.post("/api/v1/products/", json=product_data)

        assert response.status_code == 201
        data = response.json()
        assert data["collection_id"] == str(collection.id)

    def test_create_product_with_nonexistent_category_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'une catégorie inexistante retourne une erreur."""
        from uuid import uuid4

        product_data = {
            "name": "Product",
            "slug": "test-product",
            "category_id": str(uuid4()),
        }

        response = client.post("/api/v1/products/", json=product_data)

        assert response.status_code == 400
        assert "does not exist" in response.json()["detail"]

    def test_create_product_invalid_data_fails(self, client: TestClient, db: Session):
        """Test qu'une donnée invalide retourne une erreur."""
        product_data = {
            "description": "Test"
            # name et category_id manquants
        }

        response = client.post("/api/v1/products/", json=product_data)

        assert response.status_code == 422


class TestProductUpdate:
    """Tests pour PUT /api/v1/products/{id}"""

    def test_update_product_success(self, client: TestClient, db: Session):
        """Test de mise à jour d'un produit."""
        product = ProductFactory.create(db=db, name="Old Name")

        update_data = {"name": "New Name"}
        response = client.put(f"/api/v1/products/{product.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"

    def test_update_product_change_category(self, client: TestClient, db: Session):
        """Test de changement de catégorie."""
        category1 = ProductCategoryFactory.create(db=db)
        category2 = ProductCategoryFactory.create(db=db)
        product = ProductFactory.create(db=db, category=category1)

        update_data = {"category_id": str(category2.id)}
        response = client.put(f"/api/v1/products/{product.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["category_id"] == str(category2.id)

    def test_update_product_not_found(self, client: TestClient, db: Session):
        """Test qu'un produit inexistant retourne 404."""
        from uuid import uuid4

        update_data = {"name": "New Name"}
        response = client.put(f"/api/v1/products/{uuid4()}", json=update_data)

        assert response.status_code == 404

    def test_update_product_with_nonexistent_category_fails(
        self, client: TestClient, db: Session
    ):
        """Test qu'une catégorie inexistante retourne une erreur."""
        from uuid import uuid4

        product = ProductFactory.create(db=db)

        update_data = {"category_id": str(uuid4())}
        response = client.put(f"/api/v1/products/{product.id}", json=update_data)

        assert response.status_code == 400


class TestProductDelete:
    """Tests pour DELETE /api/v1/products/{id}"""

    def test_delete_product_success(self, client: TestClient, db: Session):
        """Test de suppression d'un produit."""
        product = ProductFactory.create(db=db, name="To Delete")
        product_id = product.id

        response = client.delete(f"/api/v1/products/{product_id}")

        assert response.status_code == 204

        # Vérifier que le produit est bien supprimé
        get_response = client.get(f"/api/v1/products/{product_id}")
        assert get_response.status_code == 404

    def test_delete_product_not_found(self, client: TestClient, db: Session):
        """Test qu'un produit inexistant retourne 404."""
        from uuid import uuid4

        response = client.delete(f"/api/v1/products/{uuid4()}")

        assert response.status_code == 404
