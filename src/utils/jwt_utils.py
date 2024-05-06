import datetime
import jwt


def create_token(data: dict, secret: str, duration: int, algorithm: str) -> str:
    now = datetime.datetime.now()
    return jwt.encode(
        {**data, "exp": now + datetime.timedelta(minutes=duration), "iat": now},
        secret,
        algorithm=algorithm,
    )


def decode_token(token: str, secret: str, algorithm: str) -> dict:
    return jwt.decode(token, secret, algorithms=[algorithm])
