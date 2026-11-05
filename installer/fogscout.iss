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
; 1.38.21 (audit SEC-3): always Program Files – a folder the user may write to would let anyone replace the .exe
; that the task "Fog Scout" starts with highest rights, and fogscout/paths.app_update_dir counts on this folder
DisableDirPage=yes
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
; 1.33.2: no AppMutex - a silent update aborted while Fog Scout was still closing. InitializeSetup in the code
; section waits for the program's mutex (fogscout/restart.py MUTEX_NAME); an installation by hand asks to close it.
CloseApplications=no

[Languages]
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

; 1.33.2: no InstallDelete of {app}\_internal any more - Inno Setup does not bring deleted files back when the setup
; is aborted, and an update broken off midway (a file still in use) left a program without python312.dll. Every file
; of the new version replaces the old one; at worst unused files of an older version stay behind.

[Files]
Source: "..\dist\FogScout\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
Filename: "{app}\FogScout.exe"; Parameters: "--install-tasks"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated; StatusMsg: "Fog Scout: Aufgabenplanung und Verknüpfungen …"
; started through its task: elevated without a second Windows prompt, like every later start
Filename: "{sys}\schtasks.exe"; Parameters: "/run /tn ""Fog Scout"""; Flags: runhidden nowait postinstall skipifsilent; Description: "{cm:LaunchProgram,Fog Scout}"
; 1.33: an update from the program (/update=1, relupdate.install_args) runs silently – start Fog Scout again
Filename: "{sys}\schtasks.exe"; Parameters: "/run /tn ""Fog Scout"""; Flags: runhidden nowait; Check: IsUpdate

[UninstallRun]
Filename: "{app}\FogScout.exe"; Parameters: "--remove-tasks"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated; RunOnceId: "RemoveTasks"

; 1.34 (review S1): the program starts an update setup only from a copy in {app}\update (admins only, see
; fogscout/restart.py staged_setup). Removed with the program; only that folder, never the data folder.
[UninstallDelete]
Type: files; Name: "{app}\update\*"
Type: dirifempty; Name: "{app}\update"

[Code]
const
  MutexName = 'Local\FogScout.SingleInstance';   { fogscout/restart.py MUTEX_NAME }
  UpdateWaitMs = 60000;

var
  Installed: Boolean;

function IsUpdate: Boolean;
begin
  Result := ExpandConstant('{param:update|0}') = '1';
end;

{ 1.33.2: wait for Fog Scout to end - an update from the program quits it right after starting this setup; by hand
  the user is asked to close it (Retry/Cancel) }
function WaitForProgram(Interactive: Boolean): Boolean;
var
  Waited: Integer;
begin
  Waited := 0;
  while CheckForMutexes(MutexName) do
  begin
    if Interactive then
    begin
      if MsgBox(CustomMessage('FogScoutRunning'), mbError, MB_RETRYCANCEL) <> IDRETRY then
      begin
        Result := False;
        Exit;
      end;
    end
    else
    begin
      if Waited >= UpdateWaitMs then
      begin
        Result := False;
        Exit;
      end;
      Sleep(250);
      Waited := Waited + 250;
    end;
  end;
  Result := True;
end;

function InitializeSetup(): Boolean;
begin
  Installed := False;
  Result := WaitForProgram((not IsUpdate) and (not WizardSilent));
end;

function InitializeUninstall(): Boolean;
begin
  Result := WaitForProgram(not UninstallSilent);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    Installed := True;
end;

{ 1.33.2 (M-6): an update that did not finish starts Fog Scout again anyway - nothing was deleted beforehand, the
  program that was there still runs }
procedure DeinitializeSetup();
var
  Code: Integer;
begin
  if IsUpdate and (not Installed) then
    Exec(ExpandConstant('{sys}\schtasks.exe'), '/run /tn "Fog Scout"', '', SW_HIDE, ewNoWait, Code);
end;

[CustomMessages]
de.FogScoutRunning=Fog Scout läuft noch. Bitte beenden (Infobereich: Rechtsklick auf das Symbol, dann Beenden) und danach Wiederholen wählen.
en.FogScoutRunning=Fog Scout is still running. Please close it (notification area: right-click the icon, then Exit) and choose Retry.
