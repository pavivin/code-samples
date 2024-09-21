from asyncio import get_event_loop_policy
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker

from main import app
from src.db import Base
from src.db.base import TestSessionMaker, container, test_engine, test_session_maker


@pytest.fixture(scope="session")
def event_loop():
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_db():
    # Clears previous tables in db and creates new ones
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield


@pytest_asyncio.fixture
async def db_session(prepare_db):
    async with test_session_maker() as session:
        yield session


@pytest.fixture
def client() -> Generator[None, None, AsyncClient]:
    container.register(sessionmaker, TestSessionMaker)
    yield AsyncClient(app=app, base_url="http://test")


# @pytest_asyncio.fixture
# async def token() -> AsyncSession:
#     user = await UserFactory.create()
#     access_token, _ = create_access_token(TokenData(sub=str(user.id), email=user.email, role=user.role))
#     return access_token
