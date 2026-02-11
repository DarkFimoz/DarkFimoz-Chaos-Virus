@echo off
chcp 65001 >nul
echo ============================================================
echo Установка всех зависимостей и создание EXE
echo ============================================================
echo.

echo Шаг 1: Установка всех библиотек...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Шаг 2: Создание EXE файла...
echo.

python -m PyInstaller --onefile --noconsole --name=Virus --add-data="sounds.mp3;." --hidden-import=PIL._tkinter_finder --hidden-import=win32gui --hidden-import=win32con --hidden-import=win32api --hidden-import=pygame --hidden-import=mutagen --collect-all=pygame --collect-all=PIL virus.py

echo.
echo ============================================================
echo ГОТОВО!
echo EXE файл: dist\Virus.exe
echo ============================================================
echo.
pause
