from fastapi import Depends
from src.modules.auth.schemas import UserDetail
from src.modules.auth.constants import UserRole
from src.modules.auth.config import auth_config
from src.utils.jwt_utils import jwt_cookie_security, decode_token
from src.modules.auth.service import service as auth_service
from src.exceptions import NotAuthenticated, PermissionDenied


def access_token_validation(
    required_roles: list[UserRole] = [],
    forbidden_roles: list[UserRole] = [],
    any_role: list[UserRole] = [],
):
    """
    Dependency function to validate an access token, with role-based authorization checks.

    :param required_roles: Roles that must be present for the validation to pass.
    :type required_roles: list[UserRole]
    :param forbidden_roles: Roles that should not be present for validation to pass.
    :type forbidden_roles: list[UserRole]
    :param any_role: A list of roles where having any one of them allows validation to pass.
    :type any_role: list[UserRole]

    :return: A dependency function that validates a token and enforces role checks.
    :rtype: Callable

    :raises NotAuthenticated: If the token is invalid or expired.
    :raises PermissionDenied: If the user's roles do not meet the specified conditions.
    """

    async def validate_token(token=Depends(jwt_cookie_security)) -> UserDetail:
        """
        Validate the given JWT token and apply role-based authorization checks.

        :param token: The JWT token extracted from the request's cookies via the ``jwt_cookie_security`` dependency.
        :type token: str

        :return: The authenticated user's detailed information.
        :rtype: UserDetail

        :raises NotAuthenticated: If the token is invalid or expired.
        :raises PermissionDenied: If the user's roles don't meet the required criteria.
        """
        # Decode the access token to get the user ID.
        payload = decode_token(
            token, auth_config.JWT_ACCESS_SECRET, auth_config.JWT_ALGORITHM
        )
        if not payload:
            raise NotAuthenticated("Invalid or expired access token")

        user_id = payload.get("sub")
        # Retrieve the user's details from the service using the decoded user ID.
        user = await auth_service.get_user(int(user_id))

        # If any of the roles in `any_role` are present in the user's roles, pass validation.
        if any_role and any(role in user.roles for role in any_role):
            return user

        # Ensure all required roles are present if no roles from `any_role` apply.
        if required_roles and not all(role in user.roles for role in required_roles):
            raise PermissionDenied()

        # Deny if any forbidden role is found among the user's roles.
        if forbidden_roles and any(role in user.roles for role in forbidden_roles):
            raise PermissionDenied()

        return user

    return validate_token
