from fastapi import APIRouter
from service.user_service import UserService
from utils.dependencies import CurrentPessanger
from schemas.schemas_payment import PaymentMethod


router_payment = APIRouter(prefix="/payment", tags=["Payment"])


@router_payment.post("/method")
async def payment_mathod(current_user: CurrentPessanger, data: PaymentMethod):
    return await UserService.payment_method(current_user, data)
