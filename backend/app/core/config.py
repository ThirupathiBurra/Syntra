from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Syntra Enterprise AI Platform"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_DB_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

settings = Settings()

from supabase import create_client, Client

def get_supabase_client() -> Optional[Client]:
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return None
