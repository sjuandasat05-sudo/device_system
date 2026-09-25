from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr


class UserRegister(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    role: str = Field(...)
    @field_validator("role")
    @classmethod
    def validate_role(cls, role):
        if role not in ["admin", "user","support"]:
            raise ValueError("Rol no válido")

        return role

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if " " in password:
            raise ValueError("La contraseña no puede contener espacios")

        if not any(char.isupper() for char in password):
            raise ValueError("La contraseña debe contener al menos una mayúscula")

        if not any(char.islower() for char in password):
            raise ValueError("La contraseña debe contener al menos una minúscula")

        if not any(char.isdigit() for char in password):
            raise ValueError("La contraseña debe contener al menos un número")

        return password


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str | None = None


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None = None
    role: str
    activo: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

