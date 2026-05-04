from schemas.schemas_rating import CreateRating
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
            return rating

    @staticmethod
    async def get_driver_ratings(driver_id: int) -> list[Rating]:
        async with UnitOfWork() as uow:
            driver = await uow.user.get_user(driver_id)
            if not driver:
                raise UserNotFoundError(driver_id)
            driver_ratings = await uow.rating.get_driver_ratings(driver_id)
            if not driver_ratings:
                raise TripsNotFoundError()
            return driver_ratings
        
    @staticmethod
    async def get_avg_ratings(driver_id: int) -> float:
        async with UnitOfWork() as uow:
            driver = await uow.user.get_user(driver_id)
            if not driver:
                raise UserNotFoundError(driver_id)
            rating_avg = await uow.rating.get_avg_rating(driver_id)
            return rating_avg




