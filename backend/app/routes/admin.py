from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.admin import get_current_admin
from app.dependencies_admin import require_admin
from sqlalchemy.orm import Session
from app.utils.dependencies import get_current_user
from app.redis import redis_client
from app.utils.redis_client import redis_client
import json

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users")
def list_users(
    email: str = Query(...),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return [
        {
            "email": u.email,
            "is_paid": u.is_paid,
            "is_admin": u.is_admin
        }
        for u in users
    ]


@router.post("/grant/{user_id}")
def grant_paid_access(
    user_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    user.is_paid = True
    db.commit()
    return {"message": "Paid access granted"}


@router.post("/revoke/{user_id}")
def revoke_paid_access(
    user_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    user.is_paid = False
    db.commit()
    return {"message": "Paid access revoked"}


@router.post("/signals/refresh")
def refresh_signals(
    email: str = Query(...),
    admin=Depends(require_admin)
):
    redis_client.delete("signals:v1")
    return {"status": "signals cache cleared"}


@router.post("/signals")
def push_signal(symbol: str, action: str, user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    signal = {"symbol": symbol, "action": action}

    redis_client.lpush("live_signals", json.dumps(signal))
    redis_client.ltrim("live_signals", 0, 49)  # keep last 50

    return {"status": "signal pushed", "signal": signal}