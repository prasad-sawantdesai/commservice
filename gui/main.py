import sys
import time
import logging
import os

from PySide2 import QtCore, QtGui
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QSplashScreen

from app.presenter.view.frm_add_machine import FrmAddMachine
from app.presenter.view.frm_add_modbusrtu_connection import FrmAddModbusRtuConnection
from app.presenter.view.frm_add_modbustcp_connection import FrmAddModbusTcpConnection
from app.presenter.view.frm_add_register_types import FrmAddRegisterTypes
from app.presenter.view.frm_add_tag_groups import FrmTagGroups
from app.presenter.view.frm_add_tags import FrmAddTags
from app.presenter.view.frm_addcontroller import FrmAddController
from app.presenter.view.frm_adddriver import FrmAddDriver
from app.presenter.view.frm_tag_mapping import FrmTagMapping
from app.utilities.configfilereader import ConfigFileReader
from app.utilities.database_management import DatabaseManagement

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):

		def __init__(self):
				super().__init__()
				self.InitConfig()
				self.set_window_properties()
				self.initUI()

		def InitConfig(self):

				# Read Configuration file
				application_path = ""
				# Get application executable path
				if getattr(sys, 'frozen', False):
					application_path = os.path.dirname(sys.executable)
				elif __file__:
					application_path = os.path.dirname(__file__)
				ConfigFileReader.config_file_path = os.path.join(application_path, r"configs\config.cfg")
				ConfigFileReader.application_path = application_path
				config_file_reader = ConfigFileReader()

				DatabaseManagement.db_file_path = config_file_reader.database_path
				database_management = DatabaseManagement()


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

				addDriverAct = QAction(QIcon('add.png'), '&Add Driver Type', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addDriverAct.setStatusTip('Add tag groups')
				addDriverAct.triggered.connect(self.show_frm_add_driver)

				addTagMappingAct = QAction(QIcon('add.png'), '&Add Tag Mapping', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				addTagMappingAct.setStatusTip('Add tag groups')
				addTagMappingAct.triggered.connect(self.show_frm_add_tag_mapping)


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

				configMenu.addAction(addDriverAct)
				configMenu.addAction(addTagMappingAct)

				windowMenu = menubar.addMenu('&Window')

				helpMenu = menubar.addMenu('&Help')
				self.showMaximized()
				self.setWindowTitle('X-Box Configurator')
				self.show()

		def set_window_properties(self):
				icon = QIcon()
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Normal, QIcon.Off)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Normal, QIcon.On)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Disabled, QIcon.Off)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Disabled, QIcon.On)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Active, QIcon.Off)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Active, QIcon.On)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Selected, QIcon.Off)
				icon.addPixmap(QPixmap(r'resources/icon.ico'), QIcon.Selected, QIcon.On)
				self.setWindowIcon(icon)

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


		def show_frm_add_driver(self):
				dialog = FrmAddDriver()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_tag_mapping(self):
				dialog = FrmTagMapping()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()
def main():
		app = QApplication(sys.argv)
		# for the splash screen
		splash_pix = QtGui.QPixmap("resources\\splash_screen.png")
		# Creates the splash screen
		splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
		splash.setMask(splash_pix.mask())
		# shows splash screen
		splash.show()
		app.processEvents()
		time.sleep(2)

		ex = MainWindow()
		# closes the splash screen
		splash.finish(ex)
		sys.exit(app.exec_())


if __name__ == '__main__':
		main()
