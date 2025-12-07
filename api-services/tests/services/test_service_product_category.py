"""
Tests pour le service ProductCategory.
Teste la logique métier et les validations.
"""

import pytest
from sqlalchemy.orm import Session

from app.services.product_category import product_category_service
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryUpdate
from tests.fixtures.factories import ProductCategoryFactory


class TestProductCategoryServiceGetAll:
    """Tests pour la récupération de toutes les catégories."""
    
    def test_get_all_categories_empty_database(self, db: Session):
        """Test de récupération quand la base est vide."""
        categories = product_category_service.get_all_categories(db)
        
        assert categories == []
    
    def test_get_all_categories(self, db: Session):
        """Test de récupération de toutes les catégories."""
        ProductCategoryFactory.create_batch(db=db, count=5)
        
        categories = product_category_service.get_all_categories(db)
        
        assert len(categories) == 5
    
    def test_get_all_categories_with_pagination(self, db: Session):
        """Test de pagination."""
        ProductCategoryFactory.create_batch(db=db, count=10)
        
        first_page = product_category_service.get_all_categories(db, skip=0, limit=5)
        second_page = product_category_service.get_all_categories(db, skip=5, limit=5)
        
        assert len(first_page) == 5
        assert len(second_page) == 5
        
        first_ids = [c.id for c in first_page]
        second_ids = [c.id for c in second_page]
        assert len(set(first_ids) & set(second_ids)) == 0


class TestProductCategoryServiceGetBySlug:
    """Tests pour la récupération d'une catégorie par son slug."""
    
    def test_get_category_by_slug_found(self, db: Session):
        """Test de récupération d'une catégorie existante."""
        category = ProductCategoryFactory.create(db=db, name="Electronics", slug="electronics")
        
        found = product_category_service.get_category_by_slug(db, "electronics")
        
        assert found is not None
        assert found.id == category.id
        assert found.slug == "electronics"
    
    def test_get_category_by_slug_not_found(self, db: Session):
        """Test de récupération d'une catégorie inexistante."""
        found = product_category_service.get_category_by_slug(db, "nonexistent")
        
        assert found is None


class TestProductCategoryServiceCreate:
    """Tests pour la création de catégories."""
    
    def test_create_category_success(self, db: Session):
        """Test de création d'une catégorie valide."""
        category_in = ProductCategoryCreate(
            name="Electronics",
            slug="electronics",
            description="Electronic devices"
        )
        
        category = product_category_service.create_category(db, category_in)
        
        assert category.id is not None
        assert category.name == "Electronics"
        assert category.slug == "electronics"
        assert category.description == "Electronic devices"
    
    def test_create_category_duplicate_slug_raises_error(self, db: Session):
        """Test qu'un slug dupliqué lève une erreur."""
        ProductCategoryFactory.create(db=db, slug="electronics")
        
        category_in = ProductCategoryCreate(
            name="New Category",
            slug="electronics",
            description="Test"
        )
        
        with pytest.raises(ValueError, match="slug 'electronics' already exists"):
            product_category_service.create_category(db, category_in)
    
    def test_create_category_duplicate_name_raises_error(self, db: Session):
        """Test qu'un nom dupliqué lève une erreur."""
        ProductCategoryFactory.create(db=db, name="Electronics")
        
        category_in = ProductCategoryCreate(
            name="Electronics",
            slug="electronics-new",
            description="Test"
        )
        
        with pytest.raises(ValueError, match="name 'Electronics' already exists"):
            product_category_service.create_category(db, category_in)
    
    def test_create_category_without_description(self, db: Session):
        """Test de création sans description."""
        category_in = ProductCategoryCreate(
            name="Books",
            slug="books"
        )
        
        category = product_category_service.create_category(db, category_in)
        
        assert category.name == "Books"
        assert category.description is None


class TestProductCategoryServiceUpdate:
    """Tests pour la mise à jour de catégories."""
    
    def test_update_category_name(self, db: Session):
        """Test de mise à jour du nom."""
        category = ProductCategoryFactory.create(db=db, name="Old Name", slug="old-name")
        
        category_in = ProductCategoryUpdate(name="New Name")
        updated = product_category_service.update_category(db, "old-name", category_in)
        
        assert updated.name == "New Name"
        assert updated.slug == "old-name"
    
    def test_update_category_slug(self, db: Session):
        """Test de mise à jour du slug."""
        category = ProductCategoryFactory.create(db=db, name="Category", slug="old-slug")
        
        category_in = ProductCategoryUpdate(slug="new-slug")
        updated = product_category_service.update_category(db, "old-slug", category_in)
        
        assert updated.slug == "new-slug"
        assert updated.name == "Category"
    
    def test_update_category_description(self, db: Session):
        """Test de mise à jour de la description."""
        category = ProductCategoryFactory.create(db=db, slug="test")
        
        category_in = ProductCategoryUpdate(description="New description")
        updated = product_category_service.update_category(db, "test", category_in)
        
        assert updated.description == "New description"
    
    def test_update_category_not_found_raises_error(self, db: Session):
        """Test qu'une catégorie inexistante lève une erreur."""
        category_in = ProductCategoryUpdate(name="Test")
        
        with pytest.raises(ValueError, match="Category with slug 'nonexistent' not found"):
            product_category_service.update_category(db, "nonexistent", category_in)
    
    def test_update_category_duplicate_slug_raises_error(self, db: Session):
        """Test qu'un slug dupliqué lors de l'update lève une erreur."""
        ProductCategoryFactory.create(db=db, slug="existing-slug")
        category = ProductCategoryFactory.create(db=db, slug="my-slug")
        
        category_in = ProductCategoryUpdate(slug="existing-slug")
        
        with pytest.raises(ValueError, match="slug 'existing-slug' already exists"):
            product_category_service.update_category(db, "my-slug", category_in)
    
    def test_update_category_duplicate_name_raises_error(self, db: Session):
        """Test qu'un nom dupliqué lors de l'update lève une erreur."""
        ProductCategoryFactory.create(db=db, name="Existing Name", slug="existing")
        category = ProductCategoryFactory.create(db=db, name="My Name", slug="my-slug")
        
        category_in = ProductCategoryUpdate(name="Existing Name")
        
        with pytest.raises(ValueError, match="name 'Existing Name' already exists"):
            product_category_service.update_category(db, "my-slug", category_in)
    
    def test_update_category_same_slug_allowed(self, db: Session):
        """Test qu'on peut garder le même slug lors de l'update."""
        category = ProductCategoryFactory.create(db=db, name="Old", slug="my-slug")
        
        category_in = ProductCategoryUpdate(name="New", slug="my-slug")
        updated = product_category_service.update_category(db, "my-slug", category_in)
        
        assert updated.name == "New"
        assert updated.slug == "my-slug"
    
    def test_update_category_same_name_allowed(self, db: Session):
        """Test qu'on peut garder le même nom lors de l'update."""
        category = ProductCategoryFactory.create(db=db, name="My Name", slug="old")
        
        category_in = ProductCategoryUpdate(name="My Name", slug="new")
        updated = product_category_service.update_category(db, "old", category_in)
        
        assert updated.name == "My Name"
        assert updated.slug == "new"


class TestProductCategoryServiceDelete:
    """Tests pour la suppression de catégories."""
    
    def test_delete_category_success(self, db: Session):
        """Test de suppression d'une catégorie existante."""
        category = ProductCategoryFactory.create(db=db, slug="to-delete")
        
        product_category_service.delete_category(db, "to-delete")
        
        found = product_category_service.get_category_by_slug(db, "to-delete")
        assert found is None
    
    def test_delete_category_not_found_raises_error(self, db: Session):
        """Test qu'une catégorie inexistante lève une erreur."""
        with pytest.raises(ValueError, match="Category with slug 'nonexistent' not found"):
            product_category_service.delete_category(db, "nonexistent")
