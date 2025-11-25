from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth.dependencies import get_current_user, get_current_user_optional, User

app = FastAPI(
    title="Inventory Management API",
    description="API for inventory management with Supabase authentication",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Public route - no authentication required."""
    return {
        "message": "Welcome to Inventory Management API",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/public")
async def public_route():
    """Another public route example."""
    return {
        "message": "This is a public endpoint",
        "authentication": "not required"
    }


@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    """
    Protected route - authentication required.
    
    To access this route, include the Bearer token in the Authorization header:
    Authorization: Bearer <your-jwt-token>
    """
    return {
        "message": f"Hello {user.email}!",
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "authentication": "required"
    }


@app.get("/optional-auth")
async def optional_auth_route(user: Optional[User] = Depends(get_current_user_optional)):
    """
    Route with optional authentication.
    Works both with and without a token.
    """
    if user:
        return {
            "message": f"Welcome back, {user.email}!",
            "user_id": user.user_id,
            "authenticated": True
        }
    return {
        "message": "Welcome, guest!",
        "authenticated": False
    }


@app.get("/me")
async def get_current_user_info(user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return {
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role
    }