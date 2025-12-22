from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from database.connection import get_connection
from app.models.envios import (envios_to_dict,
                               iniciar_historial_envio,
                               get_ultimo_estado_historial,
                               add_registro_historial)
from erp.empresas import router as empresas_router
from erp.empresas import CambiarEmpresaRequest
from erp.tarifas import router as tarifas_router
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
    estado: Optional[EstadosEnvios] = None
    empresa: Optional[str] =  None

class EnvioEstadoUpdate(BaseModel):
    estado: EstadosEnvios

#Cambiar el debug a False en produccion
app = FastAPI(title="API Operativas terrestres",
              description="Métodos de gestión y consulta",
              version="0.1.0",
              debug=True)

app.include_router(empresas_router, prefix="/empresas")
app.include_router(tarifas_router, prefix="/tarifas")

headers = {"content-type": "charset=utf-8"}

@app.get("/")
async def root():
    content = {"mensaje":"API REST ERP Transporte"}
    return JSONResponse(content=content,headers=headers)

#Endpoint para obtener todos los envíos
@app.get("/envios/",tags=["Envios"])
async def obtener_envios():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ENVIOS.OPERATIVA_TERRESTRE ORDER BY id;")
        envios = cursor.fetchall()
        #content = list_to_dict(envios)
        #data = jsonable_encoder(content)
        cursor.close()
        conn.close()

        return envios_to_dict(envios)
        #return JSONResponse(content = data )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener envíos: {e}")

#Endpoint para obtener un envio
@app.get("/envios/{id_envio}",tags=["Envios"])
async def get_envio(id_envio):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ENVIOS.OPERATIVA_TERRESTRE WHERE id = %s;",(id_envio,))
        envios = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(envios) == 0:
            content = {"mensaje":"No se ha encontrado el envío"}
            return JSONResponse(content=content, headers=headers)
        return envios_to_dict(envios)
        #return JSONResponse(content = data )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener envíos: {e}")


#Endpoint para crear un nuevo envío  
@app.post("/envios/crear",tags=["Envios"])
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


#Endpoint para actualizar un envío por id  
@app.put("/envios/actualizar/{id_envio}",tags=["Envios"])
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
    

#Endpoint para eliminar un envío por id  
@app.delete("/envios/borrar/{id_envio}",tags=["Envios"])
async def borrar_envio(id_envio: int):
    conn = get_connection()

    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:

        #Debemos eliminar el historial del envio para evitar problemas de integridad referencial
        cursorBorrarHistorial = conn.cursor()
        cursorBorrarEnvio = conn.cursor()
        

        # Eliminar el envío
        queryHistorial = "DELETE FROM ENVIOS.HISTORIAL_ENVIOS WHERE id_envio = %s;"
        queryEnvio = "DELETE FROM ENVIOS.OPERATIVA_TERRESTRE WHERE id = %s;"
        cursorBorrarHistorial.execute(queryHistorial, (id_envio,))
        cursorBorrarEnvio.execute(queryEnvio, (id_envio,))
        conn.commit()
        cursorBorrarEnvio.close()

        conn.close()

        response = {
            "mensaje": "Envío eliminado correctamente"
        }

        return JSONResponse(content=response, headers=headers,status_code=201)

    except Exception as e:
        print(queryEnvio)
        raise HTTPException(status_code=500, detail=f"Error al eliminar el envío: {e}")
    


@app.patch("/envios/{id_envio}/empresa",tags=["Envios"])
async def modificar_empresa_envio(body: CambiarEmpresaRequest, id_envio: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail = "Error de conexión a la base de datos")

    try:
 

        #Por lógica de negocio, solamente se pueden actualizar empresas que sean del mismo país que la ubicación de origen
        cursorPaisEnvio = conn.cursor()
        cursorPaisEmpresa = conn.cursor()

        cursorPaisEnvio.execute("""SELECT PAIS 
                       FROM maestros.ubicacion u
                       INNER JOIN envios.operativa_terrestre ot on u.id = ot.id_ubicacion_origen
                       WHERE ot.id = %s 
        """,(id_envio,))
        
        cursorPaisEmpresa.execute("""SELECT id_pais
                                  FROM maestros.empresa
                                  WHERE id_empresa = %s
        """,(body.id_empresa,))
        
        paisEnvio = cursorPaisEnvio.fetchone()[0]
        paisEmpresa = cursorPaisEmpresa.fetchone()[0]

        cursorPaisEmpresa.close()
        cursorPaisEnvio.close()

        if paisEnvio == paisEmpresa:
            cursor = conn.cursor()
            query = "UPDATE ENVIOS.OPERATIVA_TERRESTRE set empresa = %s where id = %s"
            values = (body.id_empresa,id_envio)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            response = {
                "mensaje":"Se ha actualizado la empresa del envío"
            }

            return JSONResponse(content=response,headers=headers)
        response = {
            "mensaje":"El país de la empresa es distinto del de la ubicación de origen"
        }
        return JSONResponse(status_code=403,content=response,headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al actualizar el envío: {e}")
    
@app.patch("/envios/{id}/estado",tags=["Envios"])
async def modificar_estado_envio(id_envio,body:EnvioEstadoUpdate):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail = "Error de conexión a la base de datos")
    
    try:
        cursorEstadoActual = conn.cursor()
        cursorActualizarEnvio = conn.cursor()
        cursorActualizarHistorial = conn.cursor()

        cursorEstadoActual.execute("""SELECT estado
                                   FROM ENVIOS.OPERATIVA_TERRESTRE
                                   WHERE id = %s
        """,(id_envio,))

        estadoActual = cursorEstadoActual.fetchone()[0]


        if estadoActual == body.estado:
            response = {"mensaje":"El estado no puede ser igual al actual del envío"}
            return JSONResponse(content=response,headers=headers,status_code=403)
        
        cursorActualizarEnvio.execute("""UPDATE ENVIOS.OPERATIVA_TERRESTRE
                                      SET estado = %s
                                      WHERE id = %s
        """,(body.estado,id_envio))

        cursorActualizarHistorial.execute("""INSERT INTO ENVIOS.HISTORIAL_ENVIOS
                                          (id_envio, 
                                          estado_anterior, 
                                          estado_nuevo, 
                                          fecha_cambio)
                                          VALUES (%s, %s, %s, CURRENT_TIMESTAMP)

    """,(id_envio,estadoActual,body.estado))
        
        conn.commit()
        cursorEstadoActual.close()
        cursorActualizarEnvio.close()
        cursorActualizarHistorial.close()
        conn.close()

        response = {
                "mensaje":f"Se ha actualizado el estado del envío {id_envio}"
        }

        return JSONResponse(content=response,headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al actualizar el envío: {e}")