from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from enum import Enum

class EstatusEnum(str, Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Bloqueado = "Bloqueado"
    Suspendido = "Suspendido"

class Model_tbb_usuario(BaseModel):
    ID: int
    Persona_ID: int
    Nombre_Usuario: str
    Correo_Electronico: EmailStr
    Contrasena: str
    Numero_Telefonico_Movil: str
    Estatus: EstatusEnum
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class tbb_usuarioCreate(Model_tbb_usuario):
    pass

class tbb_usuarioUpdate(Model_tbb_usuario):
    pass

class tbb_usuario(Model_tbb_usuario):
    ID: int
    Persona_ID: int
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    Nombre_Usuario: Optional[str] = None
    Correo_Electronico: Optional[str] = None
    Contrasena: str
    Numero_Telefonico_Movil: Optional[str]=None
