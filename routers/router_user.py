from fastapi import APIRouter
from service.user_service import UserService
from schemas.schemas_user import ResponseUser
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