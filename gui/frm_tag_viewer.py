import os
import sys
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QSortFilterProxyModel

from PySide2.QtGui import QIcon, Qt, QPixmap, QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QFrame, QVBoxLayout, QGroupBox, QHBoxLayout, QSizePolicy, QSpacerItem, QPushButton, \
		QLabel, QLineEdit, QTreeView, QAbstractItemView, QAction, QApplication, QMenu, QMessageBox

from app.presenter.view.frm_add_tags import FrmAddTags
from app.presenter.view.frm_edit_tags import FrmEditTags
from app.presenter.view.frm_tag_mapping import FrmTagMapping
from app.utilities.database_management import DatabaseManagement

application_path=""
if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
elif __file__:
		application_path = os.path.dirname(__file__)

IMAGE_DIRECTORY = os.path.join(application_path, "resources")


class FrmTagViewer(QFrame):

		def __init__(self):
				super(FrmTagViewer, self).__init__()
				self.selected_item_id= None
				vboxlayout_tag_viewer = QVBoxLayout()
				vboxlayout_tag_viewer.setSpacing(0)
				vboxlayout_tag_viewer.setContentsMargins(1, 1, 1, 1)

				# <editor-fold desc="Treeview operations">
				gbox_treeview_operations = QGroupBox('')
				hboxlayout_treeview_operation = QHBoxLayout()
				hboxlayout_treeview_operation.setContentsMargins(1, 1, 1, 1)

				self.pbutton_load = QPushButton("Refresh")
				self.pbutton_load.setToolTip('Refresh Tags')
				self.pbutton_load.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'refresh_16.png')))
				self.pbutton_load.clicked.connect(self.load_tags)

				hboxlayout_treeview_operation.addWidget(self.pbutton_load, 0, Qt.AlignVCenter)

				self.pbutton_expand = QPushButton("")
				self.pbutton_expand.setToolTip('Expand tag groups')
				self.pbutton_expand.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'tree_expand_24.png')))
				self.pbutton_expand.clicked.connect(self.expand_treeview_items)
				hboxlayout_treeview_operation.addWidget(self.pbutton_expand, 0, Qt.AlignVCenter)

				self.pbutton_collapse = QPushButton("")
				self.pbutton_collapse.setToolTip('Collapse tag groups')
				self.pbutton_collapse.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'tree_collapse_24.png')))
				self.pbutton_collapse.clicked.connect(self.collapse_treeview_items)
				hboxlayout_treeview_operation.addWidget(self.pbutton_collapse, 0, Qt.AlignVCenter)

				self.pbutton_clear_view = QPushButton("")
				self.pbutton_clear_view.setToolTip('Clear view')
				self.pbutton_clear_view.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'clear_24.png')))
				self.pbutton_clear_view.clicked.connect(self.clear_signals)
				hboxlayout_treeview_operation.addWidget(self.pbutton_clear_view, 0, Qt.AlignVCenter)

				self.pbutton_add_tag = QPushButton("")
				self.pbutton_add_tag.setToolTip('Add tag')
				self.pbutton_add_tag.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'plus_16.png')))
				self.pbutton_add_tag.clicked.connect(self.show_frm_add_tags)
				hboxlayout_treeview_operation.addWidget(self.pbutton_add_tag, 0, Qt.AlignVCenter)

				self.pbutton_tag_mapping = QPushButton("")
				self.pbutton_tag_mapping.setToolTip('Do Tag Mapping')
				self.pbutton_tag_mapping.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'mapping_16.png')))
				self.pbutton_tag_mapping.clicked.connect(self.show_frm_add_tag_mapping)
				hboxlayout_treeview_operation.addWidget(self.pbutton_tag_mapping, 0, Qt.AlignVCenter)

				self.label_taggroup = QLabel("No group selection yet")
				hboxlayout_treeview_operation.addWidget(self.label_taggroup, 1, Qt.AlignVCenter)
				horizontal_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding)
				hboxlayout_treeview_operation.addItem(horizontal_spacer)

				gbox_treeview_operations.setLayout(hboxlayout_treeview_operation)
				vboxlayout_tag_viewer.addWidget(gbox_treeview_operations)
				# </editor-fold>

				# <editor-fold desc="Signal Filter">
				gbox_tag_filter = QGroupBox('')
				hboxlayout_tag_filter = QHBoxLayout()
				hboxlayout_tag_filter.setSpacing(0)
				hboxlayout_tag_filter.setContentsMargins(1, 1, 1, 1)
				lbl_tag_name = QLabel("")
				lbl_tag_name.setPixmap(QPixmap(os.path.join(IMAGE_DIRECTORY, 'search_24.png')))

				hboxlayout_tag_filter.addWidget(lbl_tag_name, 0, Qt.AlignVCenter)
				lbl_spacer = QLabel("")
				hboxlayout_tag_filter.addWidget(lbl_spacer, 0, Qt.AlignVCenter)

				self.tag_name = QLineEdit()
				self.tag_name.setToolTip('Provide tag filter expression here')
				self.tag_name.textEdited.connect(self.search_text_changed)
				hboxlayout_tag_filter.addWidget(self.tag_name, 0, Qt.AlignVCenter)

				self.pbutton_tag_filter_clear = QPushButton("")
				self.pbutton_tag_filter_clear.setToolTip('Clear Filter')
				self.pbutton_tag_filter_clear.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'clear_filter_24.png')))
				self.pbutton_tag_filter_clear.setMinimumWidth(50)
				self.pbutton_tag_filter_clear.pressed.connect(self.clear_filter)
				hboxlayout_tag_filter.addWidget(self.pbutton_tag_filter_clear, 0, Qt.AlignVCenter)

				self.pbutton_tag_filter_match_case = QPushButton("Aa")
				self.pbutton_tag_filter_match_case.setToolTip('Set match case on/off')
				self.pbutton_tag_filter_match_case.setMaximumWidth(50)
				self.pbutton_tag_filter_match_case.setCheckable(True)
				self.pbutton_tag_filter_match_case.clicked.connect(lambda: self.search_text_changed())
				hboxlayout_tag_filter.addWidget(self.pbutton_tag_filter_match_case, 0, Qt.AlignVCenter)

				self.pbutton_tag_filter_regular_exp = QPushButton("RegEx")
				self.pbutton_tag_filter_regular_exp.setToolTip('Set regular expression on/off')
				self.pbutton_tag_filter_regular_exp.setMaximumWidth(80)
				self.pbutton_tag_filter_regular_exp.setCheckable(True)
				self.pbutton_tag_filter_regular_exp.clicked.connect(lambda: self.search_text_changed())
				hboxlayout_tag_filter.addWidget(self.pbutton_tag_filter_regular_exp, 0, Qt.AlignVCenter)

				gbox_tag_filter.setLayout(hboxlayout_tag_filter)

				vboxlayout_tag_viewer.addWidget(gbox_tag_filter)
				# </editor-fold>

				# <editor-fold desc="Treeview control">
				self.treeview_tags = QTreeView()

				self.treeview_tags.setSortingEnabled(True)
				self.treeview_tags.header().setStretchLastSection(True)
				self.treeview_tags.setAlternatingRowColors(True)

				self.treeview_tags.setSelectionMode(QAbstractItemView.SingleSelection)

				self.treeview_tags.setHeaderHidden(False)
				self.treeview_tags_model = QStandardItemModel()
				self.treeview_tags_model.setHorizontalHeaderLabels(['Tag Name', 'Controller', 'Machine', 'Register Type', 'Data Type','Tag ID'])
				self.treeview_tags.setColumnWidth(5, 2000)
				# Make proxy model to allow seamless filtering
				self.proxy_model = CustomProxyModel()
				self.proxy_model.setSourceModel(self.treeview_tags_model)
				self.proxy_model.sort(0)
				self.treeview_tags.setModel(self.proxy_model)

				vboxlayout_tag_viewer.addWidget(self.treeview_tags)

				# </editor-fold>

				self.setLayout(vboxlayout_tag_viewer)

				# <editor-fold desc="Context menu actions">

				self.action_edit_tag = QAction("Edit Tag ", self, triggered = self.edit_tag_by_id)
				self.action_edit_tag.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'edit_16.png')))

				self.action_delete_tag = QAction("Delete Tag ", self, triggered = self.delete_tag_by_id)
				self.action_delete_tag.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'delete_16.png')))
				# </editor-fold>

				self.selected_tag = None
				self.selected_taggroup_id = '*'
				return

		def show_frm_add_tags(self):
				dialog = FrmAddTags()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def show_frm_add_tag_mapping(self):
				dialog = FrmTagMapping()
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def edit_tag_by_id(self):
				dialog = FrmEditTags(self.selected_item_id)
				dialog.setModal(True)
				dialog.show()
				dialog.exec_()

		def delete_tag_by_id(self):
				obj_db_management = DatabaseManagement.get_instance()
				obj_db_management.delete_tag_by_id(self.selected_item_id)
				QMessageBox.information(self, 'Tag', "Tag deleted successfully",
																QMessageBox.Ok)

		def load_tags(self):
				QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
				# Clear tree model
				if self.treeview_tags_model.hasChildren():
						self.treeview_tags_model.removeRows(0, self.treeview_tags_model.rowCount())
				# Clear long device name dictionary

				root_node = self.treeview_tags_model.invisibleRootItem()
				obj_db_management = DatabaseManagement.get_instance()
				if self.selected_taggroup_id == '*':
						self.label_taggroup.setText("Showing tags from all tag groups")
						taggroups = obj_db_management.select_all_tag_groups()

						for taggroup in taggroups:
								item = QStandardItem(taggroup[1])
								item.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'taggroup_16.png')))
								item.setEditable(False)
								root_node.appendRow(item)

								tags = obj_db_management.select_all_tags_for_display(taggroup[0])
								for tag in tags:
										sub_item1 = QStandardItem(str(tag[0]))
										sub_item2 = QStandardItem(tag[1])
										sub_item3 = QStandardItem(tag[2])
										sub_item4 = QStandardItem(tag[3])
										sub_item5 = QStandardItem(tag[4])
										sub_item6 = QStandardItem(tag[5])
										sub_item2.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'tag_16.png')))
										sub_item1.setEditable(False)
										sub_item2.setEditable(False)
										sub_item3.setEditable(False)
										sub_item4.setEditable(False)
										sub_item5.setEditable(False)
										sub_item6.setEditable(False)
										sub_item1.setTextAlignment(Qt.AlignRight)
										item.appendRow([ sub_item2, sub_item3,sub_item4,sub_item5,sub_item6, sub_item1])
				else:
						taggroup_name = obj_db_management.get_tag_group_name(self.selected_taggroup_id)[0][0]
						self.label_taggroup.setText("Showing tags from " + taggroup_name)
						item = QStandardItem(taggroup_name)
						item.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'taggroup_16.png')))
						item.setEditable(False)
						root_node.appendRow(item)
						tags = obj_db_management.select_all_tags_for_display(self.selected_taggroup_id)
						for tag in tags:
								sub_item1 = QStandardItem(str(tag[0]))
								sub_item2 = QStandardItem(tag[1])
								sub_item3 = QStandardItem(tag[2])
								sub_item4 = QStandardItem(tag[3])
								sub_item5 = QStandardItem(tag[4])
								sub_item6 = QStandardItem(tag[5])
								sub_item2.setIcon(QIcon(os.path.join(IMAGE_DIRECTORY, 'tag_16.png')))
								sub_item1.setEditable(False)
								sub_item2.setEditable(False)
								sub_item3.setEditable(False)
								sub_item4.setEditable(False)
								sub_item5.setEditable(False)
								sub_item6.setEditable(False)
								sub_item1.setTextAlignment(Qt.AlignRight)
								item.appendRow([ sub_item2, sub_item3, sub_item4, sub_item5, sub_item6, sub_item1])

				self.expand_treeview_items()
				self.treeview_tags.setColumnWidth(5, 2000)
				self.proxy_model.sort(0)
				QApplication.restoreOverrideCursor()

		def expand_treeview_items(self):
				self.treeview_tags.expandAll()

		def collapse_treeview_items(self):
				self.treeview_tags.collapseAll()

		def clear_signals(self):
				if self.treeview_tags_model.hasChildren():
						self.treeview_tags_model.removeRows(0, self.treeview_tags_model.rowCount())

		def search_text_changed(self):
				"""
				Called automatically when the text in the search widget is modified.
				This method updates the RegExp and automatially filters the tree view
				according to the matching search.
				"""
				QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
				text = self.tag_name.text()
				search_type = QtCore.QRegExp.FixedString
				match_type = QtCore.Qt.CaseInsensitive

				if self.pbutton_tag_filter_regular_exp.isChecked():
						search_type = QtCore.QRegExp.RegExp

				if self.pbutton_tag_filter_match_case.isChecked():
						match_type = QtCore.Qt.CaseSensitive

				self.proxy_model.setFilterRegExp(QtCore.QRegExp(text, match_type, search_type))
				self.proxy_model.setFilterKeyColumn(0)
				self.treeview_tags.setColumnWidth(5, 2000)
				QApplication.restoreOverrideCursor()
				return

		def clear_filter(self):
				self.tag_name.clear()
				self.search_text_changed()
				self.proxy_model.sort(0)


		def contextMenuEvent(self, event):
				# Fetch item for the index fetched from the selection
				index = self.treeview_tags.selectedIndexes()[0]
				self.selected_item_id = self.treeview_tags.selectedIndexes()[5].data()
				# Get information from base model instead
				index = self.proxy_model.mapToSource(index)
				self.selected_tag = self.proxy_model.sourceModel().itemFromIndex(index)
				if self.selected_tag.parent() is not None:
						# show menu
						ctx_menu = QMenu()
						ctx_menu.addAction(self.action_edit_tag)
						ctx_menu.addAction(self.action_delete_tag)
						ctx_menu.exec_(event.globalPos())

						self.load_tags()
						# Seamless functionality for prev index
				return


class CustomProxyModel(QSortFilterProxyModel):
		"""
		Custom Proxy model used for filtering during real-time search.
		This model is needed in order to show the device's children even if the device
		itself does not match the RegExp.
		"""

		def filterAcceptsRow(self, sourceRow, sourceParent):
				"""
				Checks and accepts the row againt the RegExp.
				Reimplementing this method is needed to override the default behavior,
				which consists of not showing the node's children if the father node does
				not match the RegExp. In this new implementation, the father node (Device)
				is shown if at least one children (Signal) matches the RegExp search.
				"""
				if self.filterRegExp().isEmpty():
						# Do not filter if regular expression is empty
						return True
				else:
						# Regexpt not empty, check the node's validity
						source_index = self.sourceModel().index(sourceRow,
																										self.filterKeyColumn(),
																										sourceParent)
						if source_index.isValid():
								# Node is valid, check it's children (No pythonic iter available)
								row_number = self.sourceModel().rowCount(source_index)
								for i in range(row_number):
										if self.filterAcceptsRow(i, source_index):
												return True
								# Check the item itself.
								item_text = self.sourceModel().data(source_index, self.filterRole())
								return self.filterRegExp().indexIn(item_text) >= 0
						else:
								# Node not valid, do not show it.
								return False
