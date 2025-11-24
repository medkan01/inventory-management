# GitHub Actions Workflows

## 📋 Workflows disponibles

### `ci.yml` - Pipeline d'Intégration Continue

Ce workflow s'exécute automatiquement sur :
- Chaque push sur les branches `master`, `main`, `develop`
- Chaque pull request vers ces branches

#### Jobs exécutés :

1. **backend-lint** : Vérifie le code Python
   - Lint avec Ruff
   - Vérification de la syntaxe Python

2. **frontend-lint** : Vérifie le code TypeScript/Next.js
   - Lint avec ESLint
   - Vérification des types TypeScript

3. **docker-build** : Teste les builds Docker
   - Build de l'image backend (FastAPI)
   - Build de l'image frontend (Next.js)
   - Utilise le cache pour accélérer les builds

4. **integration-test** : Tests d'intégration
   - Lance tous les services avec Docker Compose
   - Vérifie que l'API et le frontend répondent
   - Nettoie automatiquement les ressources

5. **ci-success** : Confirmation finale
   - S'exécute uniquement si tous les jobs précédents réussissent

## 🔧 Configuration

### Ajouts futurs recommandés :

- Tests unitaires pour le backend (pytest)
- Tests unitaires pour le frontend (Jest/Vitest)
- Tests E2E (Playwright/Cypress)
- Analyse de couverture de code
- Sécurité (Dependabot, scanning de vulnérabilités)

### Variables d'environnement :

Le workflow CI crée automatiquement un fichier `.env` temporaire pour les tests.
Pour le déploiement, vous devrez configurer des secrets GitHub :
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- Ou autres secrets selon votre plateforme de déploiement

## 🚀 Évolution du workflow

Ce workflow est conçu pour évoluer avec votre projet :
- ✅ Continue sur erreur de lint (ne bloque pas le développement)
- ✅ Cache les dépendances (npm, pip, Docker layers)
- ✅ Jobs parallélisés pour rapidité
- ✅ Prêt pour ajouter des tests unitaires/E2E

## 📊 Badges de statut

Vous pouvez ajouter ce badge à votre README :

```markdown
![CI Status](https://github.com/medkan01/inventory-management/workflows/CI%20Pipeline/badge.svg)
```
