from enum import Enum


class UserRole(str, Enum):
    """
    Enum class representing different roles that a user can have.

    :cvar USER: The standard user role.
    :vartype USER: str
    """

    USER = "user"
