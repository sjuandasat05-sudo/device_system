from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# 1. URL de conexión
DATABASE_URL = "sqlite:///./app.db"
# 2. Motor de base de datos
engine = create_engine(
DATABASE_URL,
connect_args={"check_same_thread": False}
)
# 3. Fábrica de sesiones
SessionLocal = sessionmaker(
autocommit=False, autoflush=False,
bind=engine
)
# 4. Base para modelos
class Base(DeclarativeBase):
    pass
def create_tables():
    Base.metadata.create_all(bind=engine)