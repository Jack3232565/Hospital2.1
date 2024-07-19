from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class Estatus(str, enum.Enum):
    En_Proceso = "En Proceso"
    Pausado = "Pausado"
    Aprobado = "Aprobado"
    Reprogramado = "Reprogramado"
    Cancelado = "Cancelado"

class Tipo(str, enum.Enum):
    Servicio_Interno = "Servicio_Interno"
    Traslados = "Traslados"
    Subrogado = "Subrogado"
    Administrativo = "Administrativo"

class TbbAprobacionesBase(BaseModel):
    Personal_Medico_ID: int
    Solicitud_id: int
    Comentario: str
    Estatus: Estatus
    Tipo: Tipo
    Fecha_Registro: datetime
    Fecha_Actualizacion: datetime  

class TbbAprobacionesCreate(TbbAprobacionesBase):
    pass

class TbbAprobacionesUpdate(TbbAprobacionesBase):
    pass

    class Config:
        from_attributes = True
