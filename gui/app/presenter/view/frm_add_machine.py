import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmAddMachine(QDialog):

		def __init__(self):
				super(FrmAddMachine, self).__init__()

				self.setWindowTitle("Add Machine")

				# PLC Selection
				self.group_box_plc_selection = QGroupBox("PLC Selection")
				self.form_layout_plc_selection = QFormLayout()
				self.controller_collection = QComboBox()

				obj_db_management = DatabaseManagement.get_instance()
				controllers = obj_db_management.select_all_controllers()
				for controller in controllers:
						self.controller_collection.addItem(controller[1])

				self.form_layout_plc_selection.addRow(QLabel("Select PLC:"), self.controller_collection)
				self.group_box_plc_selection.setLayout(self.form_layout_plc_selection)

				# "/dev/ttyUSB0", 115200, 'N', 8, 1
				self.group_box_machine_info = QGroupBox("Machine Information")
				self.form_layout_machine_info = QFormLayout()
				self.machine_name = QLineEdit()
				self.form_layout_machine_info.addRow(QLabel("Machine Name:"), self.machine_name)
				self.machine_manual_id = QLineEdit()
				self.form_layout_machine_info.addRow(QLabel("Manual ID:"), self.machine_manual_id)
				self.group_box_machine_info.setLayout(self.form_layout_machine_info)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_plc_selection)
				main_layout.addWidget(self.group_box_machine_info)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)
				# self.setGeometry(100, 100, 600, 400)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
						machine = (self.machine_name.text(), self.machine_manual_id.text(), plc_index[0][0])
						obj_db_management.create_machine(machine)
						QMessageBox.information(self, 'Machine', "New machine added successfully",
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

		dialog = FrmAddMachine()
		sys.exit(dialog.exec_())
