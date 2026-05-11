from datetime import datetime, timedelta, timezone
from core.config import settings
import jwt
from core.exceptions import (
UserNotFoundError,
TokenExpiredError,
TokenInvalidError
)
from core.redis import redis_client
from database.unit_of_work import UnitOfWork


class AuthService:

    @staticmethod
    def create_access_token(user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> int:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise UserNotFoundError()
            return int(user_id)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise TokenInvalidError()

    @staticmethod
    def refresh_token(token: str) -> str:
        user_id = AuthService.decode_token(token)
        return AuthService.create_access_token(user_id)
    
