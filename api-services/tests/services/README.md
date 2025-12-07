# Tests Services - Logique métier

Tests de la couche service qui contient la logique métier et les validations.

## Fichiers

- **test_service_product.py** (20 tests)
  - Logique métier des produits
  - Validation des contraintes
  - Gestion des erreurs métier
  - Validation des relations catégorie/collection

- **test_service_product_category.py** (20 tests)
  - Logique métier des catégories
  - Validation unicité slug/nom
  - Gestion des duplications
  - Mise à jour avec contraintes

- **test_service_product_collection.py** (20 tests)
  - Logique métier des collections
  - Validation unicité slug/nom
  - Gestion des duplications
  - Mise à jour avec contraintes

## Couverture

✅ **91-100%** sur tous les services

## Exécution

```bash
# Tous les tests Services
pytest tests/services/ -v

# Un fichier spécifique
pytest tests/services/test_service_product.py -v
```
