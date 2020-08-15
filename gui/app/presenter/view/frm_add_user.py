import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmAddUser(QDialog):

		def __init__(self):
				super(FrmAddUser, self).__init__()

				self.setWindowTitle("Add User")

				self.group_box_user_info = QGroupBox("User Information")
				self.form_layout_user_info = QFormLayout()
				self.user_name = QLineEdit()
				self.form_layout_user_info.addRow(QLabel("User Name:"), self.user_name)
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
				main_layout.addWidget(self.group_box_user_info)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						user_role_index = obj_db_management.get_user_role_index(self.user_role.currentText())
						user = (self.user_name.text(), self.user_password.text(), user_role_index[0][0])
						obj_db_management.create_user(user)
						QMessageBox.information(self, 'User', "New user added successfully",
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

		dialog = FrmAddUser()
		sys.exit(dialog.exec_())
