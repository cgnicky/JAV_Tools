# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jav_classifier.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("JAV Classifier")
        MainWindow.resize(573, 226)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.srcPath = QtWidgets.QLabel(self.centralwidget)
        self.srcPath.setGeometry(QtCore.QRect(70, 20, 101, 17))
        self.srcPath.setObjectName("srcPath")
        self.execBtn = QtWidgets.QPushButton(self.centralwidget)
        self.execBtn.setGeometry(QtCore.QRect(460, 120, 89, 25))
        self.execBtn.setObjectName("execBtn")
        self.msgBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.msgBox.setGeometry(QtCore.QRect(70, 90, 361, 121))
        self.msgBox.setObjectName("msgBox")
        self.srcEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.srcEdit.setGeometry(QtCore.QRect(190, 20, 241, 21))
        self.srcEdit.setObjectName("srcEdit")
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearBtn.setGeometry(QtCore.QRect(460, 160, 89, 25))
        self.clearBtn.setObjectName("clearBtn")
        self.msgOutput = QtWidgets.QLabel(self.centralwidget)
        self.msgOutput.setGeometry(QtCore.QRect(70, 70, 121, 17))
        self.msgOutput.setObjectName("msgOutput")
        self.browseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browseBtn.setGeometry(QtCore.QRect(460, 20, 89, 25))
        self.browseBtn.setObjectName("browseBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("JAV Classifier", "JAV Classifier"))
        self.srcPath.setText(_translate("JAV Classifier", "Search Source"))
        self.execBtn.setText(_translate("JAV Classifier", "Execute"))
        self.clearBtn.setText(_translate("JAV Classifier", "Clear"))
        self.msgOutput.setText(_translate("JAV Classifier", "Message Output"))
        self.browseBtn.setText(_translate("JAV Classifier", "Browse"))

