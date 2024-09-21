import asyncio
from datetime import date
import uuid
from sqlalchemy import or_, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from src.app.core.exceptions import BadRequestError, NotFoundError, ServerError
from src.app.core.controller import BaseDBController
from src.app.auth.models import User
from src.app.balance.models import Balance, Transaction
from src.app.balance.schemas import TransactionCreate

from src.db.connection import DBSession


class TransactionController(BaseDBController):
    async def _select_block_balance(self, user_id: uuid.UUID, retries=3, delay=1):
        for attempt in range(retries):
            try:
                stmt = select(Balance).where(Balance.user_id == user_id)
                result = (
                    await self.db_session.execute(
                        stmt.with_for_update(),
                        execution_options={"timeout": 5},
                    )
                ).scalar_one()
                return result
            except OperationalError as e:
                if "deadlock" in str(e.orig).lower() and attempt < retries - 1:
                    await asyncio.sleep(delay)  # Wait before retrying
                    continue
                else:
                    raise ServerError(message="Something went wrong. Try again")
            except NoResultFound:
                raise NotFoundError(message="User Not Found")

    async def create(self, tr_data: TransactionCreate, user: User):
        async with DBSession(self.db_session):
            # Check for idempotency
            result = await self.db_session.execute(
                select(Transaction).where(Transaction.idempotency_key == tr_data.idempotency_key)
            )
            existing_transaction = result.scalar_one_or_none()
            if existing_transaction:
                return existing_transaction

            from_user_balance = await self._select_block_balance(user_id=user.id)

            if from_user_balance.amount - tr_data.amount < 0:
                raise BadRequestError(message="Not sufficient balance")

            to_user_balance = None
            if tr_data.user_id:
                to_user_balance = await self._select_block_balance(user_id=tr_data.user_id)

            from_user_balance.amount = from_user_balance.amount - tr_data.amount
            if to_user_balance:
                to_user_balance.amount = to_user_balance.amount + tr_data.amount

            transaction = Transaction(
                from_user_id=user.id,
                to_user_id=tr_data.user_id,
                type=tr_data.type.value,
                amount=tr_data.amount,
                idempotency_key=tr_data.idempotency_key,
            )
            self.db_session.add(transaction)
            self.db_session.refresh(transaction)
            return transaction

    async def select(self, transaction_id: uuid.UUID, user: User):
        async with DBSession(self.db_session):
            stmt = select(Transaction).where(Transaction.id == transaction_id)
            try:
                transaction = (await self.db_session.execute(stmt)).scalar_one()
            except NoResultFound:
                raise NotFoundError(message="Transaction Not Found")

            if not (transaction.from_user_id != user.id or transaction.to_user_id != user.id):
                raise NotFoundError(message="Transaction Not Found")

            return transaction

    async def select_for_period(self, user: User, start: date, end: date = None):
        async with DBSession(self.db_session):
            stmt = select(Transaction).where(  # there might be filters for income operations
                or_(Transaction.to_user_id == user.id, Transaction.from_user_id == user.id)
            )
            if end:
                stmt.where(Transaction.created_at.between(start, end))
            else:
                stmt.where(Transaction.created_at >= start)
            transactions = (await self.db_session.execute(stmt)).scalars()
            return transactions


class BalanceController(BaseDBController):
    async def _select_non_block_balance(self, user_id):
        query = select(Balance).where(Balance.user_id == user_id)
        result = (await self.db_session.execute(query)).scalar_one()
        return result

    async def select(self, user: User):
        async with DBSession(self.db_session):
            return await self._select_non_block_balance(user_id=user.id)
