from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from models.models import User
from database.unit_of_work import UnitOfWork
from service.auth_service import AuthService
from core.exceptions import (
UserNotFoundError,
PermissinError,
)
from typing import Annotated
from core.enum import Role


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user_login")


async def get_current_user(token: str = Depends(oauth_scheme)) -> User:
    user_id = AuthService.decode_token(token)
    async with UnitOfWork() as uow:
        user = await uow.user.get_user(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user
    
CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_pessanger(user: CurrentUser) -> User:
    if user.role != Role.PASSENGER:
        raise PermissinError()
    return user


CurrentPessanger = Annotated[User, Depends(require_pessanger)]


async def require_driver(user: CurrentUser) -> User:
    if user.role != Role.DRIVER:
        raise PermissinError()
    return user


CurrentDriver = Annotated[User, Depends(require_driver)]


async def require_admin(user: CurrentUser) -> User:
    if user.role != Role.ADMIN:
        raise PermissinError()
    return user

CurrentAdmin = Annotated[User, Depends(require_admin)]