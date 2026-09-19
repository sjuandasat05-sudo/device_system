from typing import Optional
from datetime import datetime

from pydantic import BaseModel ,Field

class LoanCreate(BaseModel):
    user_id: int
    device_id: int
    loan_date: datetime = Field(default_factory=datetime.utcnow)
    return_date: Optional[datetime] = None
    status: str = "active"

class LoanUpdate(BaseModel):
    return_date : Optional[datetime] = None
    status : Optional[str] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}

class LoanUserResponse(BaseModel):
    id:int
    nombre: str
    email: str


class LoanDeviceResponse(BaseModel):
    id:int
    name:str
    serial_number:str
    device_type:str
    brand: Optional[str] = None

class LoanDetailResponse(BaseModel):
    id: int
    user: LoanUserResponse
    device: LoanDeviceResponse
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}