from fastapi import APIRouter
from service.user_service import UserService
from schemas.schemas_user import ResponseUser, UserUpdate
from schemas.schemas_trip import ResponseTrip
from models.models import User
from utils.dependencies import CurrentClient, CurrentAdmin


router_user = APIRouter(prefix="/user")



@router_user.get("/", response_model=ResponseUser)
async def get_user(user_id: int) -> User:
    return await UserService.get_user(user_id)

@router_user.get("/users", response_model=list[ResponseUser])
async def get_users(_: CurrentAdmin, limit: int = 10, offset: int = 0) -> list[ResponseUser]:
    return await UserService.get_users(limit, offset)

@router_user.patch("/me", response_model=ResponseUser)
async def update_user(data: UserUpdate, current_user: CurrentClient) -> ResponseUser:
    return await UserService.user_update(current_user.id, data, current_user)

@router_user.delete("/me", status_code=204)
async def deactivated_user(current_user: CurrentClient):
    return await UserService.deactive_user(current_user.id, current_user)