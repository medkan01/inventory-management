# Fixtures - Utilitaires de test

Contient les utilitaires, fixtures et factories pour la génération de données de test.

## Fichiers

### database.py
Configuration de la base de données de test (SQLite in-memory).

**Fonctions principales:**
- `create_test_database()` - Crée la structure de la DB
- `drop_test_database()` - Supprime la DB de test
- `get_test_db()` - Fournit une session de test
- `reset_test_database()` - Reset entre les tests

### factories.py
Factories pour générer des données de test avec des valeurs cohérentes.

**Classes disponibles:**
- `ProductCategoryFactory` - Génère des catégories
- `ProductCollectionFactory` - Génère des collections
- `ProductFactory` - Génère des produits

**Usage:**
```python
# Créer une catégorie
category = ProductCategoryFactory.create(db=db)

# Créer plusieurs produits
products = ProductFactory.create_batch(db=db, count=5)

# Créer avec des paramètres spécifiques
category = ProductCategoryFactory.create(
    db=db,
    name="Electronics",
    slug="electronics"
)
```

### test_database_fixtures.py (21 tests)
Tests de validation des fixtures et factories.

## Exécution

```bash
# Tests des fixtures
pytest tests/fixtures/test_database_fixtures.py -v
```
