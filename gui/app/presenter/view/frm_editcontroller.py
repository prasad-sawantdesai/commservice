import sys

from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, \
		QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement


class FrmEditController(QDialog):

		def __init__(self, id):
				super(FrmEditController, self).__init__()
				self.id=id
				self.controller_name = QLineEdit()
				self.controller_description = QLineEdit()
				self.form_group_box = QGroupBox("Controller Information")
				self.create_from_group_box()

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.form_group_box)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)
				# self.setGeometry(100, 100, 600, 400)
				obj_db_management = DatabaseManagement.get_instance()
				row = obj_db_management.select_controller_by_id(self.id)[0]
				self.controller_name.setText(row[1])
				self.controller_description.setText(row[2])
				self.setWindowTitle("Edit Controller")

		def create_from_group_box(self):
				layout = QFormLayout()
				layout.addRow(QLabel("Controller Name:"), self.controller_name)
				layout.addRow(QLabel("Description:"), self.controller_description)
				self.form_group_box.setLayout(layout)

		def store(self):
				try:
						if self.controller_name.text() == "":
								QMessageBox.information(self, 'Controller', "Please provide controller name",
																		QMessageBox.Ok)
						else:
								obj_db_management = DatabaseManagement.get_instance()

								controller = (self.controller_name.text(), self.controller_description.text())
								obj_db_management.update_controller_by_id(controller, self.id)
								QMessageBox.information(self, 'Controller', "Controller updated successfully",
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
		dialog = FrmEditController()
		sys.exit(dialog.exec_())
