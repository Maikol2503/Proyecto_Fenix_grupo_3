from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.alumnosModel import Alumnos_model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from config.db import Session


class Alumnos_services:
    def __init__(self):
        #db para que cada vez que se ejecute ese servicio
        #se envíe una sesión a la base de datos
        self.db = Session()
        #ya puedo acceder a la base de datos desde otros métodos


    # CONSULTAR TODOS LOS ALUMNOS
    def consultar_alumnos(self):
        result = self.db.query(Alumnos_model).all()
        #obtengo todos los datos Alumnos_model y los guardo en la variable result
        if not result:
        # Si no se encuentran alumnos, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Aún no hay alumnos"}) 
        
        return JSONResponse(status_code=200, content=jsonable_encoder(result))


    # CONSULTAR UN ALUMNO POR ID
    def consultar_alumno(self, id):
        result = self.db.query(Alumnos_model).filter(Alumnos_model.id_alumno == id).first()
        # obtengo los datos de el alumno que quiero consultar filtrando por id,
        # obtengo los del primero que encuentre y los guardo en la variable result
        if not result:
            # Si no se encuentra el alumno, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message':'No existe ningún alumno con ese id'})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))


    # AGREGAR UN NUEVO ALUMNO
    def agregar_alumno(self, data):
        alumno = self.db.query(Alumnos_model).filter(Alumnos_model.id_alumno == data.id_alumno).first()

        if alumno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message':'Ya existe un alumno con este id'})

        nuevo_alumno = Alumnos_model(**data.dict())
        #Le envío el nuevo alumno
        self.db.add(nuevo_alumno)
        #Hago el commit para que se actualice
        self.db.commit()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado un nuevo alumno"})


    # EDITAR UN ALUMNO
    def editar_alumno(self, id: str, data):
        alumno = self.db.query(Alumnos_model).filter(Alumnos_model.id_alumno == id).first()

        if not alumno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"No existe ningún alumno con ese id"})

        alumno.nombre_alumno = data.nombre_alumno
        alumno.apellido_alumno = data.apellido_alumno
        alumno.edad_alumno = data.edad_alumno
        alumno.email_alumno = data.email_alumno
        alumno.telefono_alumno = data.telefono_alumno
        alumno.descuento_familiar = data.descuento_familiar

        self.db.commit()
        return JSONResponse(status_code=200, content={"message": "Se ha modificado el alumno"})


    # BORRAR UN ALUMNO
    def borrar_alumno(self, id: str):
        alumno = self.db.query(Alumnos_model).filter(Alumnos_model.id_alumno == id).first()

        if not alumno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message':'Ya existe un alumno con este id'})
        self.db.query(Alumnos_model).filter(Alumnos_model.id_alumno == id).delete()
        self.db.commit()
        return JSONResponse(status_code=200, content={"message": "Se ha eliminado el alumno"})
