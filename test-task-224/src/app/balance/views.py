from datetime import datetime
import uuid
from fastapi import APIRouter, Depends

from src.db.base import get_async_session
from src.app.auth.models import User
from src.app.balance.controllers import BalanceController, TransactionController
from src.app.balance.schemas import PeriodTransactions, TransactionCreate, TransactionRead
from src.auth.manager import current_active_user

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/balance")
async def select_balance_info(
    user: User = Depends(current_active_user), db_session: AsyncSession = Depends(get_async_session)
):
    controller = BalanceController(db_session=db_session)
    return await controller.select(user=user)


@router.get("/transaction", response_model=PeriodTransactions)
async def select_period_transactions(
    start: datetime,
    end: datetime | None = None,
    user: User = Depends(current_active_user),
    db_session: AsyncSession = Depends(get_async_session),
):
    controller = TransactionController(db_session=db_session)
    transactions = await controller.select_for_period(user=user, start=start, end=end)
    return PeriodTransactions(data=list(transactions))


@router.post("/transaction", response_model=TransactionRead)
async def add_transaction(
    transaction: TransactionCreate,
    user: User = Depends(current_active_user),
    db_session: AsyncSession = Depends(get_async_session),
):
    controller = TransactionController(db_session=db_session)
    return await controller.create(tr_data=transaction, user=user)


@router.get("/transaction/{transaction_id}", response_model=TransactionRead)
async def select_transaction_info(
    transaction_id: uuid.UUID,
    user: User = Depends(current_active_user),
    db_session: AsyncSession = Depends(get_async_session),
):
    controller = TransactionController(db_session=db_session)
    return await controller.select(user=user, transaction_id=transaction_id)
