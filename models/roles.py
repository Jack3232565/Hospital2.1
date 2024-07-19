from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from config.db import Base
from sqlalchemy.orm import relationship


class Roles(Base):
    __tablename__ = 'tbc_roles'

    id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255))
    Descripcion = Column(Text)
    Estatus = Column(Boolean, default=False)
    Fecha_Registro = Column(DateTime)
    Fecha_Actualizacion = Column(DateTime)


    usuarios = relationship("UsuarioRoles", back_populates="rol")