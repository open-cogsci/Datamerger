# -*- mode: python -*-
a = Analysis(['datamerger.py'],
             pathex=['C:\\Dropbox\\Projects\\PyQT Spreadsheet merger'],
             hiddenimports=[],
             hookspath=None)
a.datas += [('datamerger.ico','datamerger.ico','DATA'),('datamerger.ui','datamerger.ui','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'datamerger.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='datamerger.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'datamerger.exe.app'))
