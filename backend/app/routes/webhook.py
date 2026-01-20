import stripe, os
import redis
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from app.database import get_db
from app.models.user import User
from app.config import settings
from app.database import SessionLocal

router = APIRouter()

stripe.api_key = settings.STRIPE_SECRET_KEY
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    # ✅ PAYMENT SUCCESS
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session["customer_details"]["email"]

        db: Session = SessionLocal()
        user = db.query(User).filter(User.email == email).first()

        if user:
            user.is_paid = True
            db.commit()

    return {"status": "success"}