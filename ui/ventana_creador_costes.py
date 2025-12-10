from functools import partial
from PyQt5.QtWidgets import (QPushButton,
                             QMessageBox,
                             QLabel,
                             QGridLayout,
                             QDateEdit,
                             QVBoxLayout,
                             QTableWidget,
                             QTableWidgetItem,
                             QFormLayout,
                             QLineEdit,
                             QDialogButtonBox,
                             QDialog,
                             QCheckBox,
                             QHBoxLayout,
                             QComboBox
)
from app.models.costes import calcular_coste_envio, get_tarifa_base
from database.connection import get_connection


class VentanaCreadorCostes(QDialog):
    def __init__(self, datos_envio, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generar costes")
        self.campos = {}
        layout = QFormLayout()

        # Nombre del envío
        self.nombre_envio = datos_envio.get("nombre")
        self.nombre = QLineEdit(self.nombre_envio)
        self.nombre.setDisabled(True)
        layout.addRow("Envio", self.nombre)

        # Campos de entrada
        self.distancia = QLineEdit()
        layout.addRow("Distancia", self.distancia)

        self.peso = QLineEdit()
        layout.addRow("Peso", self.peso)

        # Botón para calcular costes
        self.botonCostes = QPushButton("Calcular costes")

        # Usamos partial para pasar parámetros a la función
        self.botonCostes.clicked.connect(partial(calcular_costes, self, datos_envio))
        layout.addWidget(self.botonCostes)

        self.setLayout(layout)
        self.show()


def calcular_costes(self, datos_envio):
    print(datos_envio)

    tarifa = get_tarifa_base(
        datos_envio.get("id_origen"),
        datos_envio.get("id_destino"),
        datos_envio.get("tipo_trailer")
    )

    if tarifa is None:
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Icon.Warning)
        alert.setWindowTitle("Importante")
        alert.setText("No se ha encontrado ninguna tarifa para este envío.")
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.exec()
        self.close()
        return

    costeTotal = calcular_coste_envio(
        datos_envio.get("id_origen"),
        datos_envio.get("id_destino"),
        datos_envio.get("tipo_trailer"),
        self.distancia.text(),
        self.peso.text()
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ENVIOS.OPERATIVA_TERRESTRE
        SET tarifa = %s, coste_total = %s
        WHERE id = %s
        """,
        (tarifa.get("id_tarifa"), costeTotal, datos_envio.get("id"))
    )

    conn.commit()
    cursor.close()
    conn.close()

    self.close()