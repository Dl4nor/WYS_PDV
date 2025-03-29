# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app\\main.py'],  # Entrada do script principal
    pathex=[],
    binaries=[],  # Nenhum binário extra
    datas=[
        ('app/assets', 'app/assets'),  # Assets embutidos no executável
        ('app/models', 'app/models'),
        ('app/controller', 'app/controller'),
        ('app/services', 'app/services'),
        ('app/utils', 'app/utils'),
        ('app/view', 'app/view'),
    ],
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
    a.datas,  # Embutir arquivos de dados
    [],
    name='WYS_PDV',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprimir para reduzir tamanho
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Não exibe o console, caso não precise
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app\\assets\\icons\\wys_real.ico'],  # Ícone do aplicativo
)
