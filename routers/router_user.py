from fastapi import APIRouter
from service.user_service import UserService
from schemas.schemas_user import ResponseUser
from models.models import User



router_user = APIRouter(prefix="/user")



@router_user.get("/", response_model=ResponseUser)
async def get_user(user_id: int) -> User:
    return await UserService.get_user(user_id)