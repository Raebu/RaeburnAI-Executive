from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAEBURNAI_", env_file=".env", extra="ignore")

    env: str = "development"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    web_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    secret_key: str | None = None
    database_url: str = "sqlite:///./raeburnai_executive.db"
    redis_url: str = "redis://localhost:6379/0"
    llm_provider: str = "mock"


@lru_cache
def get_settings() -> Settings:
    return Settings()
