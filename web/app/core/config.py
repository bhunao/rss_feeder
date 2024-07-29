from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    APP_TITLE: str = "RSS Feeder"
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory="templates")


settings = Settings()
