from datetime import datetime
from decimal import Decimal
import uuid

from src.app.core.protocol import BaseModel
from .enums import TransactionType


class TransactionCreate(BaseModel):
    user_id: uuid.UUID = None
    amount: Decimal
    type: TransactionType
    idempotency_key: uuid.UUID


class TransactionRead(BaseModel):
    id: uuid.UUID
    amount: Decimal
    type: TransactionType
    from_user_id: uuid.UUID
    to_user_id: uuid.UUID
    created_at: datetime


class PeriodTransactions(BaseModel):
    data: list[TransactionRead]


class BalanceRead(BaseModel):
    currency: int  # TODO: auto int -> enum converter
    amount: Decimal
