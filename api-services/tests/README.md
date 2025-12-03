# Tests Backend - API Services

## 📁 Structure

```
tests/
├── __init__.py           # Module Python
├── conftest.py          # Configuration pytest et fixtures globales
├── test_main.py         # Tests endpoints principaux
└── test_auth.py         # Tests authentification JWT
```

## 🚀 Exécution des tests

### Tests complets avec couverture
```bash
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
```

### Tests rapides (sans couverture)
```bash
pytest tests/ -v
```

### Tests spécifiques
```bash
# Un fichier
pytest tests/test_auth.py -v

# Un test précis
pytest tests/test_auth.py::test_protected_route_with_valid_token -v

# Avec markers
pytest -m unit -v
pytest -m "not slow" -v
```

### Rapport de couverture
```bash
# Générer le rapport HTML
pytest --cov=app --cov-report=html

# Ouvrir le rapport
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

## 🎯 Couverture actuelle

- **93%** de couverture globale
- **87%** sur `app/api/deps.py` (authentification)
- **100%** sur `app/api/v1/endpoints/auth.py`
- **100%** sur `app/schemas/user.py`
- **100%** sur `app/core/logging.py`

Objectif: **≥80%** pour production

## 🔧 Fixtures disponibles

### Utilisateurs
- `test_user` - Utilisateur standard (role: user)
- `admin_user` - Utilisateur admin (role: admin)

### Tokens JWT
- `valid_jwt_token` - Token JWT valide
- `admin_jwt_token` - Token JWT admin
- `expired_jwt_token` - Token expiré (pour tests négatifs)
- `invalid_signature_token` - Token avec mauvaise signature
- `auth_headers` - Headers HTTP avec Bearer token

### Clients
- `client` - TestClient FastAPI

### Exemple d'utilisation
```python
def test_protected_route(client, auth_headers, test_user):
    """Test d'une route protégée"""
    response = client.get("/api/v1/auth/protected", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["user_id"] == test_user.user_id
```

## 📝 Conventions de tests

### Naming
- Fichiers: `test_*.py`
- Classes: `Test*`
- Fonctions: `test_*`

### Structure d'un test
```python
def test_feature_scenario(client, fixtures):
    """Description claire du test"""
    # Arrange - Préparer les données
    data = {...}
    
    # Act - Exécuter l'action
    response = client.post("/endpoint", json=data)
    
    # Assert - Vérifier le résultat
    assert response.status_code == 200
    assert response.json()["key"] == "expected_value"
```

### Markers pytest
```python
@pytest.mark.unit
def test_quick_unit():
    """Test unitaire rapide"""
    pass

@pytest.mark.integration
def test_with_database(db_session):
    """Test d'intégration avec DB"""
    pass

@pytest.mark.slow
def test_long_running():
    """Test long à exécuter"""
    pass
```

## 🔐 Variables d'environnement

Les tests utilisent `.env.test` :
```env
DATABASE_URL=sqlite:///./test.db
NEXT_PUBLIC_SUPABASE_URL=https://test.supabase.co
SUPABASE_JWT_SECRET=test-jwt-secret-for-testing
```

Ces variables sont chargées dans `conftest.py` avant l'import de l'app.

## ✅ Tests implémentés

### test_main.py (4 tests)
- ✅ Route racine `/`
- ✅ Health check `/health`
- ✅ Documentation Swagger `/docs`
- ✅ Schéma OpenAPI `/api/v1/openapi.json`

### test_auth.py (10 tests)
- ✅ Auth optionnelle sans token
- ✅ Route protégée sans token (403)
- ✅ Route `/me` sans token (403)
- ✅ Route protégée avec token valide
- ✅ Route `/me` avec token valide
- ✅ Token expiré (401)
- ✅ Signature invalide (401)
- ✅ Token malformé (401)
- ✅ Auth optionnelle avec token
- ✅ Route admin avec token admin

## 🐛 Debugging

### Voir les logs pendant les tests
```bash
pytest -v -s  # -s désactive la capture de stdout/stderr
```

### Debugger avec pdb
```python
def test_something(client):
    import pdb; pdb.set_trace()  # Breakpoint
    response = client.get("/")
```

### Tests avec plus de détails
```bash
pytest -vv --tb=long  # Traceback complet
pytest -vv --tb=short # Traceback court
```

## 🎓 Bonnes pratiques

1. **Isolation** - Chaque test doit être indépendant
2. **Clarté** - Noms explicites et docstrings
3. **Rapidité** - Tests unitaires < 1s, tests d'intégration < 10s
4. **Couverture** - Viser 80%+ sur le code métier
5. **Edge cases** - Tester les cas limites et erreurs
6. **Fixtures** - Réutiliser au maximum via conftest.py
7. **Markers** - Catégoriser pour exécution sélective

## 🔄 CI/CD

Les tests s'exécutent automatiquement sur GitHub Actions :
- ✅ Chaque push sur `main`, `develop`
- ✅ Chaque Pull Request
- ✅ Coverage check ≥80% obligatoire
- ✅ Rapport de couverture uploadé sur Codecov
- ✅ Artifacts HTML disponibles 7 jours

Voir `.github/workflows/ci.yml` pour plus de détails.

## 📚 Ressources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
