from app.models.loan_model import Loan
from app.dependencies.database_dependency import obtener_db
from fastapi import APIRouter, Depends, HTTPException
from app.models.user_model import Usuario
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate
from datetime import datetime


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


# Obtener todos los préstamos o filtrar
@router.get(
    "/",
    summary="Obtener todos los préstamos",
    description="Permite consultar todos los préstamos registrados y filtrarlos por estado, correo del usuario o tipo de dispositivo.",
    response_description="Lista de préstamos registrados",
    responses={
        422: {
            "description": "El filtro de estado no es válido"
        }
    }
)
def get_loans(
    status: str = None,
    user_email: str = None,
    device_type: str = None,
    db=Depends(obtener_db)
):
    if status and status not in ["active", "returned", "overdue"]:
        raise HTTPException(
            status_code=422,
            detail="Invalid status filter"
        )

    prestamos = db.query(Loan)

    if status:
        prestamos = prestamos.where(
            Loan.status == status
        )

    if user_email:
        prestamos = prestamos.join(
            Usuario,
            Loan.user_id == Usuario.id
        ).where(
            Usuario.email.ilike(user_email)
        )

    if device_type:
        prestamos = prestamos.join(
            Device,
            Loan.device_id == Device.id
        ).where(
            Device.device_type.ilike(device_type)
        )

    return prestamos.all()


# Obtener préstamos con información del usuario y dispositivo
@router.get(
    "/details",
    summary="Obtener detalles de los préstamos",
    description="Consulta los préstamos incluyendo la información relacionada del usuario y del dispositivo.",
    response_description="Lista de préstamos con información del usuario y dispositivo"
)
def get_loan_details(
    db=Depends(obtener_db)
):
    loans = db.query(
        Loan,
        Usuario,
        Device
    )

    loans = loans.join(
        Usuario,
        Loan.user_id == Usuario.id
    )

    loans = loans.join(
        Device,
        Loan.device_id == Device.id
    )

    loans = loans.all()

    result = []

    for loan, user, device in loans:
        result.append({
            "loan_id": loan.id,
            "status": loan.status,
            "user": {
                "id": user.id,
                "name": user.nombre,
                "email": user.email
            },
            "device": {
                "id": device.id,
                "name": device.name,
                "serial_number": device.serial_number,
                "device_type": device.device_type
            }
        })

    return result


# Obtener un préstamo específico
@router.get(
    "/{loan_id}",
    summary="Obtener un préstamo",
    description="Permite consultar un préstamo específico mediante su ID.",
    response_description="Información del préstamo solicitado",
    responses={
        404: {
            "description": "Préstamo no encontrado"
        }
    }
)
def get_loan(
    loan_id: int,
    db=Depends(obtener_db)
):
    loan = db.query(Loan).filter(
        Loan.id == loan_id
    ).first()

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    return loan


# Crear un préstamo
@router.post(
    "/",
    status_code=201,
    summary="Crear un préstamo",
    description="Registra un nuevo préstamo y marca el dispositivo asociado como no disponible.",
    response_description="Préstamo creado correctamente",
    responses={
        404: {
            "description": "El usuario o dispositivo no existe"
        },
        409: {
            "description": "El dispositivo no está disponible"
        },
        422: {
            "description": "Error de validación en los datos enviados"
        }
    }
)
def create_loan(
    loan: LoanCreate,
    db=Depends(obtener_db)
):
    user = db.query(Usuario).filter(
        Usuario.id == loan.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    device = db.query(Device).filter(
        Device.id == loan.device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    # Regla de negocio:
    # un dispositivo no puede prestarse si ya está ocupado
    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail="Device is not available"
        )

    new_loan = Loan(
        user_id=loan.user_id,
        device_id=loan.device_id
    )

    db.add(new_loan)

    device.is_available = False

    db.commit()

    db.refresh(new_loan)

    return new_loan


# Devolver un préstamo
@router.patch(
    "/{loan_id}/return",
    summary="Devolver un préstamo",
    description="Registra la devolución de un préstamo, establece la fecha de devolución y vuelve a dejar disponible el dispositivo.",
    response_description="Préstamo devuelto correctamente",
    responses={
        404: {
            "description": "Préstamo o dispositivo no encontrado"
        },
        409: {
            "description": "El préstamo ya fue devuelto"
        }
    }
)
def return_loan(
    loan_id: int,
    db=Depends(obtener_db)
):
    loan = db.query(Loan).filter(
        Loan.id == loan_id
    ).first()

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    # Regla de negocio:
    # no se puede devolver un préstamo que ya fue devuelto
    if loan.status == "returned":
        raise HTTPException(
            status_code=409,
            detail="Loan has already been returned"
        )

    loan.status = "returned"
    loan.return_date = datetime.utcnow()

    device = db.query(Device).filter(
        Device.id == loan.device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    device.is_available = True

    db.commit()

    db.refresh(loan)

    return loan