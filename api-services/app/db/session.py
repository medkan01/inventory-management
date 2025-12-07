"""
Configuration de la session de base de données.
Gère la connexion SQLAlchemy avec PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer l'engine SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Vérifie la connexion avant de l'utiliser
    echo=settings.debug,  # Affiche les requêtes SQL en mode debug
)

# Créer la factory de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency pour obtenir une session de base de données.

    Utilisation dans une route:
    ```python
    @router.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return crud.item.get_multi(db)
    ```

    Yields:
        Session: Une session SQLAlchemy qui sera automatiquement fermée après usage
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
