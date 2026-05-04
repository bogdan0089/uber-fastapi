from pydantic import BaseModel


class CreateRating(BaseModel):
    driver_id: int
    score: int


class ResponseRating(BaseModel):
    trip_id: int
    passenger_id: int
    driver_id: int
    score: int
