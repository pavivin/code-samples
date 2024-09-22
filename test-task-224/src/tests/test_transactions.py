import uuid
import pytest
import pytest_asyncio
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.balance.enums import TransactionType
from src.app.balance.models import Balance
from src.app.balance.schemas import TransactionCreate
from factories.user import UserFactory
from httpx import AsyncClient

from src.app.auth.models import User
from src.tests.base import get_user_headers


async def update_balance(amount: float, user_id: uuid.UUID, db_session: AsyncSession):
    stmt = update(Balance).where(Balance.user_id == user_id).values(amount=amount)
    await db_session.execute(stmt)


@pytest_asyncio.fixture
async def user_from(db_session: AsyncSession):  # might be moved to base file with different balances
    user: User = await UserFactory.create()
    await update_balance(amount=100, user_id=user.id, db_session=db_session)
    return user


@pytest_asyncio.fixture
async def user_to():
    user = await UserFactory.create()
    return user


@pytest.mark.parametrize("amount", [100, 0, -100])
@pytest.mark.asyncio
async def test_transaction_create(
    user_from: User, user_to: User, amount: int, client: AsyncClient, db_session: AsyncSession
):
    user_from_balance = user_from.balance  # save previous balances, might be coping issues
    user_to_balance = user_to.balance

    headers = await get_user_headers(user=user_from)

    data = TransactionCreate(user_id=user_to.id, amount=amount, type=TransactionType.TRANSFER.value)
    response = await client.post("/api/transaction", json=data.json(), headers=headers)

    assert response.status_code == 200

    db_session.refresh()  # refresh data from database

    assert user_from_balance == user_from.balance - amount
    assert user_to_balance == user_to.balance + amount
