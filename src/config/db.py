
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from decouple import config
from logger import Logs

logger = Logs()


try:
    password = config("PASSWORD")
    user= config("USER_NAME")
    host= config("HOST")
    db= config("DB")
    url = f"mysql+pymysql://{user}:{password}@{host}:3306/{db}"

    # Aquí hago la conexión a la base de datos... la base de datos se llama "database_fenix"
    engine = create_engine(url)
    # Guardo la conexión en una variable para luego utilizarla en otros archivos
    # MetaData actúa como un contenedor para mantener información sobre las tablas, columnas,
    # relaciones y otros elementos de la base de datos. Se utiliza para definir y manipular
    # estructuras de la base de datos en SQLAlchemy.

    Session = sessionmaker(engine)
    
    Base = declarative_base()

    Base.metadata.create_all(bind=engine)
    
    
except SQLAlchemyError as e:
    logger.error("Error al conectar a la base de datos:")
    print(f"Error al conectar a la base de datos: {e}")
    # Puedes agregar aquí el manejo de la excepción según tus necesidades
    
    
