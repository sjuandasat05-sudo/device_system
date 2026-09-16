from sqlalchemy import Column, Integer, String, Boolean, DateTime ,ForeignKey,relationship
from app.database.connection import Base
from datetime import datetime

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer,ForeignKey("devices.id"),nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="active", nullable=False)
    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")
    
