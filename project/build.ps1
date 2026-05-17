# PowerShell Build Script for Windows Installer
# This script builds the PyInstaller executable and creates an NSIS installer
# Usage: .\build.ps1

Write-Host "=================================================="
Write-Host "  Steganography App - Windows Build Script"
Write-Host "=================================================="
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "WARNING: This script should be run as Administrator for best results" -ForegroundColor Yellow
}

# Step 1: Install build dependencies
Write-Host "[1/5] Installing build dependencies..."
if ($PSVersionTable.PSVersion.Major -lt 3) {
    Write-Host "ERROR: PowerShell 3.0 or higher required" -ForegroundColor Red
    Exit 1
}

# Install PyInstaller
python -m pip install --upgrade pyinstaller -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
    Exit 1
}
Write-Host "✓ Build dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 2: Clean previous builds
Write-Host "[2/5] Cleaning previous builds..."
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue
    Write-Host "  - Removed build directory"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue
    Write-Host "  - Removed dist directory"
}
Write-Host "✓ Previous builds cleaned" -ForegroundColor Green
Write-Host ""

# Step 3: Build executable with PyInstaller
Write-Host "[3/5] Building executable with PyInstaller..."

$iconArg = ""
if (Test-Path "app_icon.ico") {
    $iconArg = "--icon app_icon.ico"
    Write-Host "  - Using custom icon: app_icon.ico"
}

$buildCmd = "pyinstaller --onedir --windowed --name SteganographyApp $iconArg --add-data `"modules:modules`" --clean app.py"
Write-Host "  - Executing: $buildCmd"
Write-Host ""

Invoke-Expression $buildCmd

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to build executable" -ForegroundColor Red
    Exit 1
}

Write-Host ""
Write-Host "✓ Executable built successfully" -ForegroundColor Green
Write-Host "  Location: dist\SteganographyApp\SteganographyApp.exe"
Write-Host ""

# Step 4: Verify dist folder
Write-Host "[4/5] Verifying build output..."
if (Test-Path "dist\SteganographyApp\SteganographyApp.exe") {
    $exeSize = (Get-Item "dist\SteganographyApp\SteganographyApp.exe").Length / 1MB
    Write-Host "✓ Executable verified (Size: $([Math]::Round($exeSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "ERROR: SteganographyApp.exe not found in dist folder" -ForegroundColor Red
    Exit 1
}
Write-Host ""

# Step 5: Create NSIS installer
Write-Host "[5/5] Creating Windows installer with NSIS..."

# Find NSIS installation
$nsis_paths = @(
    "C:\Program Files\NSIS\makensis.exe",
    "C:\Program Files (x86)\NSIS\makensis.exe"
)

$nsis_exe = $null
foreach ($path in $nsis_paths) {
    if (Test-Path $path) {
        $nsis_exe = $path
        Write-Host "  - Found NSIS: $path"
        break
    }
}

if ($null -eq $nsis_exe) {
    Write-Host ""
    Write-Host "⚠ NSIS not found. Installer creation skipped." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create an installer, install NSIS:"
    Write-Host "  1. Download from: https://nsis.sourceforge.io/Download"
    Write-Host "  2. Run the installer and select 'Full Installation'"
    Write-Host "  3. Run this script again"
    Write-Host ""
    Write-Host "✓ Executable is ready for distribution at:"
    Write-Host "  dist\SteganographyApp\SteganographyApp.exe"
    Write-Host ""
} else {
    Write-Host "  - Building installer package..."
    & $nsis_exe /v3 /DCURRENT_BUILDDIR="$(Get-Location)" "build_installer.nsi"
    
    if ($LASTEXITCODE -eq 0) {
        if (Test-Path "SteganographyApp_Installer.exe") {
            $installerSize = (Get-Item "SteganographyApp_Installer.exe").Length / 1MB
            Write-Host ""
            Write-Host "✓ Installer created successfully" -ForegroundColor Green
            Write-Host "  Location: SteganographyApp_Installer.exe"
            Write-Host "  Size: $([Math]::Round($installerSize, 2)) MB"
        }
    } else {
        Write-Host "⚠ NSIS build encountered an issue. Check the configuration." -ForegroundColor Yellow
        Write-Host "  The executable is still available at: dist\SteganographyApp\SteganographyApp.exe"
    }
}

Write-Host ""
Write-Host "=================================================="
Write-Host "  Build Process Complete!" -ForegroundColor Green
Write-Host "=================================================="
Write-Host ""
Write-Host "Next steps:"
Write-Host "  • Run executable: dist\SteganographyApp\SteganographyApp.exe"
Write-Host "  • Or run installer: SteganographyApp_Installer.exe"
Write-Host ""

