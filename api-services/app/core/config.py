"""
Configuration centrale de l'application.
Gère toutes les variables d'environnement avec validation Pydantic.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Configuration de l'application.
    Les valeurs sont automatiquement chargées depuis les variables d'environnement.
    """
    
    # API Configuration
    project_name: str = "Inventory Management API"
    version: str = "1.0.0"
    api_v1_str: str = "/api/v1"
    debug: bool = False
    
    # Supabase
    supabase_url: str = Field(..., alias="NEXT_PUBLIC_SUPABASE_URL")
    supabase_jwt_secret: str = Field(..., alias="SUPABASE_JWT_SECRET")
    
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        alias="CORS_ORIGINS"
    )
    
    # JWT
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # Logging
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS si c'est une string séparée par des virgules."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


# Instance singleton
settings = Settings()
