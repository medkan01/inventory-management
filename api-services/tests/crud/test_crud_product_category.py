"""
Tests pour les opérations CRUD de ProductCategory.
Teste la couche d'accès aux données sans la logique métier.
"""

import pytest
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud import product_category as crud_product_category
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryUpdate
from tests.fixtures.factories import ProductCategoryFactory


class TestProductCategoryCRUDCreate:
    """Tests pour la création de catégories."""

    def test_create_category(self, db: Session):
        """Test de création d'une catégorie via CRUD."""
        category_in = ProductCategoryCreate(
            name="Electronics",
            slug="electronics",
            description="Electronic devices and accessories",
        )

        category = crud_product_category.create(db=db, obj_in=category_in)

        assert category.id is not None
        assert isinstance(category.id, UUID)
        assert category.name == "Electronics"
        assert category.slug == "electronics"
        assert category.description == "Electronic devices and accessories"
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_create_category_without_description(self, db: Session):
        """Test de création d'une catégorie sans description."""
        category_in = ProductCategoryCreate(
            name="Books",
            slug="books",
        )

        category = crud_product_category.create(db=db, obj_in=category_in)

        assert category.id is not None
        assert category.name == "Books"
        assert category.slug == "books"
        assert category.description is None

    def test_create_category_with_duplicate_name_fails(self, db: Session):
        """Test que la création d'une catégorie avec un nom dupliqué échoue."""
        # Créer la première catégorie
        ProductCategoryFactory.create(db=db, name="Electronics", slug="electronics")

        # Essayer de créer une catégorie avec le même nom
        category_in = ProductCategoryCreate(
            name="Electronics",
            slug="electronics-2",
        )

        with pytest.raises(Exception):  # IntegrityError de SQLAlchemy
            crud_product_category.create(db=db, obj_in=category_in)

    def test_create_category_with_duplicate_slug_fails(self, db: Session):
        """Test que la création d'une catégorie avec un slug dupliqué échoue."""
        # Créer la première catégorie
        ProductCategoryFactory.create(db=db, name="Electronics", slug="electronics")

        # Essayer de créer une catégorie avec le même slug
        category_in = ProductCategoryCreate(
            name="Electronics 2",
            slug="electronics",
        )

        with pytest.raises(Exception):  # IntegrityError de SQLAlchemy
            crud_product_category.create(db=db, obj_in=category_in)


class TestProductCategoryCRUDRead:
    """Tests pour la lecture de catégories."""

    def test_get_category_by_id(self, db: Session):
        """Test de récupération d'une catégorie par son ID."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(db=db, name="Electronics")

        # Récupérer par ID
        found_category = crud_product_category.get(db=db, id=category.id)

        assert found_category is not None
        assert found_category.id == category.id
        assert found_category.name == "Electronics"

    def test_get_category_by_nonexistent_id_returns_none(self, db: Session):
        """Test que la récupération d'une catégorie inexistante retourne None."""
        from uuid import uuid4

        nonexistent_id = uuid4()
        found_category = crud_product_category.get(db=db, id=nonexistent_id)

        assert found_category is None

    def test_get_category_by_name(self, db: Session):
        """Test de récupération d'une catégorie par son nom."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(db=db, name="Electronics")

        # Récupérer par nom
        found_category = crud_product_category.get_by_name(db=db, name="Electronics")

        assert found_category is not None
        assert found_category.id == category.id
        assert found_category.name == "Electronics"

    def test_get_category_by_nonexistent_name_returns_none(self, db: Session):
        """Test que la récupération par nom inexistant retourne None."""
        found_category = crud_product_category.get_by_name(db=db, name="NonExistent")

        assert found_category is None

    def test_get_category_by_slug(self, db: Session):
        """Test de récupération d'une catégorie par son slug."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics"
        )

        # Récupérer par slug
        found_category = crud_product_category.get_by_slug(db=db, slug="electronics")

        assert found_category is not None
        assert found_category.id == category.id
        assert found_category.slug == "electronics"

    def test_get_category_by_nonexistent_slug_returns_none(self, db: Session):
        """Test que la récupération par slug inexistant retourne None."""
        found_category = crud_product_category.get_by_slug(db=db, slug="nonexistent")

        assert found_category is None

    def test_get_multi_categories(self, db: Session):
        """Test de récupération de plusieurs catégories."""
        # Créer plusieurs catégories
        ProductCategoryFactory.create_batch(db=db, count=5)

        # Récupérer toutes les catégories
        categories = crud_product_category.get_multi(db=db, skip=0, limit=100)

        assert len(categories) == 5

    def test_get_multi_categories_with_pagination(self, db: Session):
        """Test de pagination lors de la récupération de catégories."""
        # Créer 10 catégories
        ProductCategoryFactory.create_batch(db=db, count=10)

        # Récupérer les 5 premières
        first_page = crud_product_category.get_multi(db=db, skip=0, limit=5)
        assert len(first_page) == 5

        # Récupérer les 5 suivantes
        second_page = crud_product_category.get_multi(db=db, skip=5, limit=5)
        assert len(second_page) == 5

        # Vérifier qu'il n'y a pas de chevauchement
        first_page_ids = [cat.id for cat in first_page]
        second_page_ids = [cat.id for cat in second_page]
        assert len(set(first_page_ids) & set(second_page_ids)) == 0

    def test_get_multi_empty_database(self, db: Session):
        """Test de récupération sur une base vide."""
        categories = crud_product_category.get_multi(db=db, skip=0, limit=100)

        assert categories == []


class TestProductCategoryCRUDUpdate:
    """Tests pour la mise à jour de catégories."""

    def test_update_category_name(self, db: Session):
        """Test de mise à jour du nom d'une catégorie."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics"
        )

        # Mettre à jour le nom
        category_update = ProductCategoryUpdate(name="Electronic Devices")
        updated_category = crud_product_category.update(
            db=db, db_obj=category, obj_in=category_update
        )

        assert updated_category.id == category.id
        assert updated_category.name == "Electronic Devices"
        assert updated_category.slug == "electronics"  # Le slug ne change pas

    def test_update_category_slug(self, db: Session):
        """Test de mise à jour du slug d'une catégorie."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics"
        )

        # Mettre à jour le slug
        category_update = ProductCategoryUpdate(slug="electronic-devices")
        updated_category = crud_product_category.update(
            db=db, db_obj=category, obj_in=category_update
        )

        assert updated_category.id == category.id
        assert updated_category.name == "Electronics"  # Le nom ne change pas
        assert updated_category.slug == "electronic-devices"

    def test_update_category_description(self, db: Session):
        """Test de mise à jour de la description d'une catégorie."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", description="Old description"
        )

        # Mettre à jour la description
        category_update = ProductCategoryUpdate(description="New description")
        updated_category = crud_product_category.update(
            db=db, db_obj=category, obj_in=category_update
        )

        assert updated_category.description == "New description"

    def test_update_category_multiple_fields(self, db: Session):
        """Test de mise à jour de plusieurs champs à la fois."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db, name="Electronics", slug="electronics", description="Old description"
        )

        # Mettre à jour plusieurs champs
        category_update = ProductCategoryUpdate(
            name="Electronic Devices",
            slug="electronic-devices",
            description="New description",
        )
        updated_category = crud_product_category.update(
            db=db, db_obj=category, obj_in=category_update
        )

        assert updated_category.name == "Electronic Devices"
        assert updated_category.slug == "electronic-devices"
        assert updated_category.description == "New description"

    def test_update_category_with_dict(self, db: Session):
        """Test de mise à jour avec un dictionnaire."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(db=db, name="Electronics")

        # Mettre à jour avec un dict
        update_data = {"name": "Updated Electronics"}
        updated_category = crud_product_category.update(
            db=db, db_obj=category, obj_in=update_data
        )

        assert updated_category.name == "Updated Electronics"

    def test_update_category_partial(self, db: Session):
        """Test de mise à jour partielle (seulement certains champs)."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db,
            name="Electronics",
            slug="electronics",
            description="Original description",
        )

        # Mettre à jour seulement le nom
        category_update = ProductCategoryUpdate(name="Electronic Devices")
        updated_category = crud_product_category.update(
            db=db, db_obj=category, obj_in=category_update
        )

        # Vérifier que seul le nom a changé
        assert updated_category.name == "Electronic Devices"
        assert updated_category.slug == "electronics"
        assert updated_category.description == "Original description"


class TestProductCategoryCRUDDelete:
    """Tests pour la suppression de catégories."""

    def test_delete_category(self, db: Session):
        """Test de suppression d'une catégorie."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(db=db, name="Electronics")
        category_id = category.id

        # Supprimer la catégorie
        deleted_category = crud_product_category.delete(db=db, id=category_id)

        assert deleted_category is not None
        assert deleted_category.id == category_id

        # Vérifier que la catégorie n'existe plus
        found_category = crud_product_category.get(db=db, id=category_id)
        assert found_category is None

    def test_delete_nonexistent_category_returns_none(self, db: Session):
        """Test que la suppression d'une catégorie inexistante retourne None."""
        from uuid import uuid4

        nonexistent_id = uuid4()
        deleted_category = crud_product_category.delete(db=db, id=nonexistent_id)

        assert deleted_category is None

    def test_delete_category_removes_from_database(self, db: Session):
        """Test que la suppression retire bien la catégorie de la base."""
        # Créer 3 catégories
        ProductCategoryFactory.create_batch(db=db, count=3)

        # Vérifier qu'il y a 3 catégories
        categories = crud_product_category.get_multi(db=db)
        assert len(categories) == 3

        # Supprimer une catégorie
        crud_product_category.delete(db=db, id=categories[0].id)

        # Vérifier qu'il n'en reste que 2
        remaining_categories = crud_product_category.get_multi(db=db)
        assert len(remaining_categories) == 2
