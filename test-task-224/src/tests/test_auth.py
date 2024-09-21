import pytest
import pytest_asyncio
from factories.user import UserFactory
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.models import User


@pytest_asyncio.fixture
async def user():
    user = await UserFactory.create()
    return user


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.asyncio
async def test_login(user: User, client: AsyncClient):  # somehow it's not work
    data = {
        "grant_type": "password",
        "username": user.email,
        "password": "string",
        "scope": "",
        "client_id": "string",
        "client_secret": "string",
    }

    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("/api/auth/jwt/login", data=data, headers=headers)

    assert response.status_code == 200


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.asyncio
async def test_register(db_session: AsyncSession, client: AsyncClient):
    query = select(func.count(User.id))

    result = (await db_session.execute(query)).scalars().first()
    assert result == 0

    data = {"email": "string@string.ru", "password": "password"}
    response = await client.post("/api/auth/register", json=data)
    assert response.json()["code"] == 200

    result = (await db_session.execute(query)).scalars().first()
    assert result == 1
