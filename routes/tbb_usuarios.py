from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import json
import crud.users
import crud.tbb_usuarios, config.db, schemas.tbb_usuarios, models.tbb_usuarios
from typing import List

from jwt_config import solicita_token   
from portadortoken import Portador

key = Fernet.generate_key()
f = Fernet(key)

tbb_usuarios_router = APIRouter()

models.tbb_usuarios.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tbb_usuarios_router.get("/tbb_usuarios/", response_model=List[schemas.tbb_usuarios.tbb_usuario], tags=["Tbb_Usuarios"], dependencies=[Depends(Portador())])
def read_tbb_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_tbb_usuarios = crud.tbb_usuarios.get_all_tbb_usuarios(db=db, skip=skip, limit=limit)
    return db_tbb_usuarios

@tbb_usuarios_router.get("/tbb_usuarios/{id}", response_model=schemas.tbb_usuarios.tbb_usuario, tags=["Tbb_Usuarios"],  dependencies=[Depends(Portador())])
def read_tbb_usuario(id: int, db: Session = Depends(get_db)):
    db_tbb_usuario = crud.tbb_usuarios.get_tbb_usuario(db=db, id=id)
    if db_tbb_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_tbb_usuario

@tbb_usuarios_router.post("/tbb_usuarios/", response_model=schemas.tbb_usuarios.tbb_usuario, tags=["Tbb_Usuarios"])
def create_tbb_usuario(tbb_usuario: schemas.tbb_usuarios.tbb_usuarioCreate, db: Session = Depends(get_db)):
    db_tbb_usuario = crud.tbb_usuarios.get_tbb_usuario_by_name(db, nombre=tbb_usuario.Nombre_Usuario)
    if db_tbb_usuario:
        raise HTTPException(status_code=400, detail="Usuario existente, intenta nuevamente")
    return crud.tbb_usuarios.create_tbb_usuario(db=db, tbb_usuario=tbb_usuario)

@tbb_usuarios_router.put("/tbb_usuarios/{id}", response_model=schemas.tbb_usuarios.tbb_usuario, tags=["Tbb_Usuarios"], dependencies=[Depends(Portador())])
def update_tbb_usuario(id: int, tbb_usuario: schemas.tbb_usuarios.tbb_usuarioUpdate, db: Session = Depends(get_db)):
    db_tbb_usuario = crud.tbb_usuarios.update_tbb_usuario(db=db, id=id, tbb_usuario=tbb_usuario)
    if db_tbb_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no existe, no actualizado")
    return db_tbb_usuario

@tbb_usuarios_router.delete("/tbb_usuarios/{id}", response_model=schemas.tbb_usuarios.tbb_usuario, tags=["Tbb_Usuarios"], dependencies=[Depends(Portador())])
def delete_tbb_usuario(id: int, db: Session = Depends(get_db)):
    db_tbb_usuario = crud.tbb_usuarios.delete_tbb_usuario(db=db, id=id)
    if db_tbb_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no existe, no se pudo eliminar")
    return db_tbb_usuario

@tbb_usuarios_router.post("/login/", response_model=schemas.tbb_usuarios.UserLogin, tags=["Usuario Login"])
def read_credentials(usuario:schemas.tbb_usuarios.UserLogin, db:Session = Depends(get_db)):
    db_credentials = crud.tbb_usuarios.get_user_by_credentials(db, username=usuario.Nombre_Usuario,
                                                               correo=usuario.Correo_Electronico,
                                                               telefono=usuario.Numero_Telefonico_Movil,
                                                               password=usuario.Contrasena)
    if db_credentials is None:
        return JSONResponse(content={'mensaje':'Acceso Denegado'}, status_code=404)
    token:str=solicita_token(usuario.dict())
    return JSONResponse(status_code=200, content=token)