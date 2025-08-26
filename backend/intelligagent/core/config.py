import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql://intelligagent:intelligagent123@db:5432/intelligagent"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # Kafkaexit
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

# Global settings instance
settings = Settings()
