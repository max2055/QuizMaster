# -*- mode: python ; coding: utf-8 -*-
"""
QuizMaster PyInstaller Configuration
Builds single-file Windows executable
"""
import sys

block_cipher = None

# macOS Info.plist configuration (force light mode)
if sys.platform == 'darwin':
    info_plist_dict = {
        "NSRequiresAquaSystemAppearance": True,
        "CFBundleName": "QuizMaster",
        "CFBundleDisplayName": "QuizMaster",
        "CFBundleVersion": "1.5.7",
        "CFBundleShortVersionString": "1.5.7",
        "NSHighResolutionCapable": True,
    }
else:
    info_plist_dict = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('quizmaster.db', '.'),  # Include database file
    ],
    hiddenimports=[
        'PyQt6.sip',
        'pandas',
        'openpyxl',
        'python-docx',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QuizMaster',
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
    # icon='resources/icons/app.ico',  # No icon yet
    info_plist=info_plist_dict,  # macOS only
)
