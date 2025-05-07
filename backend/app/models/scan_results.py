from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scan_type = Column(String(50), nullable=False)
    target = Column(String(100), nullable=False)
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
