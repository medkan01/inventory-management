"""
Tests pour les opérations CRUD de Product.
Teste la couche d'accès aux données avec relations vers Category et Collection.
"""

import pytest
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud import product as crud_product
from app.schemas.product import ProductCreate, ProductUpdate
from tests.fixtures.factories import ProductFactory, ProductCategoryFactory, ProductCollectionFactory


class TestProductCRUDCreate:
    """Tests pour la création de produits."""
    
    def test_create_product_with_category(self, db: Session):
        """Test de création d'un produit avec une catégorie."""
        category = ProductCategoryFactory.create(db=db, name="Electronics")
        
        product_in = ProductCreate(
            name="Laptop Dell XPS 13",
            slug="laptop-dell-xps-13",
            description="High-performance laptop",
            category_id=category.id,
            collection_id=None
        )
        
        product = crud_product.create(db=db, obj_in=product_in)
        
        assert product.id is not None
        assert isinstance(product.id, UUID)
        assert product.name == "Laptop Dell XPS 13"
        assert product.description == "High-performance laptop"
        assert product.category_id == category.id
        assert product.collection_id is None
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_create_product_with_category_and_collection(self, db: Session):
        """Test de création d'un produit avec catégorie et collection."""
        category = ProductCategoryFactory.create(db=db, name="Electronics")
        collection = ProductCollectionFactory.create(db=db, name="Summer Sale")
        
        product_in = ProductCreate(
            name="Laptop Dell XPS 13",
            slug="laptop-dell-xps-13-summer",
            description="High-performance laptop",
            category_id=category.id,
            collection_id=collection.id
        )
        
        product = crud_product.create(db=db, obj_in=product_in)
        
        assert product.id is not None
        assert product.category_id == category.id
        assert product.collection_id == collection.id
    
    def test_create_product_without_description(self, db: Session):
        """Test de création d'un produit sans description."""
        category = ProductCategoryFactory.create(db=db)
        
        product_in = ProductCreate(
            name="Simple Product",
            slug="simple-product",
            category_id=category.id,
        )
        
        product = crud_product.create(db=db, obj_in=product_in)
        
        assert product.name == "Simple Product"
        assert product.description is None


class TestProductCRUDRead:
    """Tests pour la lecture de produits."""
    
    def test_get_product_by_id(self, db: Session):
        """Test de récupération d'un produit par son ID."""
        product = ProductFactory.create(db=db, name="Test Product")
        
        found_product = crud_product.get(db=db, id=product.id)
        
        assert found_product is not None
        assert found_product.id == product.id
        assert found_product.name == "Test Product"
    
    def test_get_product_by_nonexistent_id_returns_none(self, db: Session):
        """Test que la récupération d'un produit inexistant retourne None."""
        from uuid import uuid4
        
        nonexistent_id = uuid4()
        found_product = crud_product.get(db=db, id=nonexistent_id)
        
        assert found_product is None
    
    def test_get_product_by_name(self, db: Session):
        """Test de récupération d'un produit par son nom."""
        product = ProductFactory.create(db=db, name="Unique Product Name")
        
        found_product = crud_product.get_by_name(db=db, name="Unique Product Name")
        
        assert found_product is not None
        assert found_product.id == product.id
        assert found_product.name == "Unique Product Name"
    
    def test_get_product_by_nonexistent_name_returns_none(self, db: Session):
        """Test que la récupération par nom inexistant retourne None."""
        found_product = crud_product.get_by_name(db=db, name="NonExistent")
        
        assert found_product is None
    
    def test_get_multi_products(self, db: Session):
        """Test de récupération de plusieurs produits."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=5, category=category)
        
        products = crud_product.get_multi(db=db, skip=0, limit=100)
        
        assert len(products) == 5
    
    def test_get_multi_products_with_pagination(self, db: Session):
        """Test de pagination lors de la récupération de produits."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=10, category=category)
        
        first_page = crud_product.get_multi(db=db, skip=0, limit=5)
        assert len(first_page) == 5
        
        second_page = crud_product.get_multi(db=db, skip=5, limit=5)
        assert len(second_page) == 5
        
        first_page_ids = [p.id for p in first_page]
        second_page_ids = [p.id for p in second_page]
        assert len(set(first_page_ids) & set(second_page_ids)) == 0
    
    def test_get_products_by_category_id(self, db: Session):
        """Test de récupération de produits par category_id."""
        category1 = ProductCategoryFactory.create(db=db, name="Electronics")
        category2 = ProductCategoryFactory.create(db=db, name="Books")
        
        ProductFactory.create_batch(db=db, count=3, category=category1)
        ProductFactory.create_batch(db=db, count=2, category=category2)
        
        electronics = crud_product.get_by_category_id(db=db, category_id=category1.id)
        
        assert len(electronics) == 3
        assert all(p.category_id == category1.id for p in electronics)
    
    def test_get_products_by_collection_id(self, db: Session):
        """Test de récupération de produits par collection_id."""
        category = ProductCategoryFactory.create(db=db)
        collection1 = ProductCollectionFactory.create(db=db, name="Summer Sale")
        collection2 = ProductCollectionFactory.create(db=db, name="Winter Sale")
        
        ProductFactory.create_batch(db=db, count=3, category=category, collection=collection1)
        ProductFactory.create_batch(db=db, count=2, category=category, collection=collection2)
        
        summer_products = crud_product.get_by_collection_id(db=db, collection_id=collection1.id)
        
        assert len(summer_products) == 3
        assert all(p.collection_id == collection1.id for p in summer_products)
    
    def test_get_products_by_category_slug(self, db: Session):
        """Test de récupération de produits par slug de catégorie."""
        category = ProductCategoryFactory.create(db=db, name="Electronics", slug="electronics")
        ProductFactory.create_batch(db=db, count=4, category=category)
        
        products = crud_product.get_by_category_slug(db=db, category_slug="electronics")
        
        assert len(products) == 4
        assert all(p.category.slug == "electronics" for p in products)
    
    def test_get_products_by_collection_slug(self, db: Session):
        """Test de récupération de produits par slug de collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db, name="Summer Sale", slug="summer-sale")
        ProductFactory.create_batch(db=db, count=3, category=category, collection=collection)
        
        products = crud_product.get_by_collection_slug(db=db, collection_slug="summer-sale")
        
        assert len(products) == 3
        assert all(p.collection.slug == "summer-sale" for p in products)
    
    def test_get_products_with_pagination_by_category(self, db: Session):
        """Test de pagination lors de la récupération par catégorie."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=10, category=category)
        
        first_page = crud_product.get_by_category_id(db=db, category_id=category.id, skip=0, limit=5)
        second_page = crud_product.get_by_category_id(db=db, category_id=category.id, skip=5, limit=5)
        
        assert len(first_page) == 5
        assert len(second_page) == 5
    
    def test_get_empty_database(self, db: Session):
        """Test de récupération sur une base vide."""
        products = crud_product.get_multi(db=db, skip=0, limit=100)
        
        assert products == []


class TestProductCRUDUpdate:
    """Tests pour la mise à jour de produits."""
    
    def test_update_product_name(self, db: Session):
        """Test de mise à jour du nom d'un produit."""
        product = ProductFactory.create(db=db, name="Old Name")
        
        product_update = ProductUpdate(name="New Name")
        updated_product = crud_product.update(
            db=db,
            db_obj=product,
            obj_in=product_update
        )
        
        assert updated_product.id == product.id
        assert updated_product.name == "New Name"
    
    def test_update_product_description(self, db: Session):
        """Test de mise à jour de la description d'un produit."""
        product = ProductFactory.create(db=db, description="Old description")
        
        product_update = ProductUpdate(description="New description")
        updated_product = crud_product.update(
            db=db,
            db_obj=product,
            obj_in=product_update
        )
        
        assert updated_product.description == "New description"
    
    def test_update_product_category(self, db: Session):
        """Test de changement de catégorie d'un produit."""
        category1 = ProductCategoryFactory.create(db=db, name="Category 1")
        category2 = ProductCategoryFactory.create(db=db, name="Category 2")
        product = ProductFactory.create(db=db, category=category1)
        
        product_update = ProductUpdate(category_id=category2.id)
        updated_product = crud_product.update(
            db=db,
            db_obj=product,
            obj_in=product_update
        )
        
        assert updated_product.category_id == category2.id
    
    def test_update_product_collection(self, db: Session):
        """Test d'ajout/changement de collection d'un produit."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db, name="New Collection")
        product = ProductFactory.create(db=db, category=category, collection=None)
        
        product_update = ProductUpdate(collection_id=collection.id)
        updated_product = crud_product.update(
            db=db,
            db_obj=product,
            obj_in=product_update
        )
        
        assert updated_product.collection_id == collection.id
    
    def test_update_product_multiple_fields(self, db: Session):
        """Test de mise à jour de plusieurs champs à la fois."""
        category = ProductCategoryFactory.create(db=db)
        new_category = ProductCategoryFactory.create(db=db, name="New Category")
        product = ProductFactory.create(
            db=db,
            name="Old Name",
            description="Old description",
            category=category
        )
        
        product_update = ProductUpdate(
            name="New Name",
            description="New description",
            category_id=new_category.id
        )
        updated_product = crud_product.update(
            db=db,
            db_obj=product,
            obj_in=product_update
        )
        
        assert updated_product.name == "New Name"
        assert updated_product.description == "New description"
        assert updated_product.category_id == new_category.id
    
    def test_update_product_partial(self, db: Session):
        """Test de mise à jour partielle."""
        product = ProductFactory.create(
            db=db,
            name="Original Name",
            description="Original description"
        )
        original_category_id = product.category_id
        
        product_update = ProductUpdate(name="Updated Name")
        updated_product = crud_product.update(
            db=db,
            db_obj=product,
            obj_in=product_update
        )
        
        assert updated_product.name == "Updated Name"
        assert updated_product.description == "Original description"
        assert updated_product.category_id == original_category_id


class TestProductCRUDDelete:
    """Tests pour la suppression de produits."""
    
    def test_delete_product(self, db: Session):
        """Test de suppression d'un produit."""
        product = ProductFactory.create(db=db, name="Product to Delete")
        product_id = product.id
        
        deleted_product = crud_product.delete(db=db, id=product_id)
        
        assert deleted_product is not None
        assert deleted_product.id == product_id
        
        found_product = crud_product.get(db=db, id=product_id)
        assert found_product is None
    
    def test_delete_nonexistent_product_returns_none(self, db: Session):
        """Test que la suppression d'un produit inexistant retourne None."""
        from uuid import uuid4
        
        nonexistent_id = uuid4()
        deleted_product = crud_product.delete(db=db, id=nonexistent_id)
        
        assert deleted_product is None
    
    def test_delete_product_removes_from_database(self, db: Session):
        """Test que la suppression retire bien le produit de la base."""
        category = ProductCategoryFactory.create(db=db)
        ProductFactory.create_batch(db=db, count=3, category=category)
        
        products = crud_product.get_multi(db=db)
        assert len(products) == 3
        
        crud_product.delete(db=db, id=products[0].id)
        
        remaining_products = crud_product.get_multi(db=db)
        assert len(remaining_products) == 2


class TestProductCRUDRelationships:
    """Tests pour vérifier les relations entre Product et autres entités."""
    
    def test_product_has_category_relationship(self, db: Session):
        """Test que le produit a bien la relation vers sa catégorie."""
        category = ProductCategoryFactory.create(db=db, name="Electronics")
        product = ProductFactory.create(db=db, name="Laptop", category=category)
        
        db.refresh(product)
        
        assert product.category is not None
        assert product.category.name == "Electronics"
        assert product.category.id == category.id
    
    def test_product_has_collection_relationship(self, db: Session):
        """Test que le produit a bien la relation vers sa collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db, name="Summer Sale")
        product = ProductFactory.create(db=db, name="Product", category=category, collection=collection)
        
        db.refresh(product)
        
        assert product.collection is not None
        assert product.collection.name == "Summer Sale"
        assert product.collection.id == collection.id
    
    def test_product_without_collection(self, db: Session):
        """Test qu'un produit peut exister sans collection."""
        product = ProductFactory.create(db=db, collection=None)
        
        db.refresh(product)
        
        assert product.collection_id is None
        assert product.collection is None
