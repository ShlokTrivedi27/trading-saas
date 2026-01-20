from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from app.database import Base, engine 
from app.models import user      
from app.routes import auth, billing, signals
from app.routes import webhook, admin

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(webhook.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(billing.router)
app.include_router(signals.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
