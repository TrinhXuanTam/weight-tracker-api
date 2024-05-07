import datetime
from src.config import db_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Any

# Configure the database URL and initialize the async engine.
DATABASE_URL = db_config.DATABASE_URL
engine = create_async_engine(str(DATABASE_URL))

# Create a session factory for asynchronous database sessions.
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """A base class for SQLAlchemy models with common columns and a type mapping.

    Attributes:
        type_annotation_map (dict[str, Any]): Maps Python types to SQLAlchemy types for annotation.
        created_at (Mapped[datetime.datetime]): Timestamp for when the record was created.
        updated_at (Mapped[datetime.datetime]): Timestamp for the last time the record was updated.
    """

    type_annotation_map = {dict[str, Any]: JSON}
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


async def close_db() -> None:
    """Close the asynchronous SQLAlchemy engine, releasing any resources.

    Returns:
        None
    """
    await engine.dispose()
