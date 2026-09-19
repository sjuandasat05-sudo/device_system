from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.dependencies.database_dependency import obtener_db
from app.models.device_model import Device
from app.schemas.device_schema import (
    DeviceResponse,
    DeviceCreate,
    DeviceUpdate,
    DevicePatch
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.loan_model import Loan


router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


# Obtener todos los dispositivos
@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Obtener todos los dispositivos",
    description="Permite consultar todos los dispositivos registrados en el sistema.",
    response_description="Lista de dispositivos registrados"
)
def get_devices(
    db=Depends(obtener_db)
):
    return db.query(Device).all()


# Obtener un dispositivo específico
@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener un dispositivo",
    description="Permite consultar un dispositivo específico mediante su ID.",
    response_description="Información del dispositivo solicitado",
    responses={
        404: {
            "description": "Dispositivo no encontrado"
        }
    }
)
def get_device(
    device_id: int,
    db=Depends(obtener_db)
):
    device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return device


# Crear un dispositivo
@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear un dispositivo",
    description="Registra un nuevo dispositivo en el sistema.",
    response_description="Dispositivo creado correctamente",
    responses={
        400: {
            "description": "El número de serie ya existe"
        },
        422: {
            "description": "Error de validación en los datos enviados"
        }
    }
)
def create_device(
    device: DeviceCreate,
    db=Depends(obtener_db)
):
    new_device = Device(
        name=device.name,
        description=device.description,
        is_available=device.is_available,
        serial_number=device.serial_number,
        device_type=device.device_type,
        brand=device.brand,
    )

    db.add(new_device)

    try:
        db.commit()
        db.refresh(new_device)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Serial number already exists"
        )

    return new_device


# Actualizar un dispositivo
@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar un dispositivo",
    description="Actualiza completamente la información de un dispositivo existente.",
    response_description="Dispositivo actualizado correctamente",
    responses={
        400: {
            "description": "El número de serie ya existe"
        },
        404: {
            "description": "Dispositivo no encontrado"
        },
        422: {
            "description": "Error de validación en los datos enviados"
        }
    }
)
def update_device(
    device_id: int,
    device: DeviceUpdate,
    db=Depends(obtener_db)
):
    existing_device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not existing_device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    existing_device.name = device.name
    existing_device.description = device.description
    existing_device.is_available = device.is_available
    existing_device.serial_number = device.serial_number
    existing_device.device_type = device.device_type
    existing_device.brand = device.brand

    try:
        db.commit()
        db.refresh(existing_device)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Serial number already exists"
        )

    return existing_device


# Actualización parcial
@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar parcialmente un dispositivo",
    description="Permite modificar uno o varios datos de un dispositivo existente.",
    response_description="Dispositivo actualizado parcialmente",
    responses={
        400: {
            "description": "El número de serie ya existe"
        },
        404: {
            "description": "Dispositivo no encontrado"
        },
        422: {
            "description": "Error de validación en los datos enviados"
        }
    }
)
def patch(
    device_id: int,
    device: DevicePatch,
    db=Depends(obtener_db)
):
    existing_device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not existing_device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    update_data = device.model_dump(
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(existing_device, key, value)

    try:
        db.commit()
        db.refresh(existing_device)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Serial number already exists"
        )

    return existing_device


# Eliminar un dispositivo
@router.delete(
    "/{device_id}",
    status_code=204,
    summary="Eliminar un dispositivo",
    description="Elimina un dispositivo existente mediante su ID.",
    response_description="Dispositivo eliminado correctamente",
    responses={
        404: {
            "description": "Dispositivo no encontrado"
        }
    }
)
def delete(
    device_id: int,
    db=Depends(obtener_db)
):
    existing_device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not existing_device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    db.delete(existing_device)
    db.commit()

    return Response(status_code=204)


# Obtener préstamos de un dispositivo
@router.get(
    "/{device_id}/loans",
    summary="Obtener préstamos de un dispositivo",
    description="Consulta los préstamos asociados a un dispositivo.",
    response_description="Lista de préstamos del dispositivo"
)
def obtener_prestamos_dispositivo(
    device_id: int,
    db: Session = Depends(obtener_db),
):
    prestamos = db.query(Loan).where(
        Loan.device_id == device_id
    ).all()

    return prestamos


