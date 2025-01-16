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

# modelo para nombramiento
class NombramientoResponse(BaseModel):
    id_nombramiento: int
    nombre_funcionario: str
    cargo_actual: str
    numero_nombramiento: str   
    fecha_inicio: datetime
    fecha_termino: Optional[datetime] = None
    estado: str = "Desconocido"
    fecha_registro: Optional[datetime]
    is_active: bool

    class Cofig:
        from_attributes = True

# modelo para crear nombramiento
class NombramientoCreate(BaseModel):
    id_nombramiento: int
    nombre_funcionario: str
    cargo_actual: str
    numero_nombramiento: str   
    fecha_inicio: datetime
    fecha_termino: Optional[datetime] = None
    estado: str = "Desconocido"
    fecha_registro: Optional[datetime]
    is_active: bool

    class Conbfig:
        from_attributes = True

# modelo para actualizar nombramiento
class NombramientoUpdate(BaseModel):
    nombre_funcionario: Optional[str]
    cargo_actual: Optional[str]
    numero_nombramiento: Optional[str]
    fecha_inicio: Optional[datetime]
    fecha_termino: Optional[datetime] = None
    estado: Optional[str] = "Desconocido"
    fecha_registro: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True