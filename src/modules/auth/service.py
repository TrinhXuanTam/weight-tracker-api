from typing import List
from src.exceptions import AlreadyExists
from src.modules.auth.schemas import UserDetail
from src.modules.auth.constants import UserRole
from src.modules.auth.repository import repository as auth_repository


class AuthService:
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
