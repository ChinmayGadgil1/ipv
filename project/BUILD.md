# Build & Distribution

## 🔨 Quick Build

```bash
.\build.bat
```

Creates `SteganographyApp_Installer.exe` ready for sharing.

---

## 📦 What Gets Created

| File | Size | Purpose |
|------|------|---------|
| `dist/SteganographyApp.exe` | ~150 MB | Standalone executable |
| `SteganographyApp_Installer.exe` | ~180 MB | Windows installer |

---

## 🌐 Share Online

### GitHub (Recommended)
1. Create GitHub repo
2. Go to Releases → Create Release
3. Upload `SteganographyApp_Installer.exe`
4. Share download link

### Google Drive / OneDrive
- Upload installer
- Share link directly

### Your Website
- Host installer on web server
- Add download button

---

## 👥 User Installation

1. Download `SteganographyApp_Installer.exe`
2. Run installer (double-click)
3. Click "Next" through wizard
4. Launch from Start Menu

**Requirements:** Windows 10/11 (64-bit)

---

## 🔧 Build Requirements

- Python 3.8+
- NSIS (auto-installs)

No user installation needed - everything bundled!

---

## ♻️ Rebuild After Changes

```bash
# Edit code, then:
.\build.bat
```

New installer created automatically.
