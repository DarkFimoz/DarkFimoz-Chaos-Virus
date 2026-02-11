"""
Скрипт для создания EXE файла
"""
import PyInstaller.__main__
import os

# Путь к иконке (если есть)
icon_path = 'icon.ico' if os.path.exists('icon.ico') else None

# Параметры для PyInstaller
params = [
    'virus.py',                    # Главный файл
    '--onefile',                   # Один EXE файл
    '--noconsole',                 # Скрыть консоль
    '--windowed',                  # Без окон
    '--name=DarkFimoz_Virus',      # Имя EXE файла
    '--add-data=sounds.mp3;.',     # Включить музыку в EXE
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=win32gui',
    '--hidden-import=win32con',
    '--hidden-import=win32api',
    '--hidden-import=win32ui',
    '--hidden-import=pygame',
    '--hidden-import=mutagen',
    '--collect-all=pygame',
    '--collect-all=PIL',
]

# Добавить иконку если есть
if icon_path:
    params.append(f'--icon={icon_path}')

print("="*60)
print("Создание EXE файла...")
print("="*60)

# Запуск PyInstaller
PyInstaller.__main__.run(params)

print("\n" + "="*60)
print("✅ EXE файл создан в папке 'dist'!")
print("="*60)
