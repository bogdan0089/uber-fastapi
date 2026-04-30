from service.user_service import UserService
from schemas.schemas_user import RegisterUser, UserLogin
from schemas.schemas_token import TokenResponse
from fastapi import APIRouter


router_auth = APIRouter(prefix="/auth")



@router_auth.post("/register")
async def register_user(data: RegisterUser) -> dict:
    return await UserService.register_user(data)

@router_auth.post("/login", response_model=TokenResponse)
async def login(data: UserLogin) -> dict | TokenResponse:
    return await UserService.login_user(data)












