import datetime
import jwt

from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import Request, Response
from src.modules.auth.config import auth_config


def create_token(data: dict, secret: str, duration: int, algorithm: str) -> str:
    """Create a JWT token with the given payload data, expiration, and algorithm.

    Args:
        data (dict): The payload data to encode into the token.
        secret (str): The secret key used to sign the token.
        duration (int): The expiration duration in minutes for the token.
        algorithm (str): The algorithm used to sign the token (e.g., HS256).

    Returns:
        str: The generated JWT token as a string.
    """
    now = datetime.datetime.now()
    # Add "exp" (expiration) and "iat" (issued at) claims to the payload and encode.
    return jwt.encode(
        {**data, "exp": now + datetime.timedelta(minutes=duration), "iat": now},
        secret,
        algorithm=algorithm,
    )


def decode_token(token: str, secret: str, algorithm: str) -> Optional[dict]:
    """Decode a JWT token, returning the payload if the token is valid.

    Args:
        token (str): The JWT token to decode.
        secret (str): The secret key used to verify the token.
        algorithm (str): The algorithm used to verify the token (e.g., HS256).

    Returns:
        Optional[dict]: The decoded payload if valid, or None if invalid.
    """
    try:
        # Decode the token with the specified secret and algorithm.
        return jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.PyJWTError:
        # Handle any JWT errors (e.g., expiration, invalid signature).
        return None


class HTTPBearerWithCookie(HTTPBearer):
    """A custom HTTPBearer security scheme that supports JWT tokens via cookies.

    Methods:
        __check_token_from_cookies: Retrieve and decode a token from cookies.
        __call__: Validate and refresh tokens, falling back to HTTP Bearer.
    """

    async def __check_token_from_cookies(
        self, token_key: str, secret_key: str, request: Request
    ) -> Optional[str]:
        """Retrieve and decode a JWT token from the request cookies.

        Args:
            token_key (str): The name of the cookie containing the token.
            secret_key (str): The secret key used to verify the token.
            request (Request): The HTTP request object.

        Returns:
            Optional[str]: The decoded payload if the token is valid, or None otherwise.
        """
        # Extract the token from cookies using the specified key.
        token = request.cookies.get(token_key)
        if not token:
            return None

        # Decode the token with the secret and algorithm from the configuration.
        return decode_token(token, secret_key, auth_config.JWT_ALGORITHM)

    async def __call__(self, request: Request, response: Response) -> Optional[str]:
        """Validate the access token from cookies, refresh if necessary, or fall back to HTTP Bearer.

        Args:
            request (Request): The incoming HTTP request.
            response (Response): The outgoing HTTP response.

        Returns:
            Optional[str]: The valid access token or None if validation fails.
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
            new_token = create_token(
                {
                    "sub": refresh_token["sub"],
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
