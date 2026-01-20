import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
DATABASE_URL = "sqlite:///app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SECRET_KEY = "supersecretkey"   # can be anything for now
ALGORITHM = "HS256"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"

    STRIPE_SECRET_KEY: str
    STRIPE_PRICE_ID: str
    STRIPE_WEBHOOK_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
STRIPE_PRICE_ID = settings.STRIPE_PRICE_ID
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
