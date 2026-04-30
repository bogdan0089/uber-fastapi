from schemas.schemas_user import RegisterUser, UserLogin, ResponseUser
from core.redis import redis_client
from utils.hash import hash_password, verify_password
from core.exceptions import (
    UserAlreadyError,
    UsersNotFoundError,
    UserNotFoundError,
    PasswordError
)
import uuid
from database.unit_of_work import UnitOfWork
from models.models import User
from service.auth_service import AuthService
from tasks.tasks import send_registration_email


class UserService:

    @staticmethod
    async def register_user(data: RegisterUser) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user_email(email=data.email)
            if user:
                raise UserAlreadyError(email=data.email)
            hashed = hash_password(data.password)
            user = await uow.user.register_user(
                data,
                hashed=hashed
            )
            token = str(uuid.uuid4())
            await redis_client.set(f"verify:{token}", user.id, ex=1000)
            send_registration_email.delay(data.email)
            return {
                "message": "Registration Successfuly."
            }
        
    @staticmethod
    async def login_user(data: UserLogin) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user_email(email=data.email)
            if not user:
                raise UserNotFoundError(data.email)
            if not verify_password(data.password, user.hashed_password):
                raise PasswordError()
            access_token = AuthService.create_access_token(user.id)
            refresh_token = AuthService.create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

    @staticmethod
    async def get_user(user_id: int) -> User:
        cached_key = f"user:{user_id}"
        cached = await redis_client.get(cached_key)
        if cached:
            return ResponseUser.model_validate_json(cached)
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise UserNotFoundError(user_id)
        await redis_client.set(cached_key, ResponseUser.model_validate(user).model_dump_json(), ex=300)
        return user

    @staticmethod
    async def get_users(limit: int, offset: int) -> list[User]:
        async with UnitOfWork() as uow:
            users = await uow.user.get_users(limit, offset)
            if not users:
                raise UsersNotFoundError()
            return users
        

    