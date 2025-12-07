"""
Tests pour le service ProductCollection.
Teste la logique métier et les validations.
"""

import pytest
from sqlalchemy.orm import Session

from app.services.product_collection import product_collection_service
from app.schemas.product_collection import (
    ProductCollectionCreate,
    ProductCollectionUpdate,
)
from tests.fixtures.factories import ProductCollectionFactory


class TestProductCollectionServiceGetAll:
    """Tests pour la récupération de toutes les collections."""

    def test_get_all_collections_empty_database(self, db: Session):
        """Test de récupération quand la base est vide."""
        collections = product_collection_service.get_all_collections(db)

        assert collections == []

    def test_get_all_collections(self, db: Session):
        """Test de récupération de toutes les collections."""
        ProductCollectionFactory.create_batch(db=db, count=5)

        collections = product_collection_service.get_all_collections(db)

        assert len(collections) == 5

    def test_get_all_collections_with_pagination(self, db: Session):
        """Test de pagination."""
        ProductCollectionFactory.create_batch(db=db, count=10)

        first_page = product_collection_service.get_all_collections(db, skip=0, limit=5)
        second_page = product_collection_service.get_all_collections(
            db, skip=5, limit=5
        )

        assert len(first_page) == 5
        assert len(second_page) == 5

        first_ids = [c.id for c in first_page]
        second_ids = [c.id for c in second_page]
        assert len(set(first_ids) & set(second_ids)) == 0


class TestProductCollectionServiceGetBySlug:
    """Tests pour la récupération d'une collection par son slug."""

    def test_get_collection_by_slug_found(self, db: Session):
        """Test de récupération d'une collection existante."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer Sale", slug="summer-sale"
        )

        found = product_collection_service.get_collection_by_slug(db, "summer-sale")

        assert found is not None
        assert found.id == collection.id
        assert found.slug == "summer-sale"

    def test_get_collection_by_slug_not_found(self, db: Session):
        """Test de récupération d'une collection inexistante."""
        found = product_collection_service.get_collection_by_slug(db, "nonexistent")

        assert found is None


class TestProductCollectionServiceCreate:
    """Tests pour la création de collections."""

    def test_create_collection_success(self, db: Session):
        """Test de création d'une collection valide."""
        collection_in = ProductCollectionCreate(
            name="Summer Sale", slug="summer-sale", description="Summer products"
        )

        collection = product_collection_service.create_collection(db, collection_in)

        assert collection.id is not None
        assert collection.name == "Summer Sale"
        assert collection.slug == "summer-sale"
        assert collection.description == "Summer products"

    def test_create_collection_duplicate_slug_raises_error(self, db: Session):
        """Test qu'un slug dupliqué lève une erreur."""
        ProductCollectionFactory.create(db=db, slug="summer-sale")

        collection_in = ProductCollectionCreate(
            name="New Collection", slug="summer-sale", description="Test"
        )

        with pytest.raises(ValueError, match="slug 'summer-sale' already exists"):
            product_collection_service.create_collection(db, collection_in)

    def test_create_collection_duplicate_name_raises_error(self, db: Session):
        """Test qu'un nom dupliqué lève une erreur."""
        ProductCollectionFactory.create(db=db, name="Summer Sale")

        collection_in = ProductCollectionCreate(
            name="Summer Sale", slug="summer-sale-new", description="Test"
        )

        with pytest.raises(ValueError, match="name 'Summer Sale' already exists"):
            product_collection_service.create_collection(db, collection_in)

    def test_create_collection_without_description(self, db: Session):
        """Test de création sans description."""
        collection_in = ProductCollectionCreate(name="Winter Sale", slug="winter-sale")

        collection = product_collection_service.create_collection(db, collection_in)

        assert collection.name == "Winter Sale"
        assert collection.description is None


class TestProductCollectionServiceUpdate:
    """Tests pour la mise à jour de collections."""

    def test_update_collection_name(self, db: Session):
        """Test de mise à jour du nom."""
        ProductCollectionFactory.create(
            db=db, name="Old Name", slug="old-name"
        )

        collection_in = ProductCollectionUpdate(name="New Name")
        updated = product_collection_service.update_collection(
            db, "old-name", collection_in
        )

        assert updated.name == "New Name"
        assert updated.slug == "old-name"

    def test_update_collection_slug(self, db: Session):
        """Test de mise à jour du slug."""
        ProductCollectionFactory.create(
            db=db, name="Collection", slug="old-slug"
        )

        collection_in = ProductCollectionUpdate(slug="new-slug")
        updated = product_collection_service.update_collection(
            db, "old-slug", collection_in
        )

        assert updated.slug == "new-slug"
        assert updated.name == "Collection"

    def test_update_collection_description(self, db: Session):
        """Test de mise à jour de la description."""
        ProductCollectionFactory.create(db=db, slug="test")

        collection_in = ProductCollectionUpdate(description="New description")
        updated = product_collection_service.update_collection(
            db, "test", collection_in
        )

        assert updated.description == "New description"

    def test_update_collection_not_found_raises_error(self, db: Session):
        """Test qu'une collection inexistante lève une erreur."""
        collection_in = ProductCollectionUpdate(name="Test")

        with pytest.raises(
            ValueError, match="Collection with slug 'nonexistent' not found"
        ):
            product_collection_service.update_collection(
                db, "nonexistent", collection_in
            )

    def test_update_collection_duplicate_slug_raises_error(self, db: Session):
        """Test qu'un slug dupliqué lors de l'update lève une erreur."""
        ProductCollectionFactory.create(db=db, slug="existing-slug")
        ProductCollectionFactory.create(db=db, slug="my-slug")

        collection_in = ProductCollectionUpdate(slug="existing-slug")

        with pytest.raises(ValueError, match="slug 'existing-slug' already exists"):
            product_collection_service.update_collection(db, "my-slug", collection_in)

    def test_update_collection_duplicate_name_raises_error(self, db: Session):
        """Test qu'un nom dupliqué lors de l'update lève une erreur."""
        ProductCollectionFactory.create(db=db, name="Existing Name", slug="existing")
        ProductCollectionFactory.create(
            db=db, name="My Name", slug="my-slug"
        )

        collection_in = ProductCollectionUpdate(name="Existing Name")

        with pytest.raises(ValueError, match="name 'Existing Name' already exists"):
            product_collection_service.update_collection(db, "my-slug", collection_in)

    def test_update_collection_same_slug_allowed(self, db: Session):
        """Test qu'on peut garder le même slug lors de l'update."""
        ProductCollectionFactory.create(db=db, name="Old", slug="my-slug")

        collection_in = ProductCollectionUpdate(name="New", slug="my-slug")
        updated = product_collection_service.update_collection(
            db, "my-slug", collection_in
        )

        assert updated.name == "New"
        assert updated.slug == "my-slug"

    def test_update_collection_same_name_allowed(self, db: Session):
        """Test qu'on peut garder le même nom lors de l'update."""
        ProductCollectionFactory.create(db=db, name="My Name", slug="old")

        collection_in = ProductCollectionUpdate(name="My Name", slug="new")
        updated = product_collection_service.update_collection(db, "old", collection_in)

        assert updated.name == "My Name"
        assert updated.slug == "new"


class TestProductCollectionServiceDelete:
    """Tests pour la suppression de collections."""

    def test_delete_collection_success(self, db: Session):
        """Test de suppression d'une collection existante."""
        ProductCollectionFactory.create(db=db, slug="to-delete")

        product_collection_service.delete_collection(db, "to-delete")

        found = product_collection_service.get_collection_by_slug(db, "to-delete")
        assert found is None

    def test_delete_collection_not_found_raises_error(self, db: Session):
        """Test qu'une collection inexistante lève une erreur."""
        with pytest.raises(
            ValueError, match="Collection with slug 'nonexistent' not found"
        ):
            product_collection_service.delete_collection(db, "nonexistent")
