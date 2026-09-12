from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserUpdate

from app.dependencies.database_dependency import obtener_db
from app.models.user_model import Usuario

router = APIRouter(prefix="/users", tags=["Usuarios"])

def convertir_usuario(usuario: Usuario):
    return {
        "id": usuario.id,
        "name": usuario.nombre,
        "email": usuario.email,
        "role": usuario.role,
        "is_active": usuario.activo,
    }


@router.get("", response_model=List[UserResponse])
def listar_usuarios(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support o user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(obtener_db),
):
    usuarios = db.query(Usuario).all()

    resultado = usuarios

    if role is not None:
        resultado = [u for u in resultado if u.role == role]

    if is_active is not None:
        resultado = [u for u in resultado if u.activo == is_active]

    return [
        {
            "id": u.id,
            "name": u.nombre,
            "email": u.email,
            "role": u.role,
            "is_active": u.activo,
        }
        for u in resultado
    ]



@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario(
    user_id: int,
    db: Session = Depends(obtener_db),
):
    usuario = db.query(Usuario).filter(
        Usuario.id == user_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con id {user_id}",
        )

    return convertir_usuario(usuario)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UserCreate,
    db: Session = Depends(obtener_db),
):
    correo_existente = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if correo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo {usuario.email}",
        )

    nuevo_usuario = Usuario(
        nombre=usuario.name,
        email=usuario.email,
        role=usuario.role,
        activo=usuario.is_active,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "id": nuevo_usuario.id,
        "name": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "role": nuevo_usuario.role,
        "is_active": nuevo_usuario.activo,
    }


@router.put("/{user_id}", response_model=UserResponse)
def actualizar_usuario(
    user_id: int,
    usuario: UserUpdate,
    db: Session = Depends(obtener_db),
):
    usuario_encontrado = db.query(Usuario).filter(
        Usuario.id == user_id
    ).first()

    if usuario_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con id {user_id}",
        )

    correo_en_uso = db.query(Usuario).filter(
        Usuario.email == usuario.email,
        Usuario.id != user_id
    ).first()

    if correo_en_uso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo {usuario.email}",
        )

    usuario_encontrado.nombre = usuario.name
    usuario_encontrado.email = usuario.email
    usuario_encontrado.role = usuario.role
    usuario_encontrado.activo = usuario.is_active

    db.commit()
    db.refresh(usuario_encontrado)

    return {
        "id": usuario_encontrado.id,
        "name": usuario_encontrado.nombre,
        "email": usuario_encontrado.email,
        "role": usuario_encontrado.role,
        "is_active": usuario_encontrado.activo,
    }

@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_usuario_parcial(
    user_id: int,
    usuario: UserPatch,
    db: Session = Depends(obtener_db),
):
    usuario_encontrado = db.query(Usuario).filter(
        Usuario.id == user_id
    ).first()

    if usuario_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con id {user_id}",
        )

    datos_actualizados = usuario.model_dump(exclude_unset=True)

    if not datos_actualizados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron campos para actualizar",
        )

    if "email" in datos_actualizados:
        correo_en_uso = db.query(Usuario).filter(
            Usuario.email == datos_actualizados["email"],
            Usuario.id != user_id
        ).first()

        if correo_en_uso:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario registrado con el correo {datos_actualizados['email']}",
            )

    if "name" in datos_actualizados:
        usuario_encontrado.nombre = datos_actualizados["name"]

    if "email" in datos_actualizados:
        usuario_encontrado.email = datos_actualizados["email"]

    if "role" in datos_actualizados:
        usuario_encontrado.role = datos_actualizados["role"]

    if "is_active" in datos_actualizados:
        usuario_encontrado.activo = datos_actualizados["is_active"]

    db.commit()
    db.refresh(usuario_encontrado)

    return {
        "id": usuario_encontrado.id,
        "name": usuario_encontrado.nombre,
        "email": usuario_encontrado.email,
        "role": usuario_encontrado.role,
        "is_active": usuario_encontrado.activo,
    }


@router.delete("/{user_id}")
def eliminar_usuario(
    user_id: int,
    db: Session = Depends(obtener_db),
):
    usuario_encontrado = db.query(Usuario).filter(
        Usuario.id == user_id
    ).first()

    if usuario_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con id {user_id}",
        )

    db.delete(usuario_encontrado)
    db.commit()

    return {
        "detail": f"Usuario con id {user_id} eliminado correctamente"
    }