import datetime
from src.config import db_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Any

DATABASE_URL = db_config.DATABASE_URL

engine = create_async_engine(str(DATABASE_URL))

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def close_db() -> None:
    await engine.dispose()
