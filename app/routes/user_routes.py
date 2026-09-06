from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Usuarios"])

usuarios_db = [
    {"id": 1, "name": "Ana Torres", "email": "ana@correo.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Luis Ramirez", "email": "luis@correo.com", "role": "user", "is_active": True},
    {"id": 3, "name": "Camilo Sarrazola", "email": "camilo@correo.com", "role": "support", "is_active": False},
]

contador_id = 4


@router.get("", response_model=List[UserResponse])
def listar_usuarios(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support o user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
):
    resultado = usuarios_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario(user_id: int):
    for usuario in usuarios_db:
        if usuario["id"] == user_id:
            return usuario

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe un usuario con id {user_id}",
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UserCreate):
    global contador_id

    correo_existente = any(u["email"] == usuario.email for u in usuarios_db)
    if correo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo {usuario.email}",
        )

    nuevo_usuario = usuario.model_dump()
    nuevo_usuario["id"] = contador_id
    contador_id += 1

    usuarios_db.append(nuevo_usuario)
    return nuevo_usuario


@router.put("/{user_id}", response_model=UserResponse)
def actualizar_usuario(user_id: int, usuario: UserUpdate):
    usuario_encontrado = None
    for u in usuarios_db:
        if u["id"] == user_id:
            usuario_encontrado = u
            break

    if usuario_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con id {user_id}",
        )

    correo_en_uso = any(
        u["email"] == usuario.email and u["id"] != user_id for u in usuarios_db
    )
    if correo_en_uso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario registrado con el correo {usuario.email}",
        )

    usuario_encontrado["name"] = usuario.name
    usuario_encontrado["email"] = usuario.email
    usuario_encontrado["role"] = usuario.role
    usuario_encontrado["is_active"] = usuario.is_active

    return usuario_encontrado


@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_usuario_parcial(user_id: int, usuario: UserPatch):
    usuario_encontrado = None
    for u in usuarios_db:
        if u["id"] == user_id:
            usuario_encontrado = u
            break

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
        correo_en_uso = any(
            u["email"] == datos_actualizados["email"] and u["id"] != user_id
            for u in usuarios_db
        )
        if correo_en_uso:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario registrado con el correo {datos_actualizados['email']}",
            )

    usuario_encontrado.update(datos_actualizados)
    return usuario_encontrado


@router.delete("/{user_id}")
def eliminar_usuario(user_id: int):
    usuario_encontrado = None
    for u in usuarios_db:
        if u["id"] == user_id:
            usuario_encontrado = u
            break

    if usuario_encontrado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con id {user_id}",
        )

    usuarios_db.remove(usuario_encontrado)
    return {"detail": f"Usuario con id {user_id} eliminado correctamente"}