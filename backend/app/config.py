from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # App
    app_name: str = "AI Office"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./ai_office.db"
    
    # API
    api_prefix: str = "/api"
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # LLM (for agents - mock for now)
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
