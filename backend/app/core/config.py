from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_env: Literal["dev", "staging", "prod"] = "dev"
    app_name: str = "InvoxelAI GST OCR"
    secret_key: str = Field(default="change-me", min_length=8)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = "invoxel"
    db_user: str = "invoxel"
    db_password: str = "invoxel"

    cors_origins: list[str] = ["http://localhost:3000"]
    upload_dir: str = "uploads"
    max_upload_mb: int = 15

    paddle_use_gpu: bool = False
    ocr_langs: str = "en,hi"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
