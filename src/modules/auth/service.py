from typing import List
from src.utils.jwt_utils import create_token
from src.exceptions import AlreadyExists, NotAuthenticated
from src.modules.auth.config import auth_config
from src.modules.auth.schemas import UserDetail, AuthTokens
from src.modules.auth.constants import UserRole
from src.modules.auth.repository import repository as auth_repository


class AuthService:
    async def generate_tokens(self, email: str, password: str) -> AuthTokens:
        user = await auth_repository.get_user_by_email(email)
        if not (user and user.validate_password(password)):
            raise NotAuthenticated("Invalid email or password")
        access_token = create_token(
            data={"sub": user.email},
            secret=auth_config.JWT_ACCESS_SECRET,
            duration=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
            algorithm=auth_config.JWT_ALGORITHM,
        )
        refresh_token = create_token(
            data={"sub": user.email},
            secret=auth_config.JWT_REFRESH_SECRET,
            duration=auth_config.REFRESH_TOKEN_EXPIRE_MINUTES,
            algorithm=auth_config.JWT_ALGORITHM,
        )
        return AuthTokens(access_token=access_token, refresh_token=refresh_token)

    async def create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        roles: List[UserRole] = [UserRole.USER],
    ) -> UserDetail:
        existing_user = await auth_repository.get_user_by_email(email)
        if existing_user:
            raise AlreadyExists("User with this email already exists")

        created_user = await auth_repository.create_user(
            full_name=full_name, email=email, password=password, roles=roles
        )

        return UserDetail.from_model(created_user)


service = AuthService()
