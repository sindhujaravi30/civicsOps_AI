from collections.abc import AsyncGenerator
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.app.core.config import get_settings
from backend.app.db.base import Base
from backend.app.db import models


logger = logging.getLogger(__name__)


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        logger.debug("Database session opened")
        try:
            yield session
        finally:
            logger.debug("Database session closed")


async def init_db() -> None:
    logger.info("Initializing database schema")
    logger.debug(
        "Registered database models: %s",
        ", ".join(models.__all__),
    )
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as exc:
        logger.error(
            "Database schema initialization failed error_type=%s",
            type(exc).__name__,
        )
        raise
    logger.info("Database schema initialized")