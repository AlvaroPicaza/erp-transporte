import sys
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout)
from PyQt5.QtGui import QFont
from ui.mostrar_envios import VentanaMostrarEnvios
from ui.crear_envio import VentanaCrearEnvio
from ui.ui_maestros import VentanaMaestros

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP Transporte")
        self.setGeometry(500, 100, 700, 400)

        # --- Botones estilo tile ---
        self.botonMostrar = QPushButton("Mostrar envíos")
        self.botonMostrar.setFixedSize(200, 100)
        self.botonMostrar.setFont(QFont("Arial", 12, QFont.Bold))
        # self.botonMostrar.setIcon(QIcon("ruta_icono_mostrar.png"))  # opcional
        self.botonMostrar.clicked.connect(self.abrir_editor)

        self.botonCrear = QPushButton("Crear envío")
        self.botonCrear.setFixedSize(200, 100)
        self.botonCrear.setFont(QFont("Arial", 12, QFont.Bold))
        # self.botonCrear.setIcon(QIcon("ruta_icono_crear.png"))
        self.botonCrear.clicked.connect(self.abrir_creador)

        self.botonMaestros = QPushButton("Maestros")
        self.botonMaestros.setFixedSize(200, 100)
        self.botonMaestros.setFont(QFont("Arial", 12, QFont.Bold))
        # self.botonMaestros.setIcon(QIcon("ruta_icono_maestros.png"))
        self.botonMaestros.clicked.connect(self.abrir_maestros)

        # Layout horizontal de tiles
        layoutTiles = QHBoxLayout()
        layoutTiles.addStretch()
        layoutTiles.addWidget(self.botonMostrar)
        layoutTiles.addWidget(self.botonCrear)
        layoutTiles.addWidget(self.botonMaestros)
        layoutTiles.addStretch()
        layoutTiles.setSpacing(40)

        # Botón de salir
        self.botonSalir = QPushButton("Cerrar ERP")
        self.botonSalir.setFixedSize(150, 50)
        self.botonSalir.clicked.connect(self.close)

        layoutSalir = QHBoxLayout()
        layoutSalir.addStretch()
        layoutSalir.addWidget(self.botonSalir)

        # Layout principal vertical
        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.addStretch()
        layoutPrincipal.addLayout(layoutTiles)
        layoutPrincipal.addStretch()
        layoutPrincipal.addLayout(layoutSalir)

        self.setLayout(layoutPrincipal)
        self.show()

    #  Métodos para abrir ventanas
    def abrir_editor(self):
        self.VentanaMostrarEnvios = VentanaMostrarEnvios()
        self.VentanaMostrarEnvios.show()

    def abrir_creador(self):
        self.VentanaCrearEnvio = VentanaCrearEnvio()
        self.VentanaCrearEnvio.show()

    def abrir_maestros(self):
        self.VentanaMaestros = VentanaMaestros()
        self.VentanaMaestros.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

