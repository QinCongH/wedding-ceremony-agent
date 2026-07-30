from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Agent 层 SQLite
engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 服务层 MySQL
mysql_engine = create_async_engine(settings.MYSQL_DATABASE_URL, echo=False)
mysql_async_session = async_sessionmaker(mysql_engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def get_mysql_db():
    async with mysql_async_session() as session:
        yield session
