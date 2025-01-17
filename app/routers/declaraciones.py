from fastapi import APIRouter, UploadFile, Form, Depends, File, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.aws import s3, BUCKET_NAME
from app.database import get_db
from app.models import Declaracion
from app.schemas import DeclaracionResponse, DeclaracionCreate, DeclaracionUpdate
from botocore.exceptions import NoCredentialsError, NoRegionError
from datetime import datetime

# Ruta para declaraciones
router = APIRouter()

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

# Obtener todas las declaraciones
@router.get("/declaraciones", response_model=List[DeclaracionResponse])
async def get_declaraciones(db: Session = Depends(get_db)):
    declaraciones = db.query(Declaracion).filter(Declaracion.is_active == True).all()
    return declaraciones

# Obtener una declaración por ID
@router.get("/declaraciones/{declaracion_id}", response_model=DeclaracionResponse)
async def get_declaracion(declaracion_id: int, db: Session = Depends(get_db)):
    declaracion = db.query(Declaracion).filter(Declaracion.id_declaracion == declaracion_id, Declaracion.is_active == True).first()
    if not declaracion:
        raise HTTPException(status_code=404, detail="Declaración no encontrada")
    return declaracion

# Eliminación lógica de una declaración
@router.delete("/declaraciones/{declaracion_id}", response_model=dict)
async def soft_delete_declaracion(declaracion_id: int, db: Session = Depends(get_db)):
    declaracion = db.query(Declaracion).filter(Declaracion.id_declaracion == declaracion_id).first()
    if not declaracion:
        raise HTTPException(status_code=404, detail="Declaración no encontrada")

    if not declaracion.is_active:
        raise HTTPException(status_code=400, detail="Declaración ya está desactivada")

    declaracion.is_active = False
    db.commit()
    return {"message": f"Declaración con id {declaracion_id} desactivada exitosamente"}

# Actualizar una declaración
@router.patch("/declaraciones/{declaracion_id}", response_model=DeclaracionResponse)
async def update_declaracion(declaracion_id: int, declaracion: DeclaracionUpdate, db: Session = Depends(get_db)):
    declaracion_db = db.query(Declaracion).filter(Declaracion.id_declaracion == declaracion_id).first()
    if not declaracion_db:
        raise HTTPException(status_code=404, detail="Declaración no encontrada")

    for key, value in declaracion.dict().items():
        setattr(declaracion_db, key, value) if value else None

    db.commit()
    db.refresh(declaracion_db)
    return declaracion_db

# Crear una nueva declaración
@router.post("/declaraciones", response_model=DeclaracionResponse)
async def create_declaracion(
    nombre_declarante: str = Form(...),
    id_tipo: int = Form(...),
    fecha_declaracion: datetime = Form(...),
    fecha_recepcion: datetime = Form(...),
    observaciones: str = Form(...),
    is_active: bool = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Archivo no proporcionado o inválido")

    # Usar el nombre original del archivo o generar uno único
    object_name = f"declaraciones/{file.filename}"

    # Subir el archivo a S3
    file_url = upload_file_to_s3(file.file, object_name)
    if not file_url:
        raise HTTPException(status_code=500, detail="Error al subir el archivo a S3")

    # Crear el registro en la base de datos
    declaracion = Declaracion(
        nombre_declarante=nombre_declarante,
        id_tipo=id_tipo,
        fecha_declaracion=fecha_declaracion,
        fecha_recepcion=fecha_recepcion,
        observaciones=observaciones,
        fecha_registro=datetime.utcnow(),
        is_active=is_active,
        imagen=file_url
    )
    db.add(declaracion)
    db.commit()
    db.refresh(declaracion)

    return declaracion
