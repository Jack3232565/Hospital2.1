from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from models.database import SessionLocal  # Ajuste el import
from models.models import Personas  # Ajuste el import


# Crear un enrutador para las rutas de persona
persona = APIRouter()

# Activacion y Cierra base de datos si no se usa
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lista para almacenar las personas en memoria (solo para demostración)
# personas = []

# Modelo de datos para una Persona
class ModelPersona(BaseModel):
    ID: int
    Titulo: Optional[str] = None
    Nombre: str
    Primer_Apellido: str
    Segundo_Apellido: Optional[str] = None
    CURP: Optional[str] = None
    Genero: str
    Grupo_Sanguineo: str
    Fecha_Nacimiento: date
    Estatus: bool = False
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelo de datos para actualizar parcialmente una Personas
class UpdatePersona(BaseModel):
    Titulo: Optional[str] = None
    Nombre: Optional[str] = None
    Primer_Apellido: Optional[str] = None
    Segundo_Apellido: Optional[str] = None
    CURP: Optional[str] = None
    Genero: Optional[str] = None
    Grupo_Sanguineo: Optional[str] = None
    Fecha_Nacimiento: Optional[date] = None
    Estatus: Optional[bool] = None
    Fecha_Actualizacion: Optional[datetime] = None


# Ruta de bienvenida
@persona.get('/')
def bienvenida():
    """
    Ruta de bienvenida.
    """
    return 'Bienvenido al Sistema'

# Ruta para obtener todas las personas
# @persona.get("/persona", response_model=List[ModelPersona])
# async def get_personas():
#     """
#     Obtiene la lista de todas las personas.
#     """
#     return personas

@persona.get("/persona", response_model=List[ModelPersona])
async def get_personas(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todas las personas.
    """
    personas = db.query(Personas).all()
    return personas


# Busca a la Persona seleccionada con la Id
@persona.get("/persona/{persona_id}", response_model=ModelPersona)
async def get_persona(persona_id: int, db: Session = Depends(get_db)):
    """
    Obtiene la persona solicitada por su ID.
    """
    persona = db.query(Personas).filter(Personas.ID == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


# Ruta para guardar una nueva persona
@persona.post("/persona", response_model=ModelPersona)
async def save_persona(datos_persona: ModelPersona, db: Session = Depends(get_db)):
    """
    Guarda una nueva persona en la base de datos.
    """
    persona = Personas(**datos_persona.dict())
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona



# Ruta para actualizar una persona existente
@persona.put("/persona/{persona_id}", response_model=ModelPersona)
async def update_persona(persona_id: int, datos_actualizados: UpdatePersona, db: Session = Depends(get_db)):
    """
    Actualiza los datos de una persona existente.
    """
    persona = db.query(Personas).filter(Personas.ID == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(persona, key, value)

    db.commit()
    db.refresh(persona)
    return persona



# Ruta para eliminar una persona existente
@persona.delete("/persona/{persona_id}")
async def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """
    Elimina una persona de la base de datos.
    """
    persona = db.query(Personas).filter(Personas.ID == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    db.delete(persona)
    db.commit()
    return {"detail": "Persona eliminada exitosamente"}












