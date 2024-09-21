from typing import AsyncGenerator
from contextlib import asynccontextmanager

import punq
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()
session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True)

test_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
sc_session = scoped_session(test_session_maker)


class SessionMaker:
    def __new__(cls):
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class TestSessionMaker:
    def __new__(cls):
        return sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


container = punq.Container()
container.register(sessionmaker, SessionMaker)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db_session():
    session = session_maker()
    try:
        yield session
        await session.commit()
    except Exception as e:
        print(e)  # for sure, logging
        await session.rollback()
    finally:
        await session.close()
