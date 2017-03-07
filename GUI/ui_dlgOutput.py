# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgOutput.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_dlgOut(object):
    def setupUi(self, dlgOut):
        dlgOut.setObjectName(_fromUtf8("dlgOut"))
        dlgOut.resize(708, 370)
        self.verticalLayout = QtGui.QVBoxLayout(dlgOut)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(dlgOut)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.wid_lbl_fname = QtGui.QLabel(dlgOut)
        self.wid_lbl_fname.setText(_fromUtf8(""))
        self.wid_lbl_fname.setObjectName(_fromUtf8("wid_lbl_fname"))
        self.horizontalLayout.addWidget(self.wid_lbl_fname)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(dlgOut)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.wid_le_saveas = QtGui.QLineEdit(dlgOut)
        self.wid_le_saveas.setObjectName(_fromUtf8("wid_le_saveas"))
        self.horizontalLayout_2.addWidget(self.wid_le_saveas)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.plainTextEdit = QtGui.QPlainTextEdit(dlgOut)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);"))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.cmdSave = QtGui.QPushButton(dlgOut)
        self.cmdSave.setObjectName(_fromUtf8("cmdSave"))
        self.verticalLayout.addWidget(self.cmdSave)
        self.pushButton = QtGui.QPushButton(dlgOut)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(dlgOut)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), dlgOut.close)
        QtCore.QMetaObject.connectSlotsByName(dlgOut)

    def retranslateUi(self, dlgOut):
        dlgOut.setWindowTitle(_translate("dlgOut", "Dialog", None))
        self.label_2.setText(_translate("dlgOut", "<html><head/><body><p><span style=\" font-weight:600;\">Opened File </span>: </p></body></html>", None))
        self.label_3.setText(_translate("dlgOut", "<html><head/><body><p align=\"right\"><span style=\" font-weight:600;\">Save As </span>: </p></body></html>", None))
        self.cmdSave.setText(_translate("dlgOut", "Save", None))
        self.pushButton.setText(_translate("dlgOut", "Quit", None))

