from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.config import get_db
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, decode_access_token
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Request models
class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Signup route
@router.post("/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=req.email, password_hash=hash_password(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# Login route
@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


# Current user
@router.get("/me")
def get_me(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    # For simplicity, token can be passed as query ?token=
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).get(payload["user_id"])
    return {"id": user.id, "email": user.email, "is_paid": user.is_paid}



# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     email: str = payload.get("sub")
#     user = db.query(User).filter(User.email == email).first()
#     return user

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Please log in to continue with billing.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401)
    return user