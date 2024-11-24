from pydantic import BaseModel

class Settings(BaseModel):
    MASTER_DATABASE_URL: str = "postgresql://eish:postgres@localhost:5432/master_db"
    DATABASE_USER: str = "eish"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
