# erp-transporte
Proyecto basado en un ERP de procesos de transporte, desarrollado en Python, con interfaz gráfica mediante PyQt5, conectado a una base de datos PostgreSQL. El sistema permite crear y gestionar envíos, consultar maestros e historial de envíos, cálculo básico de costes basados en tarifas, etc.

Se puede montar una mini demo con la bbdd en database/schema.sql y la carga de database/seed_data.sql.

--Maestros--

  Países
  Idiomas
  Empresas
  Ubicaciones
  Tipos de tráiler
  Tipos de servicio

--Gestión de envíos (Operativa Terrestre)--

  Creación, edición y eliminación lógica (fecha_baja)
  Control del estado (borrador, en progreso, enviado, entregado, cancelado)
  Historial de cambios de estado
  Asignación de empresa, tráiler y tarifas
  Cálculo básico de costes (precio base, por km y por kg)

--Gestión de tarifas--

  Tarifa base por origen/destino
  Tipos de tráiler
  Moneda
  Cálculos automáticos vinculados al envío

Este proyecto incluye una API REST desarrollada con FastAPI, Pydantic para la validación de datos y Uvicorn como servidor ASGI, que expone parte de la funcionalidad del ERP de Transporte, permitiendo interactuar con el sistema mediante peticiones HTTP.

La API está pensada como una capa de acceso a los datos del ERP, facilitando futuras integraciones con aplicaciones web, móviles o sistemas externos.
