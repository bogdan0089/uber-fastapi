from service.user_service import UserService
from service.auth_service import AuthService
from schemas.schemas_user import RegisterUser, UserLogin
from schemas.schemas_token import TokenResponse
from fastapi import APIRouter
from utils.dependencies import CurrentClient


router_auth = APIRouter(prefix="/auth", tags=["Auth"])


@router_auth.post("/register", status_code=201)
async def register_user(data: RegisterUser) -> dict:
    return await UserService.register_user(data)

@router_auth.post("/login", response_model=TokenResponse)
async def login(data: UserLogin) -> dict | TokenResponse:
    return await UserService.login_user(data)

@router_auth.get("/verify/{token}")
async def verify_user(token: str):
    return await UserService.verification_email(token)

@router_auth.post("/refresh/{token}")
async def refresh_access_token(token: str) -> str:
    return await AuthService.refresh_access_token(token)

@router_auth.post("/")
async def logout(current_user: CurrentClient) -> dict:
    return await AuthService.logout(current_user.id)






