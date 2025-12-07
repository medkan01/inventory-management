"""
Configuration globale pour pytest.
Fixtures partagées pour tous les tests.
"""

import os
import pytest
from datetime import datetime, timedelta
from jose import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Charger les variables d'environnement de test AVANT d'importer l'app
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("NEXT_PUBLIC_SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_JWT_SECRET", "test-jwt-secret-for-testing")

from app.main import app
from app.core.config import settings
from app.schemas.user import User
from app.db import get_db
from app.api.deps import get_current_user

# Import du module de base de données de test
from tests.fixtures.database import (
    create_test_database,
    drop_test_database,
    get_test_db,
    reset_test_database,
)

# Import des factories
from tests.fixtures.factories import (
    ProductCategoryFactory,
    ProductCollectionFactory,
    ProductFactory,
)


# ============================================================================
# FIXTURES DE BASE DE DONNÉES
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Fixture de session pour créer/supprimer la base de données de test.
    S'exécute automatiquement une fois au début et à la fin de la session de test.
    """
    # Setup: Créer la base de données avant tous les tests
    create_test_database()
    yield
    # Teardown: Supprimer la base de données après tous les tests
    drop_test_database()


@pytest.fixture(scope="function")
def db() -> Session:
    """
    Fixture pour obtenir une session de base de données de test.
    Réinitialise la base de données avant chaque test pour garantir l'isolation.
    
    Usage:
        def test_create_product(db):
            product = Product(name="Test Product")
            db.add(product)
            db.commit()
            assert product.id is not None
    
    Returns:
        Session: Session de base de données de test propre et isolée
    """
    # Réinitialiser la DB avant chaque test
    reset_test_database()
    
    # Créer une nouvelle session
    db_session = next(get_test_db())
    yield db_session
    
    # Nettoyer après le test
    db_session.close()


@pytest.fixture
def client(db: Session, test_user):
    """
    Fixture pour le client de test FastAPI avec base de données de test.
    Remplace automatiquement la dépendance get_db par get_test_db
    et mock l'authentification pour contourner get_current_user.

    Usage:
        def test_something(client):
            response = client.get("/api/v1/products")
            assert response.status_code == 200
    
    Args:
        db: Session de base de données de test (injection automatique)
        test_user: Utilisateur de test pour l'authentification mockée
    
    Returns:
        TestClient: Client de test configuré avec la DB de test et auth mockée
    """
    # Remplacer la dépendance get_db par get_test_db
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    # Mock de get_current_user pour contourner l'authentification JWT
    async def override_get_current_user():
        return test_user
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield TestClient(app)
    
    # Nettoyer les overrides après le test
    app.dependency_overrides.clear()


@pytest.fixture
def client_no_auth(db: Session):
    """
    Fixture pour le client de test FastAPI SANS mock d'authentification.
    Utilisé pour tester la vraie logique d'authentification JWT.

    Usage:
        def test_auth(client_no_auth):
            response = client_no_auth.get("/api/v1/auth/protected")
            assert response.status_code == 403  # Sans token
    
    Args:
        db: Session de base de données de test (injection automatique)
    
    Returns:
        TestClient: Client de test configuré avec la DB de test mais SANS auth mockée
    """
    # Remplacer uniquement la dépendance get_db, PAS get_current_user
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    # Nettoyer les overrides après le test
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    """
    Fixture pour un utilisateur de test.

    Returns:
        User: Objet utilisateur avec des données de test
    """
    return User(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        email="test@example.com",
        role="user",
    )


@pytest.fixture
def admin_user():
    """
    Fixture pour un utilisateur administrateur de test.

    Returns:
        User: Objet utilisateur admin avec des données de test
    """
    return User(
        user_id="987e6543-e21b-98d7-a654-321987654321",
        email="admin@example.com",
        role="admin",
    )


@pytest.fixture
def valid_jwt_token(test_user):
    """
    Génère un JWT valide pour les tests.

    Le token est signé avec le même secret que l'application
    et contient les claims standards de Supabase.

    Args:
        test_user: Fixture de l'utilisateur de test

    Returns:
        str: Token JWT valide
    """
    payload = {
        "sub": test_user.user_id,
        "email": test_user.email,
        "role": test_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def admin_jwt_token(admin_user):
    """
    Génère un JWT valide pour un utilisateur admin.

    Args:
        admin_user: Fixture de l'utilisateur admin

    Returns:
        str: Token JWT valide pour admin
    """
    payload = {
        "sub": admin_user.user_id,
        "email": admin_user.email,
        "role": admin_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def expired_jwt_token(test_user):
    """
    Génère un JWT expiré pour tester la validation.

    Args:
        test_user: Fixture de l'utilisateur de test

    Returns:
        str: Token JWT expiré
    """
    payload = {
        "sub": test_user.user_id,
        "email": test_user.email,
        "role": test_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() - timedelta(hours=1),  # Expiré il y a 1h
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def invalid_signature_token(test_user):
    """
    Génère un JWT avec une signature invalide.

    Args:
        test_user: Fixture de l'utilisateur de test

    Returns:
        str: Token JWT avec signature invalide
    """
    payload = {
        "sub": test_user.user_id,
        "email": test_user.email,
        "role": test_user.role,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, "wrong-secret-key", algorithm="HS256")


@pytest.fixture
def auth_headers(valid_jwt_token):
    """
    Fixture pour les headers d'authentification avec un token JWT valide.

    Args:
        valid_jwt_token: Fixture du token JWT valide

    Returns:
        dict: Headers avec Authorization Bearer
    """
    return {"Authorization": f"Bearer {valid_jwt_token}"}


# ============================================================================
# FIXTURES DE DONNÉES DE TEST (FACTORIES)
# ============================================================================


@pytest.fixture
def test_category(db: Session):
    """
    Fixture pour créer une catégorie de test.
    
    Usage:
        def test_something(test_category):
            assert test_category.name is not None
            assert test_category.slug is not None
    
    Returns:
        ProductCategory: Catégorie de test avec des valeurs par défaut
    """
    return ProductCategoryFactory.create(
        db=db,
        name="Electronics",
        slug="electronics",
        description="Electronic devices and accessories",
    )


@pytest.fixture
def test_collection(db: Session):
    """
    Fixture pour créer une collection de test.
    
    Usage:
        def test_something(test_collection):
            assert test_collection.name is not None
            assert test_collection.slug is not None
    
    Returns:
        ProductCollection: Collection de test avec des valeurs par défaut
    """
    return ProductCollectionFactory.create(
        db=db,
        name="Summer 2024",
        slug="summer-2024",
        description="Summer collection for 2024",
    )


@pytest.fixture
def test_product(db: Session, test_category):
    """
    Fixture pour créer un produit de test.
    
    Usage:
        def test_something(test_product):
            assert test_product.name is not None
            assert test_product.category_id is not None
    
    Args:
        db: Session de base de données
        test_category: Catégorie de test (injection automatique)
    
    Returns:
        Product: Produit de test avec des valeurs par défaut
    """
    return ProductFactory.create(
        db=db,
        name="Laptop Dell XPS 13",
        description="High-performance laptop with 13-inch display",
        category=test_category,
    )


@pytest.fixture
def multiple_categories(db: Session):
    """
    Fixture pour créer plusieurs catégories de test.
    
    Usage:
        def test_something(multiple_categories):
            assert len(multiple_categories) == 3
    
    Returns:
        list[ProductCategory]: Liste de 3 catégories de test
    """
    return ProductCategoryFactory.create_batch(db=db, count=3)


@pytest.fixture
def multiple_collections(db: Session):
    """
    Fixture pour créer plusieurs collections de test.
    
    Usage:
        def test_something(multiple_collections):
            assert len(multiple_collections) == 3
    
    Returns:
        list[ProductCollection]: Liste de 3 collections de test
    """
    return ProductCollectionFactory.create_batch(db=db, count=3)


@pytest.fixture
def multiple_products(db: Session, test_category):
    """
    Fixture pour créer plusieurs produits de test dans la même catégorie.
    
    Usage:
        def test_something(multiple_products):
            assert len(multiple_products) == 5
            assert all(p.category_id == multiple_products[0].category_id for p in multiple_products)
    
    Args:
        db: Session de base de données
        test_category: Catégorie de test commune
    
    Returns:
        list[Product]: Liste de 5 produits de test
    """
    return ProductFactory.create_batch(db=db, count=5, category=test_category)
