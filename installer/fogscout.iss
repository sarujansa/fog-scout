; 1.32 (.exe, stage 4): installer for Fog Scout (Inno Setup, compiled in GitHub Actions – .github/workflows/build.yml):
;     ISCC.exe /DAppVersion=<version> installer\fogscout.iss
; after PyInstaller (installer/fogscout.spec) built dist\FogScout. Result: dist\FogScout-Setup-<version>.exe.
;
; Installs to Program Files for all users (administrator rights, as the program itself runs elevated through its
; scheduled task). After copying it runs "FogScout.exe --install-tasks": the tasks "Fog Scout" / "Fog Scout
; (Autostart)" and the Start menu/desktop shortcuts now start the .exe (fogscout/autostart.py); a start.bat
; installation they started until now is noted and offered for takeover at the first start (fogscout/takeover.py,
; copy only – the old folder stays). The uninstaller runs "--remove-tasks" first; the data folder
; %LOCALAPPDATA%\FogScout stays (settings, rounds, recordings index are the user's).
; Unsigned for now (Windows SmartScreen asks once – README).

#ifndef AppVersion
  #define AppVersion "0.0"
#endif

[Setup]
AppId={{6C1E2F4B-58A3-4D1C-9F0E-2B7A6D3C8E51}
AppName=Fog Scout
AppVersion={#AppVersion}
AppVerName=Fog Scout {#AppVersion}
AppPublisher=sarujansa
AppPublisherURL=https://github.com/sarujansa/fog-scout
AppSupportURL=https://github.com/sarujansa/fog-scout/issues
DefaultDirName={autopf}\Fog Scout
DisableProgramGroupPage=yes
DisableDirPage=auto
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir=..\dist
OutputBaseFilename=FogScout-Setup-{#AppVersion}
SetupIconFile=..\build\fogscout\fogscout.ico
UninstallDisplayIcon={app}\FogScout.exe
UninstallDisplayName=Fog Scout
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; the running program holds this mutex (fogscout/restart.py MUTEX_NAME): Setup asks to close it first
AppMutex=Local\FogScout.SingleInstance
CloseApplications=no

[Languages]
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[InstallDelete]
; a newer build may drop files – never mix two versions' libraries
Type: filesandordirs; Name: "{app}\_internal"

[Files]
Source: "..\dist\FogScout\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
Filename: "{app}\FogScout.exe"; Parameters: "--install-tasks"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated; StatusMsg: "Fog Scout: Aufgabenplanung und Verknüpfungen …"
; started through its task: elevated without a second Windows prompt, like every later start
Filename: "{sys}\schtasks.exe"; Parameters: "/run /tn ""Fog Scout"""; Flags: runhidden nowait postinstall skipifsilent; Description: "{cm:LaunchProgram,Fog Scout}"

[UninstallRun]
Filename: "{app}\FogScout.exe"; Parameters: "--remove-tasks"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated; RunOnceId: "RemoveTasks"
