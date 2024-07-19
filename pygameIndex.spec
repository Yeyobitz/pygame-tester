# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pygameIndex.py'],
    pathex=['C:\\Users\\Yeyo\\Programacion\\pygame-tester'],
    binaries=[],
    datas=[
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\archer.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\background1.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\background2.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\background3.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\background_music.mp3', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\bow.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\cape1.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\cape2.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\cape3.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\cat.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\enemy.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\game_data.db', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\hat1.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\hat2.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\hat3.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\helmet1.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\helmet2.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\helmet3.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\mage.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\menu_background.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\projectile_bow.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\projectile_staff.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\projectile_sword.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\staff.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\sword.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\tower.png', 'Assets'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\Assets\\warrior.png', 'Assets')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pygameIndex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pygameIndex'
)
