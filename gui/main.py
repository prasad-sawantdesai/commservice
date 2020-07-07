import sys
import time

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QSplashScreen

from app.presenter.view.frm_add_machine import FrmAddMachine
from app.presenter.view.frm_add_modbusrtu_connection import FrmAddModbusRtuConnection
from app.presenter.view.frm_add_modbustcp_connection import FrmAddModbusTcpConnection
from app.presenter.view.frm_add_register_types import FrmAddRegisterTypes
from app.presenter.view.frm_add_tag_groups import FrmTagGroups
from app.presenter.view.frm_add_tags import FrmAddTags
from app.presenter.view.frm_addcontroller import FrmAddController
from app.utilities.database_management import DatabaseManagement


class MainWindow(QMainWindow):

		def __init__(self):
				super().__init__()

				self.initUI()

		def initUI(self):
				exitAct = QAction(QIcon('exit.png'), '&Exit', self)
				exitAct.setShortcut('Ctrl+Q')
				exitAct.setStatusTip('Exit application')
				exitAct.triggered.connect(QApplication.quit)

				addControllerAct = QAction(QIcon('add.png'), '&Add Controller', self)
				addControllerAct.setShortcut('Ctrl+A')
				addControllerAct.setStatusTip('Add new controller')
				addControllerAct.triggered.connect(self.show_frm_add_controller)

				addMachineAct = QAction(QIcon('add.png'), '&Add Machine', self)
				addMachineAct.setShortcut('Ctrl+M')
				addMachineAct.setStatusTip('Add new machine')
				addMachineAct.triggered.connect(self.show_frm_add_machine)

				addModbusRtuAct = QAction(QIcon('add.png'), '&Add Modbus RTU Connection', self)
				# addModbusRtuAct.setShortcut('Ctrl+M')
				addModbusRtuAct.setStatusTip('Add new Modbus RTU Connection')
				addModbusRtuAct.triggered.connect(self.show_frm_add_modbusrtu_connection)

				addModbusTcpAct = QAction(QIcon('add.png'), '&Add Modbus TCP Connection', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addModbusTcpAct.setStatusTip('Add new Modbus TCP Connection')
				addModbusTcpAct.triggered.connect(self.show_frm_add_modbustcp_connection)

				addRegisterTypesAct = QAction(QIcon('add.png'), '&Add Register types', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addRegisterTypesAct.setStatusTip('Add new Register Types')
				addRegisterTypesAct.triggered.connect(self.show_frm_add_register_types)

				addTagsAct = QAction(QIcon('add.png'), '&Add Tags', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addTagsAct.setStatusTip('Add tags')
				addTagsAct.triggered.connect(self.show_frm_add_tags)

				addTagsAct = QAction(QIcon('add.png'), '&Add Tags', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addTagsAct.setStatusTip('Add tags')
				addTagsAct.triggered.connect(self.show_frm_add_tags)

				addTagGroupsAct = QAction(QIcon('add.png'), '&Add Tag groups', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addTagGroupsAct.setStatusTip('Add tag groups')
				addTagGroupsAct.triggered.connect(self.show_frm_add_tag_groups)
				self.statusBar().showMessage('Ready')

				# self.toolbar = self.addToolBar('Exit')
				# self.toolbar.addAction(exitAct)

				menubar = self.menuBar()
				fileMenu = menubar.addMenu('&File')
				fileMenu.addAction(exitAct)

				configMenu = menubar.addMenu('&Config')
				configMenu.addAction(addControllerAct)
				configMenu.addAction(addMachineAct)
				connectionMenu = configMenu.addMenu('&Connections')
				connectionMenu.addAction(addModbusRtuAct)
				connectionMenu.addAction(addModbusTcpAct)

				configMenu.addAction(addRegisterTypesAct)
				configMenu.addAction(addTagsAct)
				configMenu.addAction(addTagGroupsAct)

				windowMenu = menubar.addMenu('&Window')

				helpMenu = menubar.addMenu('&Help')
				self.showMaximized()
				self.setWindowTitle('X-Box Configurator')
				self.show()

		def show_frm_add_controller(self):
				dialog = FrmAddController()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_machine(self):
				dialog = FrmAddMachine()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_modbusrtu_connection(self):
				dialog = FrmAddModbusRtuConnection()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_modbustcp_connection(self):
				dialog = FrmAddModbusTcpConnection()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_register_types(self):
				dialog = FrmAddRegisterTypes()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_tags(self):
				dialog = FrmAddTags()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_tag_groups(self):
				dialog = FrmTagGroups()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()
def main():
		app = QApplication(sys.argv)
		# for the splash screen
		splash_pix = QtGui.QPixmap(r"resources/splash_screen.png")
		# Creates the splash screen
		splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
		splash.setMask(splash_pix.mask())
		# shows splash screen
		splash.show()
		app.processEvents()
		time.sleep(2)
		obj_db_management = DatabaseManagement(
						r"/home/ujjaini/prasad/commservice/git_repo/commservice/database/commservice.db")

		ex = MainWindow()
		# closes the splash screen
		splash.finish(ex)
		sys.exit(app.exec_())


if __name__ == '__main__':
		main()
