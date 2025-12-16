from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from database.connection import get_connection
from app.models.envios import (envios_to_dict,
                               iniciar_historial_envio,
                               get_ultimo_estado_historial,
                               add_registro_historial)
from datetime import datetime
from typing import Optional
from enum import Enum

class EstadosEnvios(str,Enum):
    borrador = "BORRADOR"
    listo = "LISTO PARA ENVIAR"
    transito = "EN TRANSITO"
    entregado = "ENTREGADO"
    cancelado = "CANCELADO"

class ModeloCrearEnvio(BaseModel):

    nombre:str = Field(...,max_length=150)
    tipo_trailer: str = Field(...)
    ubicacion_origen:str = Field(...,max_length=150) 
    ubicacion_destino:str = Field(...,max_length=150)
    estado:Optional[EstadosEnvios] = None
    empresa: Optional[str] =  None



class ModeloActualizarEnvio(BaseModel):

    nombre:Optional[str] = Field(max_length=150)
    tipo_trailer: Optional[str] = None
    ubicacion_origen: Optional[str] = Field(max_length=150) 
    ubicacion_destino: Optional[str] = Field(max_length=150)
    estado: Optional[str] = Field(max_length=100,examples=["BORRADOR","LISTO PARA ENVIAR","EN TRANSITO","ENTREGADO"])
    empresa: Optional[str] =  None

#Cambiar a False en produccion
app = FastAPI(debug=True)

headers = {"content-type": "charset=utf-8"}


#Definimos el root
@app.get("/")
async def read_root():
    content = {"mensaje": "Bienvenido al API del ERP de Transporte"}
    return JSONResponse(content=content, headers=headers)


@app.get("/envios/")
async def obtener_envios():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ENVIOS.OPERATIVA_TERRESTRE ORDER BY ID;")
        envios = cursor.fetchall()
        #content = list_to_dict(envios)
        #data = jsonable_encoder(content)
        cursor.close()
        conn.close()

        return envios_to_dict(envios)
        #return JSONResponse(content = data )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener envíos: {e}")

#Endpoint para crear un nuevo envío  
@app.post("/envios/crear")
async def crear_envio(envio: ModeloCrearEnvio):

    conn = get_connection()

    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO ENVIOS.OPERATIVA_TERRESTRE (
            nombre,
            tipo_trailer,
            id_ubicacion_origen,
            ubicacion_origen,
            id_ubicacion_destino,
            ubicacion_destino,
            fecha_alta,
            estado,
            empresa
        )
        VALUES (
            %s,
            (SELECT id FROM MAESTROS.TIPO_TRAILER WHERE DESCRIPCION = %s),
            (SELECT id FROM MAESTROS.UBICACION WHERE DESCRIPCION = %s),
            %s,
            (SELECT id FROM MAESTROS.UBICACION WHERE DESCRIPCION = %s),
            %s,
            CURRENT_TIMESTAMP,
            %s,
            (SELECT id_empresa FROM MAESTROS.EMPRESA WHERE razon_social = %s)
        );
    """
        
        #Le pasamos los valores del modelo
        values = (
            envio.nombre,
            envio.tipo_trailer,
            envio.ubicacion_origen,
            envio.ubicacion_origen,
            envio.ubicacion_destino,
            envio.ubicacion_destino,
            envio.estado,
            envio.empresa,
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()


        #Creamos un nuevo cursor para obtener el ID del envío creado
        cursor_id = conn.cursor()
        cursor_id.execute("SELECT MAX(id) FROM ENVIOS.OPERATIVA_TERRESTRE;")
        new_id = cursor_id.fetchone()[0]
        cursor_id.close()

        #Creamos el historial del envío
        iniciar_historial_envio(new_id)
        

        conn.close()

        response = {
            "mensaje": "Envío creado correctamente",
            "id_envio": new_id
        }

        return JSONResponse(content=response, headers=headers,status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el envío: {e}")

#Endpoint para crear un nuevo envío  
@app.post("/envios/actualizar/{id_envio}")
async def actualizar_envio(id_envio: int, envio: ModeloActualizarEnvio):

    conn = get_connection()

    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()

        #Como no sabemos qué campos se van a actualizar, construimos la query dinámicamente
        query = """
        UPDATE ENVIOS.OPERATIVA_TERRESTRE 
        """
        
        if envio.nombre is not None:
            query += "SET nombre = %s "
        
        if envio.tipo_trailer is not None:
            if "SET" in query:
                query += ", tipo_trailer = (SELECT id FROM MAESTROS.TIPO_TRAILER WHERE DESCRIPCION = %s) "
            else:
                query += "SET tipo_trailer = (SELECT id FROM MAESTROS.TIPO_TRAILER WHERE DESCRIPCION = %s) "
        
        if envio.ubicacion_origen is not None:
            if "SET" in query:
                query += ", id_ubicacion_origen = (SELECT id FROM MAESTROS.UBICACION WHERE DESCRIPCION = %s), ubicacion_origen = %s "
            else:
                query += "SET id_ubicacion_origen = (SELECT id FROM MAESTROS.UBICACION WHERE DESCRIPCION = %s), ubicacion_origen = %s "

        if envio.ubicacion_destino is not None:
            if "SET" in query:
                query += ", id_ubicacion_destino = (SELECT id FROM MAESTROS.UBICACION WHERE DESCRIPCION = %s), ubicacion_destino = %s "
            else:
                query += "SET id_ubicacion_destino = (SELECT id FROM MAESTROS.UBICACION WHERE DESCRIPCION = %s), ubicacion_destino = %s "

        if envio.estado is not None:
            if "SET" in query:
                query += ", estado = %s "
            else:
                query += "SET estado = %s "
        
        if envio.empresa is not None:
            if "SET" in query:
                query += ", empresa = (SELECT id_empresa FROM MAESTROS.EMPRESA WHERE razon_social = %s) "
            else:
                query += "SET empresa = (SELECT id_empresa FROM MAESTROS.EMPRESA WHERE razon_social = %s) "

        query += "WHERE id = %s;"
        
        values = []
        if envio.nombre is not None:
            values.append(envio.nombre)
        if envio.tipo_trailer is not None:
            values.append(envio.tipo_trailer)
        if envio.ubicacion_origen is not None:
            values.append(envio.ubicacion_origen)
            values.append(envio.ubicacion_origen)
        if envio.ubicacion_destino is not None:
            values.append(envio.ubicacion_destino)
            values.append(envio.ubicacion_destino) 
        if envio.estado is not None:
            values.append(envio.estado)
        if envio.empresa is not None:
            values.append(envio.empresa)
        values.append(id_envio)

        #Recuperamos el ultimo estado del envio antes de la actualización
        ultimo_estado = get_ultimo_estado_historial(id_envio)

        cursor.execute(query, values)
        conn.commit()
        cursor.close()


        #Actualizamos el historial del envío
        if ultimo_estado != envio.estado and envio.estado is not None:
            add_registro_historial(id_envio, ultimo_estado,envio.estado)

        conn.close()

        response = {
            "mensaje": "Envío actualizado correctamente",
            "envio": envio.nombre
        }

        return JSONResponse(content=response, headers=headers,status_code=201)

    except Exception as e:
        print(query)
        raise HTTPException(status_code=500, detail=f"Error al actualizar el envío: {e}")