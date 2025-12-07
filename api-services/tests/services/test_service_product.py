"""
Tests pour le service Product.
Teste la logique métier et les validations.
"""

import pytest
from sqlalchemy.orm import Session
from uuid import uuid4

from app.services.product import product_service
from app.schemas.product import ProductCreate, ProductUpdate
from tests.fixtures.factories import (
    ProductFactory,
    ProductCategoryFactory,
    ProductCollectionFactory,
)


class TestProductServiceGetAll:
    """Tests pour la récupération de tous les produits."""

    def test_get_all_products_empty_database(self, db: Session):
        """Test de récupération quand la base est vide."""
        products = product_service.get_all_products(db)

        assert products == []

    def test_get_all_products(self, db: Session):
        """Test de récupération de tous les produits."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=5, category=category)

        products = product_service.get_all_products(db)

        assert len(products) == 5

    def test_get_all_products_with_pagination(self, db: Session):
        """Test de pagination."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=10, category=category)

        first_page = product_service.get_all_products(db, skip=0, limit=5)
        second_page = product_service.get_all_products(db, skip=5, limit=5)

        assert len(first_page) == 5
        assert len(second_page) == 5


class TestProductServiceGetById:
    """Tests pour la récupération d'un produit par ID."""

    def test_get_product_by_id_found(self, db: Session):
        """Test de récupération d'un produit existant."""
        product = ProductFactory.create(db=db, name="Test Product")

        found = product_service.get_product_by_id(db, product.id)

        assert found is not None
        assert found.id == product.id
        assert found.name == "Test Product"

    def test_get_product_by_id_not_found(self, db: Session):
        """Test de récupération d'un produit inexistant."""
        nonexistent_id = uuid4()
        found = product_service.get_product_by_id(db, nonexistent_id)

        assert found is None


class TestProductServiceGetByCategory:
    """Tests pour la récupération de produits par catégorie."""

    def test_get_products_by_category_id(self, db: Session):
        """Test de récupération par ID de catégorie."""
        category1 = ProductCategoryFactory.create(db=db, name="Category 1")
        category2 = ProductCategoryFactory.create(db=db, name="Category 2")
        ProductFactory.create_batch(db=db, count=3, category=category1)
        ProductFactory.create_batch(db=db, count=2, category=category2)

        products = product_service.get_products_by_category_id(db, category1.id)

        assert len(products) == 3
        assert all(p.category_id == category1.id for p in products)

    def test_get_products_by_category_slug(self, db: Session):
        """Test de récupération par slug de catégorie."""
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics"
        )
        ProductFactory.create_batch(db=db, count=4, category=category)

        products = product_service.get_products_by_category_slug(db, "electronics")

        assert len(products) == 4
        assert all(p.category.slug == "electronics" for p in products)

    def test_get_products_by_category_with_pagination(self, db: Session):
        """Test de pagination par catégorie."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=10, category=category)

        first_page = product_service.get_products_by_category_id(
            db, category.id, skip=0, limit=5
        )
        second_page = product_service.get_products_by_category_id(
            db, category.id, skip=5, limit=5
        )

        assert len(first_page) == 5
        assert len(second_page) == 5


class TestProductServiceGetByCollection:
    """Tests pour la récupération de produits par collection."""

    def test_get_products_by_collection_id(self, db: Session):
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

        products = product_service.get_products_by_collection_id(db, collection1.id)

        assert len(products) == 3
        assert all(p.collection_id == collection1.id for p in products)

    def test_get_products_by_collection_slug(self, db: Session):
        """Test de récupération par slug de collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(
            db=db, name="Summer Sale", slug="summer-sale"
        )
        ProductFactory.create_batch(
            db=db, count=4, category=category, collection=collection
        )

        products = product_service.get_products_by_collection_slug(db, "summer-sale")

        assert len(products) == 4
        assert all(p.collection.slug == "summer-sale" for p in products)


class TestProductServiceCreate:
    """Tests pour la création de produits."""

    def test_create_product_success(self, db: Session):
        """Test de création d'un produit valide."""
        category = ProductCategoryFactory.create(db=db)

        product_in = ProductCreate(
            name="Laptop Dell XPS 13",
            slug="laptop-dell-xps-13",
            description="High-performance laptop",
            category_id=category.id,
        )

        product = product_service.create_product(db, product_in)

        assert product.id is not None
        assert product.name == "Laptop Dell XPS 13"
        assert product.category_id == category.id

    def test_create_product_with_collection(self, db: Session):
        """Test de création avec une collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db)

        product_in = ProductCreate(
            name="Product",
            slug="product-with-collection",
            category_id=category.id,
            collection_id=collection.id,
        )

        product = product_service.create_product(db, product_in)

        assert product.collection_id == collection.id

    def test_create_product_with_nonexistent_category_raises_error(self, db: Session):
        """Test qu'une catégorie inexistante lève une erreur."""
        nonexistent_id = uuid4()

        product_in = ProductCreate(
            name="Product", slug="test-product", category_id=nonexistent_id
        )

        with pytest.raises(ValueError, match="Category with ID .* does not exist"):
            product_service.create_product(db, product_in)

    def test_create_product_with_nonexistent_collection_raises_error(self, db: Session):
        """Test qu'une collection inexistante lève une erreur."""
        category = ProductCategoryFactory.create(db=db)
        nonexistent_id = uuid4()

        product_in = ProductCreate(
            name="Product",
            slug="test-product-collection",
            category_id=category.id,
            collection_id=nonexistent_id,
        )

        with pytest.raises(ValueError, match="Collection with ID .* does not exist"):
            product_service.create_product(db, product_in)


class TestProductServiceUpdate:
    """Tests pour la mise à jour de produits."""

    def test_update_product_name(self, db: Session):
        """Test de mise à jour du nom."""
        product = ProductFactory.create(db=db, name="Old Name")

        product_in = ProductUpdate(name="New Name")
        updated = product_service.update_product(db, product.id, product_in)

        assert updated.name == "New Name"

    def test_update_product_category(self, db: Session):
        """Test de changement de catégorie."""
        category1 = ProductCategoryFactory.create(db=db)
        category2 = ProductCategoryFactory.create(db=db)
        product = ProductFactory.create(db=db, category=category1)

        product_in = ProductUpdate(category_id=category2.id)
        updated = product_service.update_product(db, product.id, product_in)

        assert updated.category_id == category2.id

    def test_update_product_add_collection(self, db: Session):
        """Test d'ajout d'une collection."""
        product = ProductFactory.create(db=db, collection=None)
        collection = ProductCollectionFactory.create(db=db)

        product_in = ProductUpdate(collection_id=collection.id)
        updated = product_service.update_product(db, product.id, product_in)

        assert updated.collection_id == collection.id

    def test_update_product_not_found_raises_error(self, db: Session):
        """Test qu'un produit inexistant lève une erreur."""
        nonexistent_id = uuid4()
        product_in = ProductUpdate(name="Test")

        with pytest.raises(ValueError, match="Product with ID .* not found"):
            product_service.update_product(db, nonexistent_id, product_in)

    def test_update_product_with_nonexistent_category_raises_error(self, db: Session):
        """Test qu'une catégorie inexistante lève une erreur."""
        product = ProductFactory.create(db=db)
        nonexistent_id = uuid4()

        product_in = ProductUpdate(category_id=nonexistent_id)

        with pytest.raises(ValueError, match="Category with ID .* does not exist"):
            product_service.update_product(db, product.id, product_in)

    def test_update_product_with_nonexistent_collection_raises_error(self, db: Session):
        """Test qu'une collection inexistante lève une erreur."""
        product = ProductFactory.create(db=db)
        nonexistent_id = uuid4()

        product_in = ProductUpdate(collection_id=nonexistent_id)

        with pytest.raises(ValueError, match="Collection with ID .* does not exist"):
            product_service.update_product(db, product.id, product_in)


class TestProductServiceDelete:
    """Tests pour la suppression de produits."""

    def test_delete_product_success(self, db: Session):
        """Test de suppression d'un produit existant."""
        product = ProductFactory.create(db=db, name="To Delete")
        product_id = product.id

        product_service.delete_product(db, product_id)

        found = product_service.get_product_by_id(db, product_id)
        assert found is None

    def test_delete_product_not_found_raises_error(self, db: Session):
        """Test qu'un produit inexistant lève une erreur."""
        nonexistent_id = uuid4()

        with pytest.raises(ValueError, match="Product with ID .* not found"):
            product_service.delete_product(db, nonexistent_id)
