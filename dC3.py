# Archivo creado para mantener en archivos separados los esqueletos de QtDesigner y de clases como MiGraphicsView

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QFileInfo, Qt, QDate, QPropertyAnimation, QPointF
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, \
    QGraphicsItem, QGraphicsLineItem, QGraphicsEllipseItem
from Main3 import Ui_MainWindow
from MiGV3 import MiGraphicsView
from pdC3 import Ui_Preferencias
from Kc2 import Ui_Dialog
import numpy as np
from string import Template
import sys, os, time
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty


class About(QtWidgets.QLabel):

    def __init__(self):
        QtWidgets.QLabel.__init__(self,
                                  "distCarb 1.0\n\nPor Servando Chinchón Payá, 2018\n\nPor favor no dude en comentar cualquier sugerencia\n\nservando@ietcc.csic.es\n\n¡Gracias!")
        self.setAlignment(QtCore.Qt.AlignCenter)

    def initUI(self):
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = app.desktop().availableGeometry().centre()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class mainProgram(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainProgram, self).__init__()
        self.setupUi(self)
        """
        Quito todo lo relativo al GraphicsView de Main.py y lo traigo aquí
        """
        self.graphicsView = MiGraphicsView()
        self.graphicsView.setAutoFillBackground(False)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_3.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.titulos_tabla = ["número", "ditancia(px)", "distancia(valor real)"]

        self.actionAbrir_imagen.triggered.connect(self.loadImage)
        self.actionSalir.triggered.connect(self.close_application)
        self.actionAyuda.triggered.connect(self.Ayuda)
        self.actionSobre_el_programa.triggered.connect(self.sobre_programa)
        self.actionPreferencias.triggered.connect(self.open_preferencias)
        self.actionCrear_informe.triggered.connect(self.report)
        self.actionGuardar_imagen.triggered.connect(self.guardar_imagen)
        self.actionCalcular_coeficiente_difusi_n.triggered.connect(self.open_calcular_kc)

        self.rb_escala.toggled.connect(self.pe)
        self.rb_linea.toggled.connect(self.pl)
        self.rb_puntos.toggled.connect(self.pp)

        self.pb_rehacerescala.clicked.connect(self.rehacer_escala)
        self.pb_rehacerlinea.clicked.connect(self.rehacer_linea)

        self.graphicsView.senyal_escala.connect(self.cosasdeescala)
        self.graphicsView.senyal_linea.connect(self.cosasdelinea)
        self.graphicsView.senyal_punto.connect(self.gestionar_puntos)

        self.dlg = pref()
        self.dlg.setModal(True)
        self.dlg.senyal_cambios_preferencias.connect(self.actualizar_preferencias)

        self.pb_OK.clicked.connect(self.ok_escala)
        self.pb_calcular.clicked.connect(self.calcular)

        self.pb_borrar.clicked.connect(self.borrar_punto)

        self.label = MyLabel("de prueba")
        self.label_puntos = False

        self.tabla_cara_1 = False
        self.tabla_cara_2 = False
        self.tabla_cara_3 = False
        self.tabla_cara_4 = False

        self.actionBorrar_puntos.triggered.connect(self.borrar_puntos_lista_cara)
        self.actionBorrar_l_nea.triggered.connect(self.graphicsView.borrarlinea)
        self.actionBorrar_escala.triggered.connect(self.graphicsView.borrarescala)

        self.cb_caras.currentIndexChanged.connect(self.llenar_tabla)

        self.tabla.itemClicked.connect(self.anim_start)
        self.tabla.itemDoubleClicked.connect(self.limpiar)

        self.nuevos_puntos_1 = []

        self.distancias_kc_1 = []
        self.distancias_kc_2 = []
        self.distancias_kc_3 = []
        self.distancias_kc_4 = []

        self.dlg_kc = Calc_coef(self.graphicsView.distanciasreales_1, self.graphicsView.distanciasreales_2, self.graphicsView.distanciasreales_3, self.graphicsView.distanciasreales_4)
        self.dlg_kc.setModal(True)
        self.dlg_kc.senyal_kc.connect(self.actualizar_kc)
        self.coeficiente = None
        self.unidades_tiempo = None
        self.unidades_distancia = None

    def loadImage(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Abrir imagen')
        self.img = QtGui.QPixmap(name)
        self.graphicsView.setPhoto(self.img)
        self.filename = QFileInfo(name).fileName()
        if self.graphicsView.empty == False:
            self.actionPreferencias.setEnabled(True)
            self.rb_escala.setEnabled(True)
            self.rb_escala.setChecked(True)
            # self.pb_rehacerescala.setEnabled(True)
            self.le_escala.setEnabled(True)
            self.pb_OK.setEnabled(True)
            self.rb_linea.setEnabled(True)
            # self.pb_rehacerlinea.setEnabled(True)
            self.rb_puntos.setEnabled(True)
            # self.pb_rehacerescala.setEnabled(True)

            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(3)
            self.tabla.setHorizontalHeaderLabels(self.titulos_tabla)
            self.tabla.resizeColumnsToContents()
            self.tabla.setEnabled(True)
            self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

            self.cb_caras.setEnabled(True)
            self.cb_caras.addItems(['1', '2', '3', '4'])
            self.cb_caras.setCurrentIndex(0)

            self.pb_calcular.setEnabled(True)
            self.actionGuardar_imagen.setEnabled(True)
            self.actionCrear_informe.setEnabled(True)

            self.actionBorrar_puntos.setEnabled(True)
            self.actionBorrar_escala.setEnabled(True)
            self.actionBorrar_l_nea.setEnabled(True)

    def guardar_imagen(self):
        name, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Imagen", "", "PNG(*.png);;JPEG(*.jpg)")
        if name == "":
            return
        if "." not in name:
            name += ".png"
        pixmap = QtGui.QPixmap(self.graphicsView.viewport().size())
        self.graphicsView.viewport().render(pixmap)
        pixmap.save(name)

    def close_application(self):
        choice = QMessageBox.information(None, 'Información',
                                         "¿Estás seguro de que quieres salir?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def open_preferencias(self):
        self.dlg.show()

    def open_calcular_kc(self):
        self.dlg_kc.show()

    def Ayuda(self):
        os.startfile('Tutorial.pdf')

    def sobre_programa(self):
        self.pop = About()
        self.pop.resize(555, 333)
        self.pop.setWindowTitle("Sobre distCarb")
        self.pop.show()

    def pe(self):
        if self.rb_escala.isChecked():
            self.graphicsView.borrarescala()
            self.graphicsView.apintar = 1

    def pl(self):
        if self.rb_linea.isChecked():
            self.graphicsView.borrarlinea()
            self.graphicsView.apintar = 2

    def pp(self):
        if self.rb_puntos.isChecked():
            self.graphicsView.apintar = 3
            self.pb_borrar.setEnabled(True)

    def rehacer_escala(self):
        self.graphicsView.borrarescala()
        self.graphicsView.apintar = 1
        self.rb_escala.setChecked(True)
        self.rb_escala.setEnabled(True)

    def cosasdeescala(self):
        self.rb_escala.setEnabled(False)
        self.pb_rehacerescala.setEnabled(True)

    def rehacer_linea(self):
        self.graphicsView.borrarlinea()
        self.graphicsView.apintar = 2
        self.rb_linea.setChecked(True)
        self.rb_linea.setEnabled(True)

    def cosasdelinea(self):
        self.rb_linea.setEnabled(False)
        self.pb_rehacerlinea.setEnabled(True)

    def actualizar_preferencias(self):
        self.graphicsView.grosor_escala = self.dlg.numescala
        self.graphicsView.grosor_linea = self.dlg.numlinea
        self.graphicsView.grosor_puntos = self.dlg.numpunto

        self.graphicsView.color_escala = self.dlg.colorescala
        self.graphicsView.color_linea = self.dlg.colorlinea
        self.graphicsView.color_puntos = self.dlg.colorpuntos
        self.graphicsView.brush.setColor(self.dlg.colorbrush)

        self.set_color()
        self.repintar_puntos()
        self.repintar_escala()
        self.repintar_linea()

    def ok_escala(self):
        try:
            valor_escala = int(self.le_escala.text())
            self.graphicsView.valor_de_escala = valor_escala
        except ValueError:
            info = QMessageBox.information(None, 'Información', "Has de introducir un número entero, sin decimales",
                                           QMessageBox.Ok)
            if info == QMessageBox.Ok:
                self.le_escala.clear()

    def gestionar_puntos(self):
        if self.cb_caras.currentIndex() == 0:
            self.graphicsView.elipses_cara_1.append(self.graphicsView.elipse)
            self.graphicsView.puntos_1.append(self.graphicsView.position)
        if self.cb_caras.currentIndex() == 1:
            self.graphicsView.elipses_cara_2.append(self.graphicsView.elipse)
            self.graphicsView.puntos_2.append(self.graphicsView.position)
        if self.cb_caras.currentIndex() == 2:
            self.graphicsView.elipses_cara_3.append(self.graphicsView.elipse)
            self.graphicsView.puntos_3.append(self.graphicsView.position)
        if self.cb_caras.currentIndex() == 3:
            self.graphicsView.elipses_cara_4.append(self.graphicsView.elipse)
            self.graphicsView.puntos_4.append(self.graphicsView.position)

        self.calcular()

    def calcular(self):
        """
        Cálculo de la distancia entre los dos puntos de la escala, del valor del segmento o longitud de la escala
        """
        """
        y = mx + b
        """
        if len(self.graphicsView.linea) > 1:
            m = (self.graphicsView.linea[3] - self.graphicsView.linea[1]) / (
                        self.graphicsView.linea[2] - self.graphicsView.linea[0])
            b = self.graphicsView.linea[1] - (m * self.graphicsView.linea[0])
            if self.cb_caras.currentIndex() == 0:
                self.distancias = self.graphicsView.distancias_1
                self.distanciasreales = self.graphicsView.distanciasreales_1
                self.puntos = self.graphicsView.puntos_1
            if self.cb_caras.currentIndex() == 1:
                self.distancias = self.graphicsView.distancias_2
                self.distanciasreales = self.graphicsView.distanciasreales_2
                self.puntos = self.graphicsView.puntos_2
            if self.cb_caras.currentIndex() == 2:
                self.distancias = self.graphicsView.distancias_3
                self.distanciasreales = self.graphicsView.distanciasreales_3
                self.puntos = self.graphicsView.puntos_3
            if self.cb_caras.currentIndex() == 3:
                self.distancias = self.graphicsView.distancias_4
                self.distanciasreales = self.graphicsView.distanciasreales_4
                self.puntos = self.graphicsView.puntos_4

            self.dist(m, b, self.distancias, self.distanciasreales, self.puntos)

        """
        Mucho ojo porque las coordenadas reales en la foto son (x, -y). El (0,0) es la esquina superior izquierda
        """

        # self.llenar_tabla()
        self.llenar_tabla()

    def dist(self, m, b, distancias, distanciasreales, puntos):

        distancias.clear()
        distanciasreales.clear()
        for pto in puntos:
            dist = abs(m * pto.x() - pto.y() + b) / np.sqrt((m ** 2) + 1)
            distancias.append(dist)
        if self.graphicsView.existeescala and self.graphicsView.valor_de_escala:
            self.d_escala_pix = ((self.graphicsView.escala[2] - self.graphicsView.escala[0]) ** 2 +
                                 (self.graphicsView.escala[3] - self.graphicsView.escala[1]) ** 2) ** (0.5)
            for i in distancias:
                dist_real = (self.graphicsView.valor_de_escala * i) / self.d_escala_pix
                distanciasreales.append(dist_real)
                print(dist_real)
        else:
            pass

    def llenar_tabla(self):
        if self.cb_caras.currentIndex() == 0:
            self.puntos = self.graphicsView.puntos_1
            self.distancias = self.graphicsView.distancias_1
            self.distanciasreales = self.graphicsView.distanciasreales_1
        if self.cb_caras.currentIndex() == 1:
            self.puntos = self.graphicsView.puntos_2
            self.distancias = self.graphicsView.distancias_2
            self.distanciasreales = self.graphicsView.distanciasreales_2
        if self.cb_caras.currentIndex() == 2:
            self.puntos = self.graphicsView.puntos_3
            self.distancias = self.graphicsView.distancias_3
            self.distanciasreales = self.graphicsView.distanciasreales_3
        if self.cb_caras.currentIndex() == 3:
            self.puntos = self.graphicsView.puntos_4
            self.distancias = self.graphicsView.distancias_4
            self.distanciasreales = self.graphicsView.distanciasreales_4

        n = 0
        self.tabla.setRowCount(len(self.puntos))
        for item in self.puntos:
            self.tabla.setItem(n, 0, QTableWidgetItem(str(int(item.x())) + " , " + str(int(item.y()))))
            self.tabla.resizeColumnsToContents()
            n += 1
        if self.graphicsView.existelinea:
            m = 0
            for elemento in self.distancias:
                self.tabla.setItem(m, 1, QTableWidgetItem(str(int(elemento))))
                self.tabla.resizeColumnsToContents()
                m += 1
        if self.graphicsView.existeescala:
            k = 0
            for element in self.distanciasreales:
                redondeados = round(element, 2)
                self.tabla.setItem(k, 2, QTableWidgetItem(str(redondeados)))
                self.tabla.resizeColumnsToContents()
                k += 1

    def report(self):
        filein = open('plantilla_resultados.txt')
        src = Template(filein.read())

        fecha = QDate.currentDate()
        fecha2 = fecha.toString(Qt.DefaultLocaleLongDate)
        title = "La fotografía tratada es la: " + str(self.filename)
        date = str(fecha2)
        todas_distancias_num = self.graphicsView.distanciasreales_1 + self.graphicsView.distanciasreales_2 + \
                               self.graphicsView.distanciasreales_3 + self.graphicsView.distanciasreales_4
        print(todas_distancias_num)
        distancias = [str(x) for x in todas_distancias_num]
        print(distancias)
        media = np.mean(todas_distancias_num)
        print(media)
        distancia_media = str(media)
        print(distancia_media)

        n = len(todas_distancias_num)
        print(n)

        pmax = np.amax(todas_distancias_num)
        print(pmax)

        tiempo = self.dlg_kc.le_tiempo.text()
        print(tiempo)
        # caras = "4"
        caras = self.check()
        kc = self.coeficiente
        un_tiempo = "días"
        un_distancia = "mm"
        if self.unidades_tiempo == 1:
            un_tiempo = "semanas"
        if self.unidades_tiempo == 2:
            un_tiempo = "meses"
        if self.unidades_tiempo == 3:
            un_tiempo = "años"
        if self.unidades_distancia == 1:
            un_distancia = "cm"
        un_kc = str(un_distancia) + "/RAIZ(" + str(un_tiempo) + ")"
        d = {'title': title, 'date': date, 'distancias': '\n'.join(distancias), 'distancia_media': distancia_media,
             "n": n, "pmax": pmax, "tiempo": tiempo, "un_tiempo": un_tiempo, "caras": caras, "Kc": kc, "un_kc": un_kc}
        result = src.substitute(d)

        name, _ = QFileDialog.getSaveFileName(None, 'Save file', "", "Text Files (*.txt)")
        filename = QFileInfo(name).fileName()
        if filename:
            file = open(name, 'w')
            text = result
            file.write(text)
            file.close()

    def borrar_punto(self):
        selected = self.tabla.currentRow()
        print(selected)
        if selected != -1 and self.tabla.selectedItems():
            if self.cb_caras.currentIndex() == 0:
                self.lista = self.graphicsView.elipses_cara_1
                self.puntos = self.graphicsView.puntos_1
            if self.cb_caras.currentIndex() == 1:
                self.lista = self.graphicsView.elipses_cara_2
                self.puntos = self.graphicsView.puntos_2
            if self.cb_caras.currentIndex() == 2:
                self.lista = self.graphicsView.elipses_cara_3
                self.puntos = self.graphicsView.puntos_3
            if self.cb_caras.currentIndex() == 3:
                self.lista = self.graphicsView.elipses_cara_4
                self.puntos = self.graphicsView.puntos_4

            self.graphicsView.scene.removeItem(self.lista[selected])  # funciona
            # self.graphicsView.scene.removeItem(self.puntos[selected])
            """
            aquí está el fallo. probar algo del estilo removeitemat
            """
            # x = self.puntos[selected][0]
            # y = self.puntos[selected][1]
            # self.item = self.graphicsView.scene.itemAt(x, y)
            # self.graphicsView.scene.removeItem(self.item)

            del self.lista[selected]
            del self.puntos[selected]
            self.tabla.removeRow(selected)
            print("borrar punto")
            print(self.puntos)
        if self.label_puntos:
            self.label.deleteLater()
            self.label_puntos = False

    def anim_start(self):
        if self.label_puntos:
            self.label.deleteLater()

        selected = self.tabla.currentRow()
        if self.cb_caras.currentIndex() == 0:
            self.puntos = self.graphicsView.puntos_1
        if self.cb_caras.currentIndex() == 1:
            self.puntos = self.graphicsView.puntos_2
        if self.cb_caras.currentIndex() == 2:
            self.puntos = self.graphicsView.puntos_3
        if self.cb_caras.currentIndex() == 3:
            self.puntos = self.graphicsView.puntos_4

        x = str(int(self.puntos[selected].x()))
        y = str(int(self.puntos[selected].y()))
        coordenadas = x + ', ' + y

        self.label = MyLabel(coordenadas)
        font = self.label.font()
        font.setPointSize(self.graphicsView.grosor_puntos)
        self.label.setFont(font)
        self.graphicsView.scene.addWidget(self.label)
        self.label.move(self.puntos[selected].x(), self.puntos[selected].y())

        self.anim = QPropertyAnimation(self.label, b"color")
        self.anim.setDuration(2500)
        self.anim.setLoopCount(2)
        self.anim.setStartValue(QColor(0, 0, 0))
        self.anim.setEndValue(QColor(255, 255, 255))
        self.anim.start()
        self.label_puntos = True

    def limpiar(self):
        if self.label_puntos:
            self.label.deleteLater()
            self.label_puntos = False
        else:
            pass

    def borrar_puntos_lista_cara(self):
        if self.cb_caras.currentIndex() == 0:
            self.lista_e = self.graphicsView.elipses_cara_1
            self.lista_p = self.graphicsView.puntos_1
        if self.cb_caras.currentIndex() == 1:
            self.lista_e = self.graphicsView.elipses_cara_2
            self.lista_p = self.graphicsView.puntos_2
        if self.cb_caras.currentIndex() == 2:
            self.lista_e = self.graphicsView.elipses_cara_3
            self.lista_p = self.graphicsView.puntos_3
        if self.cb_caras.currentIndex() == 3:
            self.lista_e = self.graphicsView.elipses_cara_4
            self.lista_p = self.graphicsView.puntos_4
        for n in self.lista_e:
            self.graphicsView.scene.removeItem(n)
            self.lista_e.clear()
            self.lista_p.clear()
        print(self.lista_e, self.lista_p)
        self.calcular()
        # self.llenar_tabla2()

    def set_color(self):
        if self.graphicsView.color_escala == 0:
            self.graphicsView.pen_escala.setColor(Qt.green)
        elif self.graphicsView.color_escala == 1:
            self.graphicsView.pen_escala.setColor(Qt.red)
        elif self.graphicsView.color_escala == 2:
            self.graphicsView.pen_escala.setColor(Qt.blue)
        elif self.graphicsView.color_escala == 3:
            self.graphicsView.pen_escala.setColor(Qt.yellow)
        elif self.graphicsView.color_escala == 4:
            self.graphicsView.pen_escala.setColor(Qt.black)
        elif self.graphicsView.color_escala == 5:
            self.graphicsView.pen_escala.setColor(Qt.white)

        if self.graphicsView.color_linea == 0:
            self.graphicsView.pen_linea.setColor(Qt.red)
        elif self.graphicsView.color_linea == 1:
            self.graphicsView.pen_linea.setColor(Qt.green)
        elif self.graphicsView.color_linea == 2:
            self.graphicsView.pen_linea.setColor(Qt.blue)
        elif self.graphicsView.color_linea == 3:
            self.graphicsView.pen_linea.setColor(Qt.yellow)
        elif self.graphicsView.color_linea == 4:
            self.graphicsView.pen_linea.setColor(Qt.black)
        elif self.graphicsView.color_linea == 5:
            self.graphicsView.pen_linea.setColor(Qt.white)

        if self.graphicsView.color_puntos == 0:
            self.graphicsView.pen_punto.setColor(Qt.red)
            self.graphicsView.brush.setColor(Qt.red)
        elif self.graphicsView.color_puntos == 1:
            self.graphicsView.pen_punto.setColor(Qt.green)
            self.graphicsView.brush.setColor(Qt.green)
        elif self.graphicsView.color_puntos == 2:
            self.graphicsView.pen_punto.setColor(Qt.blue)
            self.graphicsView.brush.setColor(Qt.blue)
        elif self.graphicsView.color_puntos == 3:
            self.graphicsView.pen_punto.setColor(Qt.yellow)
            self.graphicsView.brush.setColor(Qt.yellow)
        elif self.graphicsView.color_puntos == 4:
            self.graphicsView.pen_punto.setColor(Qt.black)
            self.graphicsView.brush.setColor(Qt.black)
        elif self.graphicsView.color_puntos == 5:
            self.graphicsView.pen_punto.setColor(Qt.white)
            self.graphicsView.brush.setColor(Qt.white)

    def repintar_puntos(self):
        """
        primero: eliminar todos los puntos de la escena
        segundo: repintar todos los puntos en la escena
        """
        newpos = 0.5 * self.graphicsView.grosor_puntos

        for n in self.graphicsView.elipses_cara_1:
            self.graphicsView.scene.removeItem(n)
        self.graphicsView.elipses_cara_1.clear()
        for m in self.graphicsView.puntos_1:
            self.elipse = QGraphicsEllipseItem()
            self.elipse.setRect(m.x() - newpos, m.y() - newpos, self.graphicsView.grosor_puntos,
                                self.graphicsView.grosor_puntos)
            self.elipse.setPen(self.graphicsView.pen_punto)
            self.elipse.setBrush(self.graphicsView.brush)
            self.graphicsView.scene.addItem(self.elipse)
            self.graphicsView.elipses_cara_1.append(self.elipse)
        for n2 in self.graphicsView.elipses_cara_2:
            self.graphicsView.scene.removeItem(n2)
        self.graphicsView.elipses_cara_2.clear()
        for m2 in self.graphicsView.puntos_2:
            self.elipse = QGraphicsEllipseItem()
            self.elipse.setRect(m2.x() - newpos, m2.y() - newpos, self.graphicsView.grosor_puntos,
                                self.graphicsView.grosor_puntos)
            self.elipse.setPen(self.graphicsView.pen_punto)
            self.elipse.setBrush(self.graphicsView.brush)
            self.graphicsView.scene.addItem(self.elipse)
            self.graphicsView.elipses_cara_2.append(self.elipse)
        for n3 in self.graphicsView.elipses_cara_3:
            self.graphicsView.scene.removeItem(n3)
        self.graphicsView.elipses_cara_3.clear()
        for m3 in self.graphicsView.puntos_3:
            self.elipse = QGraphicsEllipseItem()
            self.elipse.setRect(m3.x() - newpos, m3.y() - newpos, self.graphicsView.grosor_puntos,
                                self.graphicsView.grosor_puntos)
            self.elipse.setPen(self.graphicsView.pen_punto)
            self.elipse.setBrush(self.graphicsView.brush)
            self.graphicsView.scene.addItem(self.elipse)
            self.graphicsView.elipses_cara_3.append(self.elipse)
        for n4 in self.graphicsView.elipses_cara_4:
            self.graphicsView.scene.removeItem(n4)
        self.graphicsView.elipses_cara_4.clear()
        for m4 in self.graphicsView.puntos_4:
            self.elipse = QGraphicsEllipseItem()
            self.elipse.setRect(m4.x() - newpos, m4.y() - newpos, self.graphicsView.grosor_puntos,
                                self.graphicsView.grosor_puntos)
            self.elipse.setPen(self.graphicsView.pen_punto)
            self.elipse.setBrush(self.graphicsView.brush)
            self.graphicsView.scene.addItem(self.elipse)
            self.graphicsView.elipses_cara_4.append(self.elipse)

        self.calcular()

    def repintar_escala(self):
        """
        pongo el try-except porque si no he dibujado previamente la escala, crashea al aceptar las preferencias
        """
        try:
            # if self.graphicsView.laescala:
            self.set_color()

            self.escala_nueva = self.graphicsView.laescala
            self.graphicsView.scene.removeItem(self.graphicsView.laescala)
            self.graphicsView.pen_escala.setWidth(self.graphicsView.grosor_escala)
            self.escala_nueva.setPen(self.graphicsView.pen_escala)
            self.graphicsView.scene.addItem(self.escala_nueva)
            self.graphicsView.laescala = self.escala_nueva
            print(self.graphicsView.laescala)
            print(self.escala_nueva)
        except:
            pass

    def repintar_linea(self):
        try:
            self.set_color()

            self.linea_nueva = self.graphicsView.lalinea
            self.graphicsView.scene.removeItem(self.graphicsView.lalinea)
            self.graphicsView.pen_linea.setWidth(self.graphicsView.grosor_linea)
            self.linea_nueva.setPen(self.graphicsView.pen_linea)
            self.graphicsView.scene.addItem(self.linea_nueva)
            self.graphicsView.lalinea = self.linea_nueva
        except:
            pass

    def check(self):
        """
        Funición para comprobar el número de caras, de distancias reales tengo
        """
        self.cuenta = 0
        if self.graphicsView.distanciasreales_1:
            # self.distancias_cara_1 = True
            self.cuenta += 1
        if self.graphicsView.distanciasreales_2:
            # self.distancias_cara_2 = True
            self.cuenta += 1
        if self.graphicsView.distanciasreales_3:
            # self.distancias_cara_3 = True
            self.cuenta += 1
        if self.graphicsView.distanciasreales_4:
            # self.distancias_cara_4 = True
            self.cuenta += 1
        else:
            print("chekeado")
            pass
        return self.cuenta

    def prueba (self):
        print(self.cuenta)

    def actualizar_kc(self):
        self.coeficiente = self.dlg_kc.resultado
        self.unidades_tiempo = self.dlg_kc.unidades_tiempo
        self.unidades_distancia = self.dlg_kc.unidades_distancia


class MyLabel(QtWidgets.QLabel):

    def __init__(self, text):
        super().__init__(text)

    def _set_color(self, col):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        # palette.setColor(self.foregroundRole(), None)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)


class pref(QtWidgets.QDialog, Ui_Preferencias):
    senyal_cambios_preferencias = pyqtSignal()

    def __init__(self):
        super(pref, self).__init__()
        self.setupUi(self)

        self.numescala_previo = 1
        self.numlinea_previo = 1
        self.numpunto_previo = 1

        self.colorescala_previo = 0
        self.colorlinea_previo = 0
        self.colorpuntos_previo = 0
        self.colorbrush_previo = 0

        self.pb_aceptar.clicked.connect(self.actualizar)
        self.pb_cancelar.clicked.connect(self.cancelar_preferencias)

        self.cb_color_escala.addItems(["verde", "rojo", "azul", "amarillo", "negro", "blanco"])
        self.cb_color_base.addItems(["rojo", "verde", "azul", "amarillo", "negro", "blanco"])
        self.cb_color_puntos.addItems(["rojo", "verde", "azul", "amarillo", "negro", "blanco"])

    def actualizar(self):
        self.numescala = self.sb_grosor_escala.value()
        self.numlinea = self.sb_grosor_base.value()
        self.numpunto = self.sb_grosor_puntos.value()

        self.numescala_previo = self.sb_grosor_escala.value()
        self.numlinea_previo = self.sb_grosor_base.value()
        self.numpunto_previo = self.sb_grosor_puntos.value()

        self.colorescala = self.cb_color_escala.currentIndex()
        self.colorlinea = self.cb_color_base.currentIndex()
        self.colorpuntos = self.cb_color_puntos.currentIndex()
        self.colorbrush = self.cb_color_puntos.currentIndex()

        self.colorescala_previo = self.cb_color_escala.currentIndex()
        self.colorlinea_previo = self.cb_color_base.currentIndex()
        self.colorpuntos_previo = self.cb_color_puntos.currentIndex()
        self.colorbrush_previo = self.cb_color_puntos.currentIndex()

        self.senyal_cambios_preferencias.emit()
        pref.close(self)

    def cancelar_preferencias(self):
        self.sb_grosor_escala.setValue(self.numescala_previo)
        self.sb_grosor_base.setValue(self.numlinea_previo)
        self.sb_grosor_puntos.setValue(self.numpunto_previo)

        self.cb_color_escala.setCurrentIndex(self.colorescala_previo)
        self.cb_color_base.setCurrentIndex(self.colorlinea_previo)
        self.cb_color_puntos.setCurrentIndex(self.colorpuntos_previo)

        pref.close(self)


class Calc_coef(QtWidgets.QDialog, Ui_Dialog):
    senyal_kc = pyqtSignal()

    def __init__(self, lista1, lista2, lista3, lista4, parent = None):
        super(Calc_coef, self).__init__()
        self.setupUi(self)
        self.resultado = None
        self.unidades_tiempo = None
        self.unidades_distancia = None

        self.cb_unidades_distancia.addItems(["milímetros (mm)", "centímetros (cm)"])
        self.cb_unidades_tiempo.addItems(["días", "semanas", "meses", "años"])

        self.lista1 = lista1
        self.lista2 = lista2
        self.lista3 = lista3
        self.lista4 = lista4

        self.cBox_1.stateChanged.connect(self.calculo_Kc)
        self.cBox_2.stateChanged.connect(self.calculo_Kc)
        self.cBox_3.stateChanged.connect(self.calculo_Kc)
        self.cBox_4.stateChanged.connect(self.calculo_Kc)

        self.kc1 = None
        self.kc2 = None
        self.kc3 = None
        self.kc4 = None
        self.kc12 = None
        self.kc13 = None
        self.kc14 = None
        self.kc23 = None
        self.kc24 = None
        self.kc34 = None
        self.kc123 = None
        self.kc124 = None
        self.kc134 = None
        self.kc234 = None
        self.kc1234 = None

        self.pb_guardar.clicked.connect(self.guardar)
        self.pb_calcular.clicked.connect(self.calcular)

    def media(self, lista):
        media = 0
        for n in lista:
            media = media + n
        try:
            self.lamedia = media/len(lista)
        except:
            self.lamedia = 0
        return self.lamedia

    def is_number(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False


    def calculo_Kc(self):
        """
        Kc = d/RAIZ(t)
        """
        self.media1 = self.media(self.lista1)
        self.media2 = self.media(self.lista2)
        self.media3 = self.media(self.lista3)
        self.media4 = self.media(self.lista4)

        self.media1_2 = self.media(self.lista1 + self.lista2)
        self.media1_3 = self.media(self.lista1 + self.lista3)
        self.media1_4 = self.media(self.lista1 + self.lista4)

        self.media2_3 = self.media(self.lista2 + self.lista3)
        self.media2_4 = self.media(self.lista2 + self.lista4)

        self.media3_4 = self.media(self.lista3 + self.lista4)

        self.media1_2_3 = self.media(self.lista1 + self.lista2 + self.lista3)
        self.media1_2_4 = self.media(self.lista1 + self.lista2 + self.lista4)
        self.media1_3_4 = self.media(self.lista1 + self.lista3 + self.lista4)
        self.media2_3_4 = self.media(self.lista2 + self.lista3 + self.lista4)

        self.media1_2_3_4 = self.media(self.lista1 + self.lista2 + self.lista3 + self.lista4)

        if self.le_tiempo.text() == "":
            self.lb_resultado.setText("Introducir el valor de tiempo")

        self.text = self.le_tiempo.text()

        if self.is_number(self.text):
            self.raiz = float(self.text)**0.5
            print(self.raiz)
            self.kc1 = self.media1/self.raiz
            self.kc2 = self.media2/self.raiz
            self.kc3 = self.media3/self.raiz
            self.kc4 = self.media4/self.raiz
            self.kc12 = self.media1_2/self.raiz
            self.kc13 = self.media1_3/self.raiz
            self.kc14 = self.media1_4/self.raiz
            self.kc23 = self.media2_3/self.raiz
            self.kc24 = self.media2_4/self.raiz
            self.kc34 = self.media3_4/self.raiz
            self.kc123 = self.media1_2_3/self.raiz
            self.kc124 = self.media1_2_4/self.raiz
            self.kc134 = self.media1_3_4/self.raiz
            self.kc234 = self.media2_3_4/self.raiz
            self.kc1234 = self.media1_2_3_4/self.raiz

        self.mostrar_resultado()

    def mostrar_resultado(self):
        if self.is_number(self.text):
            print("si tengo valor de tiempo")

            if self.cBox_1.isChecked():
                self.lb_resultado.setText(str(self.kc1))
            if self.cBox_2.isChecked():
                self.lb_resultado.setText(str(self.kc2))
            if self.cBox_3.isChecked():
                self.lb_resultado.setText(str(self.kc3))
            if self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc4))

            if self.cBox_1.isChecked() and self.cBox_2.isChecked():
                self.lb_resultado.setText(str(self.kc12))
            if self.cBox_1.isChecked() and self.cBox_3.isChecked():
                self.lb_resultado.setText(str(self.kc13))
            if self.cBox_1.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc14))
            if self.cBox_2.isChecked() and self.cBox_3.isChecked():
                self.lb_resultado.setText(str(self.kc23))
            if self.cBox_2.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc24))
            if self.cBox_3.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc34))

            if self.cBox_1.isChecked() and self.cBox_2.isChecked() and self.cBox_3.isChecked():
                self.lb_resultado.setText(str(self.kc123))
            if self.cBox_1.isChecked() and self.cBox_2.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc124))
            if self.cBox_1.isChecked() and self.cBox_3.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc134))
            if self.cBox_2.isChecked() and self.cBox_3.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc234))

            if self.cBox_1.isChecked() and self.cBox_2.isChecked() and self.cBox_3.isChecked() and self.cBox_4.isChecked():
                self.lb_resultado.setText(str(self.kc1234))
        else:
            print("falta el tiempo")

        # self.tiempo = self.le_tiempo.text()
        # print("el tiempo es " + self.tiempo)

        # print(self.kc1)

    def calcular(self):
        self.calculo_Kc()
        print("botón calcular presionado")

    def guardar(self):
        self.calculo_Kc()
        self.resultado = self.lb_resultado.text()
        self.unidades_tiempo = self.cb_unidades_tiempo.currentIndex()
        self.unidades_distancia = self.cb_unidades_distancia.currentIndex()
        print("botón Guardar pulsado")
        print(self.unidades_distancia)
        self.senyal_kc.emit()
        Calc_coef.close(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = mainProgram()
    window.show()

    sys.exit(app.exec_())
