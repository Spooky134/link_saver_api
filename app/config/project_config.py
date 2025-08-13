from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv("/Users/andreychvankov/Projects/link_saver_api/.env")

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    # CORS_ALLOWED_ORIGINS: str


    DB_ECHO: bool
    DB_URL: str
    
    # @property
    # def DB_URL(self) -> str:
    #     return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()