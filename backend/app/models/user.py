# from sqlalchemy import Column, Integer, String, Boolean
# # from sqlalchemy.ext.declarative import declarative_base
# from app.config import Base 
# # from app.database import Base

# # Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     password_hash = Column(String, nullable=False)
#     is_paid = Column(Boolean, default=False)
#     is_admin = Column(Boolean, default=False)


from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_paid = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
