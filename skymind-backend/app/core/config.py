import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    OPENAI_API_KEY: str = "mock-key-if-not-provided"

    class Config:
        env_file = ".env"

settings = Settings()