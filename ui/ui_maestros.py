import sys
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGridLayout,
                             QSpacerItem,
                             QSizePolicy,
                             QTableWidget,
                             QTableWidgetItem,
                             QLabel,
                             QComboBox,
                             QGroupBox
)
from app.models.maestros import (get_pais,
                                 get_paises_desplegable,
                                 get_ubicaciones,
                                 get_empresas,
                                 get_trailers,
                                 get_total_ubicaciones,
                                 get_tarifas
)

class VentanaMaestros(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 900)
        self.setWindowTitle("Maestros transporte")

        main_layout = QVBoxLayout()

        # --- Grupo de botones de acción ---
        group_acciones = QGroupBox("Acciones")
        layout_acciones = QHBoxLayout()

        self.botonPaises = QPushButton("Mostrar países")
        self.botonPaises.clicked.connect(self.cargar_paises)
        self.botonTrailer = QPushButton("Mostrar tipos trailer")
        self.botonTrailer.clicked.connect(self.cargar_trailers)

        layout_acciones.addWidget(self.botonPaises)
        layout_acciones.addWidget(self.botonTrailer)
        layout_acciones.addStretch()  # empuja botones a la izquierda

        group_acciones.setLayout(layout_acciones)
        main_layout.addWidget(group_acciones)

        # --- Grupo de filtros por ubicación ---
        group_ubicacion = QGroupBox("Filtros Ubicación")
        layout_ubicacion = QGridLayout()

        self.labelPais = QLabel("País ubicación:")
        self.comboPais = QComboBox()
        self.comboPais.addItem("")
        self.comboPais.setCurrentIndex(-1)
        for pais in get_paises_desplegable():
            self.comboPais.addItem(pais)

        self.botonUbicacion = QPushButton("Buscar ubicaciones")
        self.botonUbicacion.clicked.connect(self.cargar_ubicaciones)

        layout_ubicacion.addWidget(self.labelPais, 0, 0)
        layout_ubicacion.addWidget(self.comboPais, 0, 1)
        layout_ubicacion.addWidget(self.botonUbicacion, 0, 2)

        group_ubicacion.setLayout(layout_ubicacion)
        main_layout.addWidget(group_ubicacion)

        # --- Grupo de filtros por empresa ---
        group_empresa = QGroupBox("Filtros Empresa")
        layout_empresa = QGridLayout()

        self.labelEmpresa = QLabel("País empresa:")
        self.comboPaisEmpresa = QComboBox()
        self.comboPaisEmpresa.addItem("")
        self.comboPaisEmpresa.setCurrentIndex(-1)
        for pais in get_paises_desplegable():
            self.comboPaisEmpresa.addItem(pais)

        self.botonEmpresas = QPushButton("Mostrar empresas")
        self.botonEmpresas.clicked.connect(self.cargar_empresas)

        layout_empresa.addWidget(self.labelEmpresa, 0, 0)
        layout_empresa.addWidget(self.comboPaisEmpresa, 0, 1)
        layout_empresa.addWidget(self.botonEmpresas, 0, 2)

        group_empresa.setLayout(layout_empresa)
        main_layout.addWidget(group_empresa)

        #-- Costes --

        group_costes = QGroupBox("Filtros tarifas")
        layout_costes = QGridLayout()

        self.labelOrigenCostes = QLabel("Ubicación origen:")
        self.comboUbicacionOrigenCostes = QComboBox()
        self.comboUbicacionOrigenCostes.addItem("")
        self.comboUbicacionOrigenCostes.setCurrentIndex(-1)
        for ubicacion in get_total_ubicaciones():
            self.comboUbicacionOrigenCostes.addItem(ubicacion)

        self.labelDestinoCostes = QLabel("Ubicación destino:")
        self.comboUbicacionDestinoCostes = QComboBox()
        self.comboUbicacionDestinoCostes.addItem("")
        self.comboUbicacionDestinoCostes.setCurrentIndex(-1)
        for ubicacion in get_total_ubicaciones():
            self.comboUbicacionDestinoCostes.addItem(ubicacion)

        self.botonTarifas = QPushButton("Buscar tarifas")
        self.botonTarifas.clicked.connect(self.cargar_tarifas)


        layout_costes.addWidget(self.labelOrigenCostes, 0, 0)
        layout_costes.addWidget(self.comboUbicacionOrigenCostes, 0, 1)
        layout_costes.addWidget(self.labelDestinoCostes, 1, 0)
        layout_costes.addWidget(self.comboUbicacionDestinoCostes, 1, 1)
        layout_costes.addWidget(self.botonTarifas, 1, 3)


        group_costes.setLayout(layout_costes)
        main_layout.addWidget(group_costes)

        # --- Tabla ---
        self.tabla = QTableWidget()
        main_layout.addWidget(self.tabla)

        self.setLayout(main_layout)
        self.show()

    # --- Métodos de carga ---
    def cargar_paises(self):
        self.tabla.clear()
        paises = get_pais()
        columnas = ["id","descripcion","codigo ISO","fecha alta","fecha baja"]

        self.tabla.setRowCount(len(paises))
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        for fila_id,fila in enumerate(paises):
            for columna_id,valor in enumerate(fila):
                self.tabla.setItem(fila_id,columna_id,QTableWidgetItem(str(valor)))
        self.tabla.resizeColumnsToContents()

    def cargar_trailers(self):
        self.tabla.clear()
        trailers = get_trailers()
        columnas = ["id","descripcion","fecha_alta","fecha_baja"]

        self.tabla.setRowCount(len(trailers))
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        for fila_id,fila in enumerate(trailers):
            for columna_id, valor in enumerate(fila):
                self.tabla.setItem(fila_id,columna_id,QTableWidgetItem(str(valor)))
        self.tabla.resizeColumnsToContents()

    def cargar_ubicaciones(self):
        self.tabla.clear()
        pais = self.comboPais.currentText()
        ubicaciones = get_ubicaciones(pais)
        columnas = ["id","descripcion","pais","fecha_alta","fecha_baja"]

        self.tabla.setRowCount(len(ubicaciones))
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        for fila_id,fila in enumerate(ubicaciones):
            for columna_id, valor in enumerate(fila):
                self.tabla.setItem(fila_id,columna_id,QTableWidgetItem(str(valor)))
        self.tabla.resizeColumnsToContents()

    def cargar_empresas(self):
        self.tabla.clear()
        pais = self.comboPaisEmpresa.currentText()
        empresas = get_empresas(pais)
        columnas = ["razon_social", "direccion", "pais","idioma","fecha_alta","usuario_alta","fecha_mod","usuario_mod","fecha_baja","usuario_baja"]

        self.tabla.setRowCount(len(empresas))
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        for fila_id,fila in enumerate(empresas):
            for columna_id,valor in enumerate(fila):
                self.tabla.setItem(fila_id,columna_id,QTableWidgetItem(str(valor)))
        self.tabla.resizeColumnsToContents()

    def cargar_tarifas(self):
        self.tabla.clear()
        ubicacion_origen = self.comboUbicacionOrigenCostes.currentText()
        ubicacion_destino = self.comboUbicacionDestinoCostes.currentText()
        tarifas = get_tarifas(ubicacion_origen,ubicacion_destino)
        columnas = ["ubicacion_origen", "ubicacion_destino", "tipo_trailer", "precio_base", "precio_km", "precio_kg", "moneda",
                    "fecha_alta", "fecha_baja"]

        self.tabla.setRowCount(len(tarifas))
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        for fila_id, fila in enumerate(tarifas):
            for columna_id, valor in enumerate(fila):
                self.tabla.setItem(fila_id, columna_id, QTableWidgetItem(str(valor)))
        self.tabla.resizeColumnsToContents()