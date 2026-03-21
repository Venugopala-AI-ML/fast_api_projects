from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    model_config = SettingsConfigDict(
        env_file="app/.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()