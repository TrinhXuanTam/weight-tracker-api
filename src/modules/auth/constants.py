from enum import Enum


class UserRole(str, Enum):
    """Enum class representing different roles that a user can have.

    Attributes:
        USER (str): The standard user role.
    """

    USER = "user"
