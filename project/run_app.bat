@echo off
REM Adaptive Encrypted Image Steganography - Windows Launcher
setlocal enabledelayedexpansion

echo.
echo ==================================================
echo  Adaptive Encrypted Image Steganography System
echo ==================================================
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is available in virtual environment
if exist ".venv\Scripts\python.exe" (
    echo [Running from Virtual Environment]
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo [Using System Python]
    set PYTHON_CMD=python
)

echo [Launching GUI Application...]
echo.

REM Run the app
%PYTHON_CMD% app.py

pause
