# Stabilitäts-, Installations- und Update-Audit – Fog Scout

Stand: 4.11.2026. Grundlage ist der Code im Arbeitsbaum. Nur ausgeführte Prüfungen sind als ausgeführt markiert.

## 1. Geprüfter Stand

| | |
|---|---|
| Branch | `claude/funny-feynman-gt5t6n` (= `origin/main` beim Start) |
| Commit beim Start | `76017ee` (Merge PR #314, 1.33) |
| Programmversion | vorher 1.33, nach den Fixes **1.33.1** (lokal, nicht committet, nicht gepusht) |
| Umgebung | Linux-Container (Python 3.13, PySide6 offscreen); **keine Windows-Umgebung**; CI läuft ohne Push nicht |

## 2. Geprüfte Komponenten

- **Update-System:** `fogscout/relupdate.py`, `fogscout/restart.py`, `fogscout/app_settings.py` (Update-Teil), `fogscout/__main__.py` (`--install-update`).
- **Installation und Migration:** `fogscout/paths.py`, `fogscout/takeover.py`, `fogscout/autostart.py`, `fogscout/__main__.py` (`--install-tasks`/`--remove-tasks`, `offer_takeover`), `installer/fogscout.iss`.
- **Build und Release:** `installer/fogscout.spec`, `installer/fogscout_exe.py`, `fogscout/selftest.py`, `.github/workflows/build.yml`, `requirements*.txt`, das Release `build-6`.
- **Doku:** `README.md`, `README.en.md`, `PRIVACY.md`.
- **Langzeitbetrieb:** vorhandenes Messskript `tools/bench.py` (Leerlauf); dazu eine Code-Sichtung der Bereiche, die frühere Audits schon behandelt haben (Timer-Freigabe, Thread-Wächter).

## 3. Ist-Zustand (Zusammenfassung)

Die Grundarchitektur ist solide:
- Programm- und Benutzerdaten liegen getrennt (`%LOCALAPPDATA%\FogScout`).
- Releases werden nur von main gebaut.
- Das Setup wird per Grösse und SHA-256 geprüft; GitHubs Digest und die `.sha256`-Datei müssen übereinstimmen.
- Updates sind während einer Runde, einer laufenden OBS-Aufnahme und beim Speichern von Clips gesperrt.
- Die Deinstallation lässt den Datenordner stehen.

Schwachstellen gab es an den Übergängen zwischen den Schritten:
- **Übernahme:** wurde auch nach einem Fehler als erledigt markiert.
- **Start des Setups:** keine erneute Prüfung direkt vorher, kein Auswerten des Starts.
- **UAC mit fremdem Admin-Konto:** Einrichtung landete im falschen Konto.
- **Doku:** Datenschutz und Einstieg nicht aktuell.

Ein Critical-Befund fand sich nicht.

## 4. Bestätigte Probleme

„Bestätigt“ heisst hier: im Code nachvollzogen und – wo möglich – durch einen Test reproduziert, der vor dem Fix fehlschlug bzw. das Fehlverhalten zeigte. Windows-Verhalten ist nur im Code nachvollzogen.

| ID | Prio | Problem | Ort | Status |
|---|---|---|---|---|
| H-1 | High | **Übernahme ohne zweiten Versuch und mit halben Dateien:** `offer_takeover` setzte die Marke „gefragt“ im `finally` – auch wenn `copy` scheiterte. `copy` schrieb direkt auf das Ziel (ein Absturz liess halbe Dateien zurück) und `settings.json` zuerst (danach bot `pending()` die Übernahme nie wieder an). | `__main__.offer_takeover`, `takeover.copy` | **behoben** |
| H-2 | High | **Startfehler des Setups unbemerkt:** Der Rückgabewert von `ShellExecuteW` wurde nicht ausgewertet. War die UAC-Abfrage abgelehnt oder die Datei gesperrt, war Fog Scout beendet, ohne Meldung und ohne Neustart. | `restart._shell_open`/`wait_and_install` | **behoben** |
| H-3 | High | **Keine erneute Prüfung vor dem Start:** Zwischen Download, Rückfrage und Start des Setups wurde die Prüfsumme nicht noch einmal geprüft. Eine danach veränderte Datei im Update-Ordner wäre gestartet worden. | `restart.wait_and_install` | **behoben** |
| H-4 | High | **UAC mit anderen Administrator-Daten:** `--install-tasks` lief dann als dieser Admin. Aufgaben (`WindowsIdentity.GetCurrent()`), Verknüpfungen, Autostart und die Übernahme-Notiz (sein `%LOCALAPPDATA%`) landeten in dessen Konto; der eigentliche Benutzer bekam nichts davon. | `autostart.task_script`, `__main__.install_tasks` | **behoben** (unter Windows nicht getestet) |
| M-1 | Medium | **Zwei gleichzeitige Downloads möglich:** ein Klick auf „Jetzt nach Updates suchen“ während des Ladens; beide Downloads schreiben dieselbe `.part`-Datei. | `app_settings._release_download`/`check_update` | **behoben** |
| M-2 | Medium | **Weiterleitung auf HTTP:** `urllib` folgt Weiterleitungen auch von HTTPS auf HTTP. Nur ein gesichertes Weiterleitungsziel wird akzeptiert. | `relupdate._opener` | **behoben** |
| M-3 | Medium | **Setup bleibt liegen:** Nach einem Update bleiben das Setup (~120 MB) und Reste abgebrochener Downloads (`.part`) im Update-Ordner. | `relupdate`, App-Start | **behoben** |
| M-4 | Medium | **Datenschutzangaben veraltet:** `PRIVACY.md` (DE/EN) nannte nur `git fetch` – nicht die Abfrage von `api.github.com` und den Download des Setups. | `PRIVACY.md` | **behoben** |
| M-5 | Medium | **README:** Der Installer war nicht der empfohlene Einstieg (die Anleitung begann mit Python/`start.bat`), und der Absatz „Updates“ beschrieb nur `start.bat`. | `README.md`, `README.en.md` | **behoben** |
| M-6 | Medium | **Gescheitertes Setup:** Scheitert das stille Setup selbst (z. B. eine Datei gesperrt), startet Fog Scout nicht neu. Der `[Run]`-Eintrag mit `Check: IsUpdate` läuft nur nach Erfolg, und es gibt keine Rückmeldung. | `installer/fogscout.iss` | **offen**, dokumentiert |
| L-1 | Low | **Builds und Versionsinfo:** Die .exe hat keine VERSIONINFO (Explorer zeigt keine Version). Builds sind nicht bitgenau reproduzierbar (`pip install --upgrade pip` ohne feste Version, Zeitstempel in PyInstaller und Inno Setup). | `fogscout.spec`, `build.yml` | **offen**, dokumentiert |

**Geprüft und in Ordnung (kein Befund):**
- **Update-Sperren:** Updates sind während einer Runde, einer laufenden OBS-Aufnahme und beim Speichern eines Clips gesperrt (`apply_update`: `_round_running` = offene Runde ∨ `recorder.recording`, `_clips_saving`; vor der Installation erneut in `_release_install`, dazu `_quit_phase1` für Editor-Projekte).
- **Nur eigene Release-Downloads:** Downloads kommen nur von `https://github.com/senisinx/fog-scout/releases/download/build-N/…` (`parse_release` prüft die Adresse genau).
- **Grösse und Prüfsumme:** Die Grösse wird gegen die Angabe im Release und gegen `MAX_BYTES` geprüft; die SHA-256 gegen die `.sha256`-Datei, und beide müssen mit GitHubs Digest übereinstimmen.
- **Abgebrochener Download:** Ein abgebrochener oder falscher Download löscht seine `.part`-Datei.
- **Fehler der GitHub-API:** Netzfehler, 403/Rate-Limit und kaputtes JSON werden zum Zustand `error`, kein Absturz (jetzt mit Tests).
- **Deinstallation:** Die Deinstallation enthält kein `[UninstallDelete]`; der Datenordner `%LOCALAPPDATA%\FogScout` mit Einstellungen, Runden, Match-Daten, Log, Sicherungen und eigenen Kartenbildern bleibt.
- **Saubere Programmdateien:** `[InstallDelete] {app}\_internal` verhindert, dass Bibliotheken zweier Versionen gemischt werden.

## 5. Behobene Probleme – was geändert wurde

- **H-1:**
  - `takeover._copy_file` schreibt jede Datei unter einem Temp-Namen (`fsops.tmp_name`) und benennt sie erst dann exklusiv um (`fsops.create_exclusive`). So wird nie etwas überschrieben, und es entstehen nie halbe Dateien unter dem echten Namen.
  - `settings.json` wird zuletzt kopiert (`LAST`).
  - `offer_takeover` setzt die Marke nur nach „Nein“ oder nach einer vollständigen Kopie. Ein `OSError` lässt die Notiz stehen, und beim nächsten Start wird erneut gefragt (die Fehlermeldung zeigte `main` schon vorher).
  - Eine wiederholte Übernahme ist idempotent.
- **H-2/H-3:**
  - `--install-update <setup> <sha256>`: Die App reicht die geprüfte SHA weiter (`Release.sha256`, `restart.spawn_installer`).
  - Der Helfer hasht das Setup unmittelbar vor dem Start erneut.
  - `_shell_open` meldet Erfolg nur bei einem Rückgabewert > 32.
  - Scheitert eines davon, sagt `_install_failed` Grund und Pfad, und `relaunch` startet Fog Scout wieder (installiert über die Aufgabe, sonst die .exe). So lässt sich der Vorgang erneut versuchen.
  - Fremde Pfade werden weiter still abgelehnt.
- **H-4:**
  - `autostart.for_session_user` vergleicht den Benutzer der Windows-Sitzung (`WTSQuerySessionInformationW`) mit dem Benutzer des Prozesses (`GetUserNameExW`). Verglichen wird nur der Kontoname, ohne Domain – eine abweichende Schreibweise der Domain darf eine normale Installation nicht treffen. Ist ein Wert unbekannt, bleibt das bisherige Verhalten.
  - Bei Abweichung werden keine Aufgaben, keine Verknüpfungen und keine Übernahme-Notiz angelegt, sondern eine Startmenü-Verknüpfung für alle Benutzer direkt auf die .exe (`common_shortcut_script`). Die Deinstallation entfernt sie.
  - Beides sind nur Konto-Infos; es wird kein Prozess geöffnet.
- **M-1:** `_release_busy`: nur ein Download gleichzeitig, und währenddessen keine neue Prüfung.
- **M-2:** `relupdate._HttpsOnly` – eine Weiterleitung auf etwas anderes als `https://` wird abgelehnt.
- **M-3:** `relupdate.clean_update_folder` löscht beim Start der installierten Version nur eigene Setups und deren `.part`-Reste.
- **M-4/M-5:**
  - `PRIVACY.md` (DE/EN): eine eigene Zeile für die Updates der installierten Version und der richtige Speicherort.
  - `README.md`/`README.en.md`: Der Installer ist der empfohlene Einstieg, `start.bat` die Alternative; dazu der UAC-Fall mit einem anderen Admin und das robustere Update.

## 6. Veränderte Dateien

- **Programm:**
  - `fogscout/__init__.py` (1.33.1), `fogscout/__main__.py`, `fogscout/takeover.py`, `fogscout/restart.py`
  - `fogscout/relupdate.py`, `fogscout/autostart.py`, `fogscout/app_settings.py`, `fogscout/i18n_en.py` (2 neue Meldungen)
- **Tests:** `tests/test_relupdate.py`, `tests/test_installer.py`
- **Doku:** `README.md`, `README.en.md`, `PRIVACY.md`, `CLAUDE.md`, `HISTORY.md`, dieser Bericht

Am Installer-Skript, an der Spec und an den Workflows wurde nichts geändert.

## 7./8. Ausgeführte Prüfungen und Ergebnisse

| Prüfung | Befehl | Ergebnis | Wo |
|---|---|---|---|
| Gesamte Testsuite | `DBDMS_LANG=de QT_QPA_PLATFORM=offscreen python3 -m pytest -q tests` | **1383 passed, 38 skipped**, 0 failed (vorher 1363/37) | Linux |
| Neue/geänderte Tests | `pytest tests/test_relupdate.py tests/test_installer.py` | 27 passed bzw. 21 passed + 1 skipped (Rechtetest per `chmod` läuft als root nicht; derselbe Fall ist per `PermissionError`-Simulation abgedeckt) | Linux |
| Linting | `python3 -m pyflakes fogscout tests tools installer/fogscout_exe.py` | sauber | Linux |
| Whitespace | `git diff --check` | sauber | Linux |
| Typprüfung | – | im Projekt nicht vorhanden (kein mypy/pyright konfiguriert) | – |
| Abhängigkeiten | `pip-audit -r requirements.txt` / `-r requirements-build.txt` / `-r requirements-extra.txt` (`--no-deps`, in einer Wegwerf-venv ausserhalb des Projekts) | **No known vulnerabilities found** (alle drei) | Linux |
| Build | `python3 -m PyInstaller --noconfirm --clean installer/fogscout.spec` | Exit 0 | Linux (Probe-Build, nicht der Windows-Build) |
| Selbsttest der gebauten App | `FogScout --selftest st.json` | `ok: true`, Version 1.33.1, keine Fehler | Linux |
| Update-Helfer in der gebauten App | `FogScout --install-update /nowhere/x.exe 00` | Exit 1, nichts gestartet | Linux |
| Leerlauf und Speicher | `tools/bench.py --runs 3 --only startup,idle` | Leerlauf in den ersten 10 s 7,3 % eines Kerns, danach stabil 1,6 %; RSS 246,6 MB (Median aus 3 Läufen) | Linux offscreen (keine Windows-Zahlen) |
| Security-Scan | CodeQL läuft in GitHub erst nach einem Push | **nicht ausgeführt** | – |

**Neue Tests (Auswahl):**
- *Update-System:*
  - manipulierte bzw. fehlende Setup-Datei vor dem Start (4 Fälle);
  - Startfehler (`ShellExecuteW` ≤ 32) → Meldung mit Pfad und Neustart;
  - Prüfsumme wird an den Helfer weitergereicht;
  - Weiterleitung auf HTTP abgelehnt;
  - Netzfehler, 403/Rate-Limit, Timeout, kaputtes JSON;
  - Verbindungsabbruch im Download → nichts bleibt;
  - Aufräumen beim Start nur eigener Dateien;
  - zweiter Download bzw. Prüfung während des Ladens wird abgewiesen.
- *Übernahme:*
  - Kopierfehler → nicht als erledigt markiert, erneute Frage, danach vollständig;
  - Abbruch mitten im Kopieren (Temp-Rest) → nächster Lauf vollständig, Wiederholung ändert nichts;
  - vorhandenes Ziel bleibt;
  - kaputte Quell-`settings.json` wird nur kopiert, nie ausgewertet;
  - keine Temp-Reste.
- *Installation:*
  - anderer Admin → keine Aufgaben, keine Übernahme-Notiz, kein Datenordner, Verknüpfung für alle Benutzer;
  - derselbe Benutzer (auch mit anderer Schreibweise der Domain) → wie bisher;
  - der Uninstaller rührt den Datenordner nicht an.

## 9. Nicht ausgeführte Tests

- **Windows insgesamt.** Es gibt keine Windows-Umgebung, und ohne Push laufen weder die Windows-Testsuite in `tests.yml` noch der Job `exe` in `build.yml` (Windows-Build, Installieren, Prüfen, Deinstallieren). Ungeprüft sind deshalb:
  - ob `WTSQuerySessionInformationW`/`GetUserNameExW` unter Windows die erwarteten Namen liefern;
  - `ShellExecuteW` mit echtem Setup und abgelehnter UAC-Abfrage;
  - das Anlegen der Verknüpfung in `CommonPrograms`;
  - das echte Update von Build 6 auf einen neueren Build.
- **Installation unter einem Standardkonto mit UAC-Anmeldung eines anderen Admins** – nicht manuell getestet; nur der Code-Pfad ist abgedeckt.
- **CodeQL** – läuft erst in GitHub.
- **Langzeitlauf mit DBD/OBS über Stunden** – nicht möglich (kein Windows, kein Spiel).

**Abdeckung je Bereich:**
- **Unter Linux ausgeführt und erfolgreich:** volle Testsuite, pyflakes, pip-audit, PyInstaller-Probe-Build mit Selbsttest, Leerlauf-Messung.
- **Nur durch automatisierte Tests abgedeckt (simuliert):** alle Windows-Aufrufe (Prüfung des Benutzers, ShellExecute, PowerShell-Skripte, MessageBox).
- **Nicht getestet:** alles unter Windows (siehe oben).

## 10. Verbleibende Risiken

- **Gescheitertes Setup (M-6):** Scheitert das stille Setup nach dem Start, kommt Fog Scout nicht von selbst wieder. Der Benutzer startet es dann über das Startmenü; die alte Installation ist in diesem Fall von Inno Setup zurückgerollt oder unvollständig.
- **Kein Prüfen der Installation:** Beschädigte Installationen werden nicht automatisch erkannt. `--selftest` existiert, wird aber nur in CI ausgeführt.
- **Unsigniert:** Das Setup ist nicht signiert, SmartScreen warnt. Die Integrität hängt an HTTPS zu GitHub und an der SHA-256 aus demselben Release. Das schützt vor beschädigten Downloads, nicht vor einem kompromittierten GitHub-Konto bzw. Workflow.
- **H-4 mit unbekannten Namen:** Liefern die Windows-Funktionen keine Namen, bleibt das alte Verhalten (Aufgaben für das ausführende Konto).
- **Fremdes Admin-Konto ohne Aufgaben:** Fog Scout läuft dann ohne Aufgabe und damit ohne Administratorrechte. Hosts-Datei und „Verbunden mit“ fragen per UAC nach. Autostart lässt sich in diesem Fall nicht einrichten.
- **Inno Setup 7:** nur für nicht-kommerzielle Nutzung kostenlos.

## 11. Windows-spezifische offene Prüfungen (Checkliste für Saru)

1. **Neuinstallation** mit dem Setup aus dem Release, mit eigenem Admin-Konto: Aufgaben „Fog Scout“ und „(Autostart)“ sind da, Startmenü- und Desktop-Verknüpfung auch, der Start erfolgt ohne Windows-Abfrage.
2. **Übernahme:** Die Frage kommt beim ersten Start (nur wenn vorher die `start.bat`-Verknüpfung eingerichtet war). Danach Runden und Einstellungen prüfen.
3. **Standardkonto mit anderem Admin:** Installieren mit den Daten eines anderen Admin-Kontos → keine Aufgaben, aber „Fog Scout“ im Startmenü für alle; Programm starten, „Verbunden mit“ fragt per UAC.
4. **Update:** Nach dem nächsten Merge (Build 7): „Jetzt nach Updates suchen“ → „Aktualisieren und neu starten“ → Fog Scout schliesst sich, das Setup läuft, Fog Scout ist wieder da, `%LOCALAPPDATA%\FogScout\cache\update` ist nach dem Start leer.
5. **Update mit abgelehnter UAC-Abfrage** (falls Fog Scout ohne Admin läuft): Meldung erscheint, Fog Scout startet wieder.
6. **Deinstallation:** Aufgaben und Verknüpfungen sind weg, `%LOCALAPPDATA%\FogScout` bleibt.

## 12. Empfehlungen für die nächste Version

**Vor 1.34 unbedingt:**
1. Diese Änderungen committen, als PR durch CI laufen lassen und den Windows-Build mit Installer-Test grün sehen.
2. Die Checkliste in Abschnitt 11 einmal auf dem eigenen PC durchgehen.
3. Ein echtes Update von Build 6 auf Build 7 beobachten.

**Danach, mit klarem Nutzen:**
- **M-6:** Rückmeldung nach einem gescheiterten stillen Setup, z. B. per Inno-`[Code]` `CurStepChanged`/`DeinitializeSetup`: Bei Fehler trotzdem `schtasks /run` – Fog Scout zeigt dann beim Start die alte Version an. Klein, aber nur mit Windows-Test.
- **L-1:**
  - `VERSIONINFO` in der Spec (`version=`-Datei aus `__version__` + Build);
  - `pip` in CI auf eine feste Version setzen;
  - `SOURCE_DATE_EPOCH` für reproduzierbarere Builds.
- **Prüfen auf beschädigte Installation:** `--selftest` als Knopf („Installation prüfen“) in der Diagnose.

**Authenticode-Signierung (Empfehlung, nicht eingerichtet):**
- Für ein öffentliches Open-Source-Projekt: **SignPath Foundation** (kostenloses Code-Signing für OSS, Signierung in GitHub Actions über deren Action; Zertifikat und Schlüssel bleiben bei SignPath, Freigabe je Release).
- Alternative: **Azure Trusted Signing** (kostenpflichtig, ~10 USD/Monat, braucht eine Identitätsprüfung).
- **Was signiert wird:** `FogScout.exe` (vor Inno Setup) und `FogScout-Setup-*.exe` (nach ISCC).
- **Wie:**
  - SHA-256-Signatur mit RFC-3161-Zeitstempel, damit die Signatur nach Ablauf des Zertifikats gültig bleibt.
  - Danach im Release-Job mit `Get-AuthenticodeSignature` prüfen.
  - Die Update-Prüfung könnte dann zusätzlich den Herausgeber der Signatur kontrollieren (`WinVerifyTrust`) – das schützt auch gegen ein kompromittiertes Release.
- **SmartScreen:** Die Reputation baut sich mit einem signierten Herausgeber über die Zeit auf; EV-Zertifikate geben sie nicht mehr sofort.

## Ehrliche Einschätzung

- **Stabilität:** Für den Alltag mit `start.bat` gut abgesichert: 1383 Tests, Thread-Wächter, Sperren während Runden. Der Leerlauf liegt unter Linux bei ~1,6 % eines Kerns und ~250 MB.
- **Installer-Version:** Sie ist neu und auf Windows bisher nur in CI geprüft (Build 6). Sie ist die am wenigsten erprobte Stelle.
- **Installation und Updates:**
  - Der Weg ist jetzt durchgehend geprüft: HTTPS nur zu GitHub, genaue Adresse, Grösse, zwei übereinstimmende SHA-256, erneute Prüfung direkt vor dem Start.
  - Fehlschläge enden in einem definierten Zustand: Meldung und Neustart.
  - Die fehlende Signatur ist der grösste verbleibende Unterschied zu „Premium“.
- **Verbleibende Risiken:** die Punkte unter 10; vor allem die nicht unter Windows getesteten Fixes (H-2/H-4) und M-6.
- **Breitere Veröffentlichung:** Für interessierte Nutzer mit klarem Hinweis „unsigniert, früher Stand“ ja – aber erst, nachdem die Windows-Checkliste (Abschnitt 11) einmal grün war. Für eine breite Veröffentlichung ohne Vorwarnung sollte die Signierung kommen.
- **Vor 1.34 erledigen:**
  1. Diese Fixes durch CI (Windows-Build und Installer-Test) bringen.
  2. Die Checkliste in Abschnitt 11 auf echtem Windows durchgehen, inklusive eines Updates von Build N auf N+1.
  3. Entscheiden, ob M-6 (Neustart nach gescheitertem Setup) und die Signierung in 1.34 sollen.

## Nachtrag 1.33.2 – C-1 nach der Freigabe auf echtem Windows gefunden

| ID | Schwere | Befund |
|---|---|---|
| C-1 | Critical | **Ein Update zerstörte die Installation.** Saru hat Build 6 (1.33) installiert und über „Aktualisieren und neu starten“ auf Build 9 (1.33.1) aktualisiert. Danach startete Fog Scout nicht von selbst, und beim Start von Hand kam „Failed to load Python DLL '…\_internal\python312.dll'“. |

**Ursache (aus dem Code abgeleitet; ein Setup-Log gab es noch nicht):**
- Der Update-Helfer `FogScout.exe --install-update` lief aus dem Programmordner und hielt genau die Dateien, die das Setup ersetzt (`FogScout.exe`, `python312.dll`, Qt-DLLs).
- Das Setup löschte zuerst `{app}\_internal` (`[InstallDelete]`) und kopierte dann. Das stille Setup brach an einer gesperrten Datei ab.
- Inno Setup stellt per `[InstallDelete]` Gelöschtes beim Abbruch nicht wieder her. Ausserdem brach `AppMutex` das stille Setup ab, wenn das Programm noch lief.

M-6 hatte das Risiko eines gescheiterten Setups gesehen, aber zu niedrig eingestuft. CI hatte nie ein Update über eine bestehende Installation getestet. Beides ist eine Lücke dieses Audits.

**Fix in 1.33.2:**
1. Kein Helfer mehr. Das Programm prüft die SHA-256 und den Ordner unmittelbar vor dem Start (`restart.setup_still_ours`), startet das Setup selbst und beendet sich erst dann. Scheitert der Start, bleibt es offen.
2. Das Setup wartet selbst auf das Programmende (Mutex, `[Code] WaitForProgram`). Bei einem Update geschieht das still bis 60 s, von Hand mit Wiederholen/Abbrechen. `AppMutex` ist entfernt.
3. Es wird nichts mehr vorher gelöscht (kein `[InstallDelete]`). Ein abgebrochenes Setup lässt die alte, lauffähige Version stehen.
4. Fog Scout startet auch nach einem abgebrochenen Update wieder (`DeinitializeSetup`, erledigt damit M-6).
5. Das Setup schreibt ein Log nach `%LOCALAPPDATA%\FogScout\cache\update\setup.log`.
6. CI (`build.yml`, Schritt „Installer ausprobieren“) prüft jetzt zusätzlich:
   - ein Update, während der Mutex gehalten wird: Das Setup muss warten und danach durchlaufen;
   - ein Update mit gesperrter `python3*.dll`: `FogScout.exe`, die DLL und `maps.json` müssen danach noch da sein, und der Selbsttest muss grün sein.

**Grenzen:**
- Der Weg 1.33.1 → 1.33.2 läuft noch über den alten Helfer von 1.33.1. 1.33.2 muss deshalb einmal von Hand installiert werden; erst Updates ab 1.33.2 nutzen den neuen Weg.
- Eine schon beschädigte Installation repariert das Setup aus den Releases, von Hand ausgeführt.
- Echtes Windows mit einem echten Update von Build N auf N+1 bleibt die offene Prüfung.

## Nachtrag 1.33.3 – die Sperre kam von OBS

Beim Installieren von 1.33.1 und 1.33.2 von Hand hing das Setup an `_internal\msvcp140.dll` („DeleteFile failed; code 5“). Saru hat das per PowerShell geprüft (Prozesse mit Modulen aus `C:\Program Files\Fog Scout`): Nur `obs64.exe` hatte Module von dort geladen.

**Ursache:** Fog Scout hatte OBS selbst gestartet (`rec_obs_start`). Die PyInstaller-.exe gibt an gestartete Programme drei Dinge weiter:
- ihre DLL-Suche (`SetDllDirectoryW` auf `_internal`),
- `PATH` mit `_internal` vorne,
- `QT_PLUGIN_PATH` und `QML2_IMPORT_PATH` aus dem Laufzeit-Hook von PySide6.

OBS lud deshalb die C++-Laufzeit aus Fog Scouts Ordner und hielt sie fest. Sehr wahrscheinlich war das auch der Auslöser von C-1.

**Fix in 1.33.3:** Alle fremden Programmstarts laufen über `launch.py`: Windows' eigene DLL-Suche, eine bereinigte Umgebung und ein Wächter-Test, der direkte Starts an anderer Stelle verbietet. Der Selbsttest der .exe prüft das in CI.

**Bewusst nicht umgesetzt:** Vor einem Update Prozesse mit Modulen aus dem Programmordner suchen. Das bräuchte `OpenProcess` auf fremde Prozesse, also auch auf das Spiel, und verstößt damit gegen eine harte Regel.

**Rest:** Ein OBS, das noch von 1.33.2 oder älter gestartet wurde, hält die Datei weiter, bis es beendet wird. Das Setup meldet dann „Zugriff verweigert“; OBS schließen und „Try again“ wählen. Ein stilles Update bricht in diesem Fall ab, und Fog Scout startet wieder (`DeinitializeSetup`). Dateien, die bis dahin schon kopiert waren, bleiben dabei neu, der Rest alt. Zwischen benachbarten Builds mit denselben festen Paketversionen ist das voraussichtlich lauffähig; geprüft ist es nicht. Das Setup aus den Releases von Hand repariert es.

## Nachtrag 1.33.5 – Projekt-Durchsicht, Sicherheit Paket 1

Gemeinsamer Angriffsweg: Fog Scout läuft über seine Aufgabe erhöht, ohne Abfrage. Ein normales Programm desselben Nutzers könnte steuern, was Fog Scout als Administrator löscht, schreibt, startet oder lädt. Alle Befunde wurden nur im Code gelesen und unter Linux getestet; die Windows-Teile prüft der CI-Job `windows`.

| ID | Schwere | Befund | Fix 1.33.5 |
|---|---|---|---|
| S2 | Mittel | Aufräumen der Aufnahmen löschte als Admin, was der nutzerbeschreibbare Index nannte. Eine Junction im Ordner führte hinaus. | `fsops.delete_inside`: Handle ohne Reparse-Folgen, echter Pfad muss im Ordner liegen, Löschen am Handle |
| S3 | Mittel (praktisch niedrig) | Discord-Pipe ohne Identitätsschutz und ohne Lese-Timeout | `SECURITY_IDENTIFICATION`, `PeekNamedPipe` bis `TIMEOUT` |
| S4/S5 | Mittel | Windows-Ordner aus Umgebungsvariablen (für erhöhte Aufgaben vom Nutzer setzbar), Programme per blossem Namen (u. a. `nvml.dll` per `CDLL`, `$env:SystemRoot` in der Aufgabe) | `paths.system_dir`/`known_folder`/`system_exe`, Wächter `tests/test_elevated.py` |
| S6 | Niedrig | Admin-Helfer schrieben in eine vom Nutzer angelegte Ergebnisdatei, auch wenn sie ein Link war | `open_plain_for_write`/`_open_result`: kein Link, Linkzahl 1 |
| S8 | Niedrig | `SetDllDirectoryW(None)` nahm kurz den aktuellen Ordner in die DLL-Suche | `SetDllDirectoryW("")` |
| S9 | Klein | Nur `relupdate` lehnte http-Weiterleitungen ab; urllib reicht `Authorization` an jeden Weiterleitungs-Host weiter | `net.py` `SafeRedirect` für alle Web-Clients |

**Offen:**
- S1 (Mittel-hoch): Das Update-Setup wird aus `%LOCALAPPDATA%` gestartet; zwischen Prüfung und Start kann es getauscht werden. **Behoben in 1.34:** `restart.staged_setup` kopiert es nach `<Programmordner>\update` (`paths.app_update_dir`, nur Admins schreiben), hasht beim Kopieren und unter einem Handle mit Freigabe nur „lesen“ erneut und hält den Handle bis nach `ShellExecuteW`; Log und Arbeitsordner dort. Rest: läuft Fog Scout ausnahmsweise nicht erhöht (`PermissionError`), bleibt der alte Weg – dann fragt Windows selbst per UAC.
- S7: Signatur der Updates.
- `git` in `update.py` wird per PATH gefunden; betrifft nur den Betrieb über start.bat.
