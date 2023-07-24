from sqlalchemy.exc import SQLAlchemyError
from models.profesoresModel import Profesores_model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from config.db import Session


class Profesores_services:
    def __init__(self) -> None:
        self.db = Session()
        #db para que cada vez que se ejecute ese servicio se envíe una sesión a la base de datos
        #ya puedo acceder a la base de datos desde otros métodos

    # CONSULTAR TODOS LOS PROFESORES
    def consultar_profesores(self):
            result = self.db.query(Profesores_model).all()
            # Obtengo todos los datos Profesores_model y los guardo en la variable result.
            return result

    # CONSULTAR UN PROFESOR
    def consultar_profesor(self, nombre):
        result = self.db.query(Profesores_model).filter(Profesores_model.nombre_profesor == nombre).first()
         # Obtengo los datos del profesor que quiero consultar filtrando por nombre.
         # Obtengo los del primero que encuentre y los guardo en la variable result.
        if not result:
            # Si no se encuentra el profesor, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return result

    # AGREGAR UN PROFESOR
    def agregar_profesor(self, data):
        nuevo_profesor = Profesores_model(**data.dict())
        #Le envío el nuevo profesor
        self.db.add(nuevo_profesor)
         #Hago el commit para que se actualice
        self.db.commit()
        return f"Se agregó el profesor {nuevo_profesor} correctamente"


    # EDITAR UN PROFESOR
    def editar_profesor(self, nombre: str, data):
        profesor = self.db.query(Profesores_model).filter(Profesores_model.nombre_profesor == nombre).first()
        if not profesor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")

        profesor.nombre_profesor = data.nombre_profesor
        profesor.apellido_profesor = data.apellido_profesor
        profesor.email_profesor = data.email_profesor
        self.db.commit()

        return {"message": "Profesor actualizado correctamente"}


    # BORRAR UN PROFESOR
    def borrar_profesor(self, nombre: str):
        profesor = self.db.query(Profesores_model).filter(Profesores_model.nombre_profesor == nombre).first()
        if not profesor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe ningún profesor con ese nombre")
        self.db.query(Profesores_model).filter(Profesores_model.nombre_profesor == nombre).delete()
        self.db.commit()
        return


