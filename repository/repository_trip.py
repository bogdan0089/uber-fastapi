from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from models.models import Trip, User
from schemas.schemas_trip import TripCreate
from core.enum import Status


class RepositoryTrip:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_trip(self, data: TripCreate, passenger_id: int) -> TripCreate:
        trip = Trip(
            passenger_id=passenger_id,
            **data.model_dump()
        )
        self.session.add(trip)
        await self.session.flush()
        await self.session.refresh(trip)
        return trip
            
    async def get_trip(self, trip_id: int) -> Trip | None:
        result = await self.session.execute(
            select(Trip)
            .where(Trip.id == trip_id)
        )    
        return result.scalars().first()

    async def get_trips(self, limit: int, offset: int) -> list[Trip]:
        result = await self.session.execute(
            select(Trip)
            .limit(limit).offset(offset)
        )
        return result.scalars().all()
    
    async def get_available(self, limit: int, offset: int) -> list[Trip]:
        result = await self.session.execute(
            select(Trip)
            .where(Trip.status == Status.waiting)
            .limit(limit).offset(offset)
        )
        return result.scalars().all()
    
    async def get_my_trips(self, user_id: int, limit: int, offset: int) -> list[Trip]:
        result = await self.session.execute(
            select(Trip)
            .where(
                (Trip.passenger_id == user_id) | (Trip.driver_id == user_id)
            ).limit(limit).offset(offset)
        )
        return result.scalars().all()
    
    async def update_status(self, trip_id: int, status: Status) -> Trip:
        await self.session.execute(
            update(Trip)
            .where(Trip.id == trip_id)
            .values(status=status)
        )
        await self.session.flush()
        return await self.get_trip(trip_id)
    
    async def accept_trip(self, trip_id: int, driver_id: int) -> Trip:
        await self.session.execute(
            update(Trip)
            .where(Trip.id == trip_id)
            .values(driver_id=driver_id, status=Status.in_progress)
        )
        await self.session.flush()
        return await self.get_trip(trip_id)
