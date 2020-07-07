import sys

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel, \
		QComboBox, QSpinBox, QApplication

from app.utilities.database_management import DatabaseManagement


class FrmAddDriver(QDialog):
		NumGridRows = 3
		NumButtons = 4

		def __init__(self):
				super(FrmAddDriver, self).__init__()
				self.driver_name = QLineEdit()
				self.driver_format =QLineEdit()
				self.form_group_box = QGroupBox("Driver Information")
				self.create_from_group_box()

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.form_group_box)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

				self.setWindowTitle("Add Protocol")

		def create_from_group_box(self):

				layout = QFormLayout()
				layout.addRow(QLabel("Protocol Name:"), self.driver_name)
				layout.addRow(QLabel("Protocol Format:"), self.driver_format)
				self.form_group_box.setLayout(layout)

		def store(self):
				obj_db_management = DatabaseManagement(r"/home/ujjaini/prasad/commservice/git_repo/commservice/database/commservice.db")
				driver = (self.driver_name.text(), self.driver_format.text())
				obj_db_management.create_driver(driver)
				# self.close()
		def cancel(self):
				self.close()



if __name__ == '__main__':
		app = QApplication(sys.argv)
		dialog = FrmAddDriver()
		sys.exit(dialog.exec_())