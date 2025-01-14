from pydantic import BaseModel
from datetime import datetime

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True  # Cambiado de 'orm_mode' a 'from_attributes'