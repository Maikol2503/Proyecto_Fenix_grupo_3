from datetime import date
from typing import List
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from services.pagos_services import Pagos_services
from schemas.pagos import Pagos
from config.db import Base, engine


pagos = APIRouter(tags=["pagos"])

# # CREAR TABLA DE PAGOS
# @pagos.on_event("startup")
# def startup():
#      # create db tables
#     Base.metadata.create_all(bind=engine)


# CONSULTAR TODOS LOS PAGOS
@pagos.get('/pagos', response_model= list)
def consultar_pago():
    result = Pagos_services().consultar_pagos()
    return result


# CONSULTAR LOS PAGOS CON ID ALUMNO
@pagos.get("/pagos/{id}", response_model=dict)
def consultar_pagos_con_id_alumno(id_alumno: int):
    result = Pagos_services().consultar_pago_por_id_del_alumno(id_alumno)
    return result

#MOSTRAR PAGOS POR RANGO DE FECHA
# http://tu-servidor/pagos?fecha_inicio=2023-07-01&fecha_fin=2023-07-15
@pagos.get("/pagos-fecha", response_model=dict)
def mostrar_pagos_por_fecha(fecha_inicio:str, fecha_fin:str):
    result = Pagos_services().mostrar_pagos_por_fecha(fecha_inicio, fecha_fin)
    return result



#MOSTRAR PAGOS POR RANGO DE FECHA
# http://tu-servidor/pagos?fecha_inicio=2023-07-01&fecha_fin=2023-07-15
@pagos.get("/pagos-fecha/{id_alumno}", response_model=dict)
def mostrar_pagos_de_alumno_por_fecha(fecha_inicio:str, fecha_fin:str, id_alumno):
    result = Pagos_services().mostrar_pagos_alumno_por_fecha(fecha_inicio, fecha_fin, id_alumno)
    return result



# AGREGAR UN PAGO
@pagos.post("/pagos", response_model=dict)
def agregar_pago(data:Pagos)-> dict:
    result = Pagos_services().agregar_pago(data)
    return result



