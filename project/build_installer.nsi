; NSIS Installer Script for Adaptive Encrypted Image Steganography
; Comprehensive Windows Application Installer

!include "MUI2.nsh"
!include "x64.nsh"
!include "FileFunc.nsh"

;=== Basic Installer Settings ===
Name "Adaptive Encrypted Image Steganography"
OutFile "SteganographyApp_Installer.exe"
InstallDir "$PROGRAMFILES64\SteganographyApp"
InstallDirRegKey HKLM "Software\SteganographyApp" "InstallPath"

;=== Version Information ===
VIProductVersion "1.0.0.0"
VIAddVersionKey /LANG=1033 "ProductName" "Adaptive Encrypted Image Steganography"
VIAddVersionKey /LANG=1033 "CompanyName" "Open Source"
VIAddVersionKey /LANG=1033 "FileDescription" "Hide encrypted messages and files in images using adaptive LSB steganography"
VIAddVersionKey /LANG=1033 "FileVersion" "1.0.0.0"
VIAddVersionKey /LANG=1033 "ProductVersion" "1.0.0.0"
VIAddVersionKey /LANG=1033 "LegalCopyright" "2026"

;=== Request Admin Rights ===
RequestExecutionLevel admin

;=== Compression ===
SetCompress auto
SetCompressor /SOLID lzma
SetDatablockOptimize on

;=== Modern UI Settings ===
!define MUI_ABORTWARNING

; Welcome page
!insertmacro MUI_PAGE_WELCOME

; License page (optional)
; !insertmacro MUI_PAGE_LICENSE "LICENSE"

; Directory selection page
!insertmacro MUI_PAGE_DIRECTORY

; Installation files page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!insertmacro MUI_PAGE_FINISH

; Language
!insertmacro MUI_LANGUAGE "English"

;=== Installer Section ===
Section "Install Main Application"
  SetOutPath "$INSTDIR"
  
  ; Copy all application files from dist folder
  File /r "dist\SteganographyApp\*.*"
  
  ; Create Registry entries
  WriteRegStr HKLM "Software\SteganographyApp" "InstallPath" "$INSTDIR"
  WriteRegStr HKLM "Software\SteganographyApp" "Version" "1.0.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SteganographyApp" "DisplayName" "Adaptive Encrypted Image Steganography"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SteganographyApp" "DisplayVersion" "1.0.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SteganographyApp" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SteganographyApp" "DisplayIcon" "$INSTDIR\SteganographyApp.exe"
  WriteRegDWord HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SteganographyApp" "EstimatedSize" 250000
  
  ; Write uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Create Start Menu folder
  CreateDirectory "$SMPROGRAMS\Steganography App"
  
  ; Create shortcuts
  CreateShortCut "$SMPROGRAMS\Steganography App\Steganography App.lnk" "$INSTDIR\SteganographyApp.exe" "" "$INSTDIR\SteganographyApp.exe" 0
  CreateShortCut "$SMPROGRAMS\Steganography App\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
  CreateShortCut "$DESKTOP\Steganography App.lnk" "$INSTDIR\SteganographyApp.exe"
  
  ; Log installation
  SetDetailsPrint textonly
  DetailPrint "Installation completed!"
  
SectionEnd

;=== Uninstaller Section ===
Section "Uninstall"
  ; Delete installed files and directories
  RMDir /r "$INSTDIR"
  
  ; Delete shortcuts
  RMDir /r "$SMPROGRAMS\Steganography App"
  Delete "$DESKTOP\Steganography App.lnk"
  
  ; Remove registry entries
  DeleteRegKey HKLM "Software\SteganographyApp"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SteganographyApp"
  
  MessageBox MB_OK "Steganography App has been uninstalled."
  
SectionEnd

;=== Uninstaller Finish Function ===
Function un.onUninstSuccess
FunctionEnd

;=== Callback Function ===
Function .onInit
  ${If} ${RunningX64}
    ; 64-bit system
    SetRegView 64
  ${Else}
    ; 32-bit system
    SetRegView 32
  ${EndIf}
FunctionEnd
