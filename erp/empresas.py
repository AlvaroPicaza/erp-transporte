from fastapi import APIRouter, FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from database.connection import get_connection
from typing import Optional
from enum import Enum
from app.models.maestros import empresas_to_dict

class CambiarEmpresaRequest(BaseModel):
    id_empresa: int
    #nombre:str = Field(...,max_length=150)
    #tipo_trailer: str = Field(...)
    #ubicacion_origen:str = Field(...,max_length=150) 
    #ubicacion_destino:str = Field(...,max_length=150)
    #estado:Optional[EstadosEnvios] = None
    #empresa: Optional[str] =  None

router = APIRouter()

headers = {"content-type": "charset=utf-8"}

#Endpoint para obtener todas las empresas
@router.get("/",tags=["Empresas"])
async def get_empresas():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code = 500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MAESTROS.EMPRESA order by id_pais")
        empresas = empresas_to_dict(cursor.fetchall())
        cursor.close()
        conn.close()
        return empresas
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Error al obtener las empresas: {e}")
