from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.auth import get_current_paid_user
from app.database import get_db
from app.models.user import User


def get_current_admin(
    user: User = Depends(get_current_paid_user),
    db: Session = Depends(get_db)
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user
