from src.modules.auth.models import User
from src.schemas import CustomSchema
from pydantic import Field


class SignInRequest(CustomSchema):
    """
    Schema for a user sign-in request.

    Attributes:
        email (str): The email address of the user trying to sign in.
        password (str): The user's password.
        remember_me (bool): Flag to indicate if the user wants to be remembered (default: False).
    """

    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    remember_me: bool = Field(False, description="Remember me")


class SignUpRequest(CustomSchema):
    """
    Schema for a user sign-up request.

    Attributes:
        full_name (str): The full name of the user.
        email (str): The user's email address.
        password (str): The user's password.
    """

    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")


class UserDetail(CustomSchema):
    """
    Schema representing detailed information about a user.

    Attributes:
        id (int): The unique identifier of the user.
        full_name (str): The user's full name.
        email (str): The user's email address.
        roles (list[str]): A list of role names associated with the user.
    """

    id: int = Field(..., description="User ID")
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email of the user")
    roles: list[str] = Field(..., description="Roles of the user")

    @staticmethod
    def from_model(user: User) -> "UserDetail":
        """
        Create a UserDetail schema instance from a User model instance.

        Args:
            user (User): The User model instance.

        Returns:
            UserDetail: A UserDetail instance containing the user's information.
        """
        return UserDetail(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            roles=[role.name for role in user.roles],
        )


class AuthTokens(CustomSchema):
    """
    Schema representing authentication tokens.

    Attributes:
        access_token (str): The access token for the authenticated session.
        refresh_token (str): The refresh token to obtain a new access token.
    """

    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
