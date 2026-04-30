from schemas.schemas_trip import TripCreate, ResponseTrip
from database.unit_of_work import UnitOfWork
from models.models import Trip
from core.exceptions import (
TripNotFoundError,
TripsNotFoundError
)
from core.redis import redis_client




class TripService:

    @staticmethod
    async def create_trip(data: TripCreate, pessenger_id: int) -> TripCreate:
        async with UnitOfWork() as uow:
            trip = await uow.trip.create_trip(data, pessenger_id)
            return trip

    @staticmethod
    async def get_trip(trip_id: int) -> Trip:
            cached_key = f"trip:{trip_id}"
            cached = await redis_client.get(cached_key)
            if cached:
                return ResponseTrip.model_validate_json(cached)
            async with UnitOfWork() as uow:
                trip = await uow.trip.get_trip(trip_id)
                if not trip:
                    raise TripNotFoundError(trip_id)
            await redis_client.set(cached_key, ResponseTrip.model_validate(trip).model_dump_json(), ex=300)
            return trip
    
    @staticmethod
    async def get_trips(limit: int, offset: int) -> list[Trip]:
        async with UnitOfWork() as uow:
            trips = await uow.trip.get_trips(limit, offset)
            if not trips:
                raise TripsNotFoundError()
            return trips
        
    @staticmethod
    async def get_available(limit: int, offset: int) -> list[Trip]:
        async with UnitOfWork() as uow:
            waiting_trips = await uow.trip.get_available(limit, offset)
            if not waiting_trips:
                raise TripsNotFoundError()
            return waiting_trips

    @staticmethod
    async def get_my_trips(user_id: int, limit: int, offset: int) -> list[Trip]:
        async with UnitOfWork() as uow:
            my_trips = await uow.trip.get_my_trips(user_id, limit, offset)
            if not my_trips:
                raise TripsNotFoundError()
            return my_trips
        