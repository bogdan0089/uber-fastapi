from schemas.schemas_rating import CreateRating, ResponseRating
from models.models import Rating
from database.unit_of_work import UnitOfWork
from core.exceptions import (
TripNotFoundError,
TripStatusError,
TripsNotFoundError,
UserNotFoundError,
ForbiddenStatus,
RatingAlreadyExistsError
)
from core.enum import Status
from core.redis import redis_client
from pydantic import TypeAdapter


_list_rating_adapter = TypeAdapter(list[ResponseRating])

class ServiceRating:

    @staticmethod
    async def create_rating(data: CreateRating, passenger_id: int, trip_id: int) -> Rating:
        async with UnitOfWork() as uow:
            trip = await uow.trip.get_trip(trip_id)
            if not trip:
                raise TripNotFoundError(trip_id)
            if trip.status != Status.COMPLETED:
                raise TripStatusError(trip_id)
            if trip.passenger_id != passenger_id:
                raise ForbiddenStatus(trip_id)
            existing_rating = await uow.rating.get_rating_by_trip_and_passenger(trip_id, passenger_id)
            if existing_rating is not None:
                raise RatingAlreadyExistsError()
            rating = await uow.rating.create_rating(data, passenger_id, trip_id)
            avg = await uow.rating.get_avg_rating(data.driver_id)
            driver = await uow.user.get_user(data.driver_id)
            await uow.user.update_avg_rating(driver, avg)
            await redis_client.delete(f"driver:{data.driver_id}")
            return rating

    @staticmethod
    async def get_driver_ratings(driver_id: int) -> list[ResponseRating]:
        cached_key = f"driver_id:{driver_id}"
        cached = await redis_client.get(cached_key)
        if cached:
            return _list_rating_adapter.validate_json(cached)
        async with UnitOfWork() as uow:
            driver = await uow.user.get_user(driver_id)
            if not driver:
                raise UserNotFoundError(driver_id)
            driver_ratings = await uow.rating.get_driver_ratings(driver_id)
            if not driver_ratings:
                raise TripsNotFoundError()
            validated = _list_rating_adapter.validate_python(driver_ratings)
            await redis_client.set(
                cached_key, _list_rating_adapter.dump_json(validated),
                ex=60
            )
            return validated
        
    @staticmethod
    async def get_avg_ratings(driver_id: int) -> float:
            cached_key = f"driver:{driver_id}"
            cached = await redis_client.get(cached_key)
            if cached:
                return float(cached)
            async with UnitOfWork() as uow:
                driver = await uow.user.get_user(driver_id)
                if not driver:
                    raise UserNotFoundError(driver_id)
                rating_avg = await uow.rating.get_avg_rating(driver_id)
            await redis_client.set(cached_key, str(rating_avg), ex=300)
            return rating_avg




