from datetime import datetime, timedelta, timezone
from core.config import settings
import jwt





class AuthService:

    @staticmethod
    def create_access_token(user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(client_id: int) -> str:
        payload = {
            "sub": str(client_id),
            "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> int:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise ClientNotFoundError()
            return int(user_id)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise TokenInvalidError()

    @staticmethod
    def refresh_token(token: str) -> str:
        client_id = AuthService.decode_token(token)
        return AuthService.create_access_token(client_id)