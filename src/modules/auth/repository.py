from typing import List, Optional
from sqlalchemy import select
from src.utils.db_utils import async_session
from src.modules.auth.constants import UserRole
from src.modules.auth.models import Role, User


class AuthRepository:
    async def get_roles_by_names(self, names: List[str]) -> List[Role]:
        async with async_session() as session:
            result = await session.execute(select(Role).where(Role.name.in_(names)))
            return result.scalars().all()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalars().first()

    async def create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        roles: List[UserRole] = [UserRole.USER],
    ) -> User:
        user_roles = await self.get_roles_by_names([role.value for role in roles])
        hashed_password = User.hash_password(password)
        async with async_session() as session:
            new_user = User(
                full_name=full_name,
                email=email,
                hashed_password=hashed_password,
                roles=user_roles,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user


repository = AuthRepository()
