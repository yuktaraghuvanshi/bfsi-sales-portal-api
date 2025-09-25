from pydantic import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
