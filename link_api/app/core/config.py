from pathlib import Path
from typing import Literal

from pydantic import AmqpDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = ROOT_DIR / ".env"


class DatabaseConfig(BaseModel):
    host: str
    port: int
    db: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )


class TaskiqConfig(BaseModel):
    url: AmqpDsn


class CacheConfig(BaseModel):
    url: str


class ServiceConfig(BaseModel):
    name: str
    port: int
    debug: bool


class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class CorsConfig(BaseModel):
    allowed_origins: list[str]


class LoggingConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH if ENV_FILE_PATH.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
    FRONTEND_URL: str

    MODE: Literal["DEV", "TEST", "PROD"]

    logging: LoggingConfig
    cors: CorsConfig
    auth: AuthConfig
    service: ServiceConfig
    database: DatabaseConfig
    test_database: DatabaseConfig
    taskiq: TaskiqConfig
    cache: CacheConfig


settings = Settings()
