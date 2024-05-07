from typing import List, Optional
from sqlalchemy import select
from src.utils.db_utils import async_session
from src.modules.auth.constants import UserRole
from src.modules.auth.models import Role, User


class AuthRepository:
    """
    A repository class that provides data access methods for user and role management.
    """

    async def get_roles_by_names(self, names: List[str]) -> List[Role]:
        """
        Retrieve a list of roles by their names.

        :param names: A list of role names to look up.
        :type names: List[str]

        :return: A list of Role objects that match the given names.
        :rtype: List[Role]
        """
        # Query the roles matching the specified names using a SQLAlchemy `select` query.
        async with async_session() as session:
            result = await session.execute(select(Role).where(Role.name.in_(names)))
            # Extract all matching role objects from the query results.
            return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their unique identifier.

        :param user_id: The unique identifier of the user to retrieve.
        :type user_id: int

        :return: The user object if found, or ``None`` if not found.
        :rtype: Optional[User]
        """
        # Query the user table to find a user with the specified `user_id`.
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            # Return the first matching user or `None` if not found.
            return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        :param email: The email address of the user to retrieve.
        :type email: str

        :return: The user object if found, or ``None`` if not found.
        :rtype: Optional[User]
        """
        # Query the user table to find a user with the specified email address.
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            # Return the first matching user or `None` if not found.
            return result.scalars().first()

    async def create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        roles: List[UserRole] = [UserRole.USER],
    ) -> User:
        """
        Create a new user with the specified information.

        :param full_name: The full name of the new user.
        :type full_name: str
        :param email: The email address of the new user.
        :type email: str
        :param password: The plaintext password for the new user.
        :type password: str
        :param roles: A list of user roles to assign to the new user. Defaults to standard user role.
        :type roles: List[UserRole]

        :return: The newly created user object.
        :rtype: User
        """
        # Retrieve the Role objects that correspond to the specified `UserRole` enum values.
        user_roles = await self.get_roles_by_names([role.value for role in roles])
        # Hash the plaintext password using the User model's password hashing method.
        hashed_password = User.hash_password(password)

        # Create a new user instance and commit the transaction to the database.
        async with async_session() as session:
            new_user = User(
                full_name=full_name,
                email=email,
                hashed_password=hashed_password,
                roles=user_roles,
            )
            session.add(new_user)
            # Commit the new user to the database and refresh it to get the updated state.
            await session.commit()
            await session.refresh(new_user)
            return new_user


repository = AuthRepository()
