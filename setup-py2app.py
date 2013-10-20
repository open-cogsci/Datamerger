#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

Datamerger is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Datamerger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.

This scripts builds OpenSesame as a standalone application for Mac OS.

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os
import shutil

# Clean up previous builds
try:
	shutil.rmtree("dist")
except:
	pass
try:
	shutil.rmtree("build")
except:
	pass

# Copy qt_menu.nib folder
try:
	shutil.rmtree("qt_menu.nib")
except:
	pass
shutil.copytree("/opt/local/Library/Frameworks/QtGui.framework/Resources/qt_menu.nib", "qt_menu.nib")

# Py2app doesn't like extensionless Python scripts
try:
	os.remove("datamerger.py")
except:
	pass
shutil.copyfile("datamerger", "datamerger.py")

# Build!
setup(
    app = ['datamerger.py'],
    data_files = ['datamerger.py'],
    options = {'py2app' : 
			{'argv_emulation': False, 
			 'includes' : ['PyQt4.QtCore','PyQt4.QtGui','PyQt4.QtWebKit', ],
               		 'excludes' : ['wx','pyglet','Image'],
               		 'resources' : ['resources'],
			 'iconfile' : 'resources/datamerger.icns',			
			}
		},
    setup_requires=['py2app'],
)

# Clean up qt_menu.nib
shutil.rmtree("qt_menu.nib")

# Remove datamerger.py
try:
	os.remove("datamerger.py")
except:
	pass
