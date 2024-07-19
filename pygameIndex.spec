# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pygameIndex.py'],
    pathex=['C:\\Users\\Yeyo\\Programacion\\pygame-tester'],
    binaries=[],
    datas=[
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\archer.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\background1.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\background2.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\background3.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\background_music.mp3', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\bow.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\cape1.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\cape2.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\cape3.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\cat.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\enemy.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\game_data.db', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\hat1.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\hat2.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\hat3.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\helmet1.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\helmet2.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\helmet3.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\mage.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\menu_background.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\projectile_bow.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\projectile_staff.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\projectile_sword.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\staff.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\sword.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\tower.png', '.'),
        ('C:\\Users\\Yeyo\\Programacion\\pygame-tester\\warrior.png', '.')
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
