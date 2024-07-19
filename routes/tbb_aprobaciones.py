from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.tbb_aprobaciones, config.db, schemas.tbb_aprobaciones, models.tbb_aprobaciones
from typing import List

tbb_aprobaciones = APIRouter()

models.tbb_aprobaciones.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tbb_aprobaciones.get("/tbb_aprobaciones/", response_model=List[schemas.tbb_aprobaciones.TbbAprobacionesCreate], tags=["Tbb_Aprobaciones"])  # Corregido
def read_aprobaciones(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_aprobaciones = crud.tbb_aprobaciones.get_aprobaciones(db=db, skip=skip, limit=limit)
    return db_aprobaciones

@tbb_aprobaciones.get("/tbb_aprobaciones/{id}", response_model=schemas.tbb_aprobaciones.TbbAprobacionesCreate, tags=["Tbb_Aprobaciones"])  # Corregido
def read_aprobacion(id: int, db: Session = Depends(get_db)):
    db_aprobacion = crud.tbb_aprobaciones.get_aprobacion(db=db, id=id)
    if db_aprobacion is None:
        raise HTTPException(status_code=404, detail="Aprobación no encontrada")
    return db_aprobacion

@tbb_aprobaciones.post("/tbb_aprobaciones/", response_model=schemas.tbb_aprobaciones.TbbAprobacionesCreate, tags=["Tbb_Aprobaciones"])  # Corregido
def create_tbb_aprobacion(tbb_aprobacion: schemas.tbb_aprobaciones.TbbAprobacionesCreate, db: Session = Depends(get_db)):
    return crud.tbb_aprobaciones.create_aprobacion(db=db, aprobacion=tbb_aprobacion)

@tbb_aprobaciones.put("/tbb_aprobaciones/{id}", response_model=schemas.tbb_aprobaciones.TbbAprobacionesCreate, tags=["Tbb_Aprobaciones"])  # Corregido
def update_tbb_aprobacion(id: int, tbb_aprobacion: schemas.tbb_aprobaciones.TbbAprobacionesUpdate, db: Session = Depends(get_db)):  # Corregido
    db_tbb_aprobacion = crud.tbb_aprobaciones.update_aprobacion(db=db, id=id, aprobacion=tbb_aprobacion)
    if db_tbb_aprobacion is None:
        raise HTTPException(status_code=404, detail="Aprobación no encontrada, no se pudo actualizar")
    return db_tbb_aprobacion

@tbb_aprobaciones.delete("/tbb_aprobaciones/{id}", response_model=schemas.tbb_aprobaciones.TbbAprobacionesCreate, tags=["Tbb_Aprobaciones"])  # Corregido
def delete_aprobacion(id: int, db: Session = Depends(get_db)):
    db_tbb_aprobacion = crud.tbb_aprobaciones.delete_aprobacion(db=db, id=id)
    if db_tbb_aprobacion is None:
        raise HTTPException(status_code=404, detail="Aprobación no encontrada, no se pudo eliminar")
    return db_tbb_aprobacion
