from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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

    @property
    def DB_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()