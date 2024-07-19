from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from config.db import Base
from sqlalchemy.orm import relationship
import enum

class Estatus(str, enum.Enum):
    En_Proceso = "En Proceso"  # Coincidir con los esquemas
    Pausado = "Pausado"
    Aprobado = "Aprobado"
    Reprogramado = "Reprogramado"
    Cancelado = "Cancelado"

class Tipo(str, enum.Enum):
    Servicio_Interno = "Servicio_Interno"  # Coincidir con los esquemas
    Traslados = "Traslados"
    Subrogado = "Subrogado"
    Administrativo = "Administrativo"

class Aprobaciones(Base):
    __tablename__ = "tbb_aprobaciones"
    id = Column(Integer, primary_key=True, index=True)
    # Personal_Medico_ID = Column(Integer, ForeignKey("personal_medico.id"))  # Añadido ForeignKey
    Personal_Medico_ID = Column(Integer)  # Añadido ForeignKey
    # Solicitud_id = Column(Integer, ForeignKey("solicitudes.id"))  # Añadido ForeignKey
    Solicitud_id = Column(Integer)  # Añadido ForeignKey
    Comentario = Column(String(500))
    Estatus = Column(Enum(Estatus))
    Tipo = Column(Enum(Tipo))
    Fecha_Registro = Column(DateTime)
    Fecha_Actualizacion = Column(DateTime)  # Corregido el nombre

    # # Relaciones (Si las tablas existen)
    # personal_medico = relationship("PersonalMedico", back_populates="aprobaciones")  # Ejemplo
    # solicitud = relationship("Solicitud", back_populates="aprobaciones")  # Ejemplo
