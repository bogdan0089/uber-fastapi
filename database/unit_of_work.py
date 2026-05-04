from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session_maker
from repository.repository_user import RepositoryUser
from repository.repository_trip import RepositoryTrip
from repository.repository_rating import RepositoryRating

class UnitOfWork:
    def __init__(self) -> None:
        self.session: AsyncSession | None = None
        self.session_factory = async_session_maker
        

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = RepositoryUser(self.session)
        self.trip = RepositoryTrip(self.session)
        self.rating = RepositoryRating(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()