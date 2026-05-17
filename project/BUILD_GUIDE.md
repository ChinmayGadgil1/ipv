# Windows App Build Guide

## Overview
This guide explains how to build your Steganography application into a Windows installer package.

## What You'll Get
- **SteganographyApp.exe**: Standalone executable (no Python installation required)
- **SteganographyApp_Installer.exe**: Professional Windows installer for end users

## Prerequisites

### Required
- Python 3.8+ (already installed)
- Windows 10 or 11

### Optional (for installer creation)
- NSIS (Nullsoft Scriptable Install System) - [Download](https://nsis.sourceforge.io/)
  - Allows creation of professional `.exe` installers
  - Not required to create the executable

## Quick Start

### Option 1: Using Batch Script (Easiest)
```bash
cd project
build.bat
```

### Option 2: Using PowerShell Script (More Features)
```powershell
cd project
\powershell -ExecutionPolicy Bypass -File build.ps1
```

### Option 3: Manual Build
```bash
cd project

# Install PyInstaller
python -m pip install pyinstaller

# Build the executable
pyinstaller --onedir --windowed --name SteganographyApp --icon app_icon.ico --add-data "sample_images;sample_images" --add-data "modules;modules" app.py
```

## Build Output

### After Build Completes
```
project/
├── dist/
│   └── SteganographyApp/
│       ├── SteganographyApp.exe          # Standalone executable
│       ├── _internal/                    # Supporting libraries and dependencies
│       └── [other runtime files]
├── build/                                 # Build artifacts (can be deleted)
└── SteganographyApp_Installer.exe         # Installer (if NSIS installed)
```

## Customization

### Application Icon
To add a custom app icon:
1. Create or obtain a `.ico` file (256x256 or larger)
2. Save it as `app_icon.ico` in the project root
3. The `build.bat` and `build.ps1` scripts will automatically use it

### Application Version
Edit `build_installer.nsi` to change:
- Application name and version
- Company information
- Installation directory

### Application Data
Add more data files to include in the bundle by editing `pyinstaller.spec`:
```python
datas=[
    (str(project_root / 'sample_images'), 'sample_images'),
    (str(project_root / 'other_folder'), 'other_folder'),
]
```

## Creating the Installer (Optional)

### Install NSIS
1. Download from [nsis.sourceforge.io](https://nsis.sourceforge.io/)
2. Run the installer and follow setup instructions
3. Accept default installation path

### Build Installer
After building the executable, if NSIS is installed:

```bash
# Run the build script again (it will detect NSIS)
build.bat
# Or manually:
"C:\Program Files\NSIS\makensis.exe" build_installer.nsi
```

This creates `SteganographyApp_Installer.exe` - a professional Windows installer.

## Distribution

### For End Users - Option 1: Standalone Executable
1. Copy `dist/SteganographyApp/SteganographyApp.exe` to users
2. Users can run directly - no installation needed
3. Size: ~200-300 MB

### For End Users - Option 2: Installer Package
1. Distribute `SteganographyApp_Installer.exe`
2. Users run the installer
3. Installer creates Start Menu shortcuts and Desktop shortcut
4. Professional installation experience

## Troubleshooting

### Issue: "ModuleNotFoundError" when running executable
**Solution**: Ensure all dependencies are listed in `build_requirements.txt` and in the `hiddenimports` section of `pyinstaller.spec`.

### Issue: Missing files in the bundle
**Solution**: Add file paths to the `--add-data` parameter in the build script.

### Issue: NSIS not found
**Solution**: 
- Install NSIS from https://nsis.sourceforge.io/
- Accept default installation path (C:\Program Files\NSIS\)
- Or manually run: `"C:\Program Files\NSIS\makensis.exe" build_installer.nsi`

### Issue: Icon not showing
**Solution**: 
- Create `app_icon.ico` file and place in project root
- Ensure it's at least 256x256 pixels

## File Sizes
- **Executable**: ~200-300 MB (first build)
- **Subsequent builds**: ~5-10 minutes
- **Installer**: ~150-200 MB (adds ~50 MB overhead)

## Best Practices

1. **Test the executable** before distributing:
   ```bash
   dist\SteganographyApp\SteganographyApp.exe
   ```

2. **Version your builds**:
   - Keep track of version numbers
   - Update `VIProductVersion` in `build_installer.nsi`

3. **Virus scanning**:
   - Some antivirus software may flag PyInstaller executables
   - This is normal behavior (false positive)
   - Use signed certificates to reduce this

4. **Set up versioning**:
   - Keep a `VERSION.txt` file in your project
   - Update build scripts to read from it

## Next Steps

1. Run `build.bat` to create your executable
2. Test `dist\SteganographyApp\SteganographyApp.exe`
3. (Optional) Install NSIS and rebuild for professional installer
4. Distribute the executable or installer to users
