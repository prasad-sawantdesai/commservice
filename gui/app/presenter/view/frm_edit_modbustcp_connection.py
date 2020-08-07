import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement

PROTOCOL_NAME = "Modbus RTU"


class FrmEditModbusTcpConnection(QDialog):

		def __init__(self, id, plc_name=None):
				super(FrmEditModbusTcpConnection, self).__init__()
				self.id =id
				self.setWindowTitle("Edit Modbus TCP Connection")
				# PLC Selection
				self.group_box_plc_selection = QGroupBox("PLC Selection")
				self.form_layout_plc_selection = QFormLayout()
				self.controller_collection = QComboBox()

				obj_db_management = DatabaseManagement.get_instance()
				controllers = obj_db_management.select_all_controllers()
				for controller in controllers:
						self.controller_collection.addItem(controller[1])

				self.form_layout_plc_selection.addRow(QLabel("Select PLC:"), self.controller_collection)
				if plc_name is not None:
						self.controller_collection.setCurrentText(plc_name)
						self.controller_collection.setEnabled(False)
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

				obj_db_management = DatabaseManagement.get_instance()
				row = obj_db_management.select_connection_by_id(self.id)[0]
				connection_string = dict(item.split(":") for item in row[1].split(";"))
				self.controller_ip_address.setText(connection_string['IPADDRESS'])
				self.controller_port.setText(connection_string['PORT'])

				# self.setGeometry(100, 100, 600, 400)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						connection_string = "IPADDRESS:" + self.controller_ip_address.text() + ";" + \
																"PORT:" + self.controller_port.text()

						driver_index = obj_db_management.get_driver_index("Modbus TCP")
						plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
						connection = (connection_string, driver_index[0][0], plc_index[0][0])
						obj_db_management.update_connection_by_id(connection, self.id)
						QMessageBox.information(self, 'Modbus TCP', "Connection updated successfully",
																 QMessageBox.Ok)
						self.close()
				except Exception  as err:
						mb = QMessageBox()
						mb.setIcon(mb.Icon.Warning)
						mb.setText("{0}".format(err))
						mb.setWindowTitle("Error occurred")
						mb.exec_()

		def cancel(self):
				self.close()


if __name__ == '__main__':

		app = QApplication(sys.argv)

		dialog = FrmAddModbusTcpConnection()
		sys.exit(dialog.exec_())
