from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.base import container

db_session: ContextVar[AsyncSession] = ContextVar("db_session", default=None)  # TODO: contextvar for multithreading


class DBSession:
    def __init__(self, session) -> None:
        self.session: AsyncSession = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exception_type, exception, traceback):
        if exception:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()


class OldDBSession:
    async def __aenter__(self):
        session_maker = container.resolve(sessionmaker)
        self.session: AsyncSession = session_maker()
        return self.session

    async def __aexit__(self, exception_type, exception, traceback):
        if exception:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
