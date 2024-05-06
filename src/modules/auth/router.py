from fastapi import APIRouter
from src.modules.auth.schemas import SignUpRequest
from src.modules.auth.service import service as auth_service

router: APIRouter = APIRouter()


@router.post("/sign-in")
async def sign_in():
    pass


@router.post("/sign-up")
async def sign_up(body: SignUpRequest):
    return await auth_service.create_user(**body.dict())
