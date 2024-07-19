
##############################  Archivo creado en clase 04/07/2024

## Este archivo integra la estrucutura de la base de datos
## se Instala 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

#se esta entrando en la base de datos con usuario: root y contraseña: 1234, en el puerto de conexion de MySQL 3306
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")




#Crear el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#diferencia en la base de datos en el modelo database.py
#engine = create_engine(URL_DATABSE)

#Probar la conexión
try:
   connection = engine.connect()
   print("Conexión exitosa a la base de datos de test")
   connection.close()
except Exception as e:
   print(f"Error al conectar a la base de datos: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Crear una clase base declarativa
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

# Crea las tablas en la base de datos
create_tables()