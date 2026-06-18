from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    REDIS_URL: str = ""
    JWT_SECRET: str = ""

    JWT_PRIVATE_KEY: str = "secret-key-placeholder"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: list[str] = []
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()