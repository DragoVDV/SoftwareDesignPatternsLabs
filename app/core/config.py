from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CSV_FILE_PATH: str = "data/data.csv"

    class Config:
        env_file = ".env"


settings = Settings()
