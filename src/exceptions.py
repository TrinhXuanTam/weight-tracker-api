from typing import Any

from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN

    def __init__(self, detail: str = "Permission denied") -> None:
        self.DETAIL = detail
        super().__init__()


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND

    def __init__(self, detail: str = "Entity not found") -> None:
        self.DETAIL = detail
        super().__init__()


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str = "Bad Request") -> None:
        self.DETAIL = detail
        super().__init__()


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED

    def __init__(self, detail: str = "User not authenticated") -> None:
        self.DETAIL = detail
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class BadGateway(DetailedHTTPException):
    STATUS_CODE = status.HTTP_502_BAD_GATEWAY

    def __init__(self, detail: str = "Bad Gateway") -> None:
        self.DETAIL = detail
        super().__init__()


class AlreadyExists(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT

    def __init__(self, detail: str = "Entity already exists") -> None:
        self.DETAIL = detail
        super().__init__()
