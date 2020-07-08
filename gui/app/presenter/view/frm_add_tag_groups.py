import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmTagGroups(QDialog):

		def __init__(self):
				super(FrmTagGroups, self).__init__()

				self.setWindowTitle("Add tag groups")

				# PLC Selection
				self.group_box_tag_group = QGroupBox("Tag group")
				self.form_layout_tag_group = QFormLayout()
				self.tag_group_name = QLineEdit()
				self.form_layout_tag_group.addRow(QLabel("Name:"), self.tag_group_name)
				self.controller_collection = QComboBox()
				obj_db_management = DatabaseManagement()
				controllers = obj_db_management.select_all_controllers()
				for controller in controllers:
						self.controller_collection.addItem(controller[1])
				self.controller_collection.currentTextChanged.connect(self.on_controller_changed)
				self.form_layout_tag_group.addRow(QLabel("Select PLC:"), self.controller_collection)

				# Get all machines for PLC selected
				self.machine_collection = QComboBox()
				obj_db_management = DatabaseManagement()
				plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
				machines = obj_db_management.select_all_machines(plc_index[0][0])
				for machine in machines:
						self.machine_collection.addItem(machine[1])
				self.form_layout_tag_group.addRow(QLabel("Select Machine:"), self.machine_collection)

				self.collection_method = QLineEdit()
				self.form_layout_tag_group.addRow(QLabel("Collection Method:"), self.collection_method)
				self.collection_type = QLineEdit()
				self.form_layout_tag_group.addRow(QLabel("Collection Type:"), self.collection_type)
				self.group_box_tag_group.setLayout(self.form_layout_tag_group)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_tag_group)
				main_layout.addWidget(button_box)

				self.setLayout(main_layout)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
						machine_index = obj_db_management.get_machine_index(self.machine_collection.currentText())
						tag_group = (self.tag_group_name.text(), plc_index[0][0], machine_index[0][0], int(self.collection_method.text()), self.collection_type.text())
						obj_db_management.create_tag_group(tag_group)
						QMessageBox.information(self, 'Tag groups', "Tag group added successfully",
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

		def on_controller_changed(self, value):
				obj_db_management = DatabaseManagement()
				plc_index = obj_db_management.get_plc_index(self.controller_collection.currentText())
				machines = obj_db_management.select_all_machines(plc_index[0][0])
				self.machine_collection.clear()
				for machine in machines:
						self.machine_collection.addItem(machine[1])


if __name__ == '__main__':
		app = QApplication(sys.argv)

		dialog = FrmTagGroups()
		sys.exit(dialog.exec_())
