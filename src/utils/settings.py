from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    TOKEN_EXPIRY_TIME:int
    UPLOAD_DIR: str = "storage/uploads"
    MAIL_PASS: str


settings = Settings()

UPLOAD_DIR = Path(settings.UPLOAD_DIR).expanduser()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# print(settings.DB_CONNECTION)