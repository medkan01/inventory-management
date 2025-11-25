# Authentication Backend

## Configuration

Pour activer l'authentification, vous devez ajouter le JWT secret de Supabase dans votre fichier `.env` :

```env
SUPABASE_JWT_SECRET=your-supabase-jwt-secret-here
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
```

### Trouver votre JWT Secret

1. Allez sur [Supabase Dashboard](https://supabase.com/dashboard)
2. Sélectionnez votre projet
3. Allez dans **Settings** > **API**
4. Copiez la valeur de **JWT Secret** (section "JWT Settings")

## Utilisation

### Routes publiques (pas d'authentification)

```python
@app.get("/public")
async def public_route():
    return {"message": "Accessible à tous"}
```

### Routes protégées (authentification obligatoire)

Utilisez `Depends(get_current_user)` pour protéger une route :

```python
from fastapi import Depends
from auth.dependencies import get_current_user, User

@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {
        "message": f"Hello {user.email}",
        "user_id": user.user_id
    }
```

### Routes avec authentification optionnelle

Utilisez `Depends(get_current_user_optional)` pour des routes qui fonctionnent avec ou sans authentification :

```python
from typing import Optional
from fastapi import Depends
from auth.dependencies import get_current_user_optional, User

@app.get("/optional-auth")
async def optional_route(user: Optional[User] = Depends(get_current_user_optional)):
    if user:
        return {"message": f"Bienvenue {user.email}"}
    return {"message": "Bienvenue visiteur"}
```

## Tester l'authentification

### 1. Obtenir un token

Connectez-vous via le frontend Next.js pour obtenir un token JWT.

### 2. Utiliser le token dans les requêtes

#### Avec curl :

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/protected
```

#### Avec httpie :

```bash
http GET localhost:8000/protected Authorization:"Bearer YOUR_JWT_TOKEN"
```

#### Avec Postman / Insomnia :

1. Ajoutez un header `Authorization`
2. Valeur : `Bearer YOUR_JWT_TOKEN`

### 3. Documentation Swagger

L'API est documentée avec Swagger UI : http://localhost:8000/docs

Pour tester les routes protégées dans Swagger :
1. Cliquez sur le bouton **Authorize** (cadenas)
2. Entrez votre token : `Bearer YOUR_JWT_TOKEN`
3. Testez vos routes

## Objet User

Le dependency `get_current_user` retourne un objet `User` avec :

- `user_id` : ID unique de l'utilisateur (UUID)
- `email` : Email de l'utilisateur
- `role` : Rôle de l'utilisateur (si défini dans Supabase)

## Exemples de routes

### Route protégée avec filtre par utilisateur

```python
@app.get("/my-items")
async def get_my_items(user: User = Depends(get_current_user)):
    # Filtrer les items par user_id
    items = db.query(Item).filter(Item.user_id == user.user_id).all()
    return items
```

### Route avec vérification de rôle

```python
from fastapi import HTTPException, status

@app.get("/admin")
async def admin_route(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return {"message": "Welcome admin"}
```

## Gestion des erreurs

### Token invalide ou expiré

- Status code : `401 Unauthorized`
- Message : "Invalid authentication token"

### Token manquant sur route protégée

- Status code : `401 Unauthorized`
- Message : "Not authenticated"

### Configuration serveur manquante

- Status code : `500 Internal Server Error`
- Message : "Server configuration error: JWT secret not configured"
