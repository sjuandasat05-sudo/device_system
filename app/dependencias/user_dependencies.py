"""
dependencies/user_dependencies.py

Funciones reutilizables pensadas para usarse con Depends() en las rutas.
Cada una resuelve una responsabilidad puntual (buscar usuario, validar
rol, simular configuración/autenticación) para no repetir ese código
en cada endpoint de user_routes.py.
"""

from typing import Optional

from fastapi import Header, HTTPException, Query, status

from app.data.users_db import ROLES_PERMITIDOS, usuarios_db


def obtener_usuario_o_404(user_id: int) -> dict:
    """
    Dependencia: busca un usuario por su ID.
    Si no existe, corta la ejecución con 404 antes de llegar a la ruta.
    Uso en la ruta:
        def obtener_usuario(usuario: dict = Depends(obtener_usuario_o_404)):
    """
    for usuario in usuarios_db:
        if usuario["id"] == user_id:
            return usuario

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe un usuario con id {user_id}",
    )


def validar_rol_filtro(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support o user"),
) -> Optional[str]:
    """
    Dependencia: valida que el rol usado como filtro (query param) sea
    uno de los roles permitidos. Se usa en GET /users?role=...
    """
    if role is not None and role not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no permitido. Roles válidos: {', '.join(ROLES_PERMITIDOS)}",
        )
    return role


def obtener_configuracion_api() -> dict:
    """
    Dependencia: simula la configuración general de la API,
    reutilizable en cualquier endpoint que la necesite.
    """
    return {
        "app_name": "device_system",
        "version": "2.0.0",
        "max_page_size": 50,
    }


def verificar_token(
    x_token: Optional[str] = Header(
        None, description="Token simulado de autenticación (header 'x-token')"
    )
) -> str:
    """
    Dependencia: simula autenticación básica mediante una cabecera HTTP.
    Se usa, por ejemplo, para proteger el endpoint DELETE.
    """
    TOKEN_VALIDO = "device-systems-secret-token"

    if x_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el header 'x-token'",
        )
    if x_token != TOKEN_VALIDO:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )
    return x_token