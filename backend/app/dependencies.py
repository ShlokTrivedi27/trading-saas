from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

def require_paid_user(
    email: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_paid:
        raise HTTPException(status_code=403, detail="Upgrade required")
    return user
