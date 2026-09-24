from sqlalchemy.orm import Session

from app.models.user_model import Usuario
from app.auth.security import get_password_hash, verify_password


def register_user(
    db: Session,
    nombre: str,
    email: str,
    password: str,
    role: str
):
    existing_user = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if existing_user:
        return None

    hashed_password = get_password_hash(password)

    new_user = Usuario(
        nombre=nombre,
        email=email,
        hashed_password=hashed_password,
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

