from dotenv import load_dotenv

from pydantic_settings import BaseSettings

# TODO исправить на относительный
load_dotenv("/Users/andreychvankov/Projects/link_saver_api/.env")

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    # CORS_ALLOWED_ORIGINS: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DB_ECHO: bool
    DB_URL: str
    
settings = Settings()