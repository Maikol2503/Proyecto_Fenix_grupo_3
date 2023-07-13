from fastapi import APIRouter
from services.descuentos_services import Descuentos_services
from schemas.descuentos import Descuentos




descuentos = APIRouter(tags=["descuentos"])


#COSULTAR
@descuentos.get("/descuentos")
async def todosLosAlumnos():
    descuento = Descuentos_services()
    result = descuento.descuento()
    return result



#CONSULTAR SOLO UNO
@descuentos.get("/descuento/{id}")
async def obtenerAlumnoPorNIE(id: int):
    descuento = Descuentos_services()
    result = descuento.descuento(id)
    return result


#AGREGAR
@descuentos.post("/descuentos")
async def agregarAlumno(descuento:Descuentos):
    descuentos = Descuentos_services()
    result = descuentos.agregar_descuento(descuento)
    return result
    
    

<<<<<<< HEAD
#EDITAR
# @alumnos.put("/descuento/{id}")
# async def editarAlumno(alumno_id: int, descuento:Descuentos):
#     descuentos = Descuentos_services()
#     result = Descuentos_services.ed
#     return result
=======
# #EDITAR
@descuentos.put("/descuento/{id}")
def editarAlumno(id: int, descuento:Descuentos):
    descuentos = Descuentos_services()
    result = descuentos.editar_descuento(id, descuento)
    return result
>>>>>>> e0045007b4438588e2a29781e581c50659bfeb27
