# Windows App Installer Build Instructions

## Quick Start (30 seconds)

### Step 1: Open Command Prompt
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to project folder: `cd C:\Users\chinm\ipv\project`

### Step 2: Run Build
```bash
build.bat
```

### Step 3: Wait for Completion
- Process takes 3-10 minutes depending on PC speed
- You'll see progress messages

## Output Files

✅ **Standalone Executable** (always created):
```
dist\SteganographyApp\SteganographyApp.exe
```
- Can run directly without installation
- Share this file for portable version

✅ **Windows Installer** (if NSIS installed):
```
SteganographyApp_Installer.exe
```
- Professional installer for end users
- Creates Start Menu shortcuts
- Includes uninstall option

## What Gets Created

### Desktop
- `Steganography App` shortcut (after installation)

### Program Files
```
C:\Program Files64\SteganographyApp\
├── SteganographyApp.exe
├── _internal\
└── [supporting files]
```

### Start Menu
- `Steganography App` → Launch application
- `Steganography App` → Uninstall

## Distribution Options

### Option A: Portable (No Installation)
1. Copy `dist\SteganographyApp\SteganographyApp.exe`
2. Users run directly
3. No admin rights needed
4. **Size**: ~200-300 MB

### Option B: Professional Installer
1. Share `SteganographyApp_Installer.exe`
2. Users double-click to install
3. Admin rights required for installation
4. **Size**: ~150-200 MB

## Enabling NSIS Installer (Optional)

### Install NSIS
1. Visit: https://nsis.sourceforge.io/Download
2. Download the full installer
3. Run installer with default settings
4. Restart your PC

### Check if NSIS is Found
Run `build.bat` again - if NSIS is installed, it will automatically detect and create the installer.

## Troubleshooting

### Python Not Found
- Ensure Python is installed: https://www.python.org/
- Add to PATH during installation
- Restart Command Prompt

### Build Fails
```bash
# Try these steps:
python -m pip install --upgrade pip
python -m pip install pyinstaller
build.bat
```

### NSIS Won't Create Installer
- Install NSIS from: https://nsis.sourceforge.io/
- Default path: `C:\Program Files\NSIS\`
- Rerun `build.bat`

## Testing Your Build

```bash
# Run the executable directly from build folder
dist\SteganographyApp\SteganographyApp.exe
```

## Distributing to Users

### For Friend/Email/Drive
- Attach or link: `SteganographyApp_Installer.exe`
- Users download and run it
- Done!

### For Website/Repository
- Upload `SteganographyApp_Installer.exe`
- Provide download link
- Users download and run installer

### For Portable Usage
- Share `dist\SteganographyApp\SteganographyApp.exe`
- Users can run without installation
- Can place on USB drive

## Advanced Customization

### Custom Icon
1. Create image (512x512+ PNG recommended)
2. Convert to `.ico` format (use online tool)
3. Save as `app_icon.ico` in project folder
4. Rerun `build.bat`

### Update Version Number
Edit `build_installer.nsi`:
```
VIProductVersion "1.0.0.0"  ← Change version here
```

### Change Installation Directory
Edit `build_installer.nsi`:
```
InstallDir "$PROGRAMFILES64\YourAppName"  ← Change here
```

## File Sizes Explained

- **Executable (200-300 MB)**: Includes Python runtime + all libraries
- **Installer (150-200 MB)**: Compressed executable + NSIS installer script
- **Smaller versions**: Use `--onefile` instead of `--onedir` in build commands

This is normal and expected for PyInstaller applications.

## Build Time

- **First build**: ⏱️ 5-10 minutes
- **Subsequent builds**: ⏱️ 2-5 minutes  
- **NSIS installer**: ⏱️ 30 seconds

## Need Help?

- **PyInstaller Issues**: https://pyinstaller.org/
- **NSIS Issues**: https://nsis.sourceforge.io/
- **Python Issues**: https://www.python.org/

---

**Version**: 1.0  
**Last Updated**: May 2026  
**Tested On**: Windows 10/11
