import os
import winshell
from win32com.client import Dispatch

# Ruta al ejecutable, la ubicación del acceso directo y el icono
script_dir = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(script_dir, 'dist', 'pygameIndex', 'pygameIndex.exe')
shortcut_path = os.path.join(script_dir, 'FantasyMichiHats.lnk')
icon_path = os.path.join(script_dir, 'Assets', 'ico.ico')

# Crear acceso directo
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = os.path.join(script_dir, 'dist', 'pygameIndex')
shortcut.IconLocation = icon_path
shortcut.save()

print(f"Acceso directo creado en: {shortcut_path}")
