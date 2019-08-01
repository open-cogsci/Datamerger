# -*- coding: utf-8 -*-
"""
Datamerger is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Datamerger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Refer to <http://www.gnu.org/licenses/> for a copy of the GNU General Public License.

@author Daniel Schreij
"""

import sys
import os
import sheet_io_tools
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtWebKit import QWebView

version = "1.0.4"
author = "Daniel Schreij"
email = "d.schreij@vu.nl"

aboutString = """
Datamerger v{0}

Copyright 2013-2014
{1}
{2}
""".format(version,author,email)

def get_resource_loc(item):
	"""
	Determines the correct path to the required resource.
	When the app is packaged with py2exe or py2app, the locations of some images
	or resources may change. This function should correct for that


	Arguments:
		item (string)  - the item to locate

	Returns:
		(string) - the full path to the provided item

	"""

	# When the app is packaged with py2app/exe or pyinstaller
	if getattr(sys, 'frozen', None):
		try:
			# If packaged with pyinstaller
			basedir = sys._MEIPASS
			return os.path.join(basedir,item)
		except:
			# If packaged with py2exe (but should also work for py2installer (not tested!) )
			basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
			if sys.platform == "win32":
				return os.path.join(basedir, "resources", item)
			elif sys.platform == "darwin":
				return os.path.join(basedir, "..", "Resources", "resources", item)

	# For Linux when installed through a repo
	elif os.name == 'posix' and os.path.exists('/usr/share/datamerger/resources/'):
		return os.path.join('/usr/share/datamerger/resources/', item)
	# When run from source
	else:
		basedir = os.path.dirname(__file__)
		return os.path.join(basedir,"..","resources",item)

class OutLog:
	"""
	Class that intercepts stdout and stderr prints, and shows them in te QT
	textarea of the app.
	"""
	def __init__(self, statusBox, out=None, color=None):
		"""(statusBox, out=None, color=None) -> can write stdout, stderr to a
		QTextEdit.
		edit = QTextEdit
		out = alternate stream ( can be the original sys.stdout )
		color = alternate color (i.e. color stderr a different color)
		"""
		self.statusBox = statusBox
		self.out = out
		self.color = color

	def write(self, m):
		self.statusBox.moveCursor(QtGui.QTextCursor.End)
		if self.color:
			self.statusBox.setTextColor(self.color)

		self.statusBox.insertPlainText( m )
		# Make sure the messages are immediately shown
		QtCore.QCoreApplication.instance().processEvents()

		if self.out:
			self.out.write(m)


class DataMergerUI(QtGui.QMainWindow):
	"""
	QT User interface
	"""
	def __init__(self):
		app = QtGui.QApplication(sys.argv)
		self.ui = self._initUI()
		sys.exit(app.exec_())

	def _initUI(self):
		"""
		Initializes the UI and sets button actions
		"""
		QtGui.QMainWindow.__init__(self)

		# Load resources
		ui_path = get_resource_loc("datamerger.ui")
		ico_path = get_resource_loc("datamerger.png")
		helpimg_path = get_resource_loc("help-about.png")
		aboutimg_path = get_resource_loc("help-contents.png")
		# icons
		self.help_icon = QtGui.QIcon(helpimg_path)
		self.about_icon = QtGui.QIcon(aboutimg_path)

		# Load and setup UI
		ui = uic.loadUi(ui_path)
		ui.setWindowIcon(QtGui.QIcon(ico_path))
		ui.setFixedSize(530,303)
		self.center()
		ui.setWindowTitle('Data merger')
		ui.docButton.setIcon(self.help_icon)
		ui.aboutButton.setIcon(self.about_icon)
		ui.statusBox.setReadOnly(True)
		ui.show()

		# Set button actions
		self.connect(ui.inputFolderButton, QtCore.SIGNAL("clicked()"), self.selectInputFolder)
		self.connect(ui.outputFileButton, QtCore.SIGNAL("clicked()"), self.selectOutputDestination)
		self.connect(ui.mergeButton, QtCore.SIGNAL("clicked()"), self.startMerge)
		self.connect(ui.docButton, QtCore.SIGNAL("clicked()"), self.showDocWindow)
		self.connect(ui.aboutButton, QtCore.SIGNAL("clicked()"), self.showAboutWindow)

		# Redirect console output to textbox in UI, printing stdout in black
		# and stderr in red
		sys.stdout = OutLog(ui.statusBox, sys.stdout, QtGui.QColor(0,0,0))
		if not hasattr(sys,'frozen'):
			sys.stderr = OutLog(ui.statusBox, sys.stderr, QtGui.QColor(255,0,0))
		else:
			sys.stderr = OutLog(ui.statusBox, None, QtGui.QColor(255,0,0))
		print ""

		# The folders to read data files from
		self.sourceFolder = ""
		# the folder to write the output file to
		self.destinationFile = ""

		self._lastSelectedDestDir = ""
		self._lastSelectedSourceDir = ""

		return ui

	def center(self):
		"""
		Centers the main app window on the screen
		"""
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def selectInputFolder(self):
		"""
		Select folder to read csv files from
		"""
		selectedFolder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.ui.inputFolderLocation.text()))
		# Prevent erasing previous entry on cancel press
		if selectedFolder:
			self.sourceFolder = selectedFolder
			self.ui.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
			self.ui.progressBar.setValue(0)

	def selectOutputDestination(self):
		"""
		Set file to write output to
		"""
		selectedDest = QtGui.QFileDialog.getSaveFileName(self,"Save output as..",self.ui.outputFileDestination.text(),"*.csv; *.xls; *.xlsx")
		# Prevent erasing previous entry on cancel press
		if selectedDest:
			self.destinationFile = selectedDest
			self.ui.outputFileDestination.setText(os.path.normpath(str(self.destinationFile)))
			self.ui.progressBar.setValue(0)

	def startMerge(self):
		"""
		Starts the merge operation. Uses sheet_io_tools for this.
		"""
		if self.sourceFolder == "":
			print >> sys.stderr, "Please select a source folder containing the data files to merge."
		elif self.destinationFile == "":
			print >> sys.stderr, "Please specify a filename to save the merged data with."
		else:
			print "Starting Merge operation..."
			mergedDataset = sheet_io_tools.mergeFolder(self.sourceFolder, self.destinationFile, self.ui)
			if mergedDataset:
				print "Output saved to " + self.destinationFile
				print "Ready."

	def showDocWindow(self):
		"""
		Shows documentation window (with help and licensing info)
		"""
		self.docWindow = QWebView()
		self.docWindow.closeEvent = self.closeDocWindow
		self.docWindow.setWindowTitle("Documentation")
		self.docWindow.setWindowIcon(self.help_icon)
		self.docWindow.load(QtCore.QUrl(get_resource_loc("helpfile.html")))
		self.docWindow.show()

	def closeDocWindow(self,source):
		"""
		Callback function of the docWindow QWebView item.
		Destroys reference to doc window after its closed
		"""
		del(self.docWindow)

	def showAboutWindow(self):
		"""
		Shows about window
		"""
		global aboutstring
		msgBox = QtGui.QMessageBox(self)
		msgBox.setWindowIcon(self.about_icon)
		msgBox.about(msgBox,"About",aboutString)