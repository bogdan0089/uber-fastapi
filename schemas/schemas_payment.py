from pydantic import BaseModel


class PaymentMethod(BaseModel):
    payment_id: str
