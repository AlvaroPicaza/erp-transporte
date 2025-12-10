from database.connection import get_connection


def get_tarifa_base(origen, destino, trailer):
    """
    Obtiene la tarifa base según origen, destino y tipo de trailer.
    Retorna un diccionario con la información o None si no existe.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            id_tarifa,
            precio_base,
            precio_por_km,
            precio_por_kg
        FROM MAESTROS.TARIFA_BASE AS TB
        INNER JOIN MAESTROS.TIPO_TRAILER AS TT 
            ON TT.id = TB.tipo_trailer
        WHERE 
            id_zona_origen = %s 
            AND id_zona_destino = %s 
            AND tipo_trailer = (
                SELECT id 
                FROM MAESTROS.TIPO_TRAILER 
                WHERE DESCRIPCION = %s
            )
    """

    cursor.execute(query, (origen, destino, trailer))
    tarifa = cursor.fetchone()

    cursor.close()
    conn.close()

    if tarifa is None:
        return None

    return {
        "id_tarifa": tarifa[0],
        "precio_base": tarifa[1],
        "precio_por_km": tarifa[2],
        "precio_por_kg": tarifa[3]
    }


def calcular_coste_envio(origen, destino, trailer, distancia, peso):
    """
    Calcula el coste total del envío basado en las tarifas de la base de datos.
    """
    tarifa = get_tarifa_base(origen, destino, trailer)

    if not tarifa:
        raise ValueError("No existe una tarifa aplicable a este envío")

    coste_total = (
        float(tarifa["precio_base"])
        + (float(tarifa["precio_por_km"]) * float(distancia))
        + (float(tarifa["precio_por_kg"]) * float(peso))
    )

    # incluir recargos por tipo de trailer u origenes y destinos
    return round(coste_total, 2)
