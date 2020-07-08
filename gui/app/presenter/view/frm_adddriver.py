import sys

from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, \
		QVBoxLayout, QMessageBox

from app.utilities.database_management import DatabaseManagement


class FrmAddDriver(QDialog):

		def __init__(self):
				super(FrmAddDriver, self).__init__()
				self.driver_name = QLineEdit()
				self.driver_format = QLineEdit()
				self.form_group_box = QGroupBox("Driver Information")
				self.create_from_group_box()

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.form_group_box)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

				self.setWindowTitle("Add Driver")

		def create_from_group_box(self):
				layout = QFormLayout()
				layout.addRow(QLabel("Driver Name:"), self.driver_name)
				layout.addRow(QLabel("Driver Format:"), self.driver_format)
				self.form_group_box.setLayout(layout)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						driver = (self.driver_name.text(), self.driver_format.text())
						obj_db_management.create_driver(driver)
						QMessageBox.information(self, 'Driver', "New driver added successfully",
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
		dialog = FrmAddDriver()
		sys.exit(dialog.exec_())
