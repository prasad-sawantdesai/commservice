import sys

from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QLineEdit, QRadioButton, QVBoxLayout, QListWidget

from app.utilities.database_management import DatabaseManagement


class FrmAddMachine(QDialog):
		NumGridRows = 3
		NumButtons = 4

		def __init__(self):
				super(FrmAddMachine, self).__init__()

				self.setWindowTitle("Tag groups mapping")
				self.setGeometry(100, 100, 600, 400)
				# Tag group Selection
				self.group_box_tag_group_selection = QGroupBox("Tag group Selection")
				self.form_layout_tag_group_selection = QFormLayout()
				self.tag_group_collection = QComboBox()

				obj_db_management = DatabaseManagement(
								r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				tag_groups = obj_db_management.select_all_tag_groups()
				for tag_group in tag_groups:
						self.tag_group_collection.addItem(tag_group[1])

				self.form_layout_tag_group_selection.addRow(QLabel("Select Tag group to update:"), self.tag_group_collection)
				self.group_box_tag_group_selection.setLayout(self.form_layout_tag_group_selection)


				# Select tag from tags
				self.group_box_tag_selection = QGroupBox("Tag Selection")
				self.form_layout_tag_selection = QFormLayout()
				self.tag_collection = QComboBox()

				obj_db_management = DatabaseManagement(
								r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				tags = obj_db_management.select_all_tags()
				for tag in tags:
						self.tag_group_collection.addItem(tag[1])

				self.form_layout_tag_selection.addRow(QLabel("Select tag:"), self.tag_collection)

				self.group_box_tag_selection.setLayout(self.form_layout_machine_info)

				# view attached tags
				self.group_box_tag_view = QGroupBox("Tag view")
				self.form_layout_tag_view = QFormLayout()
				self.list_tag_view = QListWidget()

				obj_db_management = DatabaseManagement(
								r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				tags = obj_db_management.select_all_tag_mapping()
				for tag in tags:
						self.tag_group_collection.addItem(tag[1])

				self.form_layout_tag_view.addRow(QLabel("Tag view:"), self.list_tag_view)

				self.group_box_tag_view.setLayout(self.form_layout_tag_view)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_tag_group_selection)
				main_layout.addWidget(self.group_box_machine_info)
				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

		def store(self):
				obj_db_management = DatabaseManagement(
								r"C:\KBData\Data\Development\iot_gui_development\sqlite_db_making\commservice.db")
				plc_index = obj_db_management.get_plc_index(self.tag_group_collection.currentText())
				machine = (self.machine_name.text(), self.machine_manual_id.text(), plc_index[0][0])
				obj_db_management.create_machine(machine)

		def cancel(self):
				self.close()

if __name__ == '__main__':

		app = QApplication(sys.argv)

		dialog = FrmAddMachine()
		sys.exit(dialog.exec_())
