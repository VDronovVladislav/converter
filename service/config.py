from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовые настройки приложения."""
    app_title: str
    currency_url: str

    class Config:
        env_file = ".env"


settings = Settings()