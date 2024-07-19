from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Usuario_RolesBase(BaseModel):
    Usuario_ID: int
    Rol_ID: int
    Estatus: bool
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime]

class Usuario_RolesCreate(Usuario_RolesBase):
    pass

class Usuario_RolesUpdate(BaseModel):
    Estatus: Optional[bool]
    Fecha_Actualizacion: Optional[datetime]

class Usuario_Roles(Usuario_RolesBase):
    class Config:
        from_attributes= True
        
