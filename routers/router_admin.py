from fastapi import APIRouter
from schemas.schemas_user import ResponseUser
from schemas.schemas_trip import ResponseTrip
from service.user_service import UserService
from service.trip_service import TripService
from utils.dependencies import CurrentAdmin


router_admin = APIRouter(prefix="/admin", tags=["Admin"])


@router_admin.get("/users", response_model=list[ResponseUser])
async def get_users(_: CurrentAdmin, limit: int = 10, offset: int = 0) -> list[ResponseUser]:
    return await UserService.get_users(limit, offset)

@router_admin.get("/trips", response_model=list[ResponseTrip])
async def get_trips(_: CurrentAdmin, limit: int = 10, offset: int = 0) -> list[ResponseTrip]:
    return await TripService.get_trips(limit, offset)

@router_admin.get("/active/verified", response_model=list[ResponseUser])
async def get_users_for_admin(_: CurrentAdmin, limit: int = 10, offset: int = 0) -> list[ResponseUser]:
    return await UserService.get_users_admin(limit, offset)