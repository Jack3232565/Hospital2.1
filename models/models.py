from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, UniqueConstraint, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.sql import func  # Importar func para usar funciones de SQL
from sqlalchemy.orm import relationship

Base = declarative_base()

class Personas(Base):
    __tablename__ = 'tbb_personas'
    
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Titulo = Column(String(20), nullable=True)
    Nombre = Column(String(80), nullable=False)
    Primer_Apellido = Column(String(80), nullable=False)
    Segundo_Apellido = Column(String(80), nullable=True)
    CURP = Column(String(18), nullable=True, unique=True)
    Genero = Column(Enum('M', 'F', 'N/B', name='genero_enum'), nullable=False)
    Grupo_Sanguineo = Column(Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='grupo_sanguineo_enum'), nullable=False)
    Fecha_Nacimiento = Column(Date, nullable=False)
    Estatus = Column(BIT(1), nullable=False, default=1)
    Fecha_Registro = Column(DateTime, nullable=False, server_default=func.now())  # Usa func.now() para establecer la fecha actual en la inserción
    Fecha_Actualizacion = Column(DateTime, nullable=True, onupdate=func.now())  # Usa func.now() para actualizar la fecha cada vez que se modifica el registro

    __table_args__ = (
        {'mysql_engine': 'InnoDB'},
    )

class Usuarios(Base):
    __tablename__ = 'tbb_usuarios'
    
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Persona_ID = Column(Integer, ForeignKey('tbb_personas.ID'), nullable=False)
    Nombre_Usuario = Column(String(60), nullable=False, unique=True)
    Correo_Electronico = Column(String(100), nullable=False, unique=True)
    Contrasena = Column(String(40), nullable=False)
    Numero_Telefonico_Movil = Column(String(19), nullable=False, unique=True)
    Estatus = Column(Enum('Activo', 'Inactivo', 'Bloqueado', 'Suspendido', name='estatus_enum'), nullable=True)
    Fecha_Registro = Column(DateTime, nullable=False, server_default=func.now())
    Fecha_Actualizacion = Column(DateTime, nullable=True, onupdate=func.now())

    # Relación con la tabla de Personas
    persona = relationship('Personas', backref='usuarios')

    __table_args__ = (
        UniqueConstraint('Correo_Electronico', name='Correo_Electronico_UNIQUE'),
        UniqueConstraint('Nombre_Usuario', name='Nombre_Usuario_UNIQUE'),
        UniqueConstraint('Numero_Telefonico_Movil', name='Numero_Telefonico_Movil_UNIQUE'),
        {'mysql_engine': 'InnoDB'},
    )