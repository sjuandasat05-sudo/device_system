from sqlalchemy import Column,Integer,String,Boolean,DateTime
from app.database.connection import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    serial_number = Column(String(50),nullable=False, unique=True)
    device_type = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    loans = relationship("Loan", back_populates="device")



