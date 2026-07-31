from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class DBSettings(BaseSettings):

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_ECHO: bool

    model_config = SettingsConfigDict(
        env_file="./.env",
        extra="ignore"
    )

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file="./.env",
        extra="ignore"
    )

db_settings = DBSettings()
app_settings = Settings()