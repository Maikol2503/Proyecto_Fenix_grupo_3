from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import and_, text
from models.pagosModel import Pagos_model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from config.db import Session
from models.incripcionesModel import Inscripciones_model
from logger import Logs

class Pagos_services:
    def __init__(self):
        self.db = Session()
        self.logger= Logs()



    # CONSULTAR TODOS LOS PAGOS
    def consultar_pagos(self):
        result = self.db.query(Pagos_model).all()
        self.logger.debug('Consultando todos los pagos')
        #obtengo todos los datos de Pagos_model y los guardo en la variable result
        if not result:
            self.logger.warning('No se encontraron pagos')
        # Si no se encuentran pagos, se lanza una excepción HTTP con el código de estado 404 y un mensaje de error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aún no hay pagos")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))


    # CONSULTAR UN PAGO POR ID DEL ALUMNO
    def consultar_pago_por_id_del_alumno(self, id):
        query = f""" SELECT p.*, i.precio_con_descuento AS monto
                    FROM pagos AS p
                    JOIN inscripciones AS i ON i.id_inscripcion = p.inscripcion_id
                    WHERE i.alumno_id = {id}"""
        results = self.db.execute(text(query)).fetchall()
        self.logger.debug(f'Consultando pago por id')

        if not results:
            self.logger.warning('No se encontró el pago')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")

        result_dict = [{"id":item[0], "id_inscripcion":item[1],"fecha":item[2], "monto":item[3]}for item in results]
        return JSONResponse(status_code=200, content=jsonable_encoder(result_dict))
    
    #CONSULTAR PAGOS POR RANGOS DE FECHA
    def mostrar_pagos_por_fecha(self, fecha_inicio, fecha_fin):
        pagos_filtrados = self.db.query(Pagos_model).filter(and_(Pagos_model.fecha_pago >= fecha_inicio, Pagos_model.fecha_pago <= fecha_fin)).all()
        if not pagos_filtrados:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"no hay pagos en este rango de fechas"})
        return JSONResponse(status_code=200, content=jsonable_encoder(pagos_filtrados))
    
    #CONSULTAR PAGOS DE UN ALUMNO POR RANGOS DE FECHA
    def mostrar_pagos_alumno_por_fecha(self, fecha_inicio, fecha_fin, id):
        query = f"""SELECT p.*, i.alumno_id
                    FROM pagos AS p
                    JOIN inscripciones AS i ON  i.id_inscripcion = p.inscripcion_id
                    JOIN alumnos AS a ON a.id_alumno = i.alumno_id
                    WHERE fecha_pago >= '{fecha_inicio}' AND fecha_pago <= '{fecha_fin}' AND a.id_alumno = {id};"""
                    
        pagos_filtrados = self.db.execute(text(query)).fetchall()
    
        if not pagos_filtrados:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"no hay pagos en este rango de fechas"})
        pagos_filtrados_dict = [{"id_pago":item[0], "id_inscripcion":item[1],"fecha_pago":item[2], "id_alumno":item[3] } for item in pagos_filtrados]
        return JSONResponse(status_code=200, content=jsonable_encoder(pagos_filtrados_dict))


    # CREAR UN PAGO
    def agregar_pago(self, data):
        pago = self.db.query(Inscripciones_model)\
                        .filter(and_(Inscripciones_model.id_inscripcion == data.inscripcion_id, Inscripciones_model.pagada == 'true')).all()
        if pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404")

        self.agregar_pago_en_inscripcion(data.inscripcion_id)
        nuevo_pago = Pagos_model(**data.dict())
        self.db.add(nuevo_pago)
        self.db.commit()
        self.logger.info("Se ha registrado un nuevo pago")
        return JSONResponse(status_code=201, content={"message": "Se ha registrado un nuevo pago correctamente"})



    # ACTUALIZAR A TRUE EN LA COLUMNA PAGADA DE LA TABLA DE INSCRIPCIONES
    def agregar_pago_en_inscripcion(self, id):
        inscripcion = self.db.query(Inscripciones_model).filter(Inscripciones_model.id_inscripcion == id).first()
        inscripcion.pagada = 'true'
        self.db.commit()
        self.logger.info("Se ha registrado un nuevo pago en la inscripcion")
        return JSONResponse(status_code=201, content={"message": "Se ha añadido el pago a la tabla de inscripciones"})
