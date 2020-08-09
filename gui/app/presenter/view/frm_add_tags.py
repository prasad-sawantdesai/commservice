import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmAddTags(QDialog):
		NumGridRows = 3
		NumButtons = 4

		def __init__(self):
				super(FrmAddTags, self).__init__()
				self.setWindowTitle("Add Tag")

				self.group_box_tag_info = QGroupBox("Tag Information")
				self.form_layout_tag_info = QFormLayout()
				self.tag_name = QLineEdit()
				self.form_layout_tag_info.addRow(QLabel("Tag Name:"), self.tag_name)

				self.register_types = QComboBox()
				obj_db_management = DatabaseManagement()
				register_types = obj_db_management.select_all_register_types()
				for register_type in register_types:
						self.register_types.addItem(register_type[1])
				self.form_layout_tag_info.addRow(QLabel("Select Register Type:"), self.register_types)

				self.address = QLineEdit()
				self.form_layout_tag_info.addRow(QLabel("Address:"), self.address)

				self.scaling = QLineEdit()
				self.form_layout_tag_info.addRow(QLabel("Scaling:"), self.scaling)

				self.data_types = QComboBox()
				self.data_types.addItems(["uint8","int16", "int32", "float32"])
				self.form_layout_tag_info.addRow(QLabel("Data type:"), self.data_types)

				self.data_size = QLineEdit()
				self.form_layout_tag_info.addRow(QLabel("Data size:"), self.data_size)

				self.group_box_tag_info.setLayout(self.form_layout_tag_info)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_tag_info)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						register_type_index = obj_db_management.get_register_type_index(self.register_types.currentText())
						tag = (self.tag_name.text(),
									 register_type_index[0][0],
									 self.address.text(),
									 self.scaling.text(),
									 self.data_types.currentText(),
									 self.data_size.text())
						obj_db_management.create_tags(tag)
						QMessageBox.information(self, 'Tags', "New Tag information added successfully",
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

		dialog = FrmAddTags()
		sys.exit(dialog.exec_())
