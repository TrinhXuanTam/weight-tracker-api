from src.modules.auth.models import User
from src.schemas import CustomSchema
from pydantic import Field


class SignInRequest(CustomSchema):
    """
    Schema for a user sign-in request.

    :ivar email: The email address of the user trying to sign in.
    :vartype email: str
    :ivar password: The user's password.
    :vartype password: str
    :ivar remember_me: Flag to indicate if the user wants to be remembered (default: False).
    :vartype remember_me: bool
    """

    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    remember_me: bool = Field(False, description="Remember me")


class SignUpRequest(CustomSchema):
    """
    Schema for a user sign-up request.

    :ivar full_name: The full name of the user.
    :vartype full_name: str
    :ivar email: The user's email address.
    :vartype email: str
    :ivar password: The user's password.
    :vartype password: str
    """

    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")


class UserDetail(CustomSchema):
    """
    Schema representing detailed information about a user.

    :ivar id: The unique identifier of the user.
    :vartype id: int
    :ivar full_name: The user's full name.
    :vartype full_name: str
    :ivar email: The user's email address.
    :vartype email: str
    :ivar roles: A list of role names associated with the user.
    :vartype roles: list[str]
    """

    id: int = Field(..., description="User ID")
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email of the user")
    roles: list[str] = Field(..., description="Roles of the user")

    @staticmethod
    def from_model(user: User) -> "UserDetail":
        """
        Create a UserDetail schema instance from a User model instance.

        :param user: The User model instance.
        :type user: User

        :return: A UserDetail instance containing the user's information.
        :rtype: UserDetail
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

    :ivar access_token: The access token for the authenticated session.
    :vartype access_token: str
    :ivar refresh_token: The refresh token to obtain a new access token.
    :vartype refresh_token: str
    """

    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
