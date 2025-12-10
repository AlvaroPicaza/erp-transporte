INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('PORTUGAL','PRT',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('FRANCIA','FRA',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('PAISES BAJOS','NLD',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('ALEMANIA','DEU',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('ITALIA','ITA',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('REINO UNIDO','GBR',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('IRLANDA','IRL',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('GRECIA','GRC',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('SUIZA','CHE',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('JAPON','JPN',CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.PAIS (descripcion,codigo_iso,fecha_alta) VALUES ('CHINA','CHN',CURRENT_TIMESTAMP);

INSERT INTO MAESTROS.TIPO_SERVICIO (descripcion,fecha_alta) VALUES ('REGULAR', CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.TIPO_SERVICIO (descripcion,fecha_alta) VALUES ('EXPRESS', CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.TIPO_SERVICIO (descripcion,fecha_alta) VALUES ('ULTRAEXPRESS', CURRENT_TIMESTAMP);
INSERT INTO MAESTROS.TIPO_SERVICIO (descripcion,fecha_alta) VALUES ('AGENCY', CURRENT_TIMESTAMP);

INSERT INTO maestros.tipo_trailer(
	descripcion, fecha_alta)
	VALUES ('LONA', CURRENT_TIMESTAMP);
INSERT INTO maestros.tipo_trailer(
	descripcion, fecha_alta)
	VALUES ('LONA', CURRENT_TIMESTAMP);
INSERT INTO maestros.tipo_trailer(
	descripcion, fecha_alta)
	VALUES ('TRAILER', CURRENT_TIMESTAMP);
INSERT INTO maestros.tipo_trailer(
	descripcion, fecha_alta)
	VALUES ('TREN DE CARRETERA', CURRENT_TIMESTAMP);
INSERT INTO maestros.tipo_trailer(
	descripcion, fecha_alta)
	VALUES ('FURGON', CURRENT_TIMESTAMP);

INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('PORTO-SANTA CATARINA', 1, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('LISBOA-AUGUSTA', 1, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('LISBOA-FONTES', 1, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('FUNCHAL-MADEIRA', 1, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('PARIS-CAMPOS ELISEOS', 2, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('LILLE-BOURSE', 2, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('MARS-LES TERRASES', 2, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('BORD-PORTE DIJEAUX', 2, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('ALM-STADSHART', 3, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('HAA-GROTE HOUTSRAAT', 3, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('AMS-KALVERSTRAAT', 3, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('AMS-ECOMM WAREHOUSE', 3, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('KOB-LORH CENTER', 4, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('FRA-BORSENSTRASSE', 4, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('LEIP-NOVA EVENTIS', 4, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('BER-FRIEDRICHSTRASSE', 4, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('MIL- SAN GOTTARDO', 5, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('ROMA-PORTA DI ROMA', 5, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('DUB-MARY ST', 7, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('CORK-MAHON POINT', 7, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('TOK-TOBU IKEBUKURO', 10, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('KYO-TAKOYAKUSHI NISHI HAIRU', 10, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('DAQING-WANDA PLAZA', 11, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('FOS-NANHAI PLAZA', 11, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('CORUÑA', 12, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('MADRID', 12, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('BARCELONA', 12, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('BILBAO', 12, CURRENT_TIMESTAMP);
INSERT INTO maestros.ubicacion(descripcion, pais, fecha_alta) VALUES ('SEVILLA', 12, CURRENT_TIMESTAMP);

INSERT INTO ENVIOS.estado_envios (estado) VALUES ('BORRADOR');
INSERT INTO ENVIOS.estado_envios (estado) VALUES ('EN PROGRESO');
INSERT INTO ENVIOS.estado_envios (estado) VALUES ('LISTO PARA ENVIAR');
INSERT INTO ENVIOS.estado_envios (estado) VALUES ('ENTREGADO');
INSERT INTO ENVIOS.estado_envios (estado) VALUES ('CANCELADO');

INSERT INTO MAESTROS.IDIOMA (idioma)
VALUES
    ('Español'),
    ('Inglés'),
    ('Francés'),
    ('Portugués')
	    ('Aleman'),
    ('Italiano'),
    ('Japones'),
    ('Chino');

INSERT INTO MAESTROS.EMPRESA (
    razon_social, direccion, id_pais, idioma,
    fecha_alta, usuario_alta
)
VALUES
    ('Transporte García S.L.', 'Calle Mayor 123, Madrid', 1, 1, CURRENT_TIMESTAMP, 'admin'),
    ('Logística Lisboa Lda.', 'Rua Central 45, Lisboa', 2, 4, CURRENT_TIMESTAMP, 'admin'),
    ('EuroFreight Ltd.', '221B Baker Street, London', 3, 2, CURRENT_TIMESTAMP, 'admin'),
    ('TransAlpes SARL', '12 Rue des Alpes, Lyon', 4, 3, CURRENT_TIMESTAMP, 'admin');


INSERT INTO MAESTROS.EMPRESA (
    razon_social, direccion, id_pais, idioma,
    fecha_alta, usuario_alta
)
VALUES
    -- 🇵🇹 PORTUGAL (id 1)
    ('Atlantic Movers SA', 'Avenida Atlântica 202, Lisboa', 1, 4, CURRENT_TIMESTAMP, 'admin'),
    ('TransLusitania Lda.', 'Rua da Liberdade 88, Oporto', 1, 4, CURRENT_TIMESTAMP, 'admin'),

    -- 🇫🇷 FRANCIA (id 2)
    ('TransFrance S.A.', '12 Rue de Rivoli, París', 2, 3, CURRENT_TIMESTAMP, 'admin'),
    ('Logistique Marseille SARL', 'Avenue du Prado 40, Marsella', 2, 3, CURRENT_TIMESTAMP, 'admin'),

    -- 🇳🇱 PAISES BAJOS (id 3)
    ('Dutch Cargo BV', 'Keizersgracht 120, Ámsterdam', 3, 2, CURRENT_TIMESTAMP, 'admin'),

    -- 🇩🇪 ALEMANIA (id 4)
    ('Cargo Express GmbH', 'Alexanderplatz 1, Berlín', 4, 5, CURRENT_TIMESTAMP, 'admin'),
    ('Rhine Logistics AG', 'Rheinstrasse 25, Frankfurt', 4, 5, CURRENT_TIMESTAMP, 'admin'),

    -- 🇮🇹 ITALIA (id 5)
    ('TransItalia S.p.A.', 'Via Roma 55, Milano', 5, 6, CURRENT_TIMESTAMP, 'admin'),
    ('Mediterranean Shipping Co.', 'Piazza Garibaldi 30, Nápoles', 5, 6, CURRENT_TIMESTAMP, 'admin'),

    -- 🇬🇧 REINO UNIDO (id 6)
    ('UK Freight Ltd.', '221B Baker Street, Londres', 6, 2, CURRENT_TIMESTAMP, 'admin'),

    -- 🇮🇪 IRLANDA (id 7)
    ('Celtic Logistics Ltd.', '42 O’Connell Street, Dublín', 7, 2, CURRENT_TIMESTAMP, 'admin'),

    -- 🇬🇷 GRECIA (id 8)
    ('Hellas Transport AE', 'Leoforos Syngrou 120, Atenas', 8, 2, CURRENT_TIMESTAMP, 'admin'),

    -- 🇨🇭 SUIZA (id 9)
    ('Alpine Transport AG', 'Bahnhofstrasse 22, Zúrich', 9, 5, CURRENT_TIMESTAMP, 'admin'),

    -- 🇯🇵 JAPÓN (id 10)
    ('Nippon Cargo KK', '2-11-1 Meguro, Tokio', 10, 7, CURRENT_TIMESTAMP, 'admin'),

    -- 🇨🇳 CHINA (id 11)
    ('Dragon Freight Co.', '88 Nanjing Road, Shanghái', 11, 8, CURRENT_TIMESTAMP, 'admin'),

    -- 🇪🇸 ESPAÑA (id 12)
    ('Iberian Freight S.L.', 'Av. Andalucía 54, Sevilla', 12, 1, CURRENT_TIMESTAMP, 'admin'),
    ('Logística Mediterránea S.A.', 'Calle Mayor 33, Valencia', 12, 1, CURRENT_TIMESTAMP, 'admin');


INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(28, 29, 1, 120.00, 0.45, 0.08, 'EUR'),  -- Madrid -> Barcelona
(29, 31, 2, 130.00, 0.46, 0.09, 'EUR'),  -- Barcelona -> Sevilla
(28, 30, 3, 125.00, 0.44, 0.07, 'EUR'),  -- Madrid -> Bilbao
(27, 28, 1, 110.00, 0.42, 0.08, 'EUR'),  -- A Coruña -> Madrid
(31, 27, 4, 135.00, 0.48, 0.10, 'EUR');  -- Sevilla -> A Coruña


-- 🇵🇹 España ↔ Portugal
INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(28, 4, 2, 180.00, 0.50, 0.09, 'EUR'),  -- Madrid -> Lisboa
(4, 28, 3, 175.00, 0.49, 0.09, 'EUR'),  -- Lisboa -> Madrid
(29, 3, 1, 160.00, 0.48, 0.08, 'EUR'),  -- Barcelona -> Porto
(5, 31, 5, 190.00, 0.52, 0.10, 'EUR');  -- Lisboa Fontes -> Sevilla


-- 🇫🇷 España ↔ Francia
INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(28, 7, 1, 220.00, 0.60, 0.11, 'EUR'),  -- Madrid -> París
(29, 8, 2, 210.00, 0.58, 0.10, 'EUR'),  -- Barcelona -> Lille
(30, 10, 4, 230.00, 0.62, 0.12, 'EUR'), -- Bilbao -> Bordeaux
(7, 28, 3, 200.00, 0.56, 0.11, 'EUR');  -- París -> Madrid


-- 🇩🇪 Francia ↔ Alemania
INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(7, 18, 2, 250.00, 0.65, 0.13, 'EUR'),  -- París -> Berlín
(16, 15, 3, 260.00, 0.68, 0.14, 'EUR'), -- Frankfurt -> Koblenz
(18, 17, 1, 240.00, 0.63, 0.12, 'EUR'); -- Berlín -> Leipzig


-- 🇮🇹 Alemania ↔ Italia
INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(18, 19, 3, 300.00, 0.70, 0.15, 'EUR'),  -- Berlín -> Milán
(19, 20, 4, 280.00, 0.68, 0.14, 'EUR'),  -- Milán -> Roma
(20, 18, 2, 290.00, 0.69, 0.13, 'EUR');  -- Roma -> Berlín


-- 🌍 Irlanda ↔ España
INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(21, 28, 1, 350.00, 0.75, 0.18, 'EUR'),  -- Dublín -> Madrid
(28, 22, 2, 340.00, 0.73, 0.17, 'EUR');  -- Madrid -> Cork


-- 🌏 Asia (larga distancia simulada)
INSERT INTO maestros.tarifa_base
(id_zona_origen, id_zona_destino, tipo_trailer, precio_base, precio_por_km, precio_por_kg, moneda)
VALUES
(28, 23, 5, 900.00, 1.50, 0.40, 'EUR'),  -- Madrid -> Tokio
(26, 25, 4, 700.00, 1.30, 0.35, 'EUR');  -- Foshan -> Daqing