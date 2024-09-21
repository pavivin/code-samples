from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from src.db.base import Base

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    email: Mapped[str] = Column(String(length=254), unique=True)
    balance = relationship("Balance", uselist=False, back_populates="user")
    expenses = relationship("Transaction", back_populates="from_user", foreign_keys="Transaction.from_user_id")
    incomes = relationship("Transaction", back_populates="to_user", foreign_keys="Transaction.to_user_id")
