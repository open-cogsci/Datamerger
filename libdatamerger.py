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

version = 1.0
author = "Daniel Schreij"
email = "d.schreij@vu.nl"

aboutString = """
Datamerger v{0}

Copyright 2013
{1}	
{2}	
""".format(version,author,email)	

def get_resource_loc(item):
	if getattr(sys, 'frozen', None):
	     basedir = sys._MEIPASS
	else:
	     basedir = os.path.dirname(__file__)
	return os.path.join(basedir,"resources",item)

class OutLog:
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
		
		self._version = 1.0
		self._author = "Daniel Schreij"

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
	def __init__(self):
		app = QtGui.QApplication(sys.argv)
		self.ui = self._initUI()	
		sys.exit(app.exec_())

	def _initUI(self):								
		QtGui.QMainWindow.__init__(self)

		# Load resources							
		ui_path = get_resource_loc("datamerger.ui")
		ico_path = get_resource_loc("datamerger.ico")
		helpimg_path = get_resource_loc("help-about.png")
		aboutimg_path = get_resource_loc("help-contents.png")		
		
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
		sys.stderr = OutLog(ui.statusBox, sys.stderr, QtGui.QColor(255,0,0))
		print ""
		
		self.sourceFolder = ""	
		self.destinationFile = ""
		
		self._lastSelectedDestDir = ""
		self._lastSelectedSourceDir = ""
	
		return ui
		
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def selectInputFolder(self):
		selectedFolder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.ui.inputFolderLocation.text()))
		# Prevent erasing previous entry on cancel press		
		if selectedFolder:
			self.sourceFolder = selectedFolder
			self.ui.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
			self.ui.progressBar.setValue(0)
	
	def selectOutputDestination(self):
		selectedDest = QtGui.QFileDialog.getSaveFileName(self,"Save output as..",self.ui.outputFileDestination.text(),".csv .xls .xlsx")
		# Prevent erasing previous entry on cancel press		
		if selectedDest:
			self.destinationFile = selectedDest
			self.ui.outputFileDestination.setText(os.path.normpath(str(self.destinationFile)))
			self.ui.progressBar.setValue(0)
			
	def startMerge(self):
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
		self.docWindow = QWebView()
		self.docWindow.closeEvent = self.closeDocWindow
		self.docWindow.setWindowTitle("Documentation")
		self.docWindow.setWindowIcon(self.help_icon)
		self.docWindow.load(QtCore.QUrl(get_resource_loc("helpfile.html")))
		self.docWindow.show()
			
	def closeDocWindow(self,source):
		del(self.docWindow)
		
	def showAboutWindow(self):
		global aboutstring
		msgBox = QtGui.QMessageBox(self)
		msgBox.setWindowIcon(self.about_icon)		
		msgBox.about(msgBox,"About",aboutString)
		#QtGui.QMessageBox.about(self,"About",aboutString)
				
	def normalOutputWritten(self, text):
		cursor = self.ui.statusBox.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.ui.statusBox.setTextCursor(cursor)
		self.ui.statusBox.ensureCursorVisible()
		
	