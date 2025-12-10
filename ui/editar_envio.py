
import faulthandler
from datetime import datetime
from PyQt5.QtWidgets import (QLabel,
                            QFormLayout,
                            QLineEdit,
                            QDialogButtonBox,
                            QDialog,
                            QCheckBox,
                            QHBoxLayout,
                            QComboBox
                        )


from app.models.envios import get_estados_desplegable
from app.models.maestros import (
                                get_pais_ubicacion,
                                get_ubicacion_desplegable,
                                get_trailers_desplegable,
                                get_id_ubicacion,
                                get_empresas_desplegable,
                                get_pais_empresa
                            )

faulthandler.enable()


class VentanaEditarEnvio(QDialog):

    def __init__(self, datos_envio, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar envío")

        self.campos = {}
        layout = QFormLayout()

        # Crear campos dinámicamente
        for campo, valor in datos_envio.items():

            entrada = QLineEdit(valor)

            # Campos deshabilitados
            if campo in ["id", "id_origen", "id_destino", "fecha_alta", "fecha_baja"]:
                entrada.setDisabled(True)

            # Campos simples
            if campo not in ["estado", "ubicacion_origen", "ubicacion_destino", "tipo_trailer", "empresa"]:
                layout.addRow(campo, entrada)

            # --- Tipo Trailer ---
            if campo == "tipo_trailer":
                self.labelTipoTrailer = QLabel("Tipo trailer")
                self.comboTipoTrailer = QComboBox()

                for trailer in get_trailers_desplegable():
                    self.comboTipoTrailer.addItem(trailer)

                layout.addRow(self.labelTipoTrailer, self.comboTipoTrailer)
                idx = self.comboTipoTrailer.findText(valor)
                self.comboTipoTrailer.setCurrentIndex(idx)

            # --- Ubicación Origen ---
            if campo == "ubicacion_origen":
                self.labelUbiOrigen = QLabel("Ubicación origen")
                self.comboUbiOrigen = QComboBox()

                pais = get_pais_ubicacion(datos_envio.get("ubicacion_origen"))
                for ubi in get_ubicacion_desplegable(pais):
                    self.comboUbiOrigen.addItem(ubi)

                layout.addRow(self.labelUbiOrigen, self.comboUbiOrigen)
                idx = self.comboUbiOrigen.findText(valor)
                self.comboUbiOrigen.setCurrentIndex(idx)

            # --- Ubicación Destino ---
            if campo == "ubicacion_destino":
                self.labelUbiDestino = QLabel("Ubicación destino")
                self.comboUbiDestino = QComboBox()

                pais = get_pais_ubicacion(datos_envio.get("ubicacion_destino"))
                for ubi in get_ubicacion_desplegable(pais):
                    self.comboUbiDestino.addItem(ubi)

                layout.addRow(self.labelUbiDestino, self.comboUbiDestino)
                idx = self.comboUbiDestino.findText(valor)
                self.comboUbiDestino.setCurrentIndex(idx)

            # --- Estado ---
            if campo == "estado":
                self.labelEstado = QLabel("Estado")
                self.comboEstado = QComboBox()

                for estado in get_estados_desplegable():
                    self.comboEstado.addItem(estado)

                layout.addRow(self.labelEstado, self.comboEstado)
                idx = self.comboEstado.findText(valor)
                self.comboEstado.setCurrentIndex(idx)

                # Si está cancelado, bloquear cambios
                if self.comboEstado.currentText() == "CANCELADO":
                    self.comboEstado.setDisabled(True)

            # --- Empresa ---
            if campo == "empresa":
                self.labelTransportista = QLabel("Transportista")
                self.comboTransportista = QComboBox()

                pais = get_pais_empresa(datos_envio.get("empresa"))
                for t in get_empresas_desplegable(pais):
                    self.comboTransportista.addItem(t)

                layout.addRow(self.labelTransportista, self.comboTransportista)
                idx = self.comboTransportista.findText(valor)
                self.comboTransportista.setCurrentIndex(idx)

            self.campos[campo] = entrada

        # --- Botones de anulación / habilitación ---
        self.botonAnular = QCheckBox("Anular envío")
        layout.addWidget(self.botonAnular)

        self.botonHabilitar = QCheckBox("Rehabilitar envío")
        layout.addWidget(self.botonHabilitar)

        # Control habilitación de botones
        if self.campos["fecha_baja"].text() != "None":
            self.botonHabilitar.setEnabled(True)
        else:
            self.botonHabilitar.setEnabled(False)

        if self.botonHabilitar.isEnabled():
            self.botonAnular.setDisabled(True)

        # Eventos de actualización de ubicaciones
        self.comboUbiOrigen.currentIndexChanged.connect(self.actualizar_ubicacion_origen)
        self.comboUbiDestino.currentIndexChanged.connect(self.actualizar_ubicacion_destino)

        # --- Botones Aceptar / Cancelar ---
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(botones)
        layout_botones.addStretch()

        layout.addRow(layout_botones)

        self.setLayout(layout)

    # -----------------------------------------------------------
    # Obtención de datos actualizados
    # -----------------------------------------------------------
    def obtener_datos_actualizados(self):

        estado = self.comboEstado.currentText()
        fecha_baja = self.campos["fecha_baja"].text()

        # Anulación / Habilitación
        if self.botonAnular.isChecked():
            fecha_baja = datetime.now()
            estado = "CANCELADO"
        #elif self.campos['fecha_baja'].text():
            #fecha_baja = None

        if self.botonHabilitar.isChecked():
            fecha_baja = None
            estado = "BORRADOR"

        #elif (self.botonHabilitar.isEnabled()) and (not self.botonHabilitar.isChecked()):
            #fecha_baja =

        if fecha_baja == 'None':
            return {
                "id": int(self.campos["id"].text()),
                "nombre": self.campos["nombre"].text(),
                "tipo_trailer": self.comboTipoTrailer.currentText(),
                "id_ubicacion_origen": int(self.campos["id_origen"].text()),
                "ubicacion_origen": self.comboUbiOrigen.currentText(),
                "id_ubicacion_destino": int(self.campos["id_destino"].text()),
                "ubicacion_destino": self.comboUbiDestino.currentText(),
                "fecha_alta": self.campos["fecha_alta"].text(),
                "fecha_baja": None,
                "estado": estado,
                "empresa": self.comboTransportista.currentText()
            }
        else:
            return {
                "id": int(self.campos["id"].text()),
                "nombre": self.campos["nombre"].text(),
                "tipo_trailer": self.comboTipoTrailer.currentText(),
                "id_ubicacion_origen": int(self.campos["id_origen"].text()),
                "ubicacion_origen": self.comboUbiOrigen.currentText(),
                "id_ubicacion_destino": int(self.campos["id_destino"].text()),
                "ubicacion_destino": self.comboUbiDestino.currentText(),
                "fecha_alta": self.campos["fecha_alta"].text(),
                "fecha_baja": fecha_baja,
                "estado": estado,
                "empresa": self.comboTransportista.currentText()
            }

    # -----------------------------------------------------------
    # Actualización de IDs según selección de combo
    # -----------------------------------------------------------
    def actualizar_ubicacion_origen(self):
        ubicacion = self.comboUbiOrigen.currentText()
        self.campos["id_origen"].clear()
        self.campos["id_origen"].setText(str(get_id_ubicacion(ubicacion)))

    def actualizar_ubicacion_destino(self):
        ubicacion = self.comboUbiDestino.currentText()
        self.campos["id_destino"].clear()
        self.campos["id_destino"].setText(str(get_id_ubicacion(ubicacion)))
