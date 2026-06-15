@echo off
echo Building RenPyTranslator.exe...
python -m PyInstaller --clean --onefile --windowed --name RenPyTranslator --paths src src/main.py
echo Build finished.
pause
