# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proxy.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Proxy(object):
    def setupUi(self, Dialog_Proxy):
        Dialog_Proxy.setObjectName("Dialog_Proxy")
        Dialog_Proxy.resize(488, 140)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Proxy)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_protocol = QtWidgets.QComboBox(Dialog_Proxy)
        self.comboBox_protocol.setObjectName("comboBox_protocol")
        self.comboBox_protocol.addItem("")
        self.comboBox_protocol.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_protocol)
        self.lineEdit_ip = QtWidgets.QLineEdit(Dialog_Proxy)
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.horizontalLayout.addWidget(self.lineEdit_ip)
        self.label = QtWidgets.QLabel(Dialog_Proxy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_port = QtWidgets.QLineEdit(Dialog_Proxy)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout.addWidget(self.lineEdit_port)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_Proxy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_Proxy)
        self.buttonBox.accepted.connect(Dialog_Proxy.accept)
        self.buttonBox.rejected.connect(Dialog_Proxy.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Proxy)

    def retranslateUi(self, Dialog_Proxy):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Proxy.setWindowTitle(_translate("Dialog_Proxy", "代理设置"))
        self.comboBox_protocol.setItemText(0, _translate("Dialog_Proxy", "http://"))
        self.comboBox_protocol.setItemText(1, _translate("Dialog_Proxy", "socks5://"))
        self.lineEdit_ip.setPlaceholderText(_translate("Dialog_Proxy", "代理IP"))
        self.label.setText(_translate("Dialog_Proxy", ":"))
        self.lineEdit_port.setPlaceholderText(_translate("Dialog_Proxy", "代理端口"))