import configparser
import os


class ConfigFileReader:
	_singleton = None
	config_file_path = ""
	application_path = ""

	@staticmethod
	def get_instance():
		""" Static access method. """
		if ConfigFileReader._singleton is None:
			ConfigFileReader()
		return ConfigFileReader._singleton

	def __init__(self):
		conf = configparser.ConfigParser()
		if ConfigFileReader.config_file_path != "":
			conf.read(ConfigFileReader.config_file_path)

			self.database_path = conf.get('database', 'path')
			if ConfigFileReader._singleton is None:
				ConfigFileReader._singleton = self
