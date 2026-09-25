import time
import uuid
import logging

from fastapi import Request


logger = logging.getLogger(__name__)


async def request_middleware(request: Request, call_next):
    # Identificador de la petición
    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())
    )

    # Tiempo inicial
    start_time = time.perf_counter()

    # Continuar con el resto de la aplicación
    response = await call_next(request)

    # Calcular tiempo de procesamiento
    process_time = time.perf_counter() - start_time

    # Agregar headers a la respuesta
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Request-ID"] = request_id

    # Registrar la petición
    logger.info(
        "%s %s -> %s",
        request.method,
        request.url.path,
        response.status_code
    )

    return response