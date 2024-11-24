# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

# Get the root directory
root_dir = Path(SPECPATH).resolve()

# Add source directory to Python path
sys.path.append(str(root_dir))

a = Analysis(
    ['src\\main.py'],
    pathex=[str(root_dir)],
    binaries=[],
    datas=[
        (str(root_dir / 'data' / 'rank_mapping.json'), 'data'),
        (str(root_dir / 'assets' / 'icon.ico'), 'assets'),
    ],
    hiddenimports=[
        'customtkinter',
        'requests',
        'bs4',
        'pyperclip',
        'lxml',
        'json',
        'threading',
        'time',
        'pathlib',
        'tkinter',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LoL Account Manager',
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
    icon=str(root_dir / 'assets' / 'icon.ico'),
    version='file_version_info.txt'
) 