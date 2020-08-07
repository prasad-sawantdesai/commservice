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

		def select_all_connections(self, plcfilter = None):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				if plcfilter is None:
						cur.execute("SELECT * FROM connection")
				else:
						cur.execute("SELECT * FROM connection where plcid=\"" + str(plcfilter) + "\"")
				rows = cur.fetchall()

				return rows

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

		def select_settings(self):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM settings")

				rows = cur.fetchall()

				return rows

		def select_controller_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM controller where id=\"" + str(id) + "\"")

				rows = cur.fetchall()

				return rows

		def select_connection_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM connection where id=\"" + str(id) + "\"")

				rows = cur.fetchall()

				return rows

		def select_taggroup_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				# select taggroups.id, taggroups.name,controller.name,machine.name,taggroups.collection_method, taggroups.collection_type   from taggroups, controller, machine where taggroups.plcid = controller.id and taggroups.machineid = machine.id
				cur.execute("SELECT taggroups.id, taggroups.name,controller.name,machine.name,taggroups.collection_method, taggroups.collection_type FROM taggroups, controller, machine where taggroups.id=" + str(id) + " and taggroups.plcid = controller.id and taggroups.machineid = machine.id")

				rows = cur.fetchall()

				return rows

		def select_machine_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("SELECT * FROM machine where id=\"" + str(id) + "\"")

				rows = cur.fetchall()

				return rows

		def update_controller_by_id(self, controller_info, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("UPDATE controller SET name=\"" + controller_info[0] + "\", description=\"" + controller_info[1] + "\" WHERE id=" + str(id) )
				self.connection.commit()
				return cur.lastrowid

		def update_settings(self, settings_info):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("UPDATE settings SET mongodbconnection=\"" + settings_info + "\"")
				self.connection.commit()
				return cur.lastrowid

		def update_taggroup_by_id(self, taggroup_info, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("UPDATE taggroups SET name=\"" + taggroup_info[0] + "\", plcid=" + str(taggroup_info[1]) + " ,machineid=" + str(taggroup_info[2]) + ", collection_method=" + str(taggroup_info[3]) + ", collection_type=\"" + taggroup_info[4] + "\" WHERE id=" + str(id) )
				self.connection.commit()
				return cur.lastrowid

		def update_machine_by_id(self, machine_info, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("UPDATE machine SET name=\"" + machine_info[0] + "\", manualid=" + str(machine_info[1]) + ", plcid=" + str(machine_info[2]) + " WHERE id=" + str(id) )
				self.connection.commit()
				return cur.lastrowid

		def update_connection_by_id(self, connection_info, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("UPDATE connection SET connection_string=\"" + connection_info[0] + "\", driverid=\"" + str(connection_info[1]) + "\", plcid=\"" + str(connection_info[2]) + "\" WHERE id=" + str(id))
				self.connection.commit()
				return cur.lastrowid

		def delete_controller_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				sql = "DELETE from controller WHERE id=?"
				cur.execute(sql, (id,))
				self.connection.commit()
				return cur.lastrowid

		def delete_taggroup_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				sql = "DELETE from taggroups WHERE id=?"
				cur.execute(sql, (id,))
				self.connection.commit()
				return cur.lastrowid

		def delete_machine_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				sql = "DELETE from machine WHERE id=?"
				cur.execute(sql, (id,))
				self.connection.commit()
				return cur.lastrowid

		def delete_connection_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				sql = "DELETE from connection WHERE id=?"
				cur.execute(sql, (id,))
				self.connection.commit()
				return cur.lastrowid

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

		def select_all_tags_for_display(self, filter=None):
				cur = self.connection.cursor()
				if filter is None:
						cur.execute("select tags.id as 'ID', tags.name as 'TagName' ,controller.name as 'Controller Name', machine.name as 'Machine Name',register_types.ragister_type as 'Register Type', tags.data_type as 'Data type' from tag_group_mapping, taggroups, tags, controller, machine, register_types where tag_group_mapping.tag_group_id = taggroups.id and tags.id = tag_group_mapping.tag_id and taggroups.plcid=controller.id and taggroups.machineid=machine.id and tags.register_typeid=register_types.id")
				else:
						cur.execute("select tags.id as 'ID', tags.name as 'TagName' ,controller.name as 'Controller Name', machine.name as 'Machine Name',register_types.ragister_type as 'Register Type', tags.data_type as 'Data type' from tag_group_mapping, taggroups, tags, controller, machine, register_types where tag_group_mapping.tag_group_id = taggroups.id and tags.id = tag_group_mapping.tag_id and taggroups.plcid=controller.id and taggroups.machineid=machine.id and tags.register_typeid=register_types.id and taggroups.id=\"" + str(filter) + "\"")
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

		def get_tag_group_name(self, id):
				cur = self.connection.cursor()
				cur.execute("SELECT taggroups.name FROM taggroups where id=" + str(id))

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

		def select_tag_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("select tags.id as 'ID',tags.name as 'Name',register_types.ragister_type as 'RegisterType', tags.address as 'Address', tags.scaling as 'Scaling', tags.data_type as 'DataType',tags.data_size as 'DataSize' from tags,register_types where register_types.id = tags.register_typeid and tags.id=" + str(id) )

				rows = cur.fetchall()

				return rows

		def delete_tag_by_id(self, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				sql = "DELETE from tags WHERE id=?"
				cur.execute(sql, (id,))
				self.connection.commit()
				return cur.lastrowid

		def delete_tagmapping_by_taggroupid(self, taggroupid):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				sql = "DELETE from tag_group_mapping WHERE tag_group_id=?"
				cur.execute(sql, (taggroupid,))
				self.connection.commit()
				return cur.lastrowid

		def update_tag_by_id(self, tag_info, id):
				"""
				Query all rows in the tasks table
				:param conn: the Connection object
				:return:
				"""
				cur = self.connection.cursor()
				cur.execute("UPDATE tags SET name=\"" + tag_info[0] + "\", register_typeid=" + str(tag_info[1]) + ", address=" + str(tag_info[2]) + ", scaling=" + str(tag_info[3]) + ", data_type=\"" + str(tag_info[4]) + "\", data_size=" + str(tag_info[5]) + " WHERE id=" + str(id))
				self.connection.commit()
				return cur.lastrowid