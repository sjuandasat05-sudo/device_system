from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth.auth_routes import router as auth_router

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

from app.database.connection import create_tables
from app.models.loan_model import Loan

from app.middlewares.request_middleware import request_middleware


# Configuración de Rate Limiting
limiter = Limiter(
    key_func=get_remote_address
)


# Configuración principal de FastAPI
app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para la gestión de usuarios, dispositivos "
        "y préstamos del sistema device_systems. "
        "Incluye autenticación mediante OAuth2 y JWT, "
        "control de roles, CORS, middleware, rate limiting "
        "y validación avanzada."
    ),
    version="3.0.0",
    contact={
        "name": "Juan",
        "email": "juan@example.com",
    },
    openapi_tags=[
        {
            "name": "Auth",
            "description": "Autenticación y gestión de acceso."
        },
        {
            "name": "Users",
            "description": "Gestión de usuarios."
        },
        {
            "name": "Devices",
            "description": "Gestión de dispositivos."
        },
        {
            "name": "Loans",
            "description": "Gestión de préstamos."
        },
        {
            "name": "Security",
            "description": "Funciones relacionadas con seguridad."
        }
    ]
)


# Conectar Rate Limiting con FastAPI
app.state.limiter = limiter


# Middleware personalizado
app.middleware("http")(request_middleware)


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Crear tablas de la base de datos
create_tables()


# Registrar routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


# Ruta principal
@app.get(
    "/",
    tags=["Root"],
    summary="Estado de la API"
)
def root():
    return {
        "message": "device_systems API activa. Visita /docs para la documentación."
    }