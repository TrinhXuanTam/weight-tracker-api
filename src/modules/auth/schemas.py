from src.modules.auth.models import User
from src.schemas import CustomSchema
from pydantic import Field


class SignUpRequest(CustomSchema):
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")


class UserDetail(CustomSchema):
    id: int = Field(..., description="User ID")
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Email of the user")
    roles: list[str] = Field(..., description="Roles of the user")

    @staticmethod
    def from_model(user: User) -> "UserDetail":
        return UserDetail(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            roles=[role.name for role in user.roles],
        )
