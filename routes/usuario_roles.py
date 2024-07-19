from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.usuario_roles  # Asegúrate de que estas importaciones existen y son correctas
import config.db
import schemas.usuario_roles
import models.usuario_roles
from typing import List
from cryptography.fernet import Fernet
from portadortoken import Portador

key=Fernet.generate_key()
f = Fernet(key)


# Definir el router
usuario_roles_router = APIRouter()

# Crear todas las tablas (esto generalmente se hace en el arranque de la aplicación, no aquí en el router)
# models.usuario_roles.Base.metadata.create_all(bind=config.db.engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para obtener todos los roles de usuario con paginación
@usuario_roles_router.get("/usuario_roles/", response_model=List[schemas.usuario_roles.Usuario_Roles], tags=["Tbd_Usuarios_Roles"], dependencies=[Depends(Portador())])
def read_usuario_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_usuario_roles = crud.usuario_roles.get_all_usuario_roles(db=db, skip=skip, limit=limit)
    return db_usuario_roles

# Ruta para obtener un rol de usuario específico por ID de usuario y rol
@usuario_roles_router.get("/usuario_roles/{usuario_id}/{rol_id}", response_model=schemas.usuario_roles.Usuario_Roles, tags=["Tbd_Usuarios_Roles"], dependencies=[Depends(Portador())])
def read_usuario_role(usuario_id: int, rol_id: int, db: Session = Depends(get_db)):
    db_usuario_role = crud.usuario_roles.get_usuario_roles(db=db, usuario_id=usuario_id, rol_id=rol_id)
    if db_usuario_role is None:
        raise HTTPException(status_code=404, detail="UsuarioRol no encontrado")
    return db_usuario_role

# Ruta para crear un nuevo rol de usuario
@usuario_roles_router.post("/usuario_roles/", response_model=schemas.usuario_roles.Usuario_Roles, tags=["Tbd_Usuarios_Roles"], dependencies=[Depends(Portador())])
def create_usuario_role(usuario_role: schemas.usuario_roles.Usuario_RolesCreate, db: Session = Depends(get_db)):
    db_usuario_role = crud.usuario_roles.get_usuario_roles(db, usuario_id=usuario_role.Usuario_ID, rol_id=usuario_role.Rol_ID)
    if db_usuario_role:
        raise HTTPException(status_code=400, detail="UsuarioRol existente, intenta nuevamente")
    return crud.usuario_roles.create_usuario_roles(db=db, usuario_roles=usuario_role)

# Ruta para actualizar un rol de usuario existente
@usuario_roles_router.put("/usuario_roles/{usuario_id}/{rol_id}", response_model=schemas.usuario_roles.Usuario_Roles, tags=["Tbd_Usuarios_Roles"], dependencies=[Depends(Portador())])
def update_usuario_role(usuario_id: int, rol_id: int, usuario_role: schemas.usuario_roles.Usuario_RolesUpdate, db: Session = Depends(get_db)):
    db_usuario_role = crud.usuario_roles.update_usuario_roles(db=db, usuario_id=usuario_id, rol_id=rol_id, usuario_roles=usuario_role)
    if db_usuario_role is None:
        raise HTTPException(status_code=404, detail="UsuarioRol no existe, no actualizado")
    return db_usuario_role

# Ruta para eliminar un rol de usuario
@usuario_roles_router.delete("/usuario_roles/{usuario_id}/{rol_id}", response_model=schemas.usuario_roles.Usuario_Roles, tags=["Tbd_Usuarios_Roles"], dependencies=[Depends(Portador())])
def delete_usuario_role(usuario_id: int, rol_id: int, db: Session = Depends(get_db)):
    db_usuario_role = crud.usuario_roles.delete_usuario_roles(db=db, usuario_id=usuario_id, rol_id=rol_id)
    if db_usuario_role is None:
        raise HTTPException(status_code=404, detail="UsuarioRol no existe, no se pudo eliminar")
    return db_usuario_role
