import bcrypt

from src.utils.db_utils import Base
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Role(Base):
    """Represents a role that can be assigned to a user.

    Attributes:
        id (Mapped[int]): The unique identifier for the role.
        name (Mapped[str]): The name of the role.
    """

    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class UserRole(Base):
    """Represents a relationship between a user and a role, implementing a many-to-many association.

    Attributes:
        user_id (Mapped[int]): The unique identifier of the user.
        role_id (Mapped[int]): The unique identifier of the role.
    """

    __tablename__ = "user_role"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True)


class User(Base):
    """Represents a user with authentication credentials and assigned roles.

    Attributes:
        id (Mapped[int]): The unique identifier for the user.
        full_name (Mapped[str]): The user's full name.
        email (Mapped[str]): The user's unique email address.
        hashed_password (Mapped[bytes]): The user's hashed password.
        roles (Mapped[List[Role]]): A list of roles associated with the user, using a many-to-many relationship.
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[bytes] = mapped_column(nullable=True)
    roles: Mapped[List[Role]] = relationship(
        secondary=UserRole.__tablename__, lazy="joined"
    )

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plaintext password using bcrypt.

        Args:
            password (str): The plaintext password to hash.

        Returns:
            str: The hashed password in bytes.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password: str) -> bool:
        """Validate a plaintext password against the stored hashed password.

        Args:
            password (str): The plaintext password to validate.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), self.hashed_password)
