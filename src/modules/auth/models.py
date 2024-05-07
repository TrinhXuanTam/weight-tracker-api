import bcrypt

from src.utils.db_utils import Base
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Role(Base):
    """
    Represents a role that can be assigned to a user.

    :ivar id: The unique identifier for the role.
    :vartype id: Mapped[int]
    :ivar name: The name of the role.
    :vartype name: Mapped[str]
    """

    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class UserRole(Base):
    """
    Represents a relationship between a user and a role, implementing a many-to-many association.

    :ivar user_id: The unique identifier of the user.
    :vartype user_id: Mapped[int]
    :ivar role_id: The unique identifier of the role.
    :vartype role_id: Mapped[int]
    """

    __tablename__ = "user_role"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True)


class User(Base):
    """
    Represents a user with authentication credentials and assigned roles.

    :ivar id: The unique identifier for the user.
    :vartype id: Mapped[int]
    :ivar full_name: The user's full name.
    :vartype full_name: Mapped[str]
    :ivar email: The user's unique email address.
    :vartype email: Mapped[str]
    :ivar hashed_password: The user's hashed password.
    :vartype hashed_password: Mapped[bytes]
    :ivar roles: A list of roles associated with the user, using a many-to-many relationship.
    :vartype roles: Mapped[List[Role]]
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
        """
        Hash a plaintext password using bcrypt.

        :param password: The plaintext password to hash.
        :type password: str

        :return: The hashed password in bytes.
        :rtype: str
        """
        # Hash the password using bcrypt and return the resulting hash.
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password: str) -> bool:
        """
        Validate a plaintext password against the stored hashed password.

        :param password: The plaintext password to validate.
        :type password: str

        :return: True if the password matches, False otherwise.
        :rtype: bool
        """
        # Check if the provided plaintext password matches the stored hashed password.
        return bcrypt.checkpw(password.encode(), self.hashed_password)
