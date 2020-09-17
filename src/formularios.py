from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout

class Alta(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nueva ficha")
        self.setFixedWidth(300)

        self.nombre = QLineEdit()
        self.tlf = QLineEdit()
        self.garage = QLineEdit()
        self.alqui = QLineEdit()

        formulario = QFormLayout()
        formulario.addRow(self.tr("&Nombre:"), self.nombre)
        formulario.addRow(self.tr("&Teléfono:"), self.tlf)
        formulario.addRow(self.tr("&Garaje:"), self.garage)
        formulario.addRow(self.tr("&Alquiler:"), self.alqui)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(formulario)
        self.layout.addWidget(botones)
