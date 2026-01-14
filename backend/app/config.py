from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str 
    JWT_SECRET_KEY: str 
    OPENCAGE_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 día
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 días
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

