from database.connection import get_connection


def mostrar_paises():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM MAESTROS.PAIS")
    result = cursor.fetchall()

    headers = [desc[0] for desc in cursor.description]
    print(headers)

    for pais in result:
        fecha_alta = pais[3]
        fecha_alta.strftime('%d/%m/%Y %H:%M:%S')

        if pais[4] is not None:
            fecha_baja = pais[4]
            fecha_baja.strftime('%d/%m/%Y %H:%M:%S')
            print(f"{pais[:3]} {fecha_alta} {fecha_baja}")
        else:
            print(f"{pais[:3]} {fecha_alta} {pais[4]}")

    cursor.close()
    conn.close()


def ubicacion_pais(pais: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            U.id, 
            U.descripcion,
            P.descripcion,
            U.fecha_alta,
            U.fecha_baja 
        FROM MAESTROS.UBICACION U 
        INNER JOIN MAESTROS.PAIS P ON U.pais = P.id 
        WHERE P.descripcion = %s
    """, (pais,))

    ubicaciones = cursor.fetchall()

    cursor.close()
    conn.close()
    return ubicaciones


def get_trailers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM MAESTROS.TIPO_TRAILER ORDER BY id")
    trailers = cursor.fetchall()

    cursor.close()
    conn.close()
    return trailers


def get_trailers_desplegable():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DESCRIPCION FROM MAESTROS.TIPO_TRAILER ORDER BY id")
    trailers = [fila[0] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()
    return trailers


def get_trailers_by_id(trailer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT DESCRIPCION FROM MAESTROS.TIPO_TRAILER WHERE id = %s",
        (trailer_id,)
    )

    trailers = [fila[0] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()
    return trailers


def get_ubicacion_desplegable(pais):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.descripcion 
        FROM MAESTROS.UBICACION AS u
        INNER JOIN MAESTROS.PAIS p ON p.id = u.pais
        WHERE p.descripcion = %s
        ORDER BY u.id
    """, (pais,))

    ubicaciones = [fila[0] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()
    return ubicaciones


def get_total_ubicaciones():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.descripcion 
        FROM MAESTROS.UBICACION AS u
        INNER JOIN MAESTROS.PAIS p ON p.id = u.pais
        ORDER BY u.id
    """)

    ubicaciones = [fila[0] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()
    return ubicaciones


def get_ubicaciones(pais=None):
    conn = get_connection()
    cursor = conn.cursor()

    if pais.strip() != '':
        cursor.execute("""
            SELECT 
                u.id, u.descripcion, u.pais, u.fecha_alta, u.fecha_baja
            FROM MAESTROS.UBICACION AS u
            INNER JOIN MAESTROS.PAIS p ON p.id = u.pais
            WHERE p.descripcion = %s
            ORDER BY u.id
        """, (pais,))
    else:
        cursor.execute("""
            SELECT 
                u.id, u.descripcion, u.pais, u.fecha_alta, u.fecha_baja
            FROM MAESTROS.UBICACION AS u
            INNER JOIN MAESTROS.PAIS p ON p.id = u.pais
            ORDER BY u.id
        """)

    ubicaciones = cursor.fetchall()

    cursor.close()
    conn.close()
    return ubicaciones


def get_id_ubicacion(ubicacion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT U.id 
        FROM MAESTROS.UBICACION AS U
        WHERE U.descripcion = %s
        ORDER BY U.id
    """, (ubicacion,))

    id_ubicacion = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return id_ubicacion


def get_pais_ubicacion(ubicacion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT P.descripcion 
        FROM MAESTROS.UBICACION AS U
        INNER JOIN MAESTROS.PAIS AS P ON U.pais = P.id 
        WHERE U.descripcion = %s
    """, (ubicacion,))

    pais = cursor.fetchall()[0]

    cursor.close()
    conn.close()
    return pais


def get_paises_desplegable():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM MAESTROS.PAIS ORDER BY id")
    paises = [fila[1] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()
    return paises


def get_pais():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM MAESTROS.PAIS ORDER BY id")
    paises = cursor.fetchall()

    cursor.close()
    conn.close()
    return paises


def get_empresas_desplegable(pais):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.razon_social 
        FROM MAESTROS.EMPRESA AS e
        INNER JOIN MAESTROS.PAIS p ON p.id = e.id_pais
        WHERE p.descripcion = %s
        ORDER BY e.id_empresa
    """, (pais,))

    empresas = [fila[0] for fila in cursor.fetchall()]

    cursor.close()
    conn.close()
    return empresas


def get_pais_empresa(empresa):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT P.descripcion 
        FROM MAESTROS.EMPRESA AS E
        INNER JOIN MAESTROS.PAIS AS P ON E.id_pais = P.id 
        WHERE E.razon_social = %s
    """, (empresa,))

    pais = cursor.fetchall()[0]

    cursor.close()
    conn.close()
    return pais


def get_empresas(pais):
    conn = get_connection()
    cursor = conn.cursor()

    base_query = """
        SELECT 
            e.razon_social,
            e.direccion,
            p.descripcion,
            i.idioma,
            e.fecha_alta,
            e.usuario_alta,
            e.fecha_modificacion,
            e.usuario_modificacion,
            e.fecha_baja,
            e.usuario_baja
        FROM MAESTROS.EMPRESA AS e
        INNER JOIN MAESTROS.PAIS p ON p.id = e.id_pais
        INNER JOIN MAESTROS.IDIOMA i ON i.id_idioma = e.idioma
    """

    if pais.strip() == '':
        query = base_query + " ORDER BY e.id_empresa"
        cursor.execute(query)
    else:
        query = base_query + " WHERE p.descripcion = %s ORDER BY e.id_empresa"
        cursor.execute(query, (pais,))

    empresas = cursor.fetchall()

    cursor.close()
    conn.close()
    return empresas


def get_tarifas(ubicacion_origen=None, ubicacion_destino=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            U.descripcion AS origen,
            UT.descripcion AS destino,
            TT.descripcion,
            TB.precio_base,
            TB.precio_por_km,
            TB.precio_por_kg,
            TB.moneda,
            TB.fecha_alta,
            TB.fecha_baja
        FROM MAESTROS.TARIFA_BASE AS TB 
        INNER JOIN MAESTROS.UBICACION AS U ON U.id = TB.id_zona_origen
        INNER JOIN MAESTROS.UBICACION AS UT ON UT.id = TB.id_zona_destino
        INNER JOIN MAESTROS.TIPO_TRAILER AS TT ON TT.id = TB.tipo_trailer
        WHERE 1 = 1
    """

    params = []

    if ubicacion_origen:
        query += " AND U.DESCRIPCION = %s"
        params.append(ubicacion_origen)

    if ubicacion_destino:
        query += " AND UT.DESCRIPCION = %s"
        params.append(ubicacion_destino)

    cursor.execute(query, params)
    tarifas = cursor.fetchall()

    cursor.close()
    conn.close()
    return tarifas

def empresas_to_dict(empresas):
    lista = []
    for empresa in empresas:
        diccionario ={
            "id_empresa":empresa[0],
            "razon_social":empresa[1],
            "direccion":empresa[2],
            "id_pais":empresa[3],
            "idioma":empresa[4],
            "fecha_alta":empresa[5],
            "usuario_alta":empresa[6],
            "fecha_modificacion":empresa[7],
            "usuario_modificacion":empresa[8],
            "fecha_baja":empresa[9],
            "usuario_baja":empresa[10]
        }
        lista.append(diccionario)
    return lista

def tarifas_to_dict(tarifas):
    lista = []
    for tarifa in tarifas:
        diccionario ={
            "id_tarifa":tarifa[0],
            "zona_origen":tarifa[1],
            "zona_destino":tarifa[2],
            "tipo_trailer":tarifa[3],
            "precio_base":tarifa[4],
            "precio_por_km":tarifa[5],
            "precio_por_kg":tarifa[6],
            "moneda":tarifa[7],
            "fecha_alta":tarifa[8],
            "fecha_baja":tarifa[9]
        }
        lista.append(diccionario)
    return lista