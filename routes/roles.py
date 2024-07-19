from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.roles, config.db, schemas.roles, models.roles
from typing import List
from cryptography.fernet import Fernet
from portadortoken import Portador

key=Fernet.generate_key()
f = Fernet(key)

roles = APIRouter()

models.roles.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@roles.get("/roles/", response_model=List[schemas.roles.Rol], tags=["Tbc_Roles"], dependencies=[Depends(Portador())])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_roles = crud.roles.get_all_roles(db=db, skip=skip, limit=limit)
    return db_roles

@roles.get("/roles/{id}", response_model=schemas.roles.Rol, tags=["Tbc_Roles"], dependencies=[Depends(Portador())])
def read_role(id: int, db: Session = Depends(get_db)):
    db_role = crud.roles.get_role(db=db, id=id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_role

@roles.post("/roles/", response_model=schemas.roles.Rol, tags=["Tbc_Roles"], dependencies=[Depends(Portador())])
def create_role(role: schemas.roles.RolCreate, db: Session = Depends(get_db)):
    db_role = crud.roles.get_role_by_name(db, nombre=role.Nombre)
    if db_role:
        raise HTTPException(status_code=400, detail="Rol existente, intenta nuevamente")
    return crud.roles.create_role(db=db, role=role)

@roles.put("/roles/{id}", response_model=schemas.roles.Rol, tags=["Tbc_Roles"], dependencies=[Depends(Portador())])
def update_role(id: int, role: schemas.roles.RolUpdate, db: Session = Depends(get_db)):
    db_role = crud.roles.update_role(db=db, id=id, role=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Rol no existe, no actualizado")
    return db_role

@roles.delete("/roles/{id}", response_model=schemas.roles.Rol, tags=["Tbc_Roles"], dependencies=[Depends(Portador())])
def delete_role(id: int, db: Session = Depends(get_db)):
    db_role = crud.roles.delete_role(db=db, id=id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Rol no existe, no se pudo eliminar")
    return db_role