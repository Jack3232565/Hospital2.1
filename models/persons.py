from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Enum , ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class genero(str, enum.Enum):
    Masculino = "Masculino"
    Femenino = "Femenino"
    Otro = "N/B"

class sangre(str, enum.Enum):
   AP = "A+"
   AN = "A-"
   BP = "B+"
   BN = "B-"
   ABP = "AB+"
   ABN = "AB-"
   OP = "O+"
   ON = "O-" 

class Person(Base):
    __tablename__ = "tbb_personas"

    id = Column(Integer, primary_key=True, index=True)
    Titulo_Cortesia = Column(String(20))
    Nombre = Column(String(80))
    Primer_Apellido = Column(String(80))
    Segundo_Apellido = Column(String(80))
    Fecha_Nacimiento = Column(Date)
    Fotografia = Column(String(100))
    Genero = Column(Enum(genero))
    Tipo_Sangre = Column(Enum(sangre))
    Estatus = Column(Boolean, default=False)
    Fecha_Registro = Column(DateTime)
    Fecha_Actualizacion = Column(DateTime)
    #items = relationship("Item", back_populates="owner")

    