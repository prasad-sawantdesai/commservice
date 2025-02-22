import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement

PROTOCOL_NAME = "Modbus RTU"


class FrmEditModbusRtuConnection(QDialog):

		def __init__(self, id, plc_name=None):
				super(FrmEditModbusRtuConnection, self).__init__()
				self.id = id
				self.setWindowTitle("Edit Modbus RTU Connection")

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
				self.group_box_modbus_rtu = QGroupBox("Connection Information")
				self.form_layout_modbus_rtu = QFormLayout()
				self.controller_com_port = QLineEdit()
				self.form_layout_modbus_rtu.addRow(QLabel("COM Port:"), self.controller_com_port)
				self.controller_baudrate = QComboBox()
				self.controller_baudrate.addItems(["9600", "19200", "57600", "115200"])
				self.form_layout_modbus_rtu.addRow(QLabel("Baud rate:"), self.controller_baudrate)
				self.controller_parity = QComboBox()
				self.controller_parity.addItems(["N", "E", "O"])
				self.form_layout_modbus_rtu.addRow(QLabel("Parity:"), self.controller_parity)
				self.controller_data_bits = QComboBox()
				self.controller_data_bits.addItems(["5", "6", "7", "8"])
				self.form_layout_modbus_rtu.addRow(QLabel("Data bits:"), self.controller_data_bits)
				self.controller_stop_bits = QComboBox()
				self.controller_stop_bits.addItems(["1", "2"])
				self.form_layout_modbus_rtu.addRow(QLabel("Stop bits:"), self.controller_stop_bits)
				self.group_box_modbus_rtu.setLayout(self.form_layout_modbus_rtu)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_plc_selection)
				main_layout.addWidget(self.group_box_modbus_rtu)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

				obj_db_management = DatabaseManagement.get_instance()
				row = obj_db_management.select_connection_by_id(self.id)[0]
				connection_string = dict(item.split(":") for item in row[1].split(";"))
				self.controller_com_port.setText(connection_string['COMPORT'])
				self.controller_baudrate.setCurrentText(connection_string['BAUDRATE'])
				self.controller_parity.setCurrentText(connection_string['PARITY'])
				self.controller_data_bits.setCurrentText(connection_string['DATABITS'])
				self.controller_stop_bits.setCurrentText(connection_string['STOPBITS'])

				# self.setGeometry(100, 100, 600, 400)

		def store(self):
				try:
						obj_db_management = DatabaseManagement()
						connection_string = "COMPORT:" + self.controller_com_port.text() + ";" + \
																"BAUDRATE:" + self.controller_baudrate.currentText() + ";" + \
																"PARITY:" + self.controller_parity.currentText() + ";" + \
																"DATABITS:" + self.controller_data_bits.currentText() + ";" + \
																"STOPBITS:" + self.controller_stop_bits.currentText()

						driver_index = obj_db_management.get_driver_index("Modbus RTU")
						plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
						connection = (connection_string, driver_index[0][0], plc_index[0][0])
						obj_db_management.update_connection_by_id(connection, self.id)
						QMessageBox.information(self, 'Modbus RTU', "Connection updated successfully",
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

		dialog = FrmEditModbusRtuConnection()
		sys.exit(dialog.exec_())
