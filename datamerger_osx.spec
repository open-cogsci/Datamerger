# -*- mode: python -*-
a = Analysis(['datamerger'],
             pathex=['/Users/dschreij/Dropbox/Projects/PyQT Spreadsheet merger'],
             hiddenimports=[],
             hookspath=None)
a.datas += [
('resources/datamerger.ico','resources/datamerger.ico','DATA'),
('resources/datamerger.ui','resources/datamerger.ui','DATA'),
('resources/help-about.png','resources/help-about.png','DATA'),
('resources/help-contents.png','resources/help-contents.png','DATA'),
('resources/helpfile.html','resources/helpfile.html','DATA'),
]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'datamerger'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='/resources/datamerger.ico')
	  
app = BUNDLE(exe,
	  name=os.path.join('dist', 'datamerger.app'),
          version="0.1")
