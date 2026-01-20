from fastapi import APIRouter, Depends, HTTPException
import stripe
import os
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import Request, Header
from app.config import settings
from app.config import STRIPE_SECRET_KEY, STRIPE_PRICE_ID, STRIPE_WEBHOOK_SECRET
from app.routes.auth import get_current_user
from app.database import get_db
from app.database import SessionLocal

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

PRICE_ID = os.getenv("STRIPE_PRICE_ID")
DOMAIN = "http://localhost:5173"  # frontend URL (Vite)

@router.post("/create-checkout")
def create_checkout(
    user=Depends(get_current_user)
):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": STRIPE_PRICE_ID,
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:3000/dashboard",
        cancel_url="http://localhost:3000/subscribe",
        customer_email=user.email,
    )

    return {"checkout_url": checkout_session.url}


@router.post("/billing/create-checkout")
def create_checkout_session(user=Depends(get_current_user)):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "inr",
                "product_data": {"name": "Trading Signals Pro"},
                "unit_amount": 49900,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:5173/success",
        cancel_url="http://localhost:5173/cancel",
        metadata={"user_id": user.id},
    )

    return {"checkout_url": session.url}

processed_events = set()

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    # ✅ PAYMENT SUCCESS
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        customer_email = session.get("customer_details", {}).get("email")

        if customer_email:
            db = SessionLocal()
            user = db.query(User).filter(User.email == customer_email).first()

            if user:
                user.is_paid = True
                db.commit()

            db.close()

    return {"status": "success"}


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        email = session["customer_email"]
        user = db.query(User).filter(User.email == email).first()

        if user:
            user.is_paid = True
            db.commit()

    return {"status": "success"}
