from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.models import Rating
from schemas.schemas_rating import CreateRating


class RepositoryRating:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_rating(self, data: CreateRating, passenger_id: int, trip_id: int) -> Rating:
        rating = Rating(
            **data.model_dump(),
            passenger_id=passenger_id,
            trip_id=trip_id
            
        )
        self.session.add(rating)
        await self.session.flush()
        await self.session.refresh(rating)
        return rating
    
    async def get_driver_ratings(self, driver_id: int) -> list[Rating]:
        driver_rating = await self.session.execute(
            select(Rating)
            .where(Rating.driver_id == driver_id)
        )
        return driver_rating.scalars().all()
    
    async def get_avg_rating(self, driver_id: int) -> float:
        rating_avg = await self.session.execute(
            select(func.avg(Rating.score))
            .where(Rating.driver_id == driver_id)
        )
        return rating_avg.scalar() or 0.0

    async def get_rating_by_trip_and_passenger(self, trip_id: int, passenger_id: int) -> Rating | None:
        result = await self.session.execute(
            select(Rating)
            .where(Rating.trip_id == trip_id)
            .where(Rating.passenger_id == passenger_id)
        )
        return result.scalar_one_or_none()