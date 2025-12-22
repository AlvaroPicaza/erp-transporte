
from ui.ventana_envio import VentanaPrincipal
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontDatabase, QPixmap
from qt_material import apply_stylesheet
import sys
from database.connection import get_connection
from app.models.envios import envios_to_dict, grabar_envio

################


class AppLoader:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ventana = VentanaPrincipal()

        # Splash
        pixmap = QPixmap("C:/Users/garci/Desktop/Python/ERP Transporte/prueba.png")
        self.splash = QSplashScreen(pixmap)
        self.splash.setMask(pixmap.mask())
        self.splash.show()

        # Barra de progreso
        self.progress = QProgressBar(self.splash)
        self.progress.setGeometry(0, pixmap.height() - 50, pixmap.width(), 20)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.show()

        # Fuente y tema
        apply_stylesheet(self.app, theme='dark_lightgreen.xml')
        #id_fuente = QFontDatabase.addApplicationFont(
            #"C:/Users/garci/Desktop/Python/ERP Transporte/fonts/inter/static/Inter_18pt-Medium.ttf")
        #familias = QFontDatabase.applicationFontFamilies(id_fuente)
        #fuente_nombre = familias[0] if familias else "Arial"

        # Control de progreso
        self.contador = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(20)  # cada 20ms

        sys.exit(self.app.exec_())

    def actualizar(self):
        self.contador += 1
        self.progress.setValue(self.contador)
        if self.contador >= 100:
            self.timer.stop()
            self.splash.finish(self.ventana)
            self.ventana.show()


if __name__ == '__main__':
    AppLoader()
    