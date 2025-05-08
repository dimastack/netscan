from sqlalchemy import Column, Integer, String
from netscan_app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
