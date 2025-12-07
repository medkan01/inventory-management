# Tests CRUD - Accès aux données

Tests de la couche CRUD (Repository pattern) pour les opérations de base de données.

## Fichiers

- **test_crud_product.py** (27 tests)
  - Opérations CRUD sur les produits
  - Requêtes par catégorie/collection
  - Filtrage par slug/nom
  - Pagination et relations

- **test_crud_product_category.py** (21 tests)
  - Opérations CRUD sur les catégories
  - Recherche par slug/nom
  - Tests d'unicité
  - Mise à jour partielle

- **test_crud_product_collection.py** (23 tests)
  - Opérations CRUD sur les collections
  - Recherche par slug/nom
  - Tests d'unicité
  - Mise à jour partielle

## Couverture

✅ **100%** sur tous les modules CRUD

## Exécution

```bash
# Tous les tests CRUD
pytest tests/crud/ -v

# Un fichier spécifique
pytest tests/crud/test_crud_product.py -v
```
