from sqlalchemy import Column, ForeignKey, Numeric, SmallInteger, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.app.balance.enums import Currency, TransactionStatus
from src.models import BaseModel


class Balance(BaseModel):
    __tablename__ = "balances"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    currency = Column(SmallInteger, nullable=False, default=Currency.RUB.value)
    amount = Column(Numeric, nullable=False, default=0)
    user = relationship("User", back_populates="balance")


class Transaction(BaseModel):
    __tablename__ = "transactions"

    from_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    to_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(SmallInteger, nullable=False)
    amount = Column(Numeric, nullable=False)
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="expenses")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="incomes")
    created_at = Column(DateTime, server_default=func.now())
    status = Column(SmallInteger, nullable=False, default=TransactionStatus.SUCCESS.value)
    idempotency_key = Column(UUID(as_uuid=True), nullable=False)
