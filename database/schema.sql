CREATE TABLE maestros.pais(
id SERIAL PRIMARY KEY,
descripcion VARCHAR(60),
codigo_iso VARCHAR(3),
fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
fecha_baja TIMESTAMP
);

CREATE TABLE IF NOT EXISTS MAESTROS.IDIOMA(
id_idioma INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
idioma VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS MAESTROS.EMPRESA(
id_empresa INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
razon_social VARCHAR(100) NOT NULL ,
direccion VARCHAR(250),
id_pais integer NOT NULL REFERENCES maestros.pais(id),
idioma integer REFERENCES maestros.idioma(id_idioma),
fecha_alta TIMESTAMP NOT NULL ,
usuario_alta  VARCHAR(100) NOT NULL,
fecha_modificacion TIMESTAMP,
usuario_modificacion VARCHAR(100),
fecha_baja TIMESTAMP,
usuario_baja VARCHAR(100)
)

CREATE TABLE maestros.ubicacion(
id SERIAL PRIMARY KEY,
descripcion VARCHAR(150),
pais INTEGER REFERENCES pais(id),
fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
fecha_baja TIMESTAMP
);

CREATE TABLE maestros.tipo_trailer(
id SERIAL PRIMARY KEY,
descripcion VARCHAR(60),
fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
fecha_baja TIMESTAMP
)

CREATE TABLE maestros.tipo_servicio(
id SERIAL PRIMARY KEY,
descripcion varchar(60),
fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
fecha_baja TIMESTAMP
)

CREATE TABLE ENVIOS.estado_envios (
id SERIAL PRIMARY KEY,
estado VARCHAR(100)
)

CREATE TABLE ENVIOS.HISTORIAL_ENVIOS(
id_historial_envios serial PRIMARY KEY,
id_envio integer NOT NULL REFERENCES envios.operativa_terrestre(id),
estado_anterior VARCHAR(100),
estado_nuevo VARCHAR(100) NOT NULL,
fecha_cambio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

ALTER TABLE ENVIOS.HISTORIAL_ESTADOS
ADD CONSTRAINT fk_historial_envio
FOREIGN KEY (id_envio) REFERENCES ENVIOS.OPERATIVA_TERRESTRE(id);

CREATE TABLE envios.operativa_terrestre(
id SERIAL PRIMARY KEY,
nombre VARCHAR(150) NOT NULL,
tipo_trailer INTEGER REFERENCES maestros.tipo_trailer(id),
id_ubicacion_origen INTEGER NOT NULL REFERENCES maestros.ubicacion(id),
ubicacion_origen VARCHAR(150) NOT NULL,
id_ubicacion_destino INTEGER NOT NULL REFERENCES maestros.ubicacion(id),
ubicacion_destino VARCHAR(150) NOT NULL,
fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
fecha_baja TIMESTAMP

--Al realizar el insert en ubicacion salta un error relacionado con la foreign key. Eliminamos la restriccion y la creamos correctamente
SELECT conname FROM pg_constraint WHERE CONRELID = 'maestros.ubicacion'::regclass
and contype = 'f'

--Borramos
ALTER TABLE maestros.ubicacion
DROP CONSTRAINT ubicacion_pais_fkey;

--Creamos
ALTER TABLE maestros.ubicacion
ADD CONSTRAINT ubicacion_pais_fkey
FOREIGN KEY (pais)
REFERENCES maestros.pais(id)

ALTER TABLE ENVIOS.OPERATIVA_TERRESTRE
ADD COLUMN empresa INTEGER;

ALTER TABLE ENVIOS.OPERATIVA_TERRESTRE
ADD CONSTRAINT empresa_fkey
FOREIGN KEY (empresa) REFERENCES MAESTROS.EMPRESA (id_empresa)

CREATE TABLE maestros.tarifa_base (
    id_tarifa SERIAL PRIMARY KEY,
    id_zona_origen INTEGER REFERENCES maestros.ubicacion(id),
    id_zona_destino INTEGER REFERENCES maestros.ubicacion(id),
    tipo_trailer INTEGER REFERENCES maestros.tipo_trailer(id),
    precio_base NUMERIC(10,2),  -- tarifa mínima o fija
    precio_por_km NUMERIC(10,2), -- coste adicional por km
    precio_por_kg NUMERIC(10,2), -- coste adicional por peso
    moneda VARCHAR(3) DEFAULT 'EUR',
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_baja TIMESTAMP
);

ALTER TABLE ENVIOS.operativa_terrestre
ADD COLUMN tarifa integer references MAESTROS.TARIFA_BASE(id_tarifa);

ALTER TABLE ENVIOS.operativa_terrestre
ADD COLUMN coste_total numeric(10,2)