from PyQt5.QtWidgets import (QDialog,
                             QVBoxLayout,
                             QTableWidget,
                             QTableWidgetItem,
                             QScrollArea,
                             QWidget
                        )
from app.models.envios import get_historial_envio


class VentanaHistorialEnvio(QDialog):
    def __init__(self, id_envio, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Historial del envío")
        self.resize(600, 400)

        #  Area de scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        #  Contenedor dentro del scroll
        contenido = QWidget()
        layout_interno = QVBoxLayout(contenido)

        self.tablaHistorial = QTableWidget()
        layout_interno.addWidget(self.tablaHistorial)

        historial = get_historial_envio(id_envio)
        columnas = ['envio', 'estado_anterior', 'estado_nuevo', 'fecha_cambio']

        self.tablaHistorial.setRowCount(len(historial))
        self.tablaHistorial.setColumnCount(len(columnas))
        self.tablaHistorial.setHorizontalHeaderLabels(columnas)

        for fila_id, fila in enumerate(historial):
            for col_id, valor in enumerate(fila):
                self.tablaHistorial.setItem(fila_id, col_id, QTableWidgetItem(str(valor)))

        # Adapta el tamaño de las columnas
        self.tablaHistorial.resizeColumnsToContents()

        #  Añadir el contenido al scroll
        scroll.setWidget(contenido)

        #  Layout principal del diálogo
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(scroll)
        self.setLayout(layout_principal)