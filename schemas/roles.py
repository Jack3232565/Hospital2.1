from typing import List, Union
from pydantic import BaseModel
from datetime import datetime

class RolBase(BaseModel):
    Nombre: str
    Descripcion: str
    Estatus: bool
    Fecha_Registro: datetime
    Fecha_Actualizacion: datetime


class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    pass

class Rol(RolBase):
    id: int
    #owner_id: int clave foranea
    class Config:
        from_attributes= True
        
# class UserLogin(BaseModel):
#     usuario: str
#     password: str