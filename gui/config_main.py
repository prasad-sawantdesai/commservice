#!/usr/bin/env python
# -*- coding: ascii -*-
from PySide2 import QtGui, QtCore
from PySide2.QtCore import QObject

from PySide2.QtWidgets import QMainWindow, QApplication, QSplashScreen



import sys
import os
import time
import logging

from config_view import ConfigView

logger = logging.getLogger(__name__)


class ConfigMain(QMainWindow):
	""" Wrapper class for setting the main window"""

	def __init__(self):
		super(ConfigMain, self).__init__()
		self.window = QMainWindow()


		view = ConfigView()
		# model = MarsModel()

		# set logger
		setup_logger(False)
		ui_log_handler = Handler(self)
		logging.getLogger().addHandler(ui_log_handler)
		logging.getLogger().setLevel(logging.DEBUG)
		ui_log_handler.signal_log_message__to_ui_sender.connect(view.append_summary)

		logger.info('Application is started')

		# create presenter
		# self.presenter = MarsPresenter(view, model)

		# set the view for the main window
		self.setCentralWidget(view)
		view.showMaximized()
		self.set_window_properties()

	def set_window_properties(self):
		"""
		set window properties
		Returns
		-------

		"""
		self.setWindowTitle("EnSeGi-0.7.6_2020_05_07_13_22_48")
		self.setWindowIcon(QtGui.QIcon(
				r'resources\mars-icon_32.png'))
		self.showMaximized()


def setup_logger(is_debugging_needed):
	if not os.path.exists(r'logs'):
		os.makedirs(r'logs')
	# setup file logger
	log_filename = r".\logs\ensegi_" + time.strftime("%Y%m%d_%H%M%S") + \
				   ".log"
	debugging_option = logging.INFO

	if is_debugging_needed is True:
		debugging_option = logging.DEBUG
	logging.basicConfig(filename = log_filename, format = '%(asctime)s, '
														  '[%(levelname)s], '
														  '%(name)s, '
														  '%(message)s',
						level = logging.DEBUG)

	# setup console logger
	console = logging.StreamHandler()
	console.setLevel(debugging_option)
	formatter = logging.Formatter('%(asctime)s, ' '[%(levelname)s], '
								  '%(name)s:, %(message)s')
	console.setFormatter(formatter)

	logging.getLogger('').addHandler(console)

	# Suppress warnings in weasyprint & matplotlib.font_manager modules
	logging.getLogger('weasyprint').setLevel(logging.CRITICAL)
	logging.getLogger('matplotlib.font_manager').setLevel(logging.CRITICAL)

class Handler(QObject, logging.Handler):

# 	signal_log_message__to_ui_sender = pyqtSignal(object)

	def __init__(self, parent):
		super().__init__(parent)
		super(logging.Handler).__init__()
		formatter = Formatter('%(asctime)s|%(levelname)s|%(message)s|', '%d/%m/%Y %H:%M:%S')
		self.setFormatter(formatter)

	def emit(self, record):
		if record.levelno == logging.DEBUG:
			return
		log_message = self.format(record)
		self.signal_log_message__to_ui_sender.emit(log_message)


class Formatter(logging.Formatter):
	def formatException(self, ei):
		result = super(Formatter, self).formatException(ei)
		return result

	def format(self, record):
		result = super(Formatter, self).format(record)
		if record.exc_text:
			result = result.replace('\n', '')
		return result

# https://stackoverflow.com/questions/42621528/why-python-console-in
# -pycharm
# -doesnt-show-any-error-message-when-pyqt-is-used
old_hook = sys.excepthook

def catch_exceptions(exception_class, exception_instance, traceback):
	"""
	raise custom exception without crashing the app
	Parameters
	----------
	exception_class
	exception_instance
	traceback

	Returns
	-------

	"""
	logging.exception("Uncaught exception", exc_info=(exception_class,
													  exception_instance,
													  traceback))
	old_hook(exception_class, exception_instance, traceback)

sys.excepthook = catch_exceptions
if __name__ == "__main__":

	app = QApplication(sys.argv)
	app.setOrganizationName("Design X")
	app.setOrganizationDomain("")
	app.setApplicationName("EnSeGi")
	# for the splash screen
	splash_pix = QtGui.QPixmap("resources\\splash_screen.png")
	# Creates the splash screen
	splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	# shows splash screen
	splash.show()
	app.processEvents()
	time.sleep(2)
	# Creates the object of ENSEGIBackend
	window = ConfigMain()
	# shows the GUI
	window.show()
	# closes the splash screen
	splash.finish(window)

	sys.exit(app.exec_())
