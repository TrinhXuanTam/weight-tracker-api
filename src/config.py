from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class DBConfig(BaseSettings):
    DATABASE_URL: PostgresDsn
    DATABASE_ENCRYPTION_KEY: str


db_config: DBConfig = DBConfig()
