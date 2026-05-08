from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str
    
    model_config = SettingsConfigDict(
        env_file=".env.local",
        extra="ignore",
    )
    

settings = Settings()
