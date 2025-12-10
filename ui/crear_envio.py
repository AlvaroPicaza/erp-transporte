from PyQt5.QtWidgets import  QPushButton, QMessageBox, \
QDialog, QFormLayout, QLineEdit, QComboBox, QHBoxLayout

from app.models.maestros import (get_trailers_desplegable,
                                 get_ubicacion_desplegable,
                                 get_paises_desplegable,
                                 get_empresas_desplegable)
from app.models.envios import  Envio, grabar_envio



class VentanaCrearEnvio(QDialog):
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("Crear envío")
        self.layout = QFormLayout()
        self.nombre = QLineEdit()
        self.layout.addRow("Nombre",self.nombre)



        #trailers
        self.comboTrailer = QComboBox()
        self.layout.addRow('Tipo trailer: ',self.comboTrailer)
        self.trailers = get_trailers_desplegable()
        for trailer in self.trailers:
            self.comboTrailer.addItem(trailer)

        #pais origen
        self.comboPaisOrigen= QComboBox()
        self.layout.addRow('País origen: ', self.comboPaisOrigen)
        self.comboPaisOrigen.currentIndexChanged.connect(self.actualizar_ubicaciones_origen)
        self.comboPaisOrigen.currentIndexChanged.connect(self.actualizar_transportista)

        #ubicacion origen
        self.comboUbiOrigen = QComboBox()
        self.comboUbiOrigen.setEnabled(False)
        self.layout.addRow('Ubicación origen: ', self.comboUbiOrigen)

        #pais destino
        self.comboPaisDestino = QComboBox()
        self.layout.addRow('País destino: ', self.comboPaisDestino)
        self.comboPaisDestino.currentIndexChanged.connect(self.actualizar_ubicaciones_destino)

        #ubicacion destino
        self.comboUbiDestino = QComboBox()
        self.comboUbiDestino.setEnabled(False)
        self.layout.addRow('Ubicación destino: ', self.comboUbiDestino)

        #empresas
        self.comboTrasportista = QComboBox()
        self.comboTrasportista.setEnabled(False)
        self.layout.addRow('Empresa:', self.comboTrasportista)

        if self.comboPaisOrigen.currentText().strip() != "":
            pais = self.comboPaisOrigen.currentText()
            transportistas = get_empresas_desplegable(pais)
            for transportista in transportistas:
                self.comboTrasportista.addItem(transportista)


        paises = get_paises_desplegable()
        for pais in paises:
            self.comboPaisOrigen.addItem(pais)
            self.comboPaisDestino.addItem(pais)


        #boton aceptar
        self.botonAceptar = QPushButton("Crear envío")
        self.botonAceptar.clicked.connect(self.grabar_envio)
        self.layoutbotones = QHBoxLayout()
        self.layoutbotones.addStretch()
        self.layoutbotones.addWidget(self.botonAceptar)
        self.layoutbotones.addStretch()
        self.layout.addRow(self.layoutbotones)


        self.setLayout(self.layout)


    def actualizar_ubicaciones_origen(self):
        pais = self.comboPaisOrigen.currentText()
        self.comboUbiOrigen.clear()
        ubicaciones = get_ubicacion_desplegable(pais)
        for ubicacion in ubicaciones:
            self.comboUbiOrigen.addItem(ubicacion)
        self.comboUbiOrigen.setEnabled(True)

    def actualizar_ubicaciones_destino(self):
        pais = self.comboPaisDestino.currentText()
        self.comboUbiDestino.clear()
        ubicaciones = get_ubicacion_desplegable(pais)
        for ubicacion in ubicaciones:
            self.comboUbiDestino.addItem(ubicacion)
        self.comboUbiDestino.setEnabled(True)

    def actualizar_transportista(self):
        self.comboTrasportista.clear()
        pais = self.comboPaisOrigen.currentText()
        trasportistas = get_empresas_desplegable(pais)
        for transportista in trasportistas:
            self.comboTrasportista.addItem(transportista)
        self.comboTrasportista.setEnabled(True)



    def grabar_envio(self):
        nombre = self.nombre.text()
        trailer = self.comboTrailer.currentText()
        ubiOrigen = self.comboUbiOrigen.currentText()
        ubiDestino = self.comboUbiDestino.currentText()
        transportista = self.comboTrasportista.currentText()
        if not nombre:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Icon.Warning)
            alert.setText("Debes indicar un nombre para el envío.")
            alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            alert.exec()
            return
        envio = Envio(nombre,trailer,ubiOrigen,ubiDestino,transportista)
        grabar_envio(envio)
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Icon.Information)
        alert.setText("Envío grabado!")
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.exec()
        self.close()
