from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""

    # Database
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    JELLYFIN_PUBLIC_URL: str

    # Security
    SECRET_KEY: str
    API_KEY: str
    WEBHOOK_SECRET: str = ""

    # App Info
    APP_NAME: str = "Servarr Hub"
    APP_VERSION: str = "1.0.0"

    @property
    def DATABASE_URL(self) -> str:
        """Construit l'URL de connexion MariaDB"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instance globale des settings
settings = Settings()
