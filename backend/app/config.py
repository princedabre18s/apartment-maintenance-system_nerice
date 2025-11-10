from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # PostgreSQL settings
    pg_host: str
    pg_database: str
    pg_user: str
    pg_password: str
    pg_sslmode: str = "require"
    pg_port: int = 5432
    
    secret_key: str = "your-secret-key-here"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_url: str = "http://localhost:5173"
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL"""
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}?ssl=require"


settings = Settings()
