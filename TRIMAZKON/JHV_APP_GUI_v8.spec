# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['JHV_APP_GUI_v8.py'],
    pathex=[],
    binaries=[],
    datas=[('images\\nothing.PNG', 'images'), ('images\\logo.png', 'images'), ('images\\24_both.PNG', 'images'), ('images\\24_cam.PNG', 'images'), ('images\\25basic.PNG', 'images'), ('images\\24_func.PNG', 'images'), ('images\\2sub_vol.PNG', 'images'), ('images\\2sub_roz.PNG', 'images'), ('images\\1sub_vol.PNG', 'images'), ('images\\1sub_roz.PNG', 'images'), ('images\\nosub_roz.PNG', 'images'), ('images\\nosub_vol.PNG', 'images'), ('images\\24_type.PNG', 'images'), ('images\\directories.png', 'images'), ('images\\logo_TRIMAZKON.ico', 'images'), ('images\\loading3.png', 'images'), ('images\\jhv_logo.png', 'images'), ('C:\\Users\\jakub.hlavacek.local\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\customtkinter', 'customtkinter/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JHV_APP_GUI_v8',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\logo_TRIMAZKON.ico'],
)
