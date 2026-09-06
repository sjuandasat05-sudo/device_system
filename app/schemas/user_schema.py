"""
schemas/user_schema.py

Modelos Pydantic de entrada y salida para el recurso 'users'.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    role: str
    is_active: bool = True


class UserCreate(UserBase):
    """Modelo usado en POST /users"""
    pass


class UserUpdate(UserBase):
    """Modelo usado en PUT /users/{user_id} (actualización completa)"""
    pass


class UserPatch(BaseModel):
    """Modelo usado en PATCH /users/{user_id} (actualización parcial).
    Todos los campos son opcionales."""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Modelo usado para las respuestas de la API"""
    id: int

    model_config = {"from_attributes": True}