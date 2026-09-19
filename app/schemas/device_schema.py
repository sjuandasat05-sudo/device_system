from typing import Optional
from pydantic import BaseModel ,Field

class DeviceBase(BaseModel):
    name:str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    serial_number: str = Field(..., min_length=2, max_length=50)
    device_type: str = Field(..., min_length=2, max_length=50)
    brand: Optional[str] = None
    is_available: bool = True

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    id:int

    model_config = {"from_attributes": True}

class DevicePatch(BaseModel):
    name :Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    serial_number: Optional[str] = Field(None, min_length=2, max_length=50)
    device_type: Optional[str] = Field(None, min_length=2, max_length=50)
    brand: Optional[str] = None
    is_available: Optional[bool] = None
