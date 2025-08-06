@echo off
REM Cleanup old
rmdir /S /Q lib 2>nul || echo Removing lib folder failed!

REM Download lib with git
git clone https://github.com/stlehmann/micropython-ssd1306 lib 2>nul || echo Git clone failed!

REM Cleanup unwanted files
del /Q /F lib\.gitignore 2>nul
del /Q /F lib\README.md 2>nul
del /Q /F lib\sdist_upip.py 2>nul
del /Q /F lib\setup.py 2>nul
rmdir /S /Q lib\.git 2>nul
