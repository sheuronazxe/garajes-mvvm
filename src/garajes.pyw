import sys, os, informes, formularios
from os.path import exists
from PyQt5.QtCore import QDate, QPersistentModelIndex, QSize, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QDateEdit, QGridLayout, QHeaderView, QMessageBox, QPushButton, QSizePolicy, QSpacerItem, QTableView, QWidget


class Ventana(QWidget):
    def __init__(self):
        super().__init__()

        self.tabla = QTableView()
        self.tabla.setModel(proxyModel)
        self.tabla.hideColumn(0)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.setColumnWidth(2,170)
        self.tabla.setColumnWidth(3,250)
        self.tabla.setColumnWidth(4,80)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.sortByColumn(1,Qt.AscendingOrder)
        self.tabla.setFont(QFont("Calibri",14))
        self.tabla.horizontalHeader().setStyleSheet("::section{ border: 0px; border-right: 1px solid silver; border-bottom: 2px solid steelblue; background-color: floralwhite; padding:4px }")
        
        btn_añadir = QPushButton(" AÑADIR")
        btn_añadir.setToolTip("Nueva ficha")
        btn_añadir.setIcon(QIcon("iconos/anadir.svg"))
        btn_añadir.setIconSize(QSize(18, 18))
        btn_añadir.setFixedSize(90, 34)
        btn_añadir.setFlat(True)
        btn_añadir.clicked.connect(self.nuevaFicha)

        btn_borrar = QPushButton(" BORRAR")
        btn_borrar.setToolTip("Borrar selección")
        btn_borrar.setIcon(QIcon("iconos/borrar.svg"))
        btn_borrar.setIconSize(QSize(18, 18))
        btn_borrar.setFixedSize(90, 34)
        btn_borrar.setFlat(True)
        btn_borrar.clicked.connect(self.borraFicha)

        self.fecha = QDateEdit()
        self.fecha.setAlignment(Qt.AlignHCenter)
        self.fecha.setDate(QDate.currentDate().addMonths(1))
        self.fecha.setDisplayFormat("MMMM yyyy")
        self.fecha.setStyleSheet("font: bold 22px; color: steelblue; background: floralwhite;")
        self.fecha.setFixedSize(240, 50)

        btn_imprimir = QPushButton(" IMPRIMIR")
        btn_imprimir.setIcon(QIcon("iconos/impresion.svg"))
        btn_imprimir.setStyleSheet("font: bold 22px; color: steelblue;")
        btn_imprimir.setFixedSize(240, 50)
        btn_imprimir.clicked.connect(self.imprimir)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.tabla, 0, 0, 1, 6)
        mainLayout.addWidget(self.fecha, 1, 0)
        mainLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 1)
        mainLayout.addWidget(btn_añadir, 1, 2)
        mainLayout.addWidget(btn_borrar, 1, 3)
        mainLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 4)
        mainLayout.addWidget(btn_imprimir, 1, 5)


    def imprimir(self):
        informes.GenerarPDF(proxyModel, self.fecha)
        self.close()


    def nuevaFicha(self):
        dialogo = formularios.Alta()
        if dialogo.exec():
            rec = model.record()
            rec.setValue(1,dialogo.nombre.text())
            rec.setValue(2,dialogo.tlf.text())
            rec.setValue(3,dialogo.garage.text())
            rec.setValue(4,dialogo.alqui.text())
            model.insertRecord(-1,rec)
            model.select()


    def borraFicha(self):
        if QMessageBox.question(self, "Confirmación", "¿Desea borrar las fichas seleccionadas?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel) == QMessageBox.Ok:
            lista = [ QPersistentModelIndex(i) for i in self.tabla.selectionModel().selectedIndexes() ]
            for i in lista:
                proxyModel.removeRow(i.row())
            model.select()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.borraFicha()


def checkDB():
    if not exists("datos"):
        os.mkdir('datos')
    if not exists("datos/clientes.db"):
        import sqlite3
        with sqlite3.connect("datos/clientes.db") as connection:
            connection.cursor().execute(""" CREATE TABLE IF NOT EXISTS clientes (
                                                id INTEGER PRIMARY KEY,
                                                Nombre TEXT NOT NULL,
                                                Teléfono INTEGER,
                                                Garaje TEXT,
                                                Alquiler INTEGER
                                                ); """)


if __name__ == '__main__':

    # Conexión con la base de datos
    checkDB()
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("datos/clientes.db")
    db.open()
    
    # Modelo de datos
    model = QSqlTableModel(None, db)
    model.setTable('clientes')
    model.select()
    proxyModel = QSortFilterProxyModel()
    proxyModel.setSourceModel(model)

    # Vista
    app = QApplication([])
    view = Ventana()
    view.setWindowTitle("Generador de recibos")
    view.setWindowIcon(QIcon("iconos/icono.svg"))
    view.setFixedSize(900, 600)
    view.show()
    sys.exit(app.exec()) 