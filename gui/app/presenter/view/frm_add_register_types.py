import sys

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel, \
		QComboBox, QSpinBox, QApplication

from app.utilities.database_management import DatabaseManagement


class FrmAddRegisterTypes(QDialog):
		NumGridRows = 3
		NumButtons = 4

		def __init__(self):
				super(FrmAddRegisterTypes, self).__init__()
				self.register_type = QLineEdit()
				self.range_lower =QLineEdit()
				self.range_upper =QLineEdit()
				self.form_group_box = QGroupBox("Register Types")
				self.create_from_group_box()

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.form_group_box)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)
				self.setGeometry(100, 100, 600, 400)
				self.setWindowTitle("Add Register Types")

		def create_from_group_box(self):

				layout = QFormLayout()
				layout.addRow(QLabel("Register Type"), self.register_type)
				layout.addRow(QLabel("Range Lower:"), self.range_lower)
				layout.addRow(QLabel("Range Upper:"), self.range_upper)
				self.form_group_box.setLayout(layout)

		def store(self):
				obj_db_management = DatabaseManagement(r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				register_type = (self.register_type.text(), self.range_lower.text(), self.range_upper.text())
				obj_db_management.create_register_types(register_type)
				# self.close()
		def cancel(self):
				self.close()



if __name__ == '__main__':
		app = QApplication(sys.argv)
		dialog = FrmAddRegisterTypes()
		sys.exit(dialog.exec_())