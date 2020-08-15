import sys

from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout, QComboBox

from app.utilities.database_management import DatabaseManagement


class FrmLogin(QDialog):

		def __init__(self):
				super(FrmLogin, self).__init__()
				self.selected_user = []
				self.setWindowTitle("User login")

				self.group_box_user_info = QGroupBox("")
				self.form_layout_user_info = QFormLayout()
				self.user_name = QLineEdit()
				self.form_layout_user_info.addRow(QLabel("User name:"), self.user_name)
				self.password = QLineEdit()
				self.password.setEchoMode(QLineEdit.Password)
				self.form_layout_user_info.addRow(QLabel("Password:"), self.password)

				self.group_box_user_info.setLayout(self.form_layout_user_info)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.login)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_user_info)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

		def login(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						user_info = (self.user_name.text(), self.password.text())
						self.selected_user = obj_db_management.select_user(user_info)
						if self.selected_user:
								self.accept()
						else:
								QMessageBox.information(self, 'Invalid User', "User is not present, Please enter valid details",
																				QMessageBox.Ok)

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

		dialog = FrmLogin()
		sys.exit(dialog.exec_())
