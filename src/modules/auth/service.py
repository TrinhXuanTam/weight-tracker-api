from typing import List
from src.utils.jwt_utils import create_token
from src.exceptions import AlreadyExists, NotAuthenticated, NotFound
from src.modules.auth.config import auth_config
from src.modules.auth.schemas import UserDetail, AuthTokens
from src.modules.auth.constants import UserRole
from src.modules.auth.repository import repository as auth_repository


class AuthService:
    """
    A service class that handles user authentication, user retrieval, and account creation.
    """

    async def generate_tokens(self, email: str, password: str) -> AuthTokens:
        """
        Generate access and refresh tokens for a user if the credentials are valid.

        Args:
            email (str): The email address of the user.
            password (str): The plaintext password of the user.

        Returns:
            AuthTokens: An object containing the access and refresh tokens.

        Raises:
            NotAuthenticated: If the user does not exist or the password is incorrect.
        """
        # Retrieve user by email; validate that the user exists and their password is correct.
        user = await auth_repository.get_user_by_email(email)
        if not (user and user.validate_password(password)):
            raise NotAuthenticated("Invalid email or password")

        # Generate an access token using the user's ID as the subject, and configured expiration time.
        access_token = create_token(
            data={"sub": user.id},
            secret=auth_config.JWT_ACCESS_SECRET,
            duration=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
            algorithm=auth_config.JWT_ALGORITHM,
        )

        # Generate a refresh token with a longer expiration time.
        refresh_token = create_token(
            data={"sub": user.id},
            secret=auth_config.JWT_REFRESH_SECRET,
            duration=auth_config.REFRESH_TOKEN_EXPIRE_MINUTES,
            algorithm=auth_config.JWT_ALGORITHM,
        )

        # Return both tokens as an AuthTokens object.
        return AuthTokens(access_token=access_token, refresh_token=refresh_token)

    async def get_user(self, user_id: int) -> UserDetail:
        """
        Retrieve user details by user ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            UserDetail: An object containing detailed information about the user.

        Raises:
            NotFound: If the user with the given ID is not found.
        """
        # Retrieve user by their unique ID; raise an exception if the user isn't found.
        user = await auth_repository.get_user_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        # Convert the user model to the UserDetail schema for response purposes.
        return UserDetail.from_model(user)

    async def create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        roles: List[UserRole] = [UserRole.USER],
    ) -> UserDetail:
        """
        Create a new user with the specified details.

        Args:
            full_name (str): The full name of the new user.
            email (str): The email address of the new user.
            password (str): The plaintext password for the new user.
            roles (List[UserRole]): A list of roles to assign to the user. Defaults to a standard user role.

        Returns:
            UserDetail: An object containing detailed information about the newly created user.

        Raises:
            AlreadyExists: If a user with the provided email address already exists.
        """
        # Check if a user with the provided email address already exists.
        existing_user = await auth_repository.get_user_by_email(email)
        if existing_user:
            raise AlreadyExists("User with this email already exists")

        # Create the new user with the specified attributes in the database.
        created_user = await auth_repository.create_user(
            full_name=full_name, email=email, password=password, roles=roles
        )

        # Convert the created user model to the UserDetail schema for the response.
        return UserDetail.from_model(created_user)


service = AuthService()
