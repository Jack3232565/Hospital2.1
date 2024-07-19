from sqlalchemy.orm import Session
from models import usuario_roles as models_usuario_roles
from schemas import usuario_roles as schemas_usuario_roles


def get_usuario_roles(db: Session, usuario_id: int, rol_id: int):
    return db.query(models_usuario_roles.UsuarioRoles).filter(
        models_usuario_roles.UsuarioRoles.Usuario_ID == usuario_id,
        models_usuario_roles.UsuarioRoles.Rol_ID == rol_id
    ).first()

def get_all_usuario_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models_usuario_roles.UsuarioRoles).offset(skip).limit(limit).all()

def get_usuario_roles_by_usuario_id(db: Session, usuario_id: int):
    return db.query(models_usuario_roles.UsuarioRoles).filter(
        models_usuario_roles.UsuarioRoles.Usuario_ID == usuario_id
    ).all()  # Cambiado a `.all()` para obtener una lista de roles, no solo el primero

def create_usuario_roles(db: Session, usuario_roles: schemas_usuario_roles.Usuario_RolesCreate):
    db_usuario_role = models_usuario_roles.UsuarioRoles(
        Usuario_ID=usuario_roles.Usuario_ID,
        Rol_ID=usuario_roles.Rol_ID,
        Estatus=usuario_roles.Estatus,
        Fecha_Registro=usuario_roles.Fecha_Registro,
        Fecha_Actualizacion=usuario_roles.Fecha_Actualizacion
    )
    db.add(db_usuario_role)
    db.commit()
    db.refresh(db_usuario_role)
    return db_usuario_role

def update_usuario_roles(db: Session, usuario_id: int, rol_id: int, usuario_roles: schemas_usuario_roles.Usuario_RolesUpdate):
    db_usuario_role = db.query(models_usuario_roles.UsuarioRoles).filter(
        models_usuario_roles.UsuarioRoles.Usuario_ID == usuario_id,
        models_usuario_roles.UsuarioRoles.Rol_ID == rol_id
    ).first()
    if db_usuario_role:
        for key, value in usuario_roles.dict(exclude_unset=True).items():
            setattr(db_usuario_role, key, value)
        db.commit()
        db.refresh(db_usuario_role)
    return db_usuario_role

def delete_usuario_roles(db: Session, usuario_id: int, rol_id: int):
    db_usuario_role = db.query(models_usuario_roles.UsuarioRoles).filter(
        models_usuario_roles.UsuarioRoles.Usuario_ID == usuario_id,
        models_usuario_roles.UsuarioRoles.Rol_ID == rol_id
    ).first()
    if db_usuario_role:
        db.delete(db_usuario_role)
        db.commit()
    return db_usuario_role
