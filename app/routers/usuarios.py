from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models import Usuario # modelo SQLAlchemy
from app.database import get_db
from app.schemas import UsuarioResponse, UsuarioCreate, UsuarioUpdate # modelo Pydantic

router = APIRouter()

usuarios_db = []

# Rutas para el CRUD de usuarios
# Ruta para obtener todos los usuarios
@router.get("/usuarios", response_model=List[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios_db = db.query(Usuario).filter(Usuario.is_active == True).all()
    print(usuarios_db)
    return usuarios_db
    
# Ruta para crear un usuario
@router.post("/usuarios", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        rol=usuario.rol,
        fecha_creacion=usuario.fecha_creacion,
        is_active=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Ruta para obtener un usuario por su ID
@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int , db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id, Usuario.is_active == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Ruta para actualizar un usuario
@router.delete("/usuarios/{usuario_id}", response_model=dict)
def soft_delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not usuario.is_active:
        raise HTTPException(status_code=400, detail="Usuario ya está desactivado")
    
    usuario.is_active = False  # Marca el usuario como inactivo
    db.commit()  # Guarda los cambios en la base de datos
    return {"message": f"Usuario con id {usuario_id} borrado exitosamente"}

#ruta para actualizar un usuario por patch
@router.patch("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def acualizar_parcial(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    
    # busca el usuario en la base de datos
    usuario_existente = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # actualiza los campos que se pasen en el body
    cambios = False # Bandera para saber si se hicieron cambios

    # VALIDA EL NOMBRE
    if usuario.nombre is not None:
        if len(usuario.nombre) < 3:
            raise HTTPException(status_code=400, detail="El nombre debe tener al menos 3 caracteres")
        usuario_existente.nombre = usuario.nombre
        cambios = True
    
    # VALIDA EL CORREO
    if usuario.correo is not None:
        if not "@" in usuario.correo:
            raise HTTPException(status_code=400, detail="Correo electrónico inválido")
        usuario_existente.correo = usuario.correo
        cambios = True
    
    # VALIDA EL ROL
    if usuario.rol is not None:
        roles_validos = ["Administrador", "Usuario", "Invitado"]
        if usuario.rol not in roles_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Rol inválido. Roles permitidos: {', '.join(roles_validos)}"
            )
        usuario_existente.rol = usuario.rol
        cambios = True

    # valida si esta activo
    if usuario.is_active is not None:
        usuario_existente.is_active = usuario.is_active
        cambios = True

     # Si no se hicieron cambios, retorna un mensaje apropiado
    if not cambios:
        raise HTTPException(status_code=400, detail="No se enviaron campos válidos para actualizar")
    
    # guardar los cmabisos en la base de datos
    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente
