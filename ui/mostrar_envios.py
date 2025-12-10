import faulthandler
import datetime

from PyQt5.QtCore import QDate, pyqtSignal, Qt, QPoint
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QMessageBox,
                             QLabel,
                             QGridLayout,
                             QDateEdit,
                             QVBoxLayout,
                             QTableWidget,
                             QTableWidgetItem,
                             QDialog,
                             QComboBox,
                             QMenu,
                             QAction,
                             QFileDialog
                        )
from PyQt5.QtGui import QFontDatabase, QFont
from qt_material import apply_stylesheet

from app.models.maestros import (get_paises_desplegable,get_ubicacion_desplegable)

from app.models.envios import (recuperar_envios_tabla,
                               actualizar_envio_por_id,
                               get_ultimo_estado_historial,
                               add_registro_historial,
                               exportar_df
                            )

from ui.editar_envio import VentanaEditarEnvio
from ui.ventana_historial import VentanaHistorialEnvio
from ui.ventana_creador_costes import VentanaCreadorCostes

faulthandler.enable()


class ClickableQTabWidget(QTableWidget):
    clicked = pyqtSignal()

    def mousePressEvent(self, e):
        self.clicked.emit()


class VentanaMostrarEnvios(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("Editar envío")

        self.layout = QGridLayout()
        self._crear_campos_fecha()
        self._crear_campos_pais()
        self._crear_campos_ubicacion()
        self._crear_tabla_envios()
        self._crear_botones()

        self.setLayout(self.layout)
        self.show()

        #Campos

    def _crear_campos_fecha(self):
        self.labelFechaDesde = QLabel("Fecha desde:*")
        self.textFechaDesde = QDateEdit()
        self.textFechaDesde.setCalendarPopup(True)
        self.textFechaDesde.setDate(QDate.currentDate())

        self.labelFechaHasta = QLabel("Fecha hasta:*")
        self.textFechaHasta = QDateEdit()
        self.textFechaHasta.setCalendarPopup(True)
        self.textFechaHasta.setDate(QDate.currentDate())

        self.layout.addWidget(self.labelFechaDesde, 0, 0)
        self.layout.addWidget(self.textFechaDesde, 0, 1)
        self.layout.addWidget(self.labelFechaHasta, 0, 3)
        self.layout.addWidget(self.textFechaHasta, 0, 4)

    def _crear_campos_pais(self):
        self.labelPaisOrigen = QLabel("País origen:")
        self.comboPaisOrigen = QComboBox()
        self.comboPaisOrigen.addItem(" ")
        self.comboPaisOrigen.setCurrentIndex(-1)
        self.comboPaisOrigen.currentIndexChanged.connect(self.pais_origen_sin_seleccionar)
        self.comboPaisOrigen.currentIndexChanged.connect(self.actualizar_ubicaciones_origen)

        self.labelPaisDestino = QLabel("País destino:")
        self.comboPaisDestino = QComboBox()
        self.comboPaisDestino.addItem(" ")
        self.comboPaisDestino.setCurrentIndex(-1)
        self.comboPaisDestino.currentIndexChanged.connect(self.pais_destino_sin_seleccionar)
        self.comboPaisDestino.currentIndexChanged.connect(self.actualizar_ubicaciones_destino)

        paises = get_paises_desplegable()
        for pais in paises:
            self.comboPaisOrigen.addItem(pais)
            self.comboPaisDestino.addItem(pais)

        self.layout.addWidget(self.labelPaisOrigen, 1, 0)
        self.layout.addWidget(self.comboPaisOrigen, 1, 1)
        self.layout.addWidget(self.labelPaisDestino, 1, 3)
        self.layout.addWidget(self.comboPaisDestino, 1, 4)

    def _crear_campos_ubicacion(self):
        self.labelUbiOrigen = QLabel("Ubicación origen:")
        self.comboUbiOrigen = QComboBox()
        self.comboUbiOrigen.setEnabled(False)

        self.labelUbiDestino = QLabel("Ubicación destino:")
        self.comboUbiDestino = QComboBox()
        self.comboUbiDestino.setEnabled(False)

        self.layout.addWidget(self.labelUbiOrigen, 2, 0)
        self.layout.addWidget(self.comboUbiOrigen, 2, 1)
        self.layout.addWidget(self.labelUbiDestino, 2, 3)
        self.layout.addWidget(self.comboUbiDestino, 2, 4)

    def _crear_tabla_envios(self):
        self.tablaEnvios = QTableWidget()
        self.tablaEnvios.cellDoubleClicked.connect(self.abrir_editor_envio)
        self.tablaEnvios.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tablaEnvios.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.layout.addWidget(self.tablaEnvios, 6, 0, 1, 5)

    def _crear_botones(self):
        self.botonEnvios = QPushButton("Mostrar envíos", self)
        self.botonEnvios.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.botonEnvios, 4, 2)

        self.botonLimpiar = QPushButton("Limpiar campos", self)
        self.botonLimpiar.clicked.connect(self.limpiar_campos)
        self.layout.addWidget(self.botonLimpiar, 4, 3)

        self.botonExportar = QPushButton("Exportar datos", self)
        self.botonExportar.clicked.connect(self.exportar_datos)
        self.layout.addWidget(self.botonExportar, 4, 4)

    # ------------------------------------------------------------------
    # LÓGICA PRINCIPAL
    # ------------------------------------------------------------------
    def cargar_datos(self):
        fecha_desde = datetime.datetime.combine(self.textFechaDesde.date().toPyDate(), datetime.time(0, 0, 0))
        fecha_hasta = datetime.datetime.combine(self.textFechaHasta.date().toPyDate(), datetime.time(23, 59, 59))

        paisOrigen = None if self.comboPaisOrigen.currentText() == ' ' else self.comboPaisOrigen.currentText()
        paisDestino = None if self.comboPaisDestino.currentText() == ' ' else self.comboPaisDestino.currentText()
        ubiOrigen = None if self.comboUbiOrigen.currentText() == ' ' else self.comboUbiOrigen.currentText()
        ubiDestino = None if self.comboUbiDestino.currentText() == ' ' else self.comboUbiDestino.currentText()

        envios = recuperar_envios_tabla(fecha_desde, fecha_hasta, paisOrigen, paisDestino, ubiOrigen, ubiDestino)
        columnas = ['id','nombre','tipo_trailer','id_origen','ubicacion_origen','id_destino','ubicacion_destino','fecha_alta','fecha_baja','estado','empresa']

        self.tablaEnvios.setRowCount(len(envios))
        self.tablaEnvios.setColumnCount(len(columnas))
        self.tablaEnvios.setHorizontalHeaderLabels(columnas)

        for fila_id, fila in enumerate(envios):
            for col_id, col in enumerate(fila):
                self.tablaEnvios.setItem(fila_id, col_id, QTableWidgetItem(str(col)))

        self.tablaEnvios.resizeColumnsToContents()


    def abrir_editor_envio(self, fila):
        datos_envio = self._obtener_datos_fila(fila)
        envio_id = datos_envio['id']

        editor = VentanaEditarEnvio(datos_envio, parent=self)

        if editor.exec_():
            nuevos_datos = editor.obtener_datos_actualizados()
            actualizar_envio_por_id(envio_id, nuevos_datos)

            if nuevos_datos.get("estado") != get_ultimo_estado_historial(nuevos_datos.get("id")):
                ultimo_estado = get_ultimo_estado_historial(nuevos_datos.get("id"))
                nuevo_estado = nuevos_datos.get("estado")
                add_registro_historial(nuevos_datos.get("id"), ultimo_estado, nuevo_estado)

            self.cargar_datos()

    def abrir_historial_envio(self, fila):
        datos_envio = self._obtener_datos_fila(fila)
        id_envio = datos_envio['id']

        historial = VentanaHistorialEnvio(id_envio, parent=self)
        historial.exec_()
        self.cargar_datos()

    def abrir_creador_costes(self, fila):
        datos_envio = self._obtener_datos_fila(fila)
        costes = VentanaCreadorCostes(datos_envio, parent=self)

        costes.exec_()
        self.cargar_datos()

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------
    def _obtener_datos_fila(self, fila):
        datos = {}
        for col_id in range(self.tablaEnvios.columnCount()):
            header = self.tablaEnvios.horizontalHeaderItem(col_id).text()
            valor = self.tablaEnvios.item(fila, col_id).text()
            datos[header] = valor
        return datos

    def actualizar_ubicaciones_origen(self):
        pais = self.comboPaisOrigen.currentText().strip()
        if not pais:
            return
        self.comboUbiOrigen.clear()
        self.comboUbiOrigen.addItem(" ")
        ubicaciones = get_ubicacion_desplegable(pais)
        for ubicacion in ubicaciones:
            self.comboUbiOrigen.addItem(ubicacion)
        self.comboUbiOrigen.setEnabled(True)
        self.comboUbiOrigen.setCurrentIndex(-1)

    def actualizar_ubicaciones_destino(self):
        pais = self.comboPaisDestino.currentText().strip()
        if not pais:
            return
        self.comboUbiDestino.clear()
        self.comboUbiDestino.addItem(" ")
        ubicaciones = get_ubicacion_desplegable(pais)
        for ubicacion in ubicaciones:
            self.comboUbiDestino.addItem(ubicacion)
        self.comboUbiDestino.setEnabled(True)
        self.comboUbiDestino.setCurrentIndex(-1)

    def pais_origen_sin_seleccionar(self):
        if self.comboPaisOrigen.currentText().strip() in ("", " "):
            self.comboUbiOrigen.clear()
            self.comboUbiOrigen.setEnabled(False)

    def pais_destino_sin_seleccionar(self):
        if self.comboPaisDestino.currentText().strip() in ("", " "):
            self.comboUbiDestino.clear()
            self.comboUbiDestino.setEnabled(False)

    def limpiar_campos(self):
        self.comboPaisOrigen.setCurrentIndex(-1)
        self.comboPaisDestino.setCurrentIndex(-1)
        self.comboUbiOrigen.clear()
        self.comboUbiOrigen.setEnabled(False)
        self.comboUbiDestino.clear()
        self.comboUbiDestino.setEnabled(False)


    def mostrar_menu_contextual(self, pos: QPoint):
        fila = self.tablaEnvios.rowAt(pos.y())
        if fila < 0:
            return

        self.tablaEnvios.selectRow(fila)
        menu = QMenu(self)

        accion_editar = QAction("Editar envío", self)
        accion_historial = QAction("Revisar historial", self)
        accion_costes = QAction("Generar costes", self)

        menu.addAction(accion_editar)
        menu.addAction(accion_historial)
        menu.addAction(accion_costes)

        accion_editar.triggered.connect(lambda _, f=fila: self.abrir_editor_envio(f))
        accion_historial.triggered.connect(lambda _, f=fila: self.abrir_historial_envio(f))
        accion_costes.triggered.connect(lambda _, f=fila: self.abrir_creador_costes(f))

        menu.exec_(self.tablaEnvios.viewport().mapToGlobal(pos))


    def exportar_datos(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar archivo Excel", "", "Archivo Excel (*.xlsx)")
        if not ruta:
            return

        columnas = [self.tablaEnvios.horizontalHeaderItem(col).text() for col in range(self.tablaEnvios.columnCount())]
        datos = []

        for fila in range(self.tablaEnvios.rowCount()):
            fila_datos = []
            for col in range(self.tablaEnvios.columnCount()):
                fila_datos.append(self.tablaEnvios.item(fila, col).text())
            datos.append(fila_datos)

        exportar_df(columnas, datos, ruta)
