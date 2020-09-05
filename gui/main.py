#!/usr/bin/env python

import logging
import os
import sys
import time
from configparser import ConfigParser

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel, Qt
from PySide2.QtWidgets import QAction, QApplication, QFrame, QHBoxLayout, QMainWindow, QMenu, QMessageBox, \
		QSplashScreen, QSplitter, QTreeView, QWidget, QFileDialog, QDialog

import internalconfig
from app.presenter.view.frm_add_machine import FrmAddMachine
from app.presenter.view.frm_add_modbusrtu_connection import FrmAddModbusRtuConnection
from app.presenter.view.frm_add_modbustcp_connection import FrmAddModbusTcpConnection
from app.presenter.view.frm_add_register_types import FrmAddRegisterTypes
from app.presenter.view.frm_add_tag_groups import FrmTagGroups
from app.presenter.view.frm_add_tags import FrmAddTags
from app.presenter.view.frm_add_user import FrmAddUser
from app.presenter.view.frm_addcontroller import FrmAddController
from app.presenter.view.frm_adddriver import FrmAddDriver
from app.presenter.view.frm_delete_user import FrmDeleteUser
from app.presenter.view.frm_edit_machine import FrmEditMachine
from app.presenter.view.frm_edit_modbusrtu_connection import FrmEditModbusRtuConnection
from app.presenter.view.frm_edit_modbustcp_connection import FrmEditModbusTcpConnection
from app.presenter.view.frm_edit_settings import FrmEditSettings
from app.presenter.view.frm_edit_tag_groups import FrmEditTagGroups
from app.presenter.view.frm_edit_user import FrmEditUser
from app.presenter.view.frm_editcontroller import FrmEditController
from app.presenter.view.frm_login import FrmLogin
from app.presenter.view.frm_tag_mapping import FrmTagMapping
from frm_tag_viewer import FrmTagViewer
from app.utilities.configfilereader import ConfigFileReader
from app.utilities.database_management import DatabaseManagement

logger = logging.getLogger(__name__)

# Get application executable path
application_path = ""
if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
elif __file__:
		application_path = os.path.dirname(__file__)

IMAGE_DIRECTORY = os.path.join(application_path, "resources")


class MainWindow(QMainWindow):
		signal_view_tags = Signal()

		def __init__(self):
				super().__init__()
				internalconfig.xboard_user_name = "unknown"
				setup_logger(False)
				logger.info('Application is started')
				self.selected_item_id = None
				self.selected_plc = None
				self.selected_connection = None
				self.selected_group_id = None
				self.selected_user = None

		def start(self):
				self.InitConfig()
				self.set_window_properties()

				self.InitMainWindow()

				self.initUI()
				self.InitLogin()

		def InitLogin(self):
				self.show_login_screen()

		def InitConfig(self):
				# Read Configuration file

				ConfigFileReader.config_file_path = os.path.join(application_path, r"configs/config.cfg")
				if not os.path.exists(ConfigFileReader.config_file_path):
						QMessageBox.warning(self, 'Config file error', "Configuration file not found.. Couldn't proceed..",
																QMessageBox.Ok)
						sys.exit(-1)
				ConfigFileReader.application_path = application_path
				config_file_reader = ConfigFileReader()

				DatabaseManagement.db_file_path = config_file_reader.database_path
				if not os.path.exists(config_file_reader.database_path):
						QMessageBox.warning(self, 'Database file error', "Database file not found.. Select database in next "
																														 "window",
																QMessageBox.Ok)
						database_filepath = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Database files (*.db )")
						config_object = ConfigParser()
						config_object["database"] = {
								"path": database_filepath[0],
						}
						config_file_reader.database_path = database_filepath[0]
						DatabaseManagement.db_file_path = config_file_reader.database_path
						with open(ConfigFileReader.config_file_path, 'w') as conf:
								config_object.write(conf)
				database_management = DatabaseManagement()

		def InitMainWindow(self):
				obj_db_management = DatabaseManagement.get_instance()
				self.tv_config_explorer = QTreeView()
				# self.tv_config_explorer.setAlternatingRowColors(True)
				self.tv_config_explorer.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
				self.tv_config_explorer.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
				self.tv_config_explorer.setHeaderHidden(False)

				self.tv_config_explorer_model = QStandardItemModel()
				self.tv_config_explorer.setModel(self.tv_config_explorer_model)
				self.tv_config_explorer.setHeaderHidden(False)
				self.tv_config_explorer.model().setHorizontalHeaderLabels(['Configuration', ''])

				root_node = self.tv_config_explorer_model.invisibleRootItem()

				for tv_node in ['Controllers', 'Tag Groups']:
						qsi_tv_node = QStandardItem(tv_node)
						root_node.appendRow(qsi_tv_node)
						if tv_node == 'Controllers':
								qsi_tv_node.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'device_16.png')))
								self.refresh_controllers(qsi_tv_node)

						if tv_node == 'Tag Groups':
								self.refresh_taggroups(qsi_tv_node)

				self.tv_config_explorer.setColumnWidth(0, 2000)
				# self.tv_config_explorer.expandAll()
				# self.tv_config_explorer.setColumnHidden(1, True)

				self.action_add_new_controller = QAction("Add new Controller ", self, triggered = self.show_frm_add_controller)
				self.action_add_new_controller.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'plus_16.png')))

				self.action_edit_controller = QAction("Edit Controller ", self, triggered = self.show_frm_edit_controller)
				self.action_edit_controller.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'edit_16.png')))

				self.action_delete_controller = QAction("Delete Controller ", self, triggered = self.delete_controller)
				self.action_delete_controller.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'delete_16.png')))

				self.action_add_new_taggroup = QAction("Add new Tag group ", self, triggered = self.show_frm_add_tag_groups)
				self.action_add_new_taggroup.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'taggroup_16.png')))

				self.action_add_new_machine = QAction("Add new Machine ", self, triggered = self.show_frm_add_machine)
				self.action_add_new_machine.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'plus_16.png')))

				self.action_add_new_modbus_rtu = QAction("Add new Modbus RTU Connection ", self,
																								 triggered = self.show_frm_add_modbusrtu_connection)
				self.action_add_new_modbus_rtu.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'plus_16.png')))

				self.action_add_new_modbus_tcp = QAction("Add new Modbus TCP Connection ", self,
																								 triggered = self.show_frm_add_modbustcp_connection)
				self.action_add_new_modbus_tcp.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'plus_16.png')))

				self.action_delete_machine = QAction("Delete Machine ", self, triggered = self.delete_machine)
				self.action_delete_machine.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'delete_16.png')))

				self.action_delete_connection = QAction("Delete Connection ", self, triggered = self.delete_connection)
				self.action_delete_connection.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'delete_16.png')))

				self.action_edit_machine = QAction("Edit Machine ", self, triggered = self.show_frm_edit_machine)
				self.action_edit_machine.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'edit_16.png')))

				self.action_edit_connection = QAction("Edit Connection ", self, triggered = self.show_frm_edit_connection)
				self.action_edit_connection.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'edit_16.png')))

				self.action_delete_taggroup = QAction("Delete Tag Group ", self, triggered = self.delete_taggroup)
				self.action_delete_taggroup.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'delete_16.png')))

				self.action_edit_taggroup = QAction("Edit Tag Group ", self, triggered = self.show_frm_edit_taggroup)
				self.action_edit_taggroup.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'edit_16.png')))

				self.action_view_all_tags = QAction("View All Tags ", self, triggered = self.view_alltags)
				self.action_view_all_tags.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'viewall_16.png')))

				self.action_view_tags = QAction("View Tags ", self, triggered = self.view_tags)
				self.action_view_tags.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'view_16.png')))

				self.action_add_tag = QAction("View Tags ", self, triggered = self.show_frm_add_tags)
				self.action_add_tag.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'view_16.png')))

				centralWidget = QWidget()
				self.setCentralWidget(centralWidget)
				layout = QHBoxLayout(centralWidget)

				# Initialize tab screen
				self.frame_right = FrmTagViewer()
				self.signal_view_tags.connect(self.frame_right.load_tags)
				self.frame_right.setFrameShape(QFrame.StyledPanel)

				widget_splitter = QSplitter(Qt.Horizontal)
				widget_splitter.addWidget(self.tv_config_explorer)
				widget_splitter.addWidget(self.frame_right)

				widget_splitter.setSizes([50, 300])

				layout.addWidget(widget_splitter)

		def refresh_controllers(self, qsi_tv_node):
				obj_db_management = DatabaseManagement.get_instance()
				controllers = obj_db_management.select_all_controllers()
				for controller in controllers:
						qsi_tv_controller = QStandardItem(controller[1])
						qsi_tv_controller.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'plc_16.png')))
						qsi_tv_controller.setEditable(False)
						qsi_tv_controller_id = QStandardItem(str(controller[0]))
						qsi_tv_node.appendRow([qsi_tv_controller, qsi_tv_controller_id])

						qsi_tv_machines = QStandardItem("Machines")
						qsi_tv_machines.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'slaves_16.png')))
						qsi_tv_controller.appendRow(qsi_tv_machines)
						machines = obj_db_management.select_all_machines(controller[0])
						for machine in machines:
								qsi_tv_machine = QStandardItem(machine[1])
								qsi_tv_machine.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'slave_16.png')))
								qsi_tv_machine.setEditable(False)
								qsi_tv_machine_id = QStandardItem(str(machine[0]))
								qsi_tv_machines.appendRow([qsi_tv_machine, qsi_tv_machine_id])

						qsi_tv_connections = QStandardItem("Connections")
						qsi_tv_connections.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'connections_16.png')))
						qsi_tv_controller.appendRow(qsi_tv_connections)
						connections = obj_db_management.select_all_connections(controller[0])
						for connection in connections:
								qsi_tv_connection = QStandardItem(connection[1])
								qsi_tv_connection.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'connection_16.png')))
								qsi_tv_connection.setEditable(False)
								qsi_tv_connection_id = QStandardItem(str(connection[0]))
								qsi_tv_connections.appendRow([qsi_tv_connection, qsi_tv_connection_id])

		def refresh_taggroups(self, qsi_tv_node):
				obj_db_management = DatabaseManagement.get_instance()
				qsi_tv_node.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'tags_16.png')))
				tag_groups = obj_db_management.select_all_tag_groups()
				for tag_group in tag_groups:
						qsi_tv_tag_group = QStandardItem(tag_group[1])
						qsi_tv_tag_group.setData(tag_group, Qt.UserRole)
						qsi_tv_tag_group.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'taggroup_16.png')))
						qsi_tv_tag_group.setEditable(False)
						qsi_tv_tag_group_id = QStandardItem(str(tag_group[0]))
						qsi_tv_node.appendRow([qsi_tv_tag_group, qsi_tv_tag_group_id])

		def contextMenuEvent(self, event):
				# Fetch item for the index fetched from the selection
				index_component_name = self.tv_config_explorer.selectedIndexes()[0]
				index_component_id = None
				if len(self.tv_config_explorer.selectedIndexes()) == 2:
						self.selected_item_id = self.tv_config_explorer.selectedIndexes()[1].data()

				# Get information from base model instead
				if index_component_name.data() == "Controllers":
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_add_new_controller)
						ctx_menu.exec_(event.globalPos())
						controllers_node = self.tv_config_explorer_model.itemFromIndex(index_component_name)
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(index_component_name),
																										 index_component_name)
						self.refresh_controllers(controllers_node)

				elif index_component_name.parent().data() == "Controllers":
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_edit_controller)
						ctx_menu.addAction(self.action_delete_controller)

						ctx_menu.exec_(event.globalPos())
						controllers_node = self.tv_config_explorer_model.itemFromIndex(index_component_name.parent())
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(
										index_component_name.parent()),
																										 index_component_name.parent())
						self.refresh_controllers(controllers_node)
				elif index_component_name.parent().parent().data() == "Controllers":
						ctx_menu = QMenu()
						self.selected_plc = index_component_name.parent().data()
						if index_component_name.data() == "Machines":
								ctx_menu.addAction(self.action_add_new_machine)

						if index_component_name.data() == "Connections":
								self.selected_plc = index_component_name.parent().data()
								ctx_menu.addAction(self.action_add_new_modbus_rtu)
								ctx_menu.addAction(self.action_add_new_modbus_tcp)

						ctx_menu.exec_(event.globalPos())
						controllers_node = self.tv_config_explorer_model.itemFromIndex(index_component_name.parent().parent())
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(
										index_component_name.parent().parent()),
																										 index_component_name.parent().parent())
						self.refresh_controllers(controllers_node)
				elif index_component_name.parent().data() == "Machines":
						self.selected_plc = index_component_name.parent().parent().data()
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_edit_machine)
						ctx_menu.addAction(self.action_delete_machine)

						ctx_menu.exec_(event.globalPos())
						controllers_node = self.tv_config_explorer_model.itemFromIndex(
										index_component_name.parent().parent().parent())
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(
										index_component_name.parent().parent().parent()),
																										 index_component_name.parent().parent().parent())
						self.refresh_controllers(controllers_node)
				elif index_component_name.parent().data() == "Connections":
						self.selected_plc = index_component_name.parent().parent().data()
						self.selected_connection = index_component_name.data()
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_edit_connection)
						ctx_menu.addAction(self.action_delete_connection)

						ctx_menu.exec_(event.globalPos())
						controllers_node = self.tv_config_explorer_model.itemFromIndex(
										index_component_name.parent().parent().parent())
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(
										index_component_name.parent().parent().parent()),
																										 index_component_name.parent().parent().parent())
						self.refresh_controllers(controllers_node)
				elif index_component_name.data() == "Tag Groups":
						self.frame_right.selected_taggroup_id = '*'
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_view_all_tags)
						ctx_menu.addAction(self.action_add_new_taggroup)
						ctx_menu.addAction(self.action_add_tag)
						ctx_menu.exec_(event.globalPos())

						taggroups_node = self.tv_config_explorer_model.itemFromIndex(index_component_name)
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(
										index_component_name), index_component_name)
						self.refresh_taggroups(taggroups_node)
				elif index_component_name.parent().data() == "Tag Groups":
						self.frame_right.selected_taggroup_id = self.selected_item_id
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_view_tags)
						ctx_menu.addAction(self.action_edit_taggroup)
						ctx_menu.addAction(self.action_delete_taggroup)
						ctx_menu.exec_(event.globalPos())

						taggroups_node = self.tv_config_explorer_model.itemFromIndex(index_component_name.parent())
						self.tv_config_explorer_model.removeRows(0, self.tv_config_explorer_model.rowCount(
										index_component_name.parent()), index_component_name.parent())
						self.refresh_taggroups(taggroups_node)
				return

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

				settingsAct = QAction(QIcon('add.png'), '&Settings', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				settingsAct.setStatusTip('Update settings')
				settingsAct.triggered.connect(self.show_frm_settings)

				adduserAct = QAction(QIcon('add.png'), '&Add User', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				adduserAct.setStatusTip('Add User')
				adduserAct.triggered.connect(self.show_frm_add_user)

				edituserAct = QAction(QIcon('add.png'), '&Edit User', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				edituserAct.setStatusTip('Edit User')
				edituserAct.triggered.connect(self.show_frm_edit_user)

				deleteuserAct = QAction(QIcon('add.png'), '&Delete User', self)
				# addModbusTcpAct.setShortcut('Ctrl+M')
				deleteuserAct.setStatusTip('Delete User')
				deleteuserAct.triggered.connect(self.show_frm_delete_user)

				self.statusBar().showMessage("Ready")
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
				configMenu.addAction(settingsAct)

				self.userManagementMenu = configMenu.addMenu('&User Management')
				self.userManagementMenu.addAction(adduserAct)
				self.userManagementMenu.addAction(edituserAct)
				self.userManagementMenu.addAction(deleteuserAct)

				windowMenu = menubar.addMenu('&Window')

				helpMenu = menubar.addMenu('&Help')
				self.showMaximized()
				self.setWindowTitle('X-Board Configurator')
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

		def show_frm_edit_controller(self):
				dialog = FrmEditController(self.selected_item_id)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def delete_controller(self):
				obj_db_management = DatabaseManagement.get_instance()
				logger.info(str(self.selected_item_id) + ' - Controller is deleting ' + " by " + internalconfig.xboard_user_name)
				obj_db_management.delete_controller_by_id(self.selected_item_id)
				QMessageBox.information(self, 'Controller', "Controller deleted successfully",
																QMessageBox.Ok)

		def show_frm_add_machine(self):
				dialog = FrmAddMachine(self.selected_plc)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_modbusrtu_connection(self):
				dialog = FrmAddModbusRtuConnection(self.selected_plc)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_modbustcp_connection(self):
				dialog = FrmAddModbusTcpConnection(self.selected_plc)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def delete_machine(self):
				obj_db_management = DatabaseManagement.get_instance()
				logger.info(
						str(self.selected_item_id) + ' - Machine is deleting ' + " by " + internalconfig.xboard_user_name)
				obj_db_management.delete_machine_by_id(self.selected_item_id)
				QMessageBox.information(self, 'Machine', "Machine deleted successfully",
																QMessageBox.Ok)

		def view_alltags(self):
				self.signal_view_tags.emit()

		def view_tags(self):
				self.signal_view_tags.emit()

		def delete_connection(self):
				obj_db_management = DatabaseManagement.get_instance()
				logger.info(
						str(self.selected_item_id) + ' - Connection is deleting ' + " by " + internalconfig.xboard_user_name)
				obj_db_management.delete_connection_by_id(self.selected_item_id)
				QMessageBox.information(self, 'Connection', "Connection deleted successfully",
																QMessageBox.Ok)

		def delete_taggroup(self):
				obj_db_management = DatabaseManagement.get_instance()
				logger.info(
						str(self.selected_item_id) + ' - Tag group is deleting ' + " by " + internalconfig.xboard_user_name)
				obj_db_management.delete_taggroup_by_id(self.selected_item_id)
				QMessageBox.information(self, 'Tag Group', "Tag Group deleted successfully",
																QMessageBox.Ok)

		def show_frm_edit_machine(self):
				dialog = FrmEditMachine(self.selected_item_id, self.selected_plc)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_edit_taggroup(self):
				dialog = FrmEditTagGroups(self.selected_item_id)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_edit_connection(self):
				if "COMPORT" in self.selected_connection:
						self.show_frm_edit_modbusrtu_connection()
				elif "IPADDRESS" in self.selected_connection:
						self.show_frm_edit_modbustcp_connection()

		def show_frm_edit_modbusrtu_connection(self):
				dialog = FrmEditModbusRtuConnection(self.selected_item_id, self.selected_plc)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_edit_modbustcp_connection(self):
				dialog = FrmEditModbusTcpConnection(self.selected_item_id, self.selected_plc)
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

		def show_frm_add_user(self):
				dialog = FrmAddUser()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_edit_user(self):
				dialog = FrmEditUser()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_delete_user(self):
				dialog = FrmDeleteUser()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_tag_mapping(self):
				dialog = FrmTagMapping()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_settings(self):
				dialog = FrmEditSettings()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_login_screen(self):
				dialog = FrmLogin()
				dialog.setModal(True)
				dialog.show()
				if dialog.exec_() == QDialog.Accepted:
						self.selected_user = dialog.selected_user
						if self.selected_user[0][3] == 'admin':
								self.userManagementMenu.setEnabled(True)
						else:
								self.userManagementMenu.setEnabled(False)
						self.setWindowTitle("X-Board Configurator - " + self.selected_user[0][1])
						internalconfig.xboard_user_name = self.selected_user[0][1]
				else:
						sys.exit(0)


def setup_logger(is_debugging_needed):
		logging_path = os.path.join(application_path, r"logs")
		if not os.path.exists(logging_path):
				os.makedirs(logging_path)
		# setup file logger
		log_filename = os.path.join(application_path, r"logs\x-board_" + time.strftime("%Y%m%d_%H%M%S") + \
									 ".log")
		debugging_option = logging.INFO

		if is_debugging_needed is True:
				debugging_option = logging.DEBUG
		logging.basicConfig(filename = log_filename, format = '%(asctime)s, '
																													'[%(levelname)s], '
																													'%(name)s, '
																													'%(message)s',
												level = logging.DEBUG)

		# setup console logger
		console = logging.StreamHandler()
		console.setLevel(debugging_option)
		formatter = logging.Formatter('%(asctime)s, ' '[%(levelname)s], '
																	'%(name)s:, %(message)s')
		console.setFormatter(formatter)

		logging.getLogger('').addHandler(console)

		# Suppress warnings in weasyprint & matplotlib.font_manager modules
		logging.getLogger('weasyprint').setLevel(logging.CRITICAL)
		logging.getLogger('matplotlib.font_manager').setLevel(logging.CRITICAL)


def main():
		app = QApplication(sys.argv)
		# for the splash screen
		config_file_path = os.path.join(application_path, r"configs/config.cfg")

		QIcon()
		splash_pix = QPixmap(os.path.join(IMAGE_DIRECTORY, 'splash_screen.png'))
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
		ex.start()

		sys.exit(app.exec_())


if __name__ == '__main__':
		main()
