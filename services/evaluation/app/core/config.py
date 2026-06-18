from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://ragops:0308@localhost:5432/ragops"
    REDIS_URL: str = "redis://:ragops_dev@localhost:6379/0"
    GOOGLE_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
