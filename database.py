from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from config import settings
from models import Base


async_engine = create_async_engine(
    settings.DB_CONNECTION_URI,
    echo=True
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await async_engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async_session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
