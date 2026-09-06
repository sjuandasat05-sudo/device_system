from fastapi import FastAPI
 
from app.routes.user_routes import router as user_router
 
app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Permite crear, consultar, filtrar, actualizar (completa y "
        "parcialmente) y eliminar usuarios, con manejo de errores y "
        "reutilización de lógica mediante Dependency Injection."
    ),
    version="2.0.0",
    contact={
        "name": "Juan",
        "email": "juan@example.com",
    },
)
 
app.include_router(user_router)
 
 
@app.get("/", tags=["Root"], summary="Estado de la API")
def root():
    return {"message": "device_systems API activa. Visita /docs para la documentación."}
 