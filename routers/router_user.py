from fastapi import APIRouter
from service.user_service import UserService
from schemas.schemas_user import ResponseUser, UserUpdate
from models.models import User
from utils.dependencies import CurrentUser


router_user = APIRouter(prefix="/user", tags=["User"])


@router_user.get("/", response_model=ResponseUser)
async def get_user(user_id: int, current_user: CurrentUser) -> User:
    return await UserService.get_user(user_id, current_user.id)

@router_user.patch("/me", response_model=ResponseUser)
async def update_user(data: UserUpdate, current_user: CurrentUser) -> ResponseUser:
    return await UserService.user_update(current_user.id, data, current_user)

@router_user.delete("/me", status_code=204)
async def deactivated_user(current_user: CurrentUser):
    return await UserService.deactive_user(current_user.id, current_user)