from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# se esta entrando en la base de datos con usuario: root y contraseña: 1234, en el puerto de conexion de MySQL 3306
URL_DATABSE = "mysql+pymysql://root:1234@localhost:3306/usuariosbd"


# Crear el motor de base de datos
engine = create_engine(URL_DATABSE)

# Probar la conexión
try:
    connection = engine.connect()
    print("Conexión exitosa a la base de datos")
    connection.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base declarativa
Base = declarative_base()

#Crear una clase base declarativa
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

# Crea las tablas en la base de datos
create_tables()