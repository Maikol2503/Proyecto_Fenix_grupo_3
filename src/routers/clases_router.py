from typing import List
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from services.clases_services import Clases_services
from schemas.clases import Clases
from config.db import Base, engine

clases = APIRouter(tags=["clases"])

@clases.on_event("startup")
def startup():
    # create db table
    Base.metadata.create_all(bind=engine)


#CONSULTAR SOLO UNO
@clases.get('/clase/{id}', response_model=Clases)
def consultar_clase_por_nombre(id: int):
    result = Clases_services().consultar_clase(nombre)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


#AGREGAR
@clases.post("/clases", response_model=dict, status_code=201)
def agregar_clase(clase: Clases)-> dict:
    Clases_services().agregar_clase(clase)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado un nuevo clase"})


#EDITAR
@clases.put("/clases/{id}", response_model=dict, status_code=200)
def editar_clase(id: int, data: Clases)-> dict:
    Clases_services().editar_clase(id, data)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el clase"})

#BORRAR
@clases.delete('/clases/{id}', response_model=dict, status_code=200)
def borrar_clase(id: int) -> dict:
    Clases_services().borrar_clase(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el clase"})


    