# Tests d'intégration

Tests d'intégration pour vérifier le fonctionnement global de l'application.

## Fichiers

### test_main.py (4 tests)
Tests des endpoints principaux de l'application.

**Tests inclus:**
- `test_root_endpoint` - Endpoint racine "/"
- `test_health_endpoint` - Health check "/health"
- `test_docs_endpoint` - Documentation Swagger "/docs"
- `test_openapi_schema` - Schéma OpenAPI "/openapi.json"

## Couverture

✅ **100%** de couverture

## Exécution

```bash
# Tous les tests d'intégration
pytest tests/integration/ -v

# Test spécifique
pytest tests/integration/test_main.py::test_health_endpoint -v
```
