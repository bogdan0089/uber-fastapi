from schemas.schemas_user import (
RegisterUser,
UserLogin,
ResponseUser,
UserUpdate
)
from core.redis import redis_client
from utils.hash import hash_password, verify_password
from core.exceptions import (
    UserAlreadyError,
    UsersNotFoundError,
    UserNotFoundError,
    PasswordError,
    TokenInvalidError
)
import uuid
from database.unit_of_work import UnitOfWork
from models.models import User
from service.auth_service import AuthService
from tasks.tasks import send_registration_email
from utils.dependencies import CurrentClient
from core.enum import Role
from pydantic import TypeAdapter


_list_users_adapter = TypeAdapter(list[ResponseUser])

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
            await redis_client.set(f"verify:{token}", user.id, ex=86400)
            send_registration_email.delay(data.email, token)
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
            refresh_token = await AuthService.create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

    @staticmethod
    async def get_user(user_id: int, current_user: CurrentClient) -> User:
        cached_key = f"user:{user_id}"
        cached = await redis_client.get(cached_key)
        if cached:
            return ResponseUser.model_validate_json(cached)
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            if current_user.id != user.id and current_user.role != Role.ADMIN:
                raise PermissionError()
        await redis_client.set(cached_key, ResponseUser.model_validate(user).model_dump_json(), ex=60)
        return user

    @staticmethod
    async def get_users(limit: int, offset: int) -> list[ResponseUser]:
        cached_key = f"limit:{limit}:offset:{offset}"
        cached = await redis_client.get(cached_key)
        if cached:
            return _list_users_adapter.validate_json(cached)
        async with UnitOfWork() as uow:
            users = await uow.user.get_users(limit, offset)
            if not users:
                raise UsersNotFoundError()
            validated = _list_users_adapter.validate_python(users)
            await redis_client.set(
                cached_key, _list_users_adapter.dump_json(validated),
                ex=60
            )
            return validated

    @staticmethod
    async def user_update(user_id: int, data: UserUpdate, current_user: User) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            if user.id != current_user.id and current_user.role != Role.ADMIN:
                raise PermissionError()
            user_update = await uow.user.update_user(user, data)
            return user_update
    
    @staticmethod
    async def deactive_user(user_id: int, current_user: User) -> bool:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            if user.id != current_user.id and current_user.role != Role.ADMIN:
                raise PermissionError()
            deactivated_user = await uow.user.deactive_user(user)
            return deactivated_user
        
    @staticmethod
    async def verification_email(token: str) -> dict:
        user_id = await redis_client.get(f"verify:{token}")
        if not user_id:
            raise TokenInvalidError()
        user_id = int(user_id.decode())
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            await uow.user.verify_email(user)
        await redis_client.delete(f"verify:{token}")
        return {"message": "Email verified successfully."}
