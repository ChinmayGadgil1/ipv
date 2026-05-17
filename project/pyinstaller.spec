# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Adaptive Encrypted Image Steganography
"""
import sys
import os
from pathlib import Path

# Get the project root directory - use current working directory when run from build.bat
if os.path.exists('app.py'):
    project_root = Path.cwd()
else:
    project_root = Path(__file__).parent

a = Analysis(
    ['app.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / 'modules'), 'modules'),
        (str(project_root / 'sample_images'), 'sample_images'),
    ],
    hiddenimports=[
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'cv2',
        'numpy',
        'numpy.core._multiarray_umath',
        'cryptography',
        'skimage',
        'skimage.metrics',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SteganographyApp',
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
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)
