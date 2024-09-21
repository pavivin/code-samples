from sqlalchemy.ext.asyncio import AsyncSession


class BaseDBController:
    default_timeout = 60

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session: AsyncSession = db_session
