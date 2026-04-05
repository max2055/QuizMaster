# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件
用于生成 Windows 单文件可执行程序
"""
import sys

block_cipher = None

# macOS Info.plist 配置（强制浅色模式）
if sys.platform == 'darwin':
    info_plist_dict = {
        "NSRequiresAquaSystemAppearance": True,
        "CFBundleName": "QuizMaster",
        "CFBundleDisplayName": "QuizMaster - 逢考必过",
        "CFBundleVersion": "1.5.5",
        "CFBundleShortVersionString": "1.5.5",
        "NSHighResolutionCapable": True,
    }
else:
    info_plist_dict = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('quizmaster.db', '.'),  # 包含数据库文件
    ],
    hiddenimports=[
        'PyQt6.sip',
        'pandas',
        'openpyxl',
        'docx',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    # icon='resources/icons/app.ico',  # 暂无图标
    info_plist=info_plist_dict,  # macOS 专用配置
)
