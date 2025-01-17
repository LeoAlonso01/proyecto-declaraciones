from fastapi import APIRouter, UploadFile, Form, Depends, File, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.aws import s3, BUCKET_NAME
from app.database import get_db
from app.models import Nombramiento
from app.schemas import NombramientoResponse, NombramientoCreate, NombramientoUpdate
from botocore.exceptions import NoCredentialsError, NoRegionError
from datetime import datetime
import uuid

# ruta para nombramientos
router = APIRouter()

file_path = "logo umsnh.png"    # Nombre del archivo de ejemplo

def upload_file_to_s3(file_obj, object_name):
    try:
        # Subir el archivo como un stream
        s3.upload_fileobj(file_obj, BUCKET_NAME, object_name)

        # Generar URL del archivo
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_name}"
        return file_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credenciales de AWS no encontradas")
    except NoRegionError:
        raise HTTPException(status_code=500, detail="Región de AWS no especificada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")

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

@router.post("/nombramientos", response_model=NombramientoResponse)
async def create_nombramiento(
    nombre_funcionario: str = Form(...),
    cargo_actual: str = Form(...),
    numero_nombramiento: str = Form(...),
    fecha_inicio: datetime = Form(...),
    fecha_termino: datetime = Form(None),
    estado: str = Form(...),
    is_active: bool = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Archivo no proporcionado o inválido")

    # Usar el nombre original del archivo o generar uno único
    object_name = f"nombramientos/{file.filename}"

    # Subir el archivo a S3
    file_url = upload_file_to_s3(file.file, object_name)
    if not file_url:
        raise HTTPException(status_code=500, detail="Error al subir el archivo a S3")

    # Crear el registro en la base de datos
    nombramiento = Nombramiento(
        nombre_funcionario=nombre_funcionario,
        cargo_actual=cargo_actual,
        numero_nombramiento=numero_nombramiento,
        fecha_inicio=fecha_inicio,
        fecha_termino=fecha_termino,
        estado=estado,
        fecha_registro=datetime.utcnow(),
        is_active=is_active,
        imagen=file_url
    )
    db.add(nombramiento)
    db.commit()
    db.refresh(nombramiento)

    return nombramiento
