from fastapi import APIRouter
from service.user_service import UserService
from utils.dependencies import CurrentPassenger
from schemas.schemas_payment import PaymentMethod


router_payment = APIRouter(prefix="/payment", tags=["Payment"])


@router_payment.post("/method")
async def payment_method(current_user: CurrentPassenger, data: PaymentMethod):
    return await UserService.payment_method(current_user, data)
