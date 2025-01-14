from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models import Usuario # modelo SQLAlchemy
from app.database import get_db
#from app.schemas import UsuarioResponse # modelo Pydantic

router = APIRouter()

usuarios_db = []

@router.get("/usuarios")
def obtener_usuarios():
    return usuarios_db
    

@router.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    usuarios_db.append(usuario)
    return usuario

@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    for usuario in usuarios_db:
        if usuario.id == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/usuarios/{usuario_id}", response_model=Usuario)
def eliminar_usuario(usuario_id: int):
    for usuario in usuarios_db:
        if usuario.id == usuario_id:
            usuarios_db.remove(usuario)
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")