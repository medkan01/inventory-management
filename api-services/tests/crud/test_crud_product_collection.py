"""
Tests pour les opérations CRUD de ProductCollection.
Teste la couche d'accès aux données sans la logique métier.
"""

import pytest
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud import product_collection as crud_product_collection
from app.schemas.product_collection import (
    ProductCollectionCreate,
    ProductCollectionUpdate,
)
from tests.fixtures.factories import ProductCollectionFactory


class TestProductCollectionCRUDCreate:
    """Tests pour la création de collections."""

    def test_create_collection(self, db: Session):
        """Test de création d'une collection via CRUD."""
        collection_in = ProductCollectionCreate(
            name="Summer 2024",
            slug="summer-2024",
            description="Summer collection for 2024",
        )

        collection = crud_product_collection.create(db=db, obj_in=collection_in)

        assert collection.id is not None
        assert isinstance(collection.id, UUID)
        assert collection.name == "Summer 2024"
        assert collection.slug == "summer-2024"
        assert collection.description == "Summer collection for 2024"
        assert collection.created_at is not None
        assert collection.updated_at is not None

    def test_create_collection_without_description(self, db: Session):
        """Test de création d'une collection sans description."""
        collection_in = ProductCollectionCreate(
            name="Winter Sale",
            slug="winter-sale",
        )

        collection = crud_product_collection.create(db=db, obj_in=collection_in)

        assert collection.id is not None
        assert collection.name == "Winter Sale"
        assert collection.slug == "winter-sale"
        assert collection.description is None

    def test_create_collection_with_duplicate_name_fails(self, db: Session):
        """Test que la création d'une collection avec un nom dupliqué échoue."""
        ProductCollectionFactory.create(db=db, name="Summer 2024", slug="summer-2024")

        collection_in = ProductCollectionCreate(
            name="Summer 2024",
            slug="summer-2024-v2",
        )

        with pytest.raises(Exception):
            crud_product_collection.create(db=db, obj_in=collection_in)

    def test_create_collection_with_duplicate_slug_fails(self, db: Session):
        """Test que la création d'une collection avec un slug dupliqué échoue."""
        ProductCollectionFactory.create(db=db, name="Summer 2024", slug="summer-2024")

        collection_in = ProductCollectionCreate(
            name="Summer 2024 V2",
            slug="summer-2024",
        )

        with pytest.raises(Exception):
            crud_product_collection.create(db=db, obj_in=collection_in)


class TestProductCollectionCRUDRead:
    """Tests pour la lecture de collections."""

    def test_get_collection_by_id(self, db: Session):
        """Test de récupération d'une collection par son ID."""
        collection = ProductCollectionFactory.create(db=db, name="Summer 2024")

        found_collection = crud_product_collection.get(db=db, id=collection.id)

        assert found_collection is not None
        assert found_collection.id == collection.id
        assert found_collection.name == "Summer 2024"

    def test_get_collection_by_nonexistent_id_returns_none(self, db: Session):
        """Test que la récupération d'une collection inexistante retourne None."""
        from uuid import uuid4

        nonexistent_id = uuid4()
        found_collection = crud_product_collection.get(db=db, id=nonexistent_id)

        assert found_collection is None

    def test_get_collection_by_name(self, db: Session):
        """Test de récupération d'une collection par son nom."""
        collection = ProductCollectionFactory.create(db=db, name="Summer 2024")

        found_collection = crud_product_collection.get_by_name(
            db=db, name="Summer 2024"
        )

        assert found_collection is not None
        assert found_collection.id == collection.id
        assert found_collection.name == "Summer 2024"

    def test_get_collection_by_nonexistent_name_returns_none(self, db: Session):
        """Test que la récupération par nom inexistant retourne None."""
        found_collection = crud_product_collection.get_by_name(
            db=db, name="NonExistent"
        )

        assert found_collection is None

    def test_get_collection_by_slug(self, db: Session):
        """Test de récupération d'une collection par son slug."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer 2024", slug="summer-2024"
        )

        found_collection = crud_product_collection.get_by_slug(
            db=db, slug="summer-2024"
        )

        assert found_collection is not None
        assert found_collection.id == collection.id
        assert found_collection.slug == "summer-2024"

    def test_get_collection_by_nonexistent_slug_returns_none(self, db: Session):
        """Test que la récupération par slug inexistant retourne None."""
        found_collection = crud_product_collection.get_by_slug(
            db=db, slug="nonexistent"
        )

        assert found_collection is None

    def test_get_multi_collections(self, db: Session):
        """Test de récupération de plusieurs collections."""
        ProductCollectionFactory.create_batch(db=db, count=5)

        collections = crud_product_collection.get_multi(db=db, skip=0, limit=100)

        assert len(collections) == 5

    def test_get_multi_collections_with_pagination(self, db: Session):
        """Test de pagination lors de la récupération de collections."""
        ProductCollectionFactory.create_batch(db=db, count=10)

        first_page = crud_product_collection.get_multi(db=db, skip=0, limit=5)
        assert len(first_page) == 5

        second_page = crud_product_collection.get_multi(db=db, skip=5, limit=5)
        assert len(second_page) == 5

        first_page_ids = [col.id for col in first_page]
        second_page_ids = [col.id for col in second_page]
        assert len(set(first_page_ids) & set(second_page_ids)) == 0

    def test_get_multi_empty_database(self, db: Session):
        """Test de récupération sur une base vide."""
        collections = crud_product_collection.get_multi(db=db, skip=0, limit=100)

        assert collections == []


class TestProductCollectionCRUDUpdate:
    """Tests pour la mise à jour de collections."""

    def test_update_collection_name(self, db: Session):
        """Test de mise à jour du nom d'une collection."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer 2024", slug="summer-2024"
        )

        collection_update = ProductCollectionUpdate(name="Summer Collection 2024")
        updated_collection = crud_product_collection.update(
            db=db, db_obj=collection, obj_in=collection_update
        )

        assert updated_collection.id == collection.id
        assert updated_collection.name == "Summer Collection 2024"
        assert updated_collection.slug == "summer-2024"

    def test_update_collection_slug(self, db: Session):
        """Test de mise à jour du slug d'une collection."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer 2024", slug="summer-2024"
        )

        collection_update = ProductCollectionUpdate(slug="summer-collection-2024")
        updated_collection = crud_product_collection.update(
            db=db, db_obj=collection, obj_in=collection_update
        )

        assert updated_collection.id == collection.id
        assert updated_collection.name == "Summer 2024"
        assert updated_collection.slug == "summer-collection-2024"

    def test_update_collection_description(self, db: Session):
        """Test de mise à jour de la description d'une collection."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer 2024", description="Old description"
        )

        collection_update = ProductCollectionUpdate(description="New description")
        updated_collection = crud_product_collection.update(
            db=db, db_obj=collection, obj_in=collection_update
        )

        assert updated_collection.description == "New description"

    def test_update_collection_multiple_fields(self, db: Session):
        """Test de mise à jour de plusieurs champs à la fois."""
        collection = ProductCollectionFactory.create(
            db=db, name="Summer 2024", slug="summer-2024", description="Old description"
        )

        collection_update = ProductCollectionUpdate(
            name="Summer Sale 2024",
            slug="summer-sale-2024",
            description="New description",
        )
        updated_collection = crud_product_collection.update(
            db=db, db_obj=collection, obj_in=collection_update
        )

        assert updated_collection.name == "Summer Sale 2024"
        assert updated_collection.slug == "summer-sale-2024"
        assert updated_collection.description == "New description"

    def test_update_collection_with_dict(self, db: Session):
        """Test de mise à jour avec un dictionnaire."""
        collection = ProductCollectionFactory.create(db=db, name="Summer 2024")

        update_data = {"name": "Updated Summer 2024"}
        updated_collection = crud_product_collection.update(
            db=db, db_obj=collection, obj_in=update_data
        )

        assert updated_collection.name == "Updated Summer 2024"

    def test_update_collection_partial(self, db: Session):
        """Test de mise à jour partielle (seulement certains champs)."""
        collection = ProductCollectionFactory.create(
            db=db,
            name="Summer 2024",
            slug="summer-2024",
            description="Original description",
        )

        collection_update = ProductCollectionUpdate(name="Summer Sale 2024")
        updated_collection = crud_product_collection.update(
            db=db, db_obj=collection, obj_in=collection_update
        )

        assert updated_collection.name == "Summer Sale 2024"
        assert updated_collection.slug == "summer-2024"
        assert updated_collection.description == "Original description"


class TestProductCollectionCRUDDelete:
    """Tests pour la suppression de collections."""

    def test_delete_collection(self, db: Session):
        """Test de suppression d'une collection."""
        collection = ProductCollectionFactory.create(db=db, name="Summer 2024")
        collection_id = collection.id

        deleted_collection = crud_product_collection.delete(db=db, id=collection_id)

        assert deleted_collection is not None
        assert deleted_collection.id == collection_id

        found_collection = crud_product_collection.get(db=db, id=collection_id)
        assert found_collection is None

    def test_delete_nonexistent_collection_returns_none(self, db: Session):
        """Test que la suppression d'une collection inexistante retourne None."""
        from uuid import uuid4

        nonexistent_id = uuid4()
        deleted_collection = crud_product_collection.delete(db=db, id=nonexistent_id)

        assert deleted_collection is None

    def test_delete_collection_removes_from_database(self, db: Session):
        """Test que la suppression retire bien la collection de la base."""
        ProductCollectionFactory.create_batch(db=db, count=3)

        collections = crud_product_collection.get_multi(db=db)
        assert len(collections) == 3

        crud_product_collection.delete(db=db, id=collections[0].id)

        remaining_collections = crud_product_collection.get_multi(db=db)
        assert len(remaining_collections) == 2
