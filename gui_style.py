# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jav_classifier.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(525, 246)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.srcPath = QtWidgets.QLabel(self.centralwidget)
        self.srcPath.setGeometry(QtCore.QRect(20, 20, 101, 17))
        self.srcPath.setObjectName("srcPath")
        self.execBtn = QtWidgets.QPushButton(self.centralwidget)
        self.execBtn.setGeometry(QtCore.QRect(410, 150, 89, 25))
        self.execBtn.setObjectName("execBtn")
        self.msgBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.msgBox.setGeometry(QtCore.QRect(20, 120, 361, 121))
        self.msgBox.setObjectName("msgBox")
        self.srcEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.srcEdit.setGeometry(QtCore.QRect(110, 20, 271, 21))
        self.srcEdit.setObjectName("srcEdit")
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearBtn.setGeometry(QtCore.QRect(410, 190, 89, 25))
        self.clearBtn.setObjectName("clearBtn")
        self.msgOutput = QtWidgets.QLabel(self.centralwidget)
        self.msgOutput.setGeometry(QtCore.QRect(20, 100, 121, 17))
        self.msgOutput.setObjectName("msgOutput")
        self.browseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browseBtn.setGeometry(QtCore.QRect(410, 20, 89, 25))
        self.browseBtn.setObjectName("browseBtn")
        self.actorRb = QtWidgets.QRadioButton(self.centralwidget)
        self.actorRb.setGeometry(QtCore.QRect(20, 60, 112, 23))
        self.actorRb.setChecked(True)
        self.actorRb.setObjectName("actorRb")
        self.labelRb = QtWidgets.QRadioButton(self.centralwidget)
        self.labelRb.setGeometry(QtCore.QRect(100, 60, 112, 23))
        self.labelRb.setObjectName("labelRb")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionCategory_Type = QtWidgets.QAction(MainWindow)
        self.actionCategory_Type.setObjectName("actionCategory_Type")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.srcPath.setText(_translate("MainWindow", "Source Path"))
        self.execBtn.setText(_translate("MainWindow", "Execute"))
        self.clearBtn.setText(_translate("MainWindow", "Clear"))
        self.msgOutput.setText(_translate("MainWindow", "Message Output"))
        self.browseBtn.setText(_translate("MainWindow", "Browse"))
        self.actorRb.setText(_translate("MainWindow", "Actor"))
        self.labelRb.setText(_translate("MainWindow", "Label"))
        self.actionCategory_Type.setText(_translate("MainWindow", "Category Type"))
