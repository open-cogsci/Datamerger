# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Dropbox\Projects\PyQT Spreadsheet merger\Spreadsheetmerger.ui'
#
# Created: Wed Feb 20 17:01:40 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, uic
import sys
import os
import mergetools

class OutLog:
	def __init__(self, statusBox, out=None, color=None):
		"""(edit, out=None, color=None) -> can write stdout, stderr to a
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

		if self.out:
			self.out.write(m)
												
		
class DataMergerUI(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi("datamerger.ui")
		self.ui.setFixedSize(530,250)
		self.ui.move(300, 300)
		self.ui.setWindowTitle('Data merger')
		self.ui.setWindowIcon(QtGui.QIcon("icon.png"))
		self.ui.show()
		
		self.connect(self.ui.inputFolderButton, QtCore.SIGNAL("clicked()"), self.selectInputFolder)
		self.connect(self.ui.outputFileButton, QtCore.SIGNAL("clicked()"), self.selectOutputDestination)
		self.connect(self.ui.mergeButton, QtCore.SIGNAL("clicked()"), self.startMerge)
		
		sys.stdout = OutLog(self.ui.statusBox, sys.stdout, QtGui.QColor(0,0,0))
		sys.stderr = OutLog(self.ui.statusBox, sys.stderr, QtGui.QColor(255,0,0))
		print ""
		
		self.sourceFolder = "H:\Desktop\csv"
		self.ui.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
		
		self.destinationFile = "H:\Desktop\\test.csv"
		self.ui.outputFileDestination.setText(os.path.normpath(str(self.destinationFile)))
		
		self._lastSelectedDestDir = ""
		self._lastSelectedSourceDir = ""
	
	def selectInputFolder(self):
		selectedFolder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.ui.inputFolderLocation.text()))
		# Prevent erasing previous entry on cancel press		
		if selectedFolder:
			self.sourceFolder = selectedFolder
			self.ui.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
			self.ui.progressBar.setValue(0)
	
	def selectOutputDestination(self):
		selectedDest = QtGui.QFileDialog.getSaveFileName(self,"Save output as..",self.ui.outputFileDestination.text(),".csv .xls")
		# Prevent erasing previous entry on cancel press		
		if selectedDest:
			self.destinationFile = selectedDest
			self.ui.outputFileDestination.setText(os.path.normpath(str(self.destinationFile)))
			self.ui.progressBar.setValue(0)
			
	def startMerge(self):
		print "Starting Merge operation..."
		mergedDataset = mergetools.mergeFolder(self.sourceFolder, self.destinationFile, self.ui)
		if mergedDataset:	
			print "Output saved to " + self.destinationFile
				
	def normalOutputWritten(self, text):
		cursor = self.ui.statusBox.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.ui.statusBox.setTextCursor(cursor)
		self.ui.statusBox.ensureCursorVisible()
		
	

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = DataMergerUI()	
	sys.exit(app.exec_())
	