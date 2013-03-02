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
"""

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtWebKit import QWebView
import sys
import os
import mergetools

version = 1.0
author = "Daniel Schreij"
email = "d.schreij@vu.nl"

aboutString = """
Datamerger v{0}

Copyright 2013
{1}	
{2}	
""".format(version,author,email)	

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
		if self.color:
			self.statusBox.setTextColor(self.color)
			
		self.statusBox.moveCursor(QtGui.QTextCursor.End)
		self.statusBox.insertPlainText( m )

		if self.out:
			self.out.write(m)

		
class DataMergerUI(QtGui.QMainWindow):
	def __init__(self):								
		QtGui.QMainWindow.__init__(self)

		if getattr(sys, 'frozen', None):
		     self.basedir = sys._MEIPASS
		else:
		     self.basedir = os.path.dirname(__file__)

		# Load resources							
		ui_path = os.path.join(self.basedir, "datamerger.ui")
		ico_path = os.path.join(self.basedir, "datamerger.ico")
		helpimg_path = os.path.join(self.basedir, "help-about.png")
		aboutimg_path = os.path.join(self.basedir, "help-contents.png")		
		
		self.help_icon = QtGui.QIcon(helpimg_path)
		self.about_icon = QtGui.QIcon(aboutimg_path)
		
		# Load and setup UI
		self.ui = uic.loadUi(ui_path)
		self.ui.setWindowIcon(QtGui.QIcon(ico_path))
		self.ui.setFixedSize(530,303)
		self.center()
		self.ui.setWindowTitle('Data merger')		
		self.ui.docButton.setIcon(self.help_icon)		
		self.ui.aboutButton.setIcon(self.about_icon)	
		self.ui.show()

		# Set button actions				
		self.connect(self.ui.inputFolderButton, QtCore.SIGNAL("clicked()"), self.selectInputFolder)
		self.connect(self.ui.outputFileButton, QtCore.SIGNAL("clicked()"), self.selectOutputDestination)
		self.connect(self.ui.mergeButton, QtCore.SIGNAL("clicked()"), self.startMerge)
		self.connect(self.ui.docButton, QtCore.SIGNAL("clicked()"), self.showDocWindow)
		self.connect(self.ui.aboutButton, QtCore.SIGNAL("clicked()"), self.showAboutWindow)
		
		# Redirect console output to textbox in UI, printing stdout in black
		# and stderr in red
		sys.stdout = OutLog(self.ui.statusBox, sys.stdout, QtGui.QColor(0,0,0))
		sys.stderr = OutLog(self.ui.statusBox, sys.stderr, QtGui.QColor(255,0,0))
		print ""
		
		self.sourceFolder = ""	
		self.destinationFile = ""
		
		self._lastSelectedDestDir = ""
		self._lastSelectedSourceDir = ""
	
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
			mergedDataset = mergetools.mergeFolder(self.sourceFolder, self.destinationFile, self.ui)
			if mergedDataset:	
				print "Output saved to " + self.destinationFile
				print "Ready."
				
	def showDocWindow(self):	
		self.docWindow = QWebView()
		self.docWindow.closeEvent = self.closeDocWindow
		self.docWindow.setWindowTitle("Documentation")
		self.docWindow.setWindowIcon(self.help_icon)
		self.docWindow.load(QtCore.QUrl(os.path.normpath(os.path.join(self.basedir,'helpfile.html'))))
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
		
	
if __name__ == "__main__":
	if len(sys.argv) == 1:
		app = QtGui.QApplication(sys.argv)
		window = DataMergerUI()	
		sys.exit(app.exec_())
	elif len(sys.argv) == 2:
		if os.path.isdir(sys.argv[1]):
			mergetools.mergeFolder(sys.argv[1],"./merged_data.csv")
		else:
			print >> sys.stderr, "The specified source folder is invalid"
	elif len(sys.argv) == 3:
		if not os.path.isdir(sys.argv[1]):
			print >> sys.stderr, "The specified source folder is invalid"
		elif not os.path.isdir(os.path.split(sys.argv[2])[0]):
			print >> sys.stderr, "Invalid folder specified for output file"
		
		if os.path.splitext(sys.argv[2])[1] not in [".csv",".xls",".xlsx"]:
			sys.argv[2] += ".csv"
		
		mergetools.mergeFolder(sys.argv[1], sys.argv[2])
		
	