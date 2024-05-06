from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str


auth_config = AuthConfig()
