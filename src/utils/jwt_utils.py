import datetime
import jwt

from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import Request, Response
from src.modules.auth.config import auth_config


def create_token(data: dict, secret: str, duration: int, algorithm: str) -> str:
    now = datetime.datetime.now()
    return jwt.encode(
        {**data, "exp": now + datetime.timedelta(minutes=duration), "iat": now},
        secret,
        algorithm=algorithm,
    )


def decode_token(token: str, secret: str, algorithm: str) -> Optional[dict]:
    try:
        return jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.PyJWTError:
        return None


class HTTPBearerWithCookie(HTTPBearer):
    async def __check_token_from_cookies(
        self, token_key: str, secret_key: str, request: Request
    ) -> str | None:
        token = request.cookies.get(token_key)
        if not token:
            return None
        return decode_token(token, secret_key, auth_config.JWT_ALGORITHM)

    async def __call__(self, request: Request, response: Response):
        payload = await self.__check_token_from_cookies(
            "access_token", auth_config.JWT_ACCESS_SECRET, request
        )
        if payload:
            return request.cookies.get("access_token")
        else:
            response.delete_cookie(key="access_token")

        refresh_token = await self.__check_token_from_cookies(
            "refresh_token", auth_config.JWT_REFRESH_SECRET, request
        )
        if refresh_token:
            refresh_payload = decode_token(
                refresh_token,
                auth_config.JWT_REFRESH_SECRET,
                auth_config.JWT_ALGORITHM,
            )

            new_token = create_token(
                {
                    "sub": refresh_payload["sub"],
                },
                auth_config.JWT_ACCESS_SECRET,
                auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
                auth_config.JWT_ALGORITHM,
            )

            response.set_cookie(
                key="access_token",
                value=new_token,
                max_age=60 * auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
                httponly=True,
            )
            return new_token
        else:
            response.delete_cookie(key="refresh_token")

        bearer_token = await super().__call__(request)
        if bearer_token:
            return bearer_token.credentials


jwt_cookie_security = HTTPBearerWithCookie(auto_error=False)
