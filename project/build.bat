@echo off
REM Batch Build Script for Windows Installer
REM Creates PyInstaller executable and optional NSIS installer

setlocal enabledelayedexpansion

echo.
echo ==================================================
echo   Steganography App - Windows Build Script
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/
    pause
    exit /b 1
)

REM Step 1: Install build dependencies
echo [1/4] Installing PyInstaller...
python -m pip install --upgrade pyinstaller -q
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo OK: PyInstaller installed
echo.

REM Step 2: Clean previous builds
echo [2/4] Cleaning previous builds...
if exist build rmdir /s /q build >nul 2>&1
if exist dist rmdir /s /q dist >nul 2>&1
echo OK: Previous builds cleaned
echo.

REM Step 3: Build executable
echo [3/4] Building executable with PyInstaller...
REM Use the spec file for complete configuration including hidden imports
pyinstaller --clean SteganographyApp.spec
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)
echo OK: Executable built successfully
echo.

REM Step 4: Create NSIS installer (if NSIS is installed)
echo [4/4] Creating NSIS Installer...

set "NSIS_PATH="
if exist "C:\Program Files\NSIS\makensis.exe" (
    set "NSIS_PATH=C:\Program Files\NSIS\makensis.exe"
) else if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set "NSIS_PATH=C:\Program Files (x86)\NSIS\makensis.exe"
)

if "%NSIS_PATH%"=="" (
    echo.
    echo WARNING: NSIS not found. Installer will not be created.
    echo To create a Windows installer:
    echo   1. Download NSIS from: https://nsis.sourceforge.io/Download
    echo   2. Install with 'Full Installation' option
    echo   3. Run this script again
    echo.
    echo Executable is ready at: dist\SteganographyApp\SteganographyApp.exe
) else (
    echo Found NSIS at: !NSIS_PATH!
    "!NSIS_PATH!" /v3 /DCURRENT_BUILDDIR="%cd%" "build_installer.nsi"
    if errorlevel 1 (
        echo WARNING: NSIS build encountered an issue
        echo Executable is still available at: dist\SteganographyApp\SteganographyApp.exe
    ) else (
        echo OK: Installer created successfully
        echo Installer: SteganographyApp_Installer.exe
    )
)

echo.
echo ==================================================
echo   Build Complete!
echo ==================================================
echo.
echo Output files:
echo   - Executable: dist\SteganographyApp\SteganographyApp.exe
if exist "SteganographyApp_Installer.exe" (
    echo   - Installer: SteganographyApp_Installer.exe
)
echo.
pause
echo.

echo ==================================================
echo   Build Complete!
echo ==================================================
echo.
pause
