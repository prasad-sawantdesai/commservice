import sqlite3
from sqlite3 import Error

from PySide2.QtWidgets import QMessageBox


class DatabaseManagement:
		_singleton = None
		db_file_path = ""

		@staticmethod
		def get_instance():
				""" Static access method. """
				if DatabaseManagement._singleton is None:
						DatabaseManagement()
				return DatabaseManagement._singleton

		def __init__(self):
				self.connection = None
				self.connect_to_db()
				if DatabaseManagement._singleton is None:
						DatabaseManagement._singleton = self

		def connect_to_db(self):
				""" create a database connection to the SQLite database
						specified by db_file
				:param db_file: database file
				:return: Connection object or None
				"""
				conn = None
				try:
						self.connection = sqlite3.connect(DatabaseManagement.db_file_path)
				except Exception  as err:
						mb = QMessageBox()
						mb.setIcon(mb.Icon.Warning)
						mb.setText("{0}".format(err))
						mb.setWindowTitle("Error occurred")
						mb.exec_()

				return conn

		def create_controller(self, controller):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO controller(name,description)
                  VALUES(?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, controller)
				self.connection.commit()
				return cur.lastrowid

		def get_plc_index(self, controller_name):
				cur = self.connection.cursor()
				cur.execute("SELECT id FROM controller where name=\"" + controller_name + "\"")

				rows = cur.fetchall()

				return rows

		def get_machine_index(self, machine_name):
				cur = self.connection.cursor()
				cur.execute("SELECT id FROM machine where name=\"" + machine_name + "\"")

				rows = cur.fetchall()

				return rows

		def create_driver(self, driver):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO driver(name,format)
                  VALUES(?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, driver)
				self.connection.commit()
				return cur.lastrowid

		def create_connection(self, connection):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO connection(connection_string,driverid, plcid)
                  VALUES(?,?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, connection)
				self.connection.commit()
				return cur.lastrowid

		def select_all_controllers(self):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM controller")

				rows = cur.fetchall()

				return rows

		def select_all_drivers(self):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM driver")

				rows = cur.fetchall()

				return rows

		def get_driver_index(self, driver_name):
				cur = self.connection.cursor()
				cur.execute("SELECT id FROM driver where name=\"" + driver_name + "\"")

				rows = cur.fetchall()

				return rows

		def create_machine(self, machine):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO machine(name,manualid, plcid)
                  VALUES(?,?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, machine)
				self.connection.commit()
				return cur.lastrowid

		def select_all_machines(self, plcfilter = None):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				if plcfilter is None:
						cur.execute("SELECT * FROM machine")
				else:
						cur.execute("SELECT * FROM machine where plcid=\"" + str(plcfilter) + "\"")
				rows = cur.fetchall()

				return rows

		def create_register_types(self, register_type):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO register_types(ragister_type,range_upper, range_lower)
                  VALUES(?,?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, register_type)
				self.connection.commit()
				return cur.lastrowid

		def select_all_register_types(self):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM register_types")

				rows = cur.fetchall()

				return rows

		def get_register_type_index(self, register_type):
				cur = self.connection.cursor()
				cur.execute("SELECT id FROM register_types where ragister_type=\"" + register_type + "\"")

				rows = cur.fetchall()

				return rows

		def create_tags(self, tag):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO tags(name,register_typeid, address, scaling, data_type, data_size)
                  VALUES(?,?,?,?,?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, tag)
				self.connection.commit()
				return cur.lastrowid

		def get_tag_index(self, tag_name):
				cur = self.connection.cursor()
				cur.execute("SELECT id FROM tags where name=\"" + tag_name + "\"")

				rows = cur.fetchall()

				return rows

		def select_all_tags(self):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM tags")

				rows = cur.fetchall()

				return rows

		def create_tag_group(self, tag_group):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO taggroups(name, plcid, machineid, collection_method, collection_type)
                  VALUES(?,?,?,?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, tag_group)
				self.connection.commit()
				return cur.lastrowid

		def select_all_tag_groups(self):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM taggroups")

				rows = cur.fetchall()

				return rows

		def select_all_tag_mapping(self, tagfilter = None):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				if tagfilter is None:
						cur.execute("SELECT * FROM tag_group_mapping")
				else:
						cur.execute("SELECT * FROM tag_group_mapping where tag_group_id=\"" + tagfilter + "\"")

				rows = cur.fetchall()

				return rows

		def create_tag_mapping(self, tag_mapping):
				"""
				Create a new project into the projects table
				:param conn:
				:param controller:
				:return: controller id
				"""
				sql = ''' INSERT INTO tag_group_mapping(tag_group_id, tag_id) VALUES(?,?) '''
				cur = self.connection.cursor()
				cur.execute(sql, tag_mapping)
				self.connection.commit()
				return cur.lastrowid

		def get_tag_group_index(self, tag_group_name):
				cur = self.connection.cursor()
				cur.execute("SELECT id FROM taggroups where name=\"" + tag_group_name + "\"")

				rows = cur.fetchall()

				return rows

		def delete_tag_mapping(self, tagfilter = None):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				if tagfilter is None:
						cur.execute("DELETE * FROM tag_group_mapping")
				else:
						cur.execute("DELETE * FROM tag_group_mapping where tag_group_id=\"" + tagfilter + "\"")

				rows = cur.fetchall()

				return rows
