select TB.id_tarifa,
U.descripcion as origen,
UT.descripcion as destino,
TB.tipo_trailer,
TB.precio_base,
TB.precio_por_km,
TB.precio_por_kg,
TB.moneda,
TB.fecha_alta
from maestros.tarifa_base as TB 
inner join maestros.ubicacion as U on (U.id = TB.id_zona_origen) 
inner join maestros.ubicacion as UT on (UT.id = TB.id_zona_destino)
--WHERE U.descripcion = 'CORUÑA'
