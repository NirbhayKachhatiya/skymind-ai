from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # --- Project Metadata ---
    PROJECT_NAME: str = "SkyMind AI Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # --- Live OpenRouter LLM Configuration ---
    # Adding this field explicitly fixes your 'extra_forbidden' validation crash
    llm_api_key: Optional[str] = None

    # --- Database / Data Mock Configurations ---
    DATA_DIR: str = "app/data"

    # --- Pydantic Settings Source Behavior ---
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allows matching llm_api_key or LLM_API_KEY flawlessly
        extra="ignore"         # Prevents crashes if there are other unmapped variables in your .env
    )

# Instantiate the settings instance for the rest of the application to import
settings = Settings()