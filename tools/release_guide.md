## Anleitung (Deutsch)

**Neu installieren**

1. Unten unter „Assets“ `FogScout-Setup-<Version>.exe` herunterladen.
2. Doppelklicken. Windows fragt einmal nach Administratorrechten (für „Verbunden mit“ und die Serverregion nötig).
3. Das Setup ist nicht signiert: Zeigt Windows SmartScreen „Der Computer wurde durch Windows geschützt“, auf „Weitere Informationen“ → „Trotzdem ausführen“ klicken.
4. Installiert wird nach `C:\Program Files\Fog Scout`; Startmenü, Desktop-Verknüpfung und Autostart richtet das Setup ein. Python ist nicht nötig.
5. Dead by Daylight im Modus **Fenster-Vollbild** starten – Fog Scout erkennt die Map beim Match-Start selbst.

**Aktualisieren**

- Eine installierte Version findet das Update selbst (Einstellungen → Allgemein → „Jetzt nach Updates suchen“) und installiert es nach Rückfrage. Einstellungen und Statistik bleiben.
- Versionen bis 1.46.4 (altes GitHub-Konto) dieses Setup einmal von Hand ausführen; danach geht es wieder von selbst.
- Startet Fog Scout nach einem Update nicht mehr: dieses Setup von Hand ausführen – es repariert die Installation.

**Prüfsumme (optional):** In PowerShell `Get-FileHash .\FogScout-Setup-<Version>.exe` – der Wert muss zur `.sha256`-Datei passen.

**Deinstallieren:** Windows-Einstellungen → Apps → „Fog Scout“ → Deinstallieren.

## Guide (English)

**Fresh install**

1. Download `FogScout-Setup-<version>.exe` below under "Assets".
2. Double-click it. Windows asks for administrator rights once (needed for "Connected to" and the server region).
3. The setup is not signed: if Windows SmartScreen shows "Windows protected your PC", click "More info" → "Run anyway".
4. It installs to `C:\Program Files\Fog Scout` and sets up the Start menu, a desktop shortcut and autostart. No Python needed.
5. Start Dead by Daylight in **windowed fullscreen** – Fog Scout detects the map at the start of a match by itself.

**Updating**

- An installed version finds the update by itself (Settings → General → "Check for updates now") and installs it after asking. Settings and statistics stay.
- Versions up to 1.46.4 (old GitHub account): run this setup once by hand; after that updates work by themselves again.
- If Fog Scout no longer starts after an update: run this setup by hand – it repairs the installation.

**Checksum (optional):** in PowerShell `Get-FileHash .\FogScout-Setup-<version>.exe` – the value must match the `.sha256` file.

**Uninstall:** Windows Settings → Apps → "Fog Scout" → Uninstall.
