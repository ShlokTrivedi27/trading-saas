from sqlalchemy.orm import Session
from app.models.user import User
from app.database import SessionLocal

def mark_user_paid(email: str):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if user:
        user.is_paid = True
        db.commit()

    db.close()
