from fastapi import APIRouter
from schemas.schemas_rating import CreateRating, ResponseRating
from models.models import Rating
from service.rating_service import ServiceRating
from utils.dependencies import CurrentPessanger, CurrentClient


router_rating = APIRouter(prefix="/rating")


@router_rating.post("/", response_model=ResponseRating)
async def create_rating(trip_id: int, data: CreateRating, user: CurrentPessanger) -> Rating:
    return await ServiceRating.create_rating(data, user.id, trip_id)

@router_rating.get("/driver/{driver_id}", response_model=list[ResponseRating])
async def get_driver_ratings(driver_id: int, _: CurrentClient) -> list[Rating]:
    return await ServiceRating.get_driver_ratings(driver_id)

@router_rating.get("/driver/{driver_id}/avg",)
async def get_avg_ratings(driver_id: int, _: CurrentClient) -> Rating:
    return await ServiceRating.get_avg_ratings(driver_id)