from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base

""" class TipoDeclaracion(enum.Enum):
    INICIO = "INICIO"
    MODIFICACION = "MODIFICACION"
    CONCLUSION = "CONCLUSION"
    NOTA_ACLARATORIA = "NOTA_ACLARATORIA"
    AVISO_CAMBIO_FUNCIONES = "AVISO_CAMBIO_FUNCIONES" """

class TipoDeclaracion(Base):
    __tablename__ = "tipos_declaraciones"
    id_tipo = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    rol = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)

class Nombramiento(Base):
    __tablename__ = "nombramientos"
    id_nombramiento = Column(Integer, primary_key=True, index=True)
    nombre_funcionario = Column(String, nullable=False)
    cargo_actual = Column(String, nullable=False)
    numero_nombramiento = Column(String, unique=True, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_termino = Column(DateTime, nullable=True)
    estado = Column(String, nullable=False)
    fecha_registro = Column(DateTime, nullable=False)

class HistorialCargo(Base):
    __tablename__ = "historial_cargos"
    id_historial_cargo = Column(Integer, primary_key=True, index=True)
    id_nombramiento = Column(Integer, ForeignKey("nombramientos.id"), nullable=False)
    cargo_anterior = Column(String, nullable=False)
    motivo_cambio = Column(Text)

class Historial(Base):
    __tablename__ = "historial"
    id_historial = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    accion = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)


class Declaracion(Base):
    __tablename__ = "declaraciones_entregadas"
    id_declaracion = Column(Integer, primary_key=True, index=True)
    nombre_declarante = Column(String, nullable=False)
    id_tipo = Column(Enum(TipoDeclaracion), nullable=False)
    fecha_declaracion = Column(DateTime, nullable=False)
    fecha_recepcion = Column(DateTime, nullable=False)
    observaciones = Column(Text)
    imagen = Column(String, nullable=True)
    fecha_registro = Column(DateTime, nullable=False)
