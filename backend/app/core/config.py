"""
Application configuration management using pydantic-settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Prompt Optimizer"
    DEBUG: bool = False
    SECRET_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./prompt_optimizer.db"
    
    # OpenRouter API
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # JWT Settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: str = "json,txt"
    UPLOAD_DIR: str = "uploads"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Convert comma-separated extensions to list"""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
