from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from models.database import SessionLocal  # Ajuste el import
from models.models import Usuarios  # Ajuste el import

# Crear un enrutador para las rutas de persona
usuario = APIRouter()

# Activacion y Cierra base de datos si no se usa
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ModelUsuario(BaseModel):
    ID: int
    Persona_ID: int
    Nombre_Usuario: str
    Correo_Electronico: EmailStr
    Contrasena: str
    Numero_Telefonico_Movil: str
    Estatus: Optional[str] = None  # Los estatus son 'Activo', 'Inactivo', 'Bloqueado', 'Suspendido'
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class UpdateUsuario(BaseModel):
    Persona_ID: Optional[int]
    Nombre_Usuario: Optional[str]
    Correo_Electronico: Optional[str]
    Contrasena: Optional[str]
    Numero_Telefonico_Movil: Optional[str]
    Estatus: Optional[str]  # Los estatus son 'Activo', 'Inactivo', 'Bloqueado', 'Suspendido'
    Fecha_Actualizacion: Optional[datetime] = None

@usuario.get('/', operation_id="bienvenida_get")
def bienvenida():
    """
    Ruta de bienvenida.
    """
    return 'Bienvenido al Sistema'

@usuario.get("/usuario", response_model=List[ModelUsuario], operation_id="get_usuarios")
async def get_usuarios(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios.
    """
    usuarios = db.query(Usuarios).all()
    return usuarios

@usuario.post("/usuario", response_model=ModelUsuario, operation_id="save_usuario")
async def save_usuario(datos_usuario: ModelUsuario, db: Session = Depends(get_db)):
    """
    Guarda un nuevo usuario en la base de datos.
    """
    usuario_dict = datos_usuario.dict(exclude_unset=True, exclude={'Fecha_Registro', 'Fecha_Actualizacion'})
    usuario = Usuarios(**usuario_dict)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@usuario.put("/usuario/{usuario_id}", response_model=ModelUsuario, operation_id="update_usuario")
async def update_usuario(usuario_id: int, datos_actualizados: UpdateUsuario, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario existente.
    """
    usuario = db.query(Usuarios).filter(Usuarios.ID == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario

@usuario.delete("/usuario/{usuario_id}", operation_id="delete_usuario")
async def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos.
    """
    usuario = db.query(Usuarios).filter(Usuarios.ID == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"detail": "Usuario eliminado exitosamente"}

@usuario.get("/usuario/{usuario_id}", response_model=ModelUsuario, operation_id="get_usuario")
async def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el usuario solicitado por su ID.
    """
    usuario = db.query(Usuarios).filter(Usuarios.ID == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
