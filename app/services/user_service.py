from typing import Dict, List, Optional
 
from fastapi import HTTPException, status
 
from app.data.users_db import ALLOWED_ROLES, generate_id, users_db
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate
 
 
def get_all_users(role: Optional[str] = None, is_active: Optional[bool] = None) -> List[Dict]:
    """Lista usuarios, permitiendo filtrar opcionalmente por rol y/o estado."""
    result = users_db
    if role is not None:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result
 
 
def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Busca un usuario por ID. Devuelve None si no existe (no lanza error aquí)."""
    return next((u for u in users_db if u["id"] == user_id), None)
 
 
def email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    """
    Verifica si un correo ya está registrado.
    'exclude_id' permite ignorar al propio usuario en actualizaciones
    (para que un usuario pueda 'reenviar' su propio correo sin error).
    """
    return any(
        u["email"].lower() == email.lower() and u["id"] != exclude_id
        for u in users_db
    )
 
 
def validate_role(role: str) -> None:
    """Lanza 400 si el rol no está dentro de los roles permitidos."""
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no permitido. Roles válidos: {', '.join(ALLOWED_ROLES)}",
        )
 
 
def create_user(user_data: UserCreate) -> Dict:
    """Crea un nuevo usuario (POST /users)."""
    if email_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )
    validate_role(user_data.role)
 
    new_user = {
        "id": generate_id(),
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active,
    }
    users_db.append(new_user)
    return new_user
 
 
def replace_user(user_id: int, user_data: UserUpdate) -> Dict:
    """Reemplaza completamente un usuario existente (PUT /users/{user_id})."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
 
    if email_exists(user_data.email, exclude_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )
    validate_role(user_data.role)
 
    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    user["is_active"] = user_data.is_active
    return user
 
 
def update_user_partial(user_id: int, patch_data: UserPatch) -> Dict:
    """Actualiza parcialmente un usuario (PATCH /users/{user_id})."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
 
    # exclude_unset=True -> solo incluye los campos que el cliente SI envió
    update_dict = patch_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron campos para actualizar",
        )
 
    if "email" in update_dict and email_exists(update_dict["email"], exclude_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )
    if "role" in update_dict:
        validate_role(update_dict["role"])
 
    user.update(update_dict)
    return user
 
 
def delete_user(user_id: int) -> None:
    """Elimina un usuario existente (DELETE /users/{user_id})."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    users_db.remove(user)
 