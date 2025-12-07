"""
Tests de base pour valider l'infrastructure de test (DB, fixtures, factories).
Ces tests s'assurent que l'environnement de test fonctionne correctement.
"""

import pytest
from sqlalchemy.orm import Session

from app.models.product import Product, ProductCategory, ProductCollection
from tests.fixtures.factories import (
    ProductCategoryFactory,
    ProductCollectionFactory,
    ProductFactory,
)


class TestDatabaseFixtures:
    """Tests pour vérifier que les fixtures de base de données fonctionnent."""
    
    def test_db_session_is_clean(self, db: Session):
        """Vérifie que la session DB est propre au début de chaque test."""
        # La base de données devrait être vide au départ
        categories_count = db.query(ProductCategory).count()
        collections_count = db.query(ProductCollection).count()
        products_count = db.query(Product).count()
        
        assert categories_count == 0
        assert collections_count == 0
        assert products_count == 0
    
    def test_db_session_isolation(self, db: Session):
        """Vérifie que chaque test a sa propre session isolée."""
        # Créer une catégorie
        category = ProductCategoryFactory.create(
            db=db,
            name="Test Category",
            slug="test-category",
        )
        
        assert category.id is not None
        assert db.query(ProductCategory).count() == 1


class TestFactories:
    """Tests pour vérifier que les factories fonctionnent correctement."""
    
    def test_category_factory_creates_category(self, db: Session):
        """Vérifie que CategoryFactory crée une catégorie valide."""
        category = ProductCategoryFactory.create(
            db=db,
            name="Electronics",
            slug="electronics",
            description="Electronic devices",
        )
        
        assert category.id is not None
        assert category.name == "Electronics"
        assert category.slug == "electronics"
        assert category.description == "Electronic devices"
        assert category.created_at is not None
        assert category.updated_at is not None
    
    def test_category_factory_generates_unique_names(self, db: Session):
        """Vérifie que CategoryFactory génère des noms uniques automatiquement."""
        import time
        
        category1 = ProductCategoryFactory.create(db=db)
        time.sleep(0.001)  # Petit délai pour garantir des timestamps différents
        category2 = ProductCategoryFactory.create(db=db)
        
        assert category1.name != category2.name
        assert category1.slug != category2.slug
        assert category1.id != category2.id
    
    def test_category_factory_batch(self, db: Session):
        """Vérifie que CategoryFactory peut créer plusieurs catégories."""
        categories = ProductCategoryFactory.create_batch(db=db, count=5)
        
        assert len(categories) == 5
        assert db.query(ProductCategory).count() == 5
        
        # Vérifier que tous les slugs sont uniques
        slugs = [cat.slug for cat in categories]
        assert len(slugs) == len(set(slugs))
    
    def test_collection_factory_creates_collection(self, db: Session):
        """Vérifie que CollectionFactory crée une collection valide."""
        collection = ProductCollectionFactory.create(
            db=db,
            name="Summer 2024",
            slug="summer-2024",
            description="Summer collection",
        )
        
        assert collection.id is not None
        assert collection.name == "Summer 2024"
        assert collection.slug == "summer-2024"
        assert collection.description == "Summer collection"
    
    def test_collection_factory_batch(self, db: Session):
        """Vérifie que CollectionFactory peut créer plusieurs collections."""
        collections = ProductCollectionFactory.create_batch(db=db, count=3)
        
        assert len(collections) == 3
        assert db.query(ProductCollection).count() == 3
    
    def test_product_factory_creates_product(self, db: Session):
        """Vérifie que ProductFactory crée un produit valide."""
        category = ProductCategoryFactory.create(db=db, name="Electronics")
        
        product = ProductFactory.create(
            db=db,
            name="Laptop",
            description="High-performance laptop",
            category=category,
        )
        
        assert product.id is not None
        assert product.name == "Laptop"
        assert product.description == "High-performance laptop"
        assert product.category_id == category.id
        assert product.category.name == "Electronics"
    
    def test_product_factory_creates_category_if_not_provided(self, db: Session):
        """Vérifie que ProductFactory crée une catégorie si non fournie."""
        product = ProductFactory.create(db=db, name="Test Product")
        
        assert product.id is not None
        assert product.category_id is not None
        assert product.category is not None
        
        # Vérifier que la catégorie a été créée
        assert db.query(ProductCategory).count() == 1
    
    def test_product_factory_with_collection(self, db: Session):
        """Vérifie que ProductFactory peut associer une collection."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db, name="Winter Sale")
        
        product = ProductFactory.create(
            db=db,
            name="Winter Jacket",
            category=category,
            collection=collection,
        )
        
        assert product.collection_id == collection.id
        assert product.collection.name == "Winter Sale"
    
    def test_product_factory_batch(self, db: Session):
        """Vérifie que ProductFactory peut créer plusieurs produits."""
        category = ProductCategoryFactory.create(db=db)
        products = ProductFactory.create_batch(db=db, count=10, category=category)
        
        assert len(products) == 10
        assert db.query(Product).count() == 10
        
        # Tous les produits devraient avoir la même catégorie
        assert all(p.category_id == category.id for p in products)


class TestFixturesIntegration:
    """Tests pour vérifier que les fixtures pytest fonctionnent."""
    
    def test_test_category_fixture(self, test_category):
        """Vérifie que la fixture test_category fonctionne."""
        assert test_category.id is not None
        assert test_category.name == "Electronics"
        assert test_category.slug == "electronics"
    
    def test_test_collection_fixture(self, test_collection):
        """Vérifie que la fixture test_collection fonctionne."""
        assert test_collection.id is not None
        assert test_collection.name == "Summer 2024"
        assert test_collection.slug == "summer-2024"
    
    def test_test_product_fixture(self, test_product):
        """Vérifie que la fixture test_product fonctionne."""
        assert test_product.id is not None
        assert test_product.name == "Laptop Dell XPS 13"
        assert test_product.category_id is not None
    
    def test_multiple_categories_fixture(self, multiple_categories):
        """Vérifie que la fixture multiple_categories fonctionne."""
        assert len(multiple_categories) == 3
        assert all(cat.id is not None for cat in multiple_categories)
    
    def test_multiple_collections_fixture(self, multiple_collections):
        """Vérifie que la fixture multiple_collections fonctionne."""
        assert len(multiple_collections) == 3
        assert all(col.id is not None for col in multiple_collections)
    
    def test_multiple_products_fixture(self, multiple_products):
        """Vérifie que la fixture multiple_products fonctionne."""
        assert len(multiple_products) == 5
        assert all(prod.id is not None for prod in multiple_products)
        
        # Tous les produits devraient avoir la même catégorie
        category_ids = [p.category_id for p in multiple_products]
        assert len(set(category_ids)) == 1


class TestDatabaseRelationships:
    """Tests pour vérifier que les relations SQLAlchemy fonctionnent."""
    
    def test_product_category_relationship(self, db: Session):
        """Vérifie que la relation Product -> Category fonctionne."""
        category = ProductCategoryFactory.create(db=db, name="Books")
        product = ProductFactory.create(db=db, name="Python Guide", category=category)
        
        # Recharger depuis la DB
        db.refresh(product)
        
        assert product.category.name == "Books"
        assert product.category.id == category.id
    
    def test_category_products_relationship(self, db: Session):
        """Vérifie que la relation Category -> Products fonctionne."""
        category = ProductCategoryFactory.create(db=db, name="Electronics")
        
        ProductFactory.create(db=db, name="Laptop", category=category)
        ProductFactory.create(db=db, name="Mouse", category=category)
        ProductFactory.create(db=db, name="Keyboard", category=category)
        
        # Recharger depuis la DB
        db.refresh(category)
        
        assert len(category.products) == 3
        product_names = [p.name for p in category.products]
        assert "Laptop" in product_names
        assert "Mouse" in product_names
        assert "Keyboard" in product_names
    
    def test_product_collection_relationship(self, db: Session):
        """Vérifie que la relation Product -> Collection fonctionne."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db, name="Best Sellers")
        product = ProductFactory.create(
            db=db,
            name="Top Product",
            category=category,
            collection=collection,
        )
        
        db.refresh(product)
        
        assert product.collection.name == "Best Sellers"
        assert product.collection.id == collection.id
    
    def test_collection_products_relationship(self, db: Session):
        """Vérifie que la relation Collection -> Products fonctionne."""
        category = ProductCategoryFactory.create(db=db)
        collection = ProductCollectionFactory.create(db=db, name="Winter Sale")
        
        ProductFactory.create(db=db, name="Product 1", category=category, collection=collection)
        ProductFactory.create(db=db, name="Product 2", category=category, collection=collection)
        
        db.refresh(collection)
        
        assert len(collection.products) == 2
