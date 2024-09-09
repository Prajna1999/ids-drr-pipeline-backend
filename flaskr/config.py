from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_URL: str
    API_KEY: str
    DATABASE_URL: str  

    class Config:
        env_file = ".env"
        case_sensitive = False  # This allows for case-insensitive env var names

settings = Settings()