import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QRadioButton, QVBoxLayout, QMessageBox

from app.utilities.database_management import DatabaseManagement

PROTOCOL_NAME = "Modbus RTU"
class FrmAddModbusTcpConnection(QDialog):
		NumGridRows = 3
		NumButtons = 4

		def __init__(self):
				super(FrmAddModbusTcpConnection, self).__init__()

				self.setWindowTitle("Add Modbus TCP Connection")
				self.setGeometry(100, 100, 600, 400)
				# PLC Selection
				self.group_box_plc_selection = QGroupBox("PLC Selection")
				self.form_layout_plc_selection = QFormLayout()
				self.controller_collection = QComboBox()

				obj_db_management = DatabaseManagement(
								r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				controllers = obj_db_management.select_all_controllers()
				for controller in controllers:
						self.controller_collection.addItem(controller[1])

				self.form_layout_plc_selection.addRow(QLabel("Select PLC:"), self.controller_collection)
				self.group_box_plc_selection.setLayout(self.form_layout_plc_selection)

				# "/dev/ttyUSB0", 115200, 'N', 8, 1
				self.group_box_modbus_tcp = QGroupBox("Connection Information")
				self.form_layout_modbus_tcp = QFormLayout()
				self.controller_ip_address = QLineEdit()
				self.form_layout_modbus_tcp.addRow(QLabel("Controller IP Address:"), self.controller_ip_address)
				self.controller_port = QLineEdit()
				self.form_layout_modbus_tcp.addRow(QLabel("Port:"), self.controller_port)
				self.group_box_modbus_tcp.setLayout(self.form_layout_modbus_tcp)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_plc_selection)
				main_layout.addWidget(self.group_box_modbus_tcp)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)
				self.setGeometry(100, 100, 600, 400)

		def store(self):
				obj_db_management = DatabaseManagement(
								r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				connection_string = "IPADDRESS:" + self.controller_ip_address.text() + ";" +\
				"PORT:" + self.controller_port.text()

				driver_index = obj_db_management.get_driver_index("Modbus TCP")
				plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
				controller = (connection_string, driver_index[0][0], plc_index[0][0])
				obj_db_management.create_connection(controller)
				QMessageBox.question(self, 'Machine', "New connection added successfully",
																					 QMessageBox.Ok)
				self.close()
		def cancel(self):
				self.close()

if __name__ == '__main__':

		app = QApplication(sys.argv)

		dialog = FrmAddModbusTcpConnection()
		sys.exit(dialog.exec_())
