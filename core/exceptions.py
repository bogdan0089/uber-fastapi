from fastapi import status


class BaseAppException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class PasswordError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid password"
        )
    
class UserNotFoundError(BaseAppException):
    def __init__(self, user_id: int | None = None, email: str | None = None) -> None:
        if user_id is not None:
            detail = f"Client with id {user_id} not found."
        elif email:
            detail = f"Client with email '{email}' not found."
        else:
            detail = "Client not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class TokenExpiredError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token expired error."
        )

class TokenInvalidError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token Invalid Error."
        )

class UserAlreadyError(BaseAppException):
    def __init__(self, email: str | None = None, user_id: int | None = None) -> None:
        if user_id is not None:
            detail = f"User with id {user_id} is already registered."
        elif email:
            detail = f"User with email '{email}' is already registered."
        else:
            detail = "User is already registered."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UsersNotFoundError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found error."
        )

class DriversNotFoundError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Drivers not found."
        )

class PermissinError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied"
        )

class TripNotFoundError(BaseAppException):
    def __init__(self, trip_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found"
        )
        
class TripsNotFoundError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trips not found."
        )

class TripStatusError(BaseAppException):
    def __init__(self, trip_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Trip {trip_id} error status"
        )
        
class ForbiddenStatus(BaseAppException):
    def __init__(self, trip_id: int):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access to trip {trip_id} is forbidden"
        )

class RatingAlreadyExistsError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rating for this trip already exists"
        )