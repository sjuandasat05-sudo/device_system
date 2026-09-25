from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.database_dependency import obtener_db
from app.auth.auth_service import register_user, authenticate_user
from app.auth.security import create_access_token
from app.models.user_model import Usuario

from app.schemas.auth_schema import (
    UserRegister,
    UserResponse,
    Token
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


limiter = Limiter(
    key_func=get_remote_address
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(obtener_db)
):
    user = register_user(
        db=db,
        nombre=user_data.nombre,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    return user


@router.post(
    "/login",
    response_model=Token
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(obtener_db)
):
    user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: Usuario = Depends(get_current_user)
):
    return current_user