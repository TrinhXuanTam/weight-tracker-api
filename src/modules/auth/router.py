from fastapi import APIRouter, Response
from src.modules.auth.config import auth_config
from src.modules.auth.schemas import SignUpRequest, SignInRequest, AuthTokens
from src.modules.auth.service import service as auth_service

router: APIRouter = APIRouter()


@router.post("/sign-in")
async def sign_in(body: SignInRequest, response: Response) -> AuthTokens:
    tokens = await auth_service.generate_tokens(body.email, body.password)
    access_token_age = None
    refresh_token_age = None

    if body.remember_me:
        access_token_age = 60 * auth_config.ACCESS_TOKEN_EXPIRE_MINUTES
        refresh_token_age = 60 * auth_config.REFRESH_TOKEN_EXPIRE_MINUTES

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
async def sign_up(body: SignUpRequest):
    return await auth_service.create_user(**body.dict())


@router.post("/sign-out")
async def sign_out(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
