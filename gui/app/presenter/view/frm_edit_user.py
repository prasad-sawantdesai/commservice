import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmEditUser(QDialog):

		def __init__(self):
				super(FrmEditUser, self).__init__()
				self.setWindowTitle("Edit user")
				# PLC Selection

				self.group_box_user_selection = QGroupBox("User Selection")
				self.form_layout_user_selection = QFormLayout()
				self.user_collection = QComboBox()

				obj_db_management = DatabaseManagement.get_instance()
				users = obj_db_management.select_all_users()
				for user in users:
						self.user_collection.addItem(user[1])

				self.form_layout_user_selection.addRow(QLabel("Select User:"), self.user_collection)
				self.user_collection.currentTextChanged.connect(self.on_user_changed)

				self.group_box_user_selection.setLayout(self.form_layout_user_selection)

				# "/dev/ttyUSB0", 115200, 'N', 8, 1
				self.group_box_user_info = QGroupBox("User Information")
				self.form_layout_user_info = QFormLayout()
				self.user_name = QLineEdit()
				self.form_layout_user_info.addRow(QLabel("Name:"), self.user_name)
				self.user_password = QLineEdit()
				self.user_password.setEchoMode(QLineEdit.Password)
				self.form_layout_user_info.addRow(QLabel("Password:"), self.user_password)
				self.user_role = QComboBox()
				self.user_role.addItems(["admin", "user"])
				self.form_layout_user_info.addRow(QLabel("Role :"), self.user_role)
				self.group_box_user_info.setLayout(self.form_layout_user_info)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_user_selection)
				main_layout.addWidget(self.group_box_user_info)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

				self.on_user_changed()

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						user_index = obj_db_management.get_user_index(self.user_collection.currentText())
						user_role_index = obj_db_management.get_role_index(self.user_role.currentText())
						user_info = (self.user_name.text(), self.user_password.text(), user_role_index[0][0])
						obj_db_management.update_user_by_id(user_info, user_index[0][0])
						QMessageBox.information(self, 'User', "User updated successfully",
																 QMessageBox.Ok)
						self.close()
				except Exception  as err:
						mb = QMessageBox()
						mb.setIcon(mb.Icon.Warning)
						mb.setText("{0}".format(err))
						mb.setWindowTitle("Error occurred")
						mb.exec_()

		def on_user_changed(self, value=None):
				obj_db_management = DatabaseManagement.get_instance()
				row = obj_db_management.select_user_by_name(self.user_collection.currentText())[0]

				self.user_name.setText(row[1])
				self.user_password.setText(str(row[2]))
				self.user_role.setCurrentText(str(row[3]))

		def cancel(self):
				self.close()


if __name__ == '__main__':
		app = QApplication(sys.argv)

		dialog = FrmEditUser()
		sys.exit(dialog.exec_())
