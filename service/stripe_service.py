import stripe
from core.config import settings
import asyncio



stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:

    @staticmethod
    async def charge(amount: float, payment_id: str) -> dict:
        payment = await asyncio.to_thread(
            stripe.PaymentIntent.create,
            amount=int(amount * 100),
            currency="usd",
            payment_method=payment_id,
            confirm=True,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"}
        )
        return {"payment_intent_id": payment.id, "status": payment.status}
