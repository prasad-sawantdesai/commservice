import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QRadioButton, QVBoxLayout, QMessageBox

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
				self.data_types.addItems(["Integer", "Float", "Boolean"])
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
				# self.setGeometry(100, 100, 600, 400)

		def store(self):
				obj_db_management = DatabaseManagement()
				register_type_index = obj_db_management.get_register_type_index(self.register_types.currentText())
				tag = (self.tag_name.text(),
									 register_type_index[0][0],
									 self.address.text(),
									 self.scaling.text(),
									 self.data_types.currentText(),
									 self.data_size.text())
				obj_db_management.create_tags(tag)
				QMessageBox.question(self, 'Tags', "Tag information added successfully",
																					 QMessageBox.Ok)
				self.close()
		def cancel(self):
				self.close()


if __name__ == '__main__':
		obj_db_management = DatabaseManagement(
						r"/home/ujjaini/prasad/commservice/git_repo/commservice/database/commservice.db")
		app = QApplication(sys.argv)

		dialog = FrmAddTags()
		sys.exit(dialog.exec_())
