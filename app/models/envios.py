import pandas as pd
from database.connection import get_connection

class Envio:
    def __init__(self, nombre: str, tipo_trailer: str, ubi_origen: str, ubi_destino: str, trasportista: str):
        self.trasportista = trasportista
        self.nombre = nombre
        self.tipo_trailer = tipo_trailer
        self.ubi_origen = ubi_origen
        self.ubi_destino = ubi_destino
        self.trasportista = trasportista


def grabar_envio(envio: Envio):
    """Guarda un envío en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()

    estado = "BORRADOR"

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

    cursor.execute(query, (
        envio.nombre,
        envio.tipo_trailer,
        envio.ubi_origen,
        envio.ubi_origen,
        envio.ubi_destino,
        envio.ubi_destino,
        estado,
        envio.trasportista
    ))

    conn.commit()

    # Último ID insertado
    cursor.execute("SELECT LASTVAL()")
    id_envio = cursor.fetchone()[0]

    iniciar_historial_envio(id_envio)
    conn.commit()

    cursor.close()
    conn.close()


def mostrar_envios(fecha_desde="CURRENT_TIMESTAMP", fecha_hasta="CURRENT_TIMESTAMP"):
    """Muestra envíos por consola."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM ENVIOS.OPERATIVA_TERRESTRE 
        WHERE (FECHA_ALTA >= %s) AND (FECHA_ALTA <= %s)
    """, (fecha_desde, fecha_hasta))

    envios = cursor.fetchall()

    for envio in envios:
        fecha_alta = envio[7]
        fecha_alta.strftime('%d/%m/%Y %H:%M:%S')

        if envio[8] is not None:
            fecha_baja = envio[8]
            fecha_baja.strftime('%d/%m/%Y %H:%M:%S')
            print(f"{envio[:7]} {fecha_alta} {fecha_baja}")
        else:
            print(f"{envio[:7]} {fecha_alta} {envio[8]}")

    cursor.close()
    conn.close()


def df_envios(fecha_desde="CURRENT_TIMESTAMP", fecha_hasta="CURRENT_TIMESTAMP"):
    """Exporta envíos a Excel."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM ENVIOS.OPERATIVA_TERRESTRE 
        WHERE (FECHA_ALTA >= %s) AND (FECHA_ALTA <= %s)
    """, (fecha_desde, fecha_hasta))

    envios = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data=envios)
    df.to_excel("export.xlsx", header=headers, index=False)


def recuperar_envios_tabla(fecha_desde= "CURRENT_TIMESTAMP", fecha_hasta="CURRENT_TIMESTAMP",pais_origen= None, pais_destino= None, ubi_origen = None, ubi_destino=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT 
     OT.id,
     OT.nombre,
     TT.descripcion,
     OT.id_ubicacion_origen,
     OT.ubicacion_origen,
     OT.id_ubicacion_destino,
     OT.ubicacion_destino,
     OT.fecha_alta,
     OT.fecha_baja,
     OT.estado,
     E.razon_social
     FROM ENVIOS.OPERATIVA_TERRESTRE AS OT
     INNER JOIN MAESTROS.TIPO_TRAILER AS TT on OT.tipo_trailer = TT.id
     INNER JOIN MAESTROS.UBICACION AS U on OT.ubicacion_origen = U.descripcion
     INNER JOIN MAESTROS.ubicacion AS UT on OT.ubicacion_destino = UT.descripcion
     INNER JOIN MAESTROS.PAIS AS P on U.pais =  P.id
     INNER JOIN MAESTROS.PAIS AS PD on UT.pais = PD.id
     INNER JOIN MAESTROS.EMPRESA AS E on E.id_empresa = OT.empresa
     WHERE (OT.FECHA_ALTA >= %s) AND (OT.FECHA_ALTA<= %s)"""

    params = [fecha_desde,fecha_hasta]

    if pais_origen:
        query += " AND P.descripcion = %s"
        params.append(pais_origen)

    if pais_destino:
        query += " AND PD.descripcion = %s"
        params.append(pais_destino)

    if ubi_origen:
        query += " AND U.descripcion = %s"
        params.append(ubi_origen)
    if ubi_destino:
        query += " AND UT.descripcion = %s"
        params.append(ubi_destino)

    query += " ORDER BY OT.id"

    print("QUERY:", query)
    print("PARAMS:", params)

    cursor.execute(query, params)

    envios = cursor.fetchall()

    cursor.close()
    conn.close()
    return envios


def actualizar_envio_por_id(id_envio, nuevos_datos):
    """Actualiza un envío según su ID."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE ENVIOS.OPERATIVA_TERRESTRE SET 
            id = %s,
            nombre = %s,
            tipo_trailer = (SELECT id FROM MAESTROS.TIPO_TRAILER WHERE descripcion = %s),
            id_ubicacion_origen = %s,
            ubicacion_origen = %s,
            id_ubicacion_destino = %s,
            ubicacion_destino = %s,
            fecha_alta = %s,
            fecha_baja = %s,
            estado = %s,
            empresa = (SELECT id_empresa FROM MAESTROS.EMPRESA WHERE razon_social = %s)
        WHERE id = %s
    """

    cursor.execute(query, (
        nuevos_datos.get("id"),
        nuevos_datos.get("nombre"),
        nuevos_datos.get("tipo_trailer"),
        nuevos_datos.get("id_ubicacion_origen"),
        nuevos_datos.get("ubicacion_origen"),
        nuevos_datos.get("id_ubicacion_destino"),
        nuevos_datos.get("ubicacion_destino"),
        nuevos_datos.get("fecha_alta"),
        nuevos_datos.get("fecha_baja"),
        nuevos_datos.get("estado"),
        nuevos_datos.get("empresa"),
        nuevos_datos.get("id")
    ))

    conn.commit()
    cursor.close()
    conn.close()


def iniciar_historial_envio(id):
    """Inserta la primera entrada en el historial del envío."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ENVIOS.HISTORIAL_ENVIOS 
        (ID_ENVIO, ESTADO_ANTERIOR, ESTADO_NUEVO, FECHA_CAMBIO)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
    """, (id, None, 'BORRADOR'))

    conn.commit()
    cursor.close()
    conn.close()


def get_estados_desplegable():
    """Retorna lista de estados disponibles."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT estado FROM envios.estado_envios ORDER BY id")

    estados = [fila[0] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()

    return estados


def get_historial_envio(id_envio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT OT.nombre, HE.estado_anterior, HE.estado_nuevo, HE.fecha_cambio 
        FROM ENVIOS.HISTORIAL_ENVIOS HE
        INNER JOIN ENVIOS.OPERATIVA_TERRESTRE OT ON HE.id_envio = OT.id
        WHERE HE.id_envio = %s
    """, (id_envio,))

    historial = cursor.fetchall()

    cursor.close()
    conn.close()

    return historial


def get_ultimo_estado_historial(id_envio):
    """Obtiene el último estado registrado en el historial."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT estado_nuevo 
        FROM ENVIOS.historial_envios 
        WHERE id_envio = %s 
        ORDER BY historial_envios.fecha_cambio DESC 
        LIMIT 1
    """, (id_envio,))

    estado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return estado


def add_registro_historial(id_envio, estado_anterior, estado_nuevo):
    """Agrega un registro al historial de un envío."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ENVIOS.historial_envios 
        (id_envio, estado_anterior, estado_nuevo, fecha_cambio)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
    """, (id_envio, estado_anterior, estado_nuevo))

    conn.commit()
    cursor.close()
    conn.close()


def exportar_df(columnas, lista, ruta):
    """Exporta un DataFrame a Excel."""
    df = pd.DataFrame(columns=columnas, data=lista)
    print(df)
    df.to_excel(ruta, sheet_name="Envios", index=False)

def envios_to_dict(lista):
    lista_dict = []
    for envio in lista:
        diccionario = {"id":envio[0],
                   "nombre":envio[1],
                   "tipo_trailer":envio[2],
                   "id_ubicacion_origen":envio[3],
                   "ubicacion_origen":envio[4],
                   "id_ubicacion_destino":envio[5],
                   "ubicacion_destino":envio[6],
                   "fecha_alta":envio[7],
                   "fecha_baja":envio[8],
                   "estado":envio[9],
                   "empresa":envio[10],
                   "tarifa":envio[11],
                  "coste_total":envio[12]
                   }
        lista_dict.append(diccionario)
    return lista_dict


