from fastapi import APIRouter, Depends, Query
from app.utils.dependencies import get_current_user
from app.utils.redis_client import redis_client
from app.services.signals import get_mock_signals
from app.utils.auth import get_current_paid_user
from app.services.signals_engine import generate_signals
from app.dependencies import require_paid_user
import json

router = APIRouter(prefix="/signals", tags=["signals"])

CACHE_KEY = "signals:v1"
CACHE_TTL = 50  # 5 minutes

# @router.get("")
# def get_signals(user=Depends(get_current_user)):
#     # 1. Try Redis cache
#     cached = redis_client.get(CACHE_KEY)
#     if cached:
#         signals = json.loads(cached)
#     else:
#         # 2. Generate new signals
#         signals = get_mock_signals()
#         redis_client.setex(CACHE_KEY, CACHE_TTL, json.dumps(signals))

#     # 3. Access control
#     if not user.is_paid:
#         return {
#             "type": "free",
#             "signals": signals[:2]
#         }

#     return {
#         "type": "paid",
#         "signals": signals
#     }

@router.get("")
def get_signals(user=Depends(get_current_user)):
    cached = redis_client.lrange("live_signals", 0, -1)

    signals = [json.loads(s) for s in cached]

    if not user.is_paid:
        return {"signals": signals[:2]}

    return {"signals": signals}


@router.get("/premium")
def premium_signals(user=Depends(get_current_paid_user)):
    return {
        "message": "Premium access granted",
        "signal": "BUY BTC"
    }

# @router.get("/signals")
# def get_signals(
#     email: str = Query(...),
#     user=Depends(require_paid_user)
# ):
#     cached = redis_client.get(CACHE_KEY)
#     if cached:
#         return {"source": "cache", "data": eval(cached)}

#     signals = generate_signals()
#     redis_client.setex(CACHE_KEY, CACHE_TTL, str(signals))
#     return {"source": "live", "data": signals}
# @router.get("/signals")
# def get_signals(user=Depends(get_current_user)):
#     if not user.is_paid:
#         raise HTTPException(status_code=403, detail="Subscription required")

#     return [
#         {"symbol": "NIFTY", "action": "BUY"},
#         {"symbol": "BANKNIFTY", "action": "SELL"},
#     ]