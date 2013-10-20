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

from distutils.core import setup
import py2exe
import os
import shutil

SCRIPT_NAME = "datamerger"

# Clean up previous builds
try:
	shutil.rmtree("dist")
except:
	pass
try:
	shutil.rmtree("build")
except:
	pass

# Add resources folder (containing images and such)
print os.listdir('resources')
Mydata_files = []
for files in os.listdir('resources'):
	f1 = os.path.join('resources', files)
	if os.path.isfile(f1) or os.path.splitext(f1) == ".db": # skip directories
		f2 = 'resources', [f1]
		Mydata_files.append(f2)


# Build!
setup(
	windows = [
		{
		'script': SCRIPT_NAME,
		'icon_resources' : [(1,'resources\\datamerger.ico')],	
		}
	],
	data_files = Mydata_files,
	options = {'py2exe' : 
			{
			"compressed" : True,
			"optimize": 2,
			"bundle_files": 3,
			'includes' : ['sip','PyQt4.QtCore','PyQt4.QtGui','PyQt4.QtWebKit','PyQt4.QtNetwork' ],
			'excludes' : ['wx','numpy','Image','PIL'],						
			"dll_excludes" : ["MSVCP90.DLL","libzmq.dll","icuuc50.dll"],
			}
	}
)