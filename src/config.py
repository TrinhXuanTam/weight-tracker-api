from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class DBConfig(BaseSettings):
    DATABASE_URL: PostgresDsn
    DATABASE_ENCRYPTION_KEY: str

class CorsConfig(BaseSettings):
    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    CORS_METHODS: list[str]

db_config: DBConfig = DBConfig()
cors_config: CorsConfig = CorsConfig()