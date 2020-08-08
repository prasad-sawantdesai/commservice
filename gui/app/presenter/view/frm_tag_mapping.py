import sys

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, \
		QVBoxLayout, QMessageBox

from app.utilities.database_management import DatabaseManagement


class FrmTagMapping(QDialog):

		def __init__(self):
				super(FrmTagMapping, self).__init__()

				self.setWindowTitle("Tag groups mapping")
				self.mInput = QtWidgets.QListWidget()
				self.mOuput = QtWidgets.QListWidget()
				# Tag group Selection
				self.group_box_tag_group_selection = QGroupBox("Tag group Selection")
				self.form_layout_tag_group_selection = QFormLayout()
				self.tag_group_collection = QComboBox()
				obj_db_management = DatabaseManagement.get_instance()
				tag_groups = obj_db_management.select_all_tag_groups()
				for tag_group in tag_groups:
						self.tag_group_collection.addItem(str(tag_group[1]))
				self.tag_group_collection.currentTextChanged.connect(self.on_tag_group_changed)
				if self.tag_group_collection.count()>0:
						self.on_tag_group_changed()
				self.form_layout_tag_group_selection.addRow(QLabel("Select Tag group to update:"), self.tag_group_collection)
				self.group_box_tag_group_selection.setLayout(self.form_layout_tag_group_selection)

				self.group_box_tag_definition = QGroupBox("Define Tags here")
				lay = QtWidgets.QHBoxLayout(self)


				self.mButtonToSelected = QtWidgets.QPushButton(">>")
				self.mBtnMoveToAvailable = QtWidgets.QPushButton(">")
				self.mBtnMoveToSelected = QtWidgets.QPushButton("<")
				self.mButtonToAvailable = QtWidgets.QPushButton("<<")

				vlay = QtWidgets.QVBoxLayout()
				vlay.addStretch()
				vlay.addWidget(self.mButtonToSelected)
				vlay.addWidget(self.mBtnMoveToAvailable)
				vlay.addWidget(self.mBtnMoveToSelected)
				vlay.addWidget(self.mButtonToAvailable)
				vlay.addStretch()

				self.mBtnUp = QtWidgets.QPushButton("Up")
				self.mBtnDown = QtWidgets.QPushButton("Down")

				vlay2 = QtWidgets.QVBoxLayout()
				vlay2.addStretch()
				vlay2.addWidget(self.mBtnUp)
				vlay2.addWidget(self.mBtnDown)
				vlay2.addStretch()

				lay.addWidget(self.mInput)
				lay.addLayout(vlay)
				lay.addWidget(self.mOuput)
				lay.addLayout(vlay2)

				self.update_buttons_status()
				self.connections()

				self.group_box_tag_definition.setLayout(lay)

				button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
				button_box.accepted.connect(self.store)
				button_box.rejected.connect(self.cancel)

				main_layout = QVBoxLayout()
				main_layout.addWidget(self.group_box_tag_group_selection)
				main_layout.addWidget(self.group_box_tag_definition)

				main_layout.addWidget(button_box)
				self.setLayout(main_layout)

		def store(self):
				try:
						obj_db_management = DatabaseManagement.get_instance()

						tag_group_index = obj_db_management.get_tag_group_index(self.tag_group_collection.currentText())
						obj_db_management.delete_tagmapping_by_taggroupid(int(tag_group_index[0][0]))
						for selectedItem in self.get_right_elements():
								tag_index = obj_db_management.get_tag_index(selectedItem)
								mapping = (int(tag_group_index[0][0]), tag_index[0][0])

								obj_db_management.create_tag_mapping(mapping)

						QMessageBox.information(self, 'Tag Mapping', "Tag mapping done successfully",
																 QMessageBox.Ok)
				except Exception  as err:
						mb = QMessageBox()
						mb.setIcon(mb.Icon.Warning)
						mb.setText("{0}".format(err))
						mb.setWindowTitle("Error occurred")
						mb.exec_()
				self.close()

		def on_tag_group_changed(self, value=None):
				obj_db_management = DatabaseManagement()
				self.mInput.clear()
				alltags = []
				received_tags = obj_db_management.select_all_tags()
				for tag in received_tags:
						alltags.append(tag[1])

				tag_group_index = obj_db_management.get_tag_group_index(self.tag_group_collection.currentText())
				tags = obj_db_management.select_all_tags_for_display(tag_group_index[0][0])
				self.mOuput.clear()
				for tag in tags:
						self.mOuput.addItem(tag[1])
						if tag[1] in alltags:
								alltags.remove(tag[1])
				self.addAvailableItems(alltags)
		def cancel(self):
				self.close()

		def update_buttons_status(self):
				self.mBtnUp.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == 0)
				self.mBtnDown.setDisabled(
								not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == (self.mOuput.count() - 1))
				self.mBtnMoveToAvailable.setDisabled(not bool(self.mInput.selectedItems()) or self.mOuput.currentRow() == 0)
				self.mBtnMoveToSelected.setDisabled(not bool(self.mOuput.selectedItems()))

		def connections(self):
				self.mInput.itemSelectionChanged.connect(self.update_buttons_status)
				self.mOuput.itemSelectionChanged.connect(self.update_buttons_status)
				self.mBtnMoveToAvailable.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
				self.mBtnMoveToSelected.clicked.connect(self.on_mBtnMoveToSelected_clicked)
				self.mButtonToAvailable.clicked.connect(self.on_mButtonToAvailable_clicked)
				self.mButtonToSelected.clicked.connect(self.on_mButtonToSelected_clicked)
				self.mBtnUp.clicked.connect(self.on_mBtnUp_clicked)
				self.mBtnDown.clicked.connect(self.on_mBtnDown_clicked)

		# @QtCore.pyqtSlot()
		def on_mBtnMoveToAvailable_clicked(self):
				self.mOuput.addItem(self.mInput.takeItem(self.mInput.currentRow()))

		# @QtCore.pyqtSlot()
		def on_mBtnMoveToSelected_clicked(self):
				self.mInput.addItem(self.mOuput.takeItem(self.mOuput.currentRow()))

		# @QtCore.pyqtSlot()
		def on_mButtonToAvailable_clicked(self):
				while self.mOuput.count() > 0:
						self.mInput.addItem(self.mOuput.takeItem(0))

		# @QtCore.pyqtSlot()
		def on_mButtonToSelected_clicked(self):
				while self.mInput.count() > 0:
						self.mOuput.addItem(self.mInput.takeItem(0))

		# @QtCore.pyqtSlot()
		def on_mBtnUp_clicked(self):
				row = self.mOuput.currentRow()
				currentItem = self.mOuput.takeItem(row)
				self.mOuput.insertItem(row - 1, currentItem)
				self.mOuput.setCurrentRow(row - 1)

		# @QtCore.pyqtSlot()
		def on_mBtnDown_clicked(self):
				row = self.mOuput.currentRow()
				currentItem = self.mOuput.takeItem(row)
				self.mOuput.insertItem(row + 1, currentItem)
				self.mOuput.setCurrentRow(row + 1)

		def addAvailableItems(self, items):
				self.mInput.addItems(items)

		def get_left_elements(self):
				r = []
				for i in range(self.mInput.count()):
						it = self.mInput.item(i)
						r.append(it.text())
				return r

		def get_right_elements(self):
				r = []
				for i in range(self.mOuput.count()):
						it = self.mOuput.item(i)
						r.append(it.text())
				return r


if __name__ == '__main__':

		app = QApplication(sys.argv)

		dialog = FrmTagMapping()
		sys.exit(dialog.exec_())
