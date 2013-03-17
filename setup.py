#!/usr/bin/env python

"""
This file is part of datamerger.

datamerger is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

datamerger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with datamerger.  If not, see <http://www.gnu.org/licenses/>.
"""

import glob
from libdatamerger import datamerger_ui
from distutils.core import setup

setup(name="datamerger",

	version = str(datamerger_ui.version),
	description = "Merges separate spreadsheets into one large spreadsheet",
	author = "Daniel Schreij",
	author_email = "dschreij@vu.nl",
	url = "https://github.com/dschreij/Datamerger",
	scripts = ["datamerger"],
	packages = [ \
		"libdatamerger", \
		],
	package_dir = { \
		"libdatamerger" : "libdatamerger", \
		},
	data_files=[
		("/usr/share/datamerger", ["COPYING"]), \
		("/usr/share/applications", ["data/datamerger.desktop"]), \
		("/usr/share/datamerger/resources", \
			glob.glob("resources/*")),			
		]
	)
