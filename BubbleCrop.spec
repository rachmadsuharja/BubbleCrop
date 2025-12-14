# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

hiddenimports = [
    "inference",
]

hiddenimports += collect_submodules("ultralytics")
hiddenimports += collect_submodules("torch")
hiddenimports += collect_submodules("torchvision")

hiddenimports += collect_submodules("PySide6.QtCore")
hiddenimports += collect_submodules("PySide6.QtGui")
hiddenimports += collect_submodules("PySide6.QtWidgets")

excludes = [
    "nvidia",
    "cupy",
    "onnx",
    "onnxruntime",
    "onnxruntime_gpu",
    "tensorrt",

    "PySide6.Qt3DCore",
    "PySide6.Qt3DRender",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DExtras",
    "PySide6.QtCharts",
    "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebEngineQuick",
    "PySide6.QtLocation",
    "PySide6.QtPositioning",
    "PySide6.QtQuick",
    "PySide6.QtQml",
    "PySide6.QtQuickWidgets",
]

datas = []
datas += collect_data_files("ultralytics")
datas += [
    ("models/best.pt", "models"),
    ("config.json", "."),
    ("classes.json", "."),
]

a = Analysis(
    ["src/app.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="BubbleCrop",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,   # ganti False kalau mau GUI-only
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[
        "libQt6WebEngineCore.so",
        "libQt6WebEngineWidgets.so",
    ],
    name="BubbleCrop",
)
