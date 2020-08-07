import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmEditMachine(QDialog):

		def __init__(self, id, plc_name=None):
				super(FrmEditMachine, self).__init__()
				self.id = id
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

				obj_db_management = DatabaseManagement.get_instance()
				row = obj_db_management.select_machine_by_id(self.id)[0]
				self.machine_name.setText(row[1])
				self.machine_manual_id.setText(str(row[2]))
				self.setWindowTitle("Edit Machine")
				# self.setGeometry(100, 100, 600, 400)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
						machine = (self.machine_name.text(), self.machine_manual_id.text(), plc_index[0][0])
						obj_db_management.update_machine_by_id(machine, self.id)
						QMessageBox.information(self, 'Machine', "New machine updated successfully",
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

		dialog = FrmEditMachine()
		sys.exit(dialog.exec_())
