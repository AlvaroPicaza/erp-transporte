from fastapi import APIRouter, FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from database.connection import get_connection
from typing import Optional
from enum import Enum
from app.models.maestros import tarifas_to_dict

router = APIRouter()

headers = {"content-type": "charset=utf-8"}

#Endpoint para obtener todas las empresas
@router.get("/",tags=["Tarifas"])
async def get_tarifas():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code = 500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()
        cursor.execute("""select TB.id_tarifa,
                            U.descripcion as origen,
                            UT.descripcion as destino,
                            TB.tipo_trailer,
                            TB.precio_base,
                            TB.precio_por_km,
                            TB.precio_por_kg,
                            TB.moneda,
                            TB.fecha_alta,
                            TB.fecha_baja
                            from maestros.tarifa_base as TB 
                            inner join maestros.ubicacion as U on (U.id = TB.id_zona_origen) 
                            inner join maestros.ubicacion as UT on (UT.id = TB.id_zona_destino)""")
        tarifas = tarifas_to_dict(cursor.fetchall())
        cursor.close()
        conn.close()
        return tarifas
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error al obtener las tarifas: {e}")
