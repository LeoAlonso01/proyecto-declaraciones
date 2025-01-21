from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Leer la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://example_postgresql_db_wgru_user:LL2xL05p8ljzOs7cnh2tCYlST07v42QO@dpg-cu2n79jqf0us73bpp5c0-a:5432/example_postgresql_db_wgru")
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