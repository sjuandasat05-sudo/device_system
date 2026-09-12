from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


def obtener_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()