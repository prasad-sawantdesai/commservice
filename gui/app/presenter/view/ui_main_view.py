# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(504, 457)
        self.actionOpen_Database = QAction(MainWindow)
        self.actionOpen_Database.setObjectName(u"actionOpen_Database")
        self.actionClose_Database = QAction(MainWindow)
        self.actionClose_Database.setObjectName(u"actionClose_Database")
        self.actionSave_Database = QAction(MainWindow)
        self.actionSave_Database.setObjectName(u"actionSave_Database")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionPLC_Configuration = QAction(MainWindow)
        self.actionPLC_Configuration.setObjectName(u"actionPLC_Configuration")
        self.actionMachine_Configuration = QAction(MainWindow)
        self.actionMachine_Configuration.setObjectName(u"actionMachine_Configuration")
        self.actionTag_Configuration = QAction(MainWindow)
        self.actionTag_Configuration.setObjectName(u"actionTag_Configuration")
        self.actionTag_Collection = QAction(MainWindow)
        self.actionTag_Collection.setObjectName(u"actionTag_Collection")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 504, 18))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuConfig = QMenu(self.menubar)
        self.menuConfig.setObjectName(u"menuConfig")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Database)
        self.menuFile.addAction(self.actionClose_Database)
        self.menuFile.addAction(self.actionSave_Database)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuConfig.addAction(self.actionPLC_Configuration)
        self.menuConfig.addAction(self.actionMachine_Configuration)
        self.menuConfig.addAction(self.actionTag_Configuration)
        self.menuConfig.addAction(self.actionTag_Collection)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Configurator", None))
        self.actionOpen_Database.setText(QCoreApplication.translate("MainWindow", u"Open Database", None))
        self.actionClose_Database.setText(QCoreApplication.translate("MainWindow", u"Close Database", None))
        self.actionSave_Database.setText(QCoreApplication.translate("MainWindow", u"Save Database", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionPLC_Configuration.setText(QCoreApplication.translate("MainWindow", u"PLC Configuration", None))
        self.actionMachine_Configuration.setText(QCoreApplication.translate("MainWindow", u"Machine Configuration", None))
        self.actionTag_Configuration.setText(QCoreApplication.translate("MainWindow", u"Tag Configuration", None))
        self.actionTag_Collection.setText(QCoreApplication.translate("MainWindow", u"Tag Collection", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuConfig.setTitle(QCoreApplication.translate("MainWindow", u"Config", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

