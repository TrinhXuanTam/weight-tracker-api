import datetime
import jwt

from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import Request, Response
from src.modules.auth.config import auth_config


def create_token(data: dict, secret: str, duration: int, algorithm: str) -> str:
    """
    Create a JWT token with the given payload data, expiration, and algorithm.

    :param data: The payload data to encode into the token.
    :type data: dict
    :param secret: The secret key used to sign the token.
    :type secret: str
    :param duration: The expiration duration in minutes for the token.
    :type duration: int
    :param algorithm: The algorithm used to sign the token (e.g., HS256).
    :type algorithm: str

    :return: The generated JWT token as a string.
    :rtype: str
    """
    now = datetime.datetime.now()
    # Add "exp" (expiration) and "iat" (issued at) claims to the payload and encode.
    return jwt.encode(
        {**data, "exp": now + datetime.timedelta(minutes=duration), "iat": now},
        secret,
        algorithm=algorithm,
    )


def decode_token(token: str, secret: str, algorithm: str) -> Optional[dict]:
    """
    Decode a JWT token, returning the payload if the token is valid.

    :param token: The JWT token to decode.
    :type token: str
    :param secret: The secret key used to verify the token.
    :type secret: str
    :param algorithm: The algorithm used to verify the token (e.g., HS256).
    :type algorithm: str

    :return: The decoded payload if valid, or None if invalid.
    :rtype: Optional[dict]
    """
    try:
        # Decode the token with the specified secret and algorithm.
        return jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.PyJWTError:
        # Handle any JWT errors (e.g., expiration, invalid signature).
        return None


class HTTPBearerWithCookie(HTTPBearer):
    """
    A custom HTTPBearer security scheme that supports JWT tokens via cookies.

    Methods:
        __check_token_from_cookies: Retrieve and decode a token from cookies.
        __call__: Validate and refresh tokens, falling back to HTTP Bearer.
    """

    async def __check_token_from_cookies(
        self, token_key: str, secret_key: str, request: Request
    ) -> str | None:
        """
        Retrieve and decode a JWT token from the request cookies.

        :param token_key: The name of the cookie containing the token.
        :type token_key: str
        :param secret_key: The secret key used to verify the token.
        :type secret_key: str
        :param request: The HTTP request object.
        :type request: Request

        :return: The decoded payload if the token is valid, or None otherwise.
        :rtype: str | None
        """
        # Extract the token from cookies using the specified key.
        token = request.cookies.get(token_key)
        if not token:
            return None

        # Decode the token with the secret and algorithm from the configuration.
        return decode_token(token, secret_key, auth_config.JWT_ALGORITHM)

    async def __call__(self, request: Request, response: Response):
        """
        Validate the access token from cookies, refresh if necessary, or fall back to HTTP Bearer.

        :param request: The incoming HTTP request.
        :type request: Request
        :param response: The outgoing HTTP response.
        :type response: Response

        :return: The valid access token or None if validation fails.
        :rtype: str | None
        """
        # Check if a valid access token is in the cookies; remove if invalid.
        payload = await self.__check_token_from_cookies(
            "access_token", auth_config.JWT_ACCESS_SECRET, request
        )
        if payload:
            return request.cookies.get("access_token")
        else:
            response.delete_cookie(key="access_token")

        # Check if a valid refresh token is available; remove if invalid.
        refresh_token = await self.__check_token_from_cookies(
            "refresh_token", auth_config.JWT_REFRESH_SECRET, request
        )
        if refresh_token:
            # Decode the refresh token payload and create a new access token.
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

            # Set the new access token in the cookies.
            response.set_cookie(
                key="access_token",
                value=new_token,
                max_age=60 * auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
                httponly=True,
            )
            return new_token
        else:
            response.delete_cookie(key="refresh_token")

        # Fall back to the standard HTTP Bearer token if cookies fail.
        bearer_token = await super().__call__(request)
        if bearer_token:
            return bearer_token.credentials


jwt_cookie_security = HTTPBearerWithCookie(auto_error=False)
