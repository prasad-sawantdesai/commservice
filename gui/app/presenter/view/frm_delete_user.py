import sys
import logging
from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QMessageBox, QVBoxLayout

from app.utilities.database_management import DatabaseManagement
import internalconfig
logger = logging.getLogger(__name__)

class FrmDeleteUser(QDialog):

		def __init__(self):
				super(FrmDeleteUser, self).__init__()
				self.id = id
				# PLC Selection

				self.group_box_user_selection = QGroupBox("User Selection")
				self.form_layout_user_selection = QFormLayout()
				self.user_collection = QComboBox()

				obj_db_management = DatabaseManagement.get_instance()
				users = obj_db_management.select_all_users()
				for user in users:
						self.user_collection.addItem(user[1])

				self.form_layout_user_selection.addRow(QLabel("Select User:"), self.user_collection)

				self.group_box_user_selection.setLayout(self.form_layout_user_selection)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_user_selection)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)
				self.setWindowTitle("Delete user")

				
		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()
						logger.info(self.user_collection.currentText() + ' - User is deleting ' + " by " + internalconfig.xboard_user_name)
						user_index = obj_db_management.get_user_index(self.user_collection.currentText())
						obj_db_management.delete_user_by_id(user_index[0][0])
						QMessageBox.information(self, 'User', "User deleted successfully",
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

		dialog = FrmDeleteUser()
		sys.exit(dialog.exec_())
