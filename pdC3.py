# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pdC3.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Preferencias(object):
    def setupUi(self, Preferencias):
        Preferencias.setObjectName("Preferencias")
        Preferencias.resize(376, 520)
        self.gridLayout_7 = QtWidgets.QGridLayout(Preferencias)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_7 = QtWidgets.QFrame(Preferencias)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.frame_8 = QtWidgets.QFrame(self.frame_7)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_aceptar = QtWidgets.QPushButton(self.frame_8)
        self.pb_aceptar.setObjectName("pb_aceptar")
        self.horizontalLayout.addWidget(self.pb_aceptar)
        self.pb_cancelar = QtWidgets.QPushButton(self.frame_8)
        self.pb_cancelar.setObjectName("pb_cancelar")
        self.horizontalLayout.addWidget(self.pb_cancelar)
        self.gridLayout_8.addWidget(self.frame_8, 4, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.frame_2.setFont(font)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lb_Puntos = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_Puntos.setFont(font)
        self.lb_Puntos.setObjectName("lb_Puntos")
        self.gridLayout_2.addWidget(self.lb_Puntos, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.sb_grosor_puntos = QtWidgets.QSpinBox(self.frame)
        self.sb_grosor_puntos.setMinimum(1)
        self.sb_grosor_puntos.setProperty("value", 1)
        self.sb_grosor_puntos.setObjectName("sb_grosor_puntos")
        self.gridLayout.addWidget(self.sb_grosor_puntos, 1, 1, 1, 1)
        self.cb_color_puntos = QtWidgets.QComboBox(self.frame)
        self.cb_color_puntos.setObjectName("cb_color_puntos")
        self.gridLayout.addWidget(self.cb_color_puntos, 2, 1, 1, 1)
        self.lb_color_puntos = QtWidgets.QLabel(self.frame)
        self.lb_color_puntos.setObjectName("lb_color_puntos")
        self.gridLayout.addWidget(self.lb_color_puntos, 2, 0, 1, 1)
        self.lb_grosor_puntos = QtWidgets.QLabel(self.frame)
        self.lb_grosor_puntos.setObjectName("lb_grosor_puntos")
        self.gridLayout.addWidget(self.lb_grosor_puntos, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.gridLayout_8.addWidget(self.frame_2, 3, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame_7)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lb_Lineaescala = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_Lineaescala.setFont(font)
        self.lb_Lineaescala.setObjectName("lb_Lineaescala")
        self.gridLayout_3.addWidget(self.lb_Lineaescala, 0, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lb_color_escala = QtWidgets.QLabel(self.frame_4)
        self.lb_color_escala.setObjectName("lb_color_escala")
        self.gridLayout_4.addWidget(self.lb_color_escala, 2, 0, 1, 1)
        self.cb_color_escala = QtWidgets.QComboBox(self.frame_4)
        self.cb_color_escala.setObjectName("cb_color_escala")
        self.gridLayout_4.addWidget(self.cb_color_escala, 2, 1, 1, 1)
        self.sb_grosor_escala = QtWidgets.QSpinBox(self.frame_4)
        self.sb_grosor_escala.setMinimum(1)
        self.sb_grosor_escala.setProperty("value", 1)
        self.sb_grosor_escala.setObjectName("sb_grosor_escala")
        self.gridLayout_4.addWidget(self.sb_grosor_escala, 1, 1, 1, 1)
        self.lb_grosor_escala = QtWidgets.QLabel(self.frame_4)
        self.lb_grosor_escala.setObjectName("lb_grosor_escala")
        self.gridLayout_4.addWidget(self.lb_grosor_escala, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_4, 1, 0, 1, 1)
        self.gridLayout_8.addWidget(self.frame_3, 1, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame_7)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_6 = QtWidgets.QFrame(self.frame_5)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.lb_color_base = QtWidgets.QLabel(self.frame_6)
        self.lb_color_base.setObjectName("lb_color_base")
        self.gridLayout_6.addWidget(self.lb_color_base, 2, 0, 1, 1)
        self.cb_color_base = QtWidgets.QComboBox(self.frame_6)
        self.cb_color_base.setObjectName("cb_color_base")
        self.gridLayout_6.addWidget(self.cb_color_base, 2, 1, 1, 1)
        self.sb_grosor_base = QtWidgets.QSpinBox(self.frame_6)
        self.sb_grosor_base.setMinimum(1)
        self.sb_grosor_base.setProperty("value", 1)
        self.sb_grosor_base.setObjectName("sb_grosor_base")
        self.gridLayout_6.addWidget(self.sb_grosor_base, 1, 1, 1, 1)
        self.lb_grosor_base = QtWidgets.QLabel(self.frame_6)
        self.lb_grosor_base.setObjectName("lb_grosor_base")
        self.gridLayout_6.addWidget(self.lb_grosor_base, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_6, 1, 0, 1, 1)
        self.lb_Lineabase = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_Lineabase.setFont(font)
        self.lb_Lineabase.setObjectName("lb_Lineabase")
        self.gridLayout_5.addWidget(self.lb_Lineabase, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.frame_5, 2, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frame_7, 0, 0, 1, 1)

        self.retranslateUi(Preferencias)
        QtCore.QMetaObject.connectSlotsByName(Preferencias)

    def retranslateUi(self, Preferencias):
        _translate = QtCore.QCoreApplication.translate
        Preferencias.setWindowTitle(_translate("Preferencias", "Dialog"))
        self.pb_aceptar.setText(_translate("Preferencias", "Aceptar"))
        self.pb_cancelar.setText(_translate("Preferencias", "Cancelar"))
        self.lb_Puntos.setText(_translate("Preferencias", "Puntos"))
        self.lb_color_puntos.setText(_translate("Preferencias", "color"))
        self.lb_grosor_puntos.setText(_translate("Preferencias", "grosor"))
        self.lb_Lineaescala.setText(_translate("Preferencias", "Escala"))
        self.lb_color_escala.setText(_translate("Preferencias", "color"))
        self.lb_grosor_escala.setText(_translate("Preferencias", "grosor"))
        self.lb_color_base.setText(_translate("Preferencias", "color"))
        self.lb_grosor_base.setText(_translate("Preferencias", "grosor"))
        self.lb_Lineabase.setText(_translate("Preferencias", "Línea"))
