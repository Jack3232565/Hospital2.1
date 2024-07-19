from sqlalchemy.orm import Session
import models.tbb_aprobaciones
import schemas.tbb_aprobaciones

def get_aprobaciones(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.tbb_aprobaciones.Aprobaciones).offset(skip).limit(limit).all()

def get_aprobacion(db: Session, id: int):
    return db.query(models.tbb_aprobaciones.Aprobaciones).filter(models.tbb_aprobaciones.Aprobaciones.id == id).first()

def create_aprobacion(db: Session, aprobacion: schemas.tbb_aprobaciones.TbbAprobacionesCreate):
    db_aprobacion = models.tbb_aprobaciones.Aprobaciones(
        Personal_Medico_ID=aprobacion.Personal_Medico_ID,
        Solicitud_id=aprobacion.Solicitud_id,
        Comentario=aprobacion.Comentario,
        Estatus=aprobacion.Estatus,
        Tipo=aprobacion.Tipo,
        Fecha_Registro=aprobacion.Fecha_Registro,
        Fecha_Actualizacion=aprobacion.Fecha_Actualizacion,
    )
    db.add(db_aprobacion)
    db.commit()
    db.refresh(db_aprobacion)
    return db_aprobacion

def update_aprobacion(db: Session, id: int, aprobacion: schemas.tbb_aprobaciones.TbbAprobacionesUpdate):
    db_aprobacion = db.query(models.tbb_aprobaciones.Aprobaciones).filter(models.tbb_aprobaciones.Aprobaciones.id == id).first()
    if db_aprobacion:
        db_aprobacion.Personal_Medico_ID = aprobacion.Personal_Medico_ID
        db_aprobacion.Solicitud_id = aprobacion.Solicitud_id
        db_aprobacion.Comentario = aprobacion.Comentario
        db_aprobacion.Estatus = aprobacion.Estatus
        db_aprobacion.Tipo = aprobacion.Tipo
        db_aprobacion.Fecha_Registro = aprobacion.Fecha_Registro
        db_aprobacion.Fecha_Actualizacion = aprobacion.Fecha_Actualizacion
        db.commit()
        db.refresh(db_aprobacion)
    return db_aprobacion

def delete_aprobacion(db: Session, id: int):
    db_aprobacion = db.query(models.tbb_aprobaciones.Aprobaciones).filter(models.tbb_aprobaciones.Aprobaciones.id == id).first()
    if db_aprobacion:
        db.delete(db_aprobacion)
        db.commit()
    return db_aprobacion
