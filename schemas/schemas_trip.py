from pydantic import BaseModel, ConfigDict
from core.enum import Status
from datetime import datetime


class TripCreate(BaseModel):
    pickup_address: str
    dropoff_address: str
    pickup_lat: float
    pickup_lon: float
    dropoff_lat: float
    dropoff_lon: float

class ResponseTrip(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    passenger_id: int
    driver_id: int | None
    status: Status
    pickup_address: str
    dropoff_address: str
    created_at: datetime
    price: float