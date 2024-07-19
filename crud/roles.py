from sqlalchemy.orm import Session
from models import roles as models_roles
from schemas import roles as schemas_roles

def get_role(db: Session, id: int):
    return db.query(models_roles.Roles).filter(models_roles.Roles.id == id).first()

def get_all_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models_roles.Roles).offset(skip).limit(limit).all()

def get_role_by_name(db: Session, nombre: str):
    return db.query(models_roles.Roles).filter(models_roles.Roles.Nombre == nombre).first()

def create_role(db: Session, role: schemas_roles.RolCreate):
    db_role = models_roles.Roles(
        Nombre=role.Nombre,
        Descripcion=role.Descripcion,
        Estatus=role.Estatus,
        Fecha_Registro=role.Fecha_Registro,
        Fecha_Actualizacion=role.Fecha_Actualizacion
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, id: int, role: schemas_roles.RolUpdate):
    db_role = db.query(models_roles.Roles).filter(models_roles.Roles.id == id).first()
    if db_role:
        for key, value in role.dict(exclude_unset=True).items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_role(db: Session, id: int):
    db_role = db.query(models_roles.Roles).filter(models_roles.Roles.id == id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role