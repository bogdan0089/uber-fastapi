from schemas.schemas_trip import TripCreate, ResponseTrip
from database.unit_of_work import UnitOfWork
from models.models import Trip
from core.exceptions import (
TripNotFoundError,
TripsNotFoundError,
TripStatusError
)
from core.redis import redis_client
from core.enum import Status
from utils.price_calculator import price_calculate


class TripService:

    @staticmethod
    async def create_trip(data: TripCreate, pessenger_id: int) -> TripCreate:
        async with UnitOfWork() as uow:
            price = price_calculate(data.pickup_lat, data.pickup_lon, data.dropoff_lat, data.dropoff_lon)
            trip = await uow.trip.create_trip(data, pessenger_id, price)
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
        
    @staticmethod
    async def update_status(trip_id: int, new_status: Status, driver_id: int | None = None) -> Trip:
        async with UnitOfWork() as uow:
            trip = await uow.trip.get_trip(trip_id)
            if not trip:
                raise TripNotFoundError(trip_id)
            allowed_transistion = {
                Status.WAITING: [Status.IN_PROGRESS, Status.CANCELLED],
                Status.IN_PROGRESS: [Status.COMPLETED, Status.CANCELLED],
                Status.COMPLETED: [],
                Status.CANCELLED: []
            }
            if new_status not in allowed_transistion[trip.status]:
                raise TripStatusError()
            if new_status == Status.IN_PROGRESS and driver_id:
                return await uow.trip.accept_trip(trip.id, driver_id)
            return await uow.trip.update_status(trip.id, new_status)
            
        