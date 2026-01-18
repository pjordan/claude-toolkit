"""Application configuration."""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "advanced-apim-api"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # APIM
    apim_gateway_url: str = ""
    validate_subscription_key: bool = True

    # Azure AD / Entra ID
    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_audience: str = ""

    # Database (example)
    database_url: Optional[str] = None

    # Redis (example)
    redis_url: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or text

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
