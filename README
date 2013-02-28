Datamerger
==========
Copyright Daniel Schreij (2013)

ABOUT
-----
Datamerger can merge separate spreadsheets into one large spreadsheet. While doing so,
it takes column names into account, and therefore can correct for small inconsistenties
between the spreadsheets to be merged (e.g. different column order, missing columns in some sheets).
It is therefore important that each file to be merged contains a header, which is a row of textual labels
at the top to identify the data in each column.
Data merger can read from and write to several formats (comma separated value lists (.csv), Excel 97-2003 (.xls)
and Excel 2007 and higher (.xlsx))


DOCUMENTATION AND INSTALLATION INSTRUCTIONS
-------------------------------------------
This is a standalone program that does not need to be installed. Make sure your 
python environment meets all dependencies specified below and that all files in
this repository are located in the same folder.

If you want to use the GUI simply run the program by

    python datamerger.py

It is also possible to use the program from CLI:

    python datamerger.py <source_folder> [<target_file>]

If a source folder (and target_file) is specified, the GUI will not be started and Datamerger will
immediately start merging the files (.csv .xls .xlsx) found in the source folder.
If a target folder is specified, the program will save the merged data to this filename.
This file will be of the type csv, xls or xlsx, depending on the extension
that was given for target_file. If only a source_folder is given and the target_file argument
is ommitted, the output will be saved to merged_data.csv


DEPENDENCIES
------------
- PyQt4 (QtGui, QtCore, uic) <http://www.riverbankcomputing.com/software/pyqt/download>
- xlrd and xlwt <http://www.python-excel.org/>
- openpyxl <https://bitbucket.org/ericgazoni/openpyxl/wiki/Home>