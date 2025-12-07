"""
Module de configuration de la base de données pour les tests.
Fournit une base de données SQLite en mémoire isolée pour chaque test.
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.models.base import Base

# Configuration de la base de données de test (SQLite en mémoire)
# StaticPool garde la même connexion pour éviter les problèmes avec :memory:
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Créer l'engine de test avec une configuration spéciale pour SQLite
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Nécessaire pour SQLite
    poolclass=StaticPool,  # Garde une seule connexion en mémoire
    echo=False,  # Pas de logs SQL pendant les tests (mettre True pour debug)
)


# Activer les foreign keys pour SQLite (désactivées par défaut)
@event.listens_for(test_engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Active les contraintes de clés étrangères pour SQLite."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Factory de sessions pour les tests
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def create_test_database():
    """
    Crée toutes les tables de la base de données de test.
    À appeler une fois au début de la session de test.
    """
    Base.metadata.create_all(bind=test_engine)


def drop_test_database():
    """
    Supprime toutes les tables de la base de données de test.
    À appeler une fois à la fin de la session de test.
    """
    Base.metadata.drop_all(bind=test_engine)


def get_test_db() -> Generator[Session, None, None]:
    """
    Génère une session de base de données de test.
    Utilisée pour remplacer la dépendance get_db dans les tests.
    
    Yields:
        Session: Session de base de données de test
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_test_database():
    """
    Réinitialise complètement la base de données de test.
    Utile pour s'assurer d'un état propre entre les tests.
    """
    drop_test_database()
    create_test_database()
