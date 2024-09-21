import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from uuid_extensions import uuid7

from src.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid7)
    # TODO: get


class BaseDatetimeModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
