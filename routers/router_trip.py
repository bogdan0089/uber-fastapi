from fastapi import APIRouter
from service.trip_service import TripService
from schemas.schemas_trip import TripCreate, ResponseTrip
from schemas.schemas_user import ResponseUser
from utils.dependencies import CurrentPessanger, CurrentClient, CurrentDriver
from models.models import Trip
from core.enum import Status


router_trip = APIRouter(prefix="/trip", tags=["Trip"])



@router_trip.post("/",response_model=ResponseTrip)
async def create_trip(data: TripCreate, user: CurrentPessanger) -> TripCreate:
    return await TripService.create_trip(data, user.id)

@router_trip.get("/", response_model=list[ResponseTrip])
async def get_available(_: CurrentDriver, limit: int = 10, offset: int = 0, ) -> list[ResponseTrip]:
    return await TripService.get_available(limit, offset)

@router_trip.get("/my", response_model=list[ResponseTrip])
async def get_my_trips(user: CurrentClient, limit: int = 10, offset: int = 0) -> list[ResponseTrip]:
    return await TripService.get_my_trips(user.id, limit, offset)

@router_trip.get("/{trip_id}", response_model=ResponseTrip)
async def get_trip(trip_id: int, _: CurrentClient) -> Trip:
    return await TripService.get_trip(trip_id)

@router_trip.get("/", response_model=list[ResponseTrip])
async def get_trips(limit: int = 10, offset: int = 0) -> list[ResponseTrip]:
    return await TripService.get_trips(limit, offset)

@router_trip.post("/{trip_id}/accept", response_model=ResponseTrip)
async def accept_trip(trip_id: int, user: CurrentDriver) -> ResponseTrip:
    return await TripService.update_status(trip_id, Status.IN_PROGRESS, user.id)

@router_trip.post("/{trip_id}/completed", response_model=ResponseTrip)
async def completed_trip(trip_id: int, user: CurrentDriver) -> ResponseTrip:
    return await TripService.update_status(trip_id, Status.COMPLETED, user.id)

@router_trip.post("/{trip_id}/cancel", response_model=ResponseTrip)
async def cancel_trip(trip_id: int, user: CurrentClient) -> ResponseTrip:
    return await TripService.update_status(trip_id, Status.CANCELLED, user.id)