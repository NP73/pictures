from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):

    """
    Хранит в себе данные настроек с валидацией 
    Pydantic
    Берет данные переменных из .env файла
    """
    postgres_db: str = None
    postgres_user: str = None
    postgres_password: str = None
    id_client_google:str = None
    secret_key_google_auth: str = None
    secret_key: str = 'hfyh88884zhs4569hg'

 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Settings = Settings()
