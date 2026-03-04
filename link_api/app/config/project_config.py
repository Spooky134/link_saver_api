import os


from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = ROOT_DIR / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH if ENV_FILE_PATH.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    MODE: Literal["DEV", "TEST", "PROD"]

    SECRET_KEY: str
    SERVICE_NAME: str
    SERVICE_PORT: int
    SERVICE_ALGORITHM: str
    SERVICE_ACCESS_TOKEN_EXPIRE_MINUTES: int
    SERVICE_CORS_ALLOWED_ORIGINS: str
    SERVICE_DEBUG: bool

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD:str

    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int


    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def test_db_url(self):
        return (
            f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}"
            f"@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
        )

    @property
    def cache_url(self):
        return f"redis://{self.CACHE_HOST}:{self.CACHE_PORT}"


settings = Settings()