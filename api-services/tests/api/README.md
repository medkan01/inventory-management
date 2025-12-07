# Tests API - Endpoints HTTP

Tests des routes FastAPI et de leurs réponses HTTP.

## Fichiers

- **test_auth.py** (10 tests)
  - Tests d'authentification JWT
  - Validation des tokens
  - Routes protégées et optionnelles
  - Tests avec tokens valides, expirés, invalides

- **test_api_product.py** (20 tests)
  - CRUD complet des produits via API
  - Filtrage par catégorie/collection
  - Pagination et limites
  - Gestion des erreurs 404, 422

- **test_api_product_category.py** (17 tests)
  - CRUD des catégories via API
  - Recherche par slug
  - Validation des contraintes d'unicité

- **test_api_product_collection.py** (17 tests)
  - CRUD des collections via API
  - Recherche par slug
  - Validation des contraintes d'unicité

## Exécution

```bash
# Tous les tests API
pytest tests/api/ -v

# Un fichier spécifique
pytest tests/api/test_auth.py -v
```
