from fastapi import Depends
from src.modules.auth.schemas import UserDetail
from src.modules.auth.constants import UserRole
from src.modules.auth.config import auth_config
from src.utils.jwt_utils import jwt_cookie_security
from src.modules.auth.service import service as auth_service
from src.exceptions import NotAuthenticated, PermissionDenied
from src.utils.jwt_utils import decode_token


def access_token_validation(
    required_roles: list[UserRole] = [],
    forbidden_roles: list[UserRole] = [],
    any_role: list[UserRole] = [],
):
    async def validate_token(token=Depends(jwt_cookie_security)) -> UserDetail:
        payload = decode_token(
            token, auth_config.JWT_ACCESS_SECRET, auth_config.JWT_ALGORITHM
        )
        if not payload:
            raise NotAuthenticated("Invalid or expired access token")

        user_id = payload.get("sub")
        user = await auth_service.get_user(int(user_id))

        # If `any_role` is defined and the user has at least one, the check passes
        if any_role and any(role in user.roles for role in any_role):
            return user

        # Ensure all required roles are present if `any_role` doesn't apply
        if required_roles and not all(role in user.roles for role in required_roles):
            raise PermissionDenied()

        # Deny if any forbidden role is found
        if forbidden_roles and any(role in user.roles for role in forbidden_roles):
            raise PermissionDenied()

        return user

    return validate_token
