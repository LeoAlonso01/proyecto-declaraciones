from fastapi import APIRouter, UploadFile, Depends, File, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.aws import s3, BUCKET_NAME
from app.database import get_db
from app.models import Nombramiento
from app.schemas import NombramientoResponse, NombramientoCreate, NombramientoUpdate
from botocore.exceptions import NoCredentialsError, NoRegionError
from datetime import datetime

example_file = "example.txt"    # Nombre del archivo de ejemplo

def upload_file_to_s3(file_path, object_name):
    try:
        #subir el archivo
        s3.upload_file(file_path, BUCKET_NAME, object_name)

        #generar Url del Archivo
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_name}"
        return file_url
    except FileNotFoundError:
        return "El archivo no fue encontrado"   
    except NoCredentialsError:
        return "Credenciales no encontradas"
    except NoRegionError:
        return "Region no encontrada"

# ruta para nombramientos
router = APIRouter()

Nombramiento_db = []

# traer la lista de nombramientos
@router.get("/nombramientos", response_model=List[NombramientoResponse])
async def get_nombramientos(db:Session = Depends(get_db)):
    Nombramiento_db = db.query(Nombramiento).filter(Nombramiento.is_active == True).all()
    # limpia los datos
    for nombramiento in Nombramiento_db:
        if nombramiento.fecha_termino == None:
            nombramiento.fecha_termino = datetime.now()
        if nombramiento.estado not in ["Activo", "Inactivo"]:
            nombramiento.estado = "Desconocido"
    return Nombramiento_db

# traen solo un nombramiento
@router.get("/nombramientos/{nombramiento_id}", response_model=NombramientoResponse)
async def get_nombramiento(nombramiento_id: int, db: Session = Depends(get_db)):
    nombramiento = db.query(Nombramiento).filter(Nombramiento.id_nombramiento == nombramiento_id, Nombramiento.is_active == True).first()
    if not nombramiento:
        raise HTTPException(status_code=404, detail="Nombramiento no encontrado")
    return nombramiento

# sohft delete de nombramiento
@router.delete("/nombramientos/{nombramiento_id}", response_model=dict)
async def soft_delete_nombramiento(nombramiento_id: int, db: Session = Depends(get_db)):
    nombramiento = db.query(Nombramiento).filter(Nombramiento.id_nombramiento == nombramiento_id).first()
    if not nombramiento:
        raise HTTPException(status_code=404, detail="Nombramiento no encontrado")
    
    if not nombramiento.is_active:
        raise HTTPException(status_code=400, detail="Nombramiento ya está desactivado")
    
    nombramiento.is_active = False  # Marca el nombramiento como inactivo
    db.commit()
    return {"message": f"Nombramiento con id {nombramiento_id} borrado exitosamente"}

# endponint para actualizar un nombramiento
@router.patch("/nombramientos/{nombramiento_id}", response_model=NombramientoResponse)
async def update_nombramiento(nombramiento_id: int, nombramiento: NombramientoUpdate, db: Session = Depends(get_db)):
    nombramiento_db = db.query(Nombramiento).filter(Nombramiento.id_nombramiento == nombramiento_id).first()
    if not nombramiento_db:
        raise HTTPException(status_code=404, detail="Nombramiento no encontrado")
    
    for key, value in nombramiento.dict().items():
        setattr(nombramiento_db, key, value) if value else None
    
    db.commit()
    db.refresh(nombramiento_db)
    return nombramiento_db

@router.post("/nombramientos")
async def create_nombramiento(nombramiento: dict):
    return {"message": "Nombramiento creado", "nombramiento": nombramiento}
