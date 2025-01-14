from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.database import Base

""" class TipoDeclaracion(enum.Enum):
    INICIO = "INICIO"
    MODIFICACION = "MODIFICACION"
    CONCLUSION = "CONCLUSION"
    NOTA_ACLARATORIA = "NOTA_ACLARATORIA"
    AVISO_CAMBIO_FUNCIONES = "AVISO_CAMBIO_FUNCIONES" """

class TipoDeclaracion(Base):
    __tablename__ = "public.tipos_declaraciones"
    id_tipo = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)

class Usuario(Base):
    __tablename__ = "public.usuarios"  # Nombre de la tabla en la base de datos
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    rol = Column(String)
    fecha_creacion = Column(DateTime)

class Nombramiento(Base):
    __tablename__ = "public.nombramientos"
    id_nombramiento = Column(Integer, primary_key=True, index=True)
    nombre_funcionario = Column(String, nullable=False)
    cargo_actual = Column(String, nullable=False)
    numero_nombramiento = Column(String, unique=True, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_termino = Column(DateTime, nullable=True)
    estado = Column(String, nullable=False)
    fecha_registro = Column(DateTime, nullable=False)

class HistorialCargo(Base):
    __tablename__ = "public.historial_cargos"
    id_historial_cargo = Column(Integer, primary_key=True, index=True)
    id_nombramiento = Column(Integer, ForeignKey("public.nombramientos.id_nombramiento"), nullable=False)
    cargo_anterior = Column(String, nullable=False)
    motivo_cambio = Column(Text)

class Historial(Base):
    __tablename__ = "public.historial"
    id_historial = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("public.usuarios.id_usuario"), nullable=False)
    accion = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)


class Declaracion(Base):
    __tablename__ = "public.declaraciones_entregadas"
    id_declaracion = Column(Integer, primary_key=True, index=True)
    nombre_declarante = Column(String, nullable=False)
    id_tipo = Column(Integer, ForeignKey("public.tipos_declaraciones.id_tipo"), nullable=False)
    fecha_declaracion = Column(DateTime, nullable=False)
    fecha_recepcion = Column(DateTime, nullable=False)
    observaciones = Column(Text)
    imagen = Column(String, nullable=True)
    fecha_registro = Column(DateTime, nullable=False)
