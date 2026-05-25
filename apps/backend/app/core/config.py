from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SANSON Legal OS"
    app_version: str = "1.0.0"
    api_version: str = "v1"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://sanson:sanson_dev_password@localhost:5433/sanson_legal"
    redis_url: str = "redis://localhost:6380/0"

    jwt_secret: str = "change-me-to-a-secure-random-string-min-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    cors_origins: str = "http://localhost:3100,http://127.0.0.1:3100,http://localhost:8081"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    ollama_enabled: bool = False
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "sanson_documents"

    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "sanson_minio"
    s3_secret_key: str = "sanson_minio_secret"
    s3_bucket: str = "sanson-documents"
    s3_region: str = "us-east-1"
    s3_use_ssl: bool = False

    rate_limit_per_minute: int = 60

    gcash_enabled: bool = False

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v: str | List[str]) -> str:
        if isinstance(v, list):
            return ",".join(v)
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
