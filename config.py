from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_CONNECTION_URI: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    SENDGRID_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
