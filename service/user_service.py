from schemas.schemas_user import RegisterUser
from core.redis import redis_client
from utils.hash import hash_password
from core.exceptions import (
    UserAlreadyError,
    UsersNotFoundError,
    UserNotFoundError
)
import uuid
from database.unit_of_work import UnitOfWork
from models.models import User



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
            return {
                "message": "Registration Successfuly."
            }
        
    @staticmethod
    async def get_user(user_id: int) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            return user

    @staticmethod
    async def get_users(limit: int, offset: int) -> list[User]:
        async with UnitOfWork() as uow:
            users = await uow.user.get_users(limit, offset)
            if not users:
                raise UsersNotFoundError()
            return users
        

    