from fastapi import APIRouter, Response, status, Depends
from src.modules.auth.config import auth_config
from src.modules.auth.schemas import (
    SignUpRequest,
    SignInRequest,
    AuthTokens,
    UserDetail,
)
from src.modules.auth.service import service as auth_service
from src.modules.auth.dependencies import access_token_validation

router: APIRouter = APIRouter()


@router.get("/me")
async def get_me(user: UserDetail = Depends(access_token_validation())) -> UserDetail:
    """
    Get the details of the authenticated user.

    Args:
        user (UserDetail): The authenticated user's information, retrieved via the
                           `access_token_validation` dependency.

    Returns:
        UserDetail: The authenticated user's detailed information.
    """
    return user


@router.post("/sign-in")
async def sign_in(body: SignInRequest, response: Response) -> AuthTokens:
    """
    Sign in the user with the provided email and password.

    Args:
        body (SignInRequest): The sign-in request containing the user's email, password,
                              and an optional "remember_me" flag.
        response (Response): The HTTP response object to set authentication cookies.

    Returns:
        AuthTokens: The generated access and refresh tokens for the authenticated user.
    """
    # Generate the access and refresh tokens.
    tokens = await auth_service.generate_tokens(body.email, body.password)
    access_token_age = None
    refresh_token_age = None

    # Set the token age based on the "remember_me" flag.
    if body.remember_me:
        access_token_age = 60 * auth_config.ACCESS_TOKEN_EXPIRE_MINUTES
        refresh_token_age = 60 * auth_config.REFRESH_TOKEN_EXPIRE_MINUTES

    # Set the authentication cookies.
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        max_age=access_token_age,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=refresh_token_age,
        httponly=True,
    )
    return tokens


@router.post("/sign-up")
async def sign_up(body: SignUpRequest) -> UserDetail:
    """
    Register a new user with the given sign-up details.

    Args:
        body (SignUpRequest): The sign-up request containing the new user's information.

    Returns:
        UserDetail: The newly created user's detailed information.
    """
    return await auth_service.create_user(**body.dict())


@router.post("/sign-out", status_code=status.HTTP_204_NO_CONTENT)
async def sign_out(response: Response) -> None:
    """
    Sign out the user by deleting authentication cookies.

    Args:
        response (Response): The HTTP response object to remove authentication cookies.

    Returns:
        None
    """
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
