"""
data/users_db.py

Simulación de base de datos en memoria para el recurso 'users'.
Se centraliza aquí para que tanto las rutas como las dependencias
trabajen sobre la misma lista de usuarios.
"""

usuarios_db = [
    {"id": 1, "name": "Ana Torres", "email": "ana@correo.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Luis Ramirez", "email": "luis@correo.com", "role": "user", "is_active": True},
    {"id": 3, "name": "Camilo Sarrazola", "email": "camilo@correo.com", "role": "support", "is_active": False},
]

contador_id = 4

ROLES_PERMITIDOS = ["admin", "support", "user"]


def generar_id() -> int:
    """Genera y consume el siguiente ID disponible para un nuevo usuario."""
    global contador_id
    id_generado = contador_id
    contador_id += 1
    return id_generado