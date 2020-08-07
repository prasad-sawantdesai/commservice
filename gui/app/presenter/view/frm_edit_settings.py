import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmEditSettings(QDialog):

		def __init__(self):
				super(FrmEditSettings, self).__init__()

				# "/dev/ttyUSB0", 115200, 'N', 8, 1
				self.group_box_settings = QGroupBox("Settings")
				self.form_layout_settings = QFormLayout()
				self.mongodb_connection = QLineEdit()
				self.form_layout_settings.addRow(QLabel("MongoDB Connection:"), self.mongodb_connection)
				self.group_box_settings.setLayout(self.form_layout_settings)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_settings)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

				obj_db_management = DatabaseManagement.get_instance()
				row = obj_db_management.select_settings()[0]
				self.mongodb_connection.setText(row[0])
				self.setWindowTitle("Edit Settings")

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						settingsinfo = self.mongodb_connection.text()
						obj_db_management.update_settings(settingsinfo)
						QMessageBox.information(self, 'Settings', "Settings updated successfully",
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

		dialog = FrmEditSettings()
		sys.exit(dialog.exec_())
