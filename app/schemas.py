from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    rol: str
    fecha_creacion: Optional[datetime]
    is_active: bool

# modelo para crear usuario 
class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str
    fecha_creacion: Optional[datetime]
    is_active: bool

# modelo para actualizar usuario
class UsuarioUpdate(BaseModel):
    nombre: Optional[str]
    correo: Optional[EmailStr]
    rol: Optional[str]
    fecha_creacion: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True  # Cambiado de 'orm_mode' a 'from_attributes'