from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    secret_key: str
    google_client_id: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

settings = Settings()