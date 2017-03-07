# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
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

class Ui_frmSettings(object):
    def setupUi(self, frmSettings):
        frmSettings.setObjectName(_fromUtf8("frmSettings"))
        frmSettings.resize(664, 144)
        self.verticalLayout = QtGui.QVBoxLayout(frmSettings)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(frmSettings)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.wid_le_sflow = QtGui.QLineEdit(frmSettings)
        self.wid_le_sflow.setObjectName(_fromUtf8("wid_le_sflow"))
        self.horizontalLayout.addWidget(self.wid_le_sflow)
        self.cmd_sflow = QtGui.QPushButton(frmSettings)
        self.cmd_sflow.setObjectName(_fromUtf8("cmd_sflow"))
        self.horizontalLayout.addWidget(self.cmd_sflow)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(frmSettings)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.wid_le_db = QtGui.QLineEdit(frmSettings)
        self.wid_le_db.setObjectName(_fromUtf8("wid_le_db"))
        self.horizontalLayout_2.addWidget(self.wid_le_db)
        self.cmd_db = QtGui.QPushButton(frmSettings)
        self.cmd_db.setObjectName(_fromUtf8("cmd_db"))
        self.horizontalLayout_2.addWidget(self.cmd_db)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.cmdOk = QtGui.QPushButton(frmSettings)
        self.cmdOk.setObjectName(_fromUtf8("cmdOk"))
        self.verticalLayout.addWidget(self.cmdOk)

        self.retranslateUi(frmSettings)
        QtCore.QMetaObject.connectSlotsByName(frmSettings)

    def retranslateUi(self, frmSettings):
        frmSettings.setWindowTitle(_translate("frmSettings", "Settings", None))
        self.label.setText(_translate("frmSettings", "Ship Flow bat file", None))
        self.cmd_sflow.setText(_translate("frmSettings", "Set file", None))
        self.label_2.setText(_translate("frmSettings", "Database folder", None))
        self.cmd_db.setText(_translate("frmSettings", "set folder", None))
        self.cmdOk.setText(_translate("frmSettings", "&Ok", None))

