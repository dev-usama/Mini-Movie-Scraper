from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".env"))

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    postgres_url: str 
    omdb_api_key: str
    
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)

settings = Settings()

db_engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)