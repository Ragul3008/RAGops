from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    COHERE_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    DATABASE_URL: str | None = None
    EMBEDDING_PROVIDER: str = "openai"
    LOCAL_MODEL: str = "all-MiniLM-L6-v2"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
