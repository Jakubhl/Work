# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['JHV_APP_GUI_v5.py'],
    pathex=[],
    binaries=[],
    datas=[('images\\nothing.PNG', 'images'), ('images\\logo.png', 'images'), ('images\\24_both.PNG', 'images'), ('images\\24_cam.PNG', 'images'), ('images\\25basic.PNG', 'images'), ('images\\24_func.PNG', 'images'), ('images\\dirs_ba.PNG', 'images'), ('images\\more_dirs.PNG', 'images'), ('images\\24_type.PNG', 'images'), ('images\\directories.png', 'images'), ('images\\JHV.ico', 'images'), ('c:\\users\\kubah\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.10_qbz5n2kfra8p0\\localcache\\local-packages\\python310\\site-packages/customtkinter', 'customtkinter/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JHV_APP_GUI_v5',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\JHV.ico'],
)
