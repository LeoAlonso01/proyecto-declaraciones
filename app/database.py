from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Leer la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:052613@localhost/Test")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está definida en las variables de entorno")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    from app.models import TipoDeclaracion, Usuario, Nombramiento, HistorialCargo, Historial, Declaracion
    Base.metadata.create_all(bind=engine)

# dependencia para obtener la sesion de la bd
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()