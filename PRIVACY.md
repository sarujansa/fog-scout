# Datenschutzerklärung – Fog Scout

*English version below.*

Fog Scout ist ein Open-Source-Programm für Windows, das lokal auf deinem PC läuft. Es gibt keinen Server, kein Konto, keine Telemetrie und keine Werbung. Alles, was das Programm speichert (Einstellungen, Rundenverlauf, Statistik), liegt in seinem eigenen Ordner auf deinem PC. Dieses Dokument nennt alles, was das Programm nach aussen sendet – jeder Punkt ist einzeln abschaltbar oder nur auf deinen Klick aktiv.

| Funktion | Wohin | Was | Wann |
|---|---|---|---|
| Updates | GitHub (`github.com`) | `git fetch` dieses Repositorys | Beim Start (abschaltbar) und auf Klick „Jetzt nach Updates suchen“ |
| Tab „Server“ | AWS GameLift (`amazonaws.com`, `api.aws`) | Ping (ICMP oder UDP-Beacon), DNS-Auflösung | Nur im Tab „Server“ bzw. solange „Verbunden mit“ läuft |
| Offizielle Match-Daten | Keine eigene Verbindung | Dein Browser lädt mit einem Userscript die Match-Daten, die stats.deadbydaylight.com dir selbst anzeigt, als Datei in den Download-Ordner; das Programm liest nur diese Datei | Nur mit dem Userscript, das du selbst installierst |
| OBS | Nur `127.0.0.1` (dein eigener PC) | Befehle an OBS Studio über obs-websocket | Nur mit eingeschalteter Aufnahme |
| Discord Rich Presence | Nur der lokale Discord-Client (IPC-Pipe) | Map, Rolle, Lobby-Zustand | Nur eingeschaltet und mit eigener Application-ID |
| Spotify „Als nächstes“ | Spotify Web API (`api.spotify.com`, `accounts.spotify.com`) | Anmeldung (OAuth 2 PKCE), Lesen der Warteschlange – nie steuern | Nur eingeschaltet und nach deiner Anmeldung |
| YouTube-Upload | Google (`accounts.google.com`, `oauth2.googleapis.com`, `www.googleapis.com`) | Siehe unten | Nur eingeschaltet bzw. je Datei auf Klick |
| Suche mit Claude (seit 1.26) | Anthropic (`api.anthropic.com`) | Deine Suchfrage und die festen Namen der Einstellungen, Seiten und Aktionen des Programms (nur Texte, die wörtlich im Programm stehen – seit 1.28 nie Statuszeilen, Fehlermeldungen, Pfade, Pings oder Statistikwerte); nie Runden, Maps, Killer oder Spieldaten. Dein eigener API-Key wird mit der Windows-Datenschutz-API (DPAPI) verschlüsselt gespeichert; ist sie nicht verfügbar, gilt er nur bis zum Beenden und wird nicht gespeichert. Nie in Sicherung, Log oder Diagnose | Nur eingeschaltet und nur, wenn du in der Suche „Claude fragen“ wählst |
| Clip-Editor mit Claude (seit 1.27) | Anthropic (`api.anthropic.com`) | Deine Bitte und der Schnitt als Zahlen (Zeiten, Tempo, Blenden, Export-Art, eigene Short-Texte, Zeitpunkte deiner F8-Marken) – kein Bild, kein Dateiname, keine Map, kein Killer | Nur mit eingeschaltetem Häkchen „Im Clip-Editor Claude nutzen“ und nur auf „Vorschlagen“ |
| Stats-Seite nach dem Spiel öffnen | Dein Standardbrowser öffnet `stats.deadbydaylight.com` (das Programm selbst sendet nichts) | – | Nur mit dem Häkchen „Stats-Seite öffnen, wenn DBD beendet wird“ (Standard aus), frühestens 15 s nachdem DBD geschlossen ist und eine Runde gespielt wurde – nie während DBD läuft |

Das Programm fasst Dead by Daylight nie an: keine Eingaben, kein Zugriff auf den Spielprozess oder Spieldateien. Es liest Bildschirmpixel, Fensterinformationen und – auf Wunsch – Systemwerte (CPU/GPU-Auslastung und -Temperatur).

**Zugangsdaten auf diesem PC:** API-Key (Claude), OBS-Passwort, Spotify- und YouTube-Anmeldung und das YouTube-Client-Secret werden nur mit der Windows-Datenschutz-API (DPAPI, an dein Windows-Konto gebunden) verschlüsselt in `settings.json` gespeichert. Ist sie nicht verfügbar, gilt der Wert nur bis zum Beenden und wird nicht gespeichert – nie als Klartext. Werte aus Versionen vor 1.28 (nur Base64) werden beim Start einmal verschlüsselt; geht das nicht, bleiben sie und das Log nennt die Einstellung (nie den Wert). Keiner dieser Werte steht in einer Sicherung (Export), im Log oder in der Diagnose; die YouTube-Warteschlange (Upload-Adressen, Dateipfade) kommt seit 1.28 ebenfalls nicht in den Export.

**„Diagnose kopieren“** legt einen Text in die Zwischenablage, den du selbst weitergibst: Programm-, Python- und Qt-Version, Fenster- und Overlay-Zustand (Positionen, Grössen), die letzten Erkennungs- und Rundenende-Prüfungen, Zähler und Zeiten der Einstellungen und Dienste, Server-Adressen maskiert. Andere Programme erscheinen nur als Art und Fensterklasse („anderes Programm [Klasse]“), nie mit Fenstertitel; der Benutzerordner steht als `~` (seit 1.28). Keine Zugangsdaten, keine Liedtitel, keine Claude-Fragen.

## YouTube-Upload (Google-Nutzerdaten)

Der YouTube-Upload ist standardmässig aus. Schaltest du ihn ein, gilt:

- **Angeforderter Bereich (Scope):** `https://www.googleapis.com/auth/youtube.upload` – das Programm kann Videos auf deinen Kanal hochladen, sonst nichts. Nur wenn du „Uploads in Playlists einsortieren“ einschaltest, fragt die Anmeldung zusätzlich `https://www.googleapis.com/auth/youtube` an; davon nutzt das Programm ausschliesslich das Auflisten deiner eigenen Playlists (Titel und ID, für die Auswahl) und das Einsortieren des gerade hochgeladenen Videos in die gewählte Playlist. Es liest sonst keine Daten aus deinem Google-Konto oder Kanal; die Antworten, die es auswertet, sind die Zugangstoken, die Video-ID des hochgeladenen Videos und diese Playlist-Liste.
- **Gesendet werden** die Videodatei aus deinem Aufnahmeordner sowie Titel und Beschreibung, die das Programm aus Map, Rolle/Killer, Datum und Dauer bildet. Keine Spielernamen, keine anderen Daten.
- **Gespeichert wird** das Refresh-Token von Google zusammen mit Client-ID und Client-Secret deines eigenen OAuth-Clients – verschlüsselt mit der Windows-Datenschutz-API (DPAPI) in der Datei `settings.json` auf deinem PC. Diese Werte kommen in keine Sicherung und keinen Export. „YouTube-Verbindung trennen“ löscht sie; zusätzlich kannst du den Zugriff jederzeit unter <https://myaccount.google.com/permissions> entziehen.
- **Weitergabe:** keine. Die Daten gehen nur an Google und bleiben sonst auf deinem PC. Es gibt keinen Server des Programms, keine Analyse, keine Werbung.
- **Kontrolle:** Jeder Upload lässt sich in der Warteschlange entfernen, die lokale Datei bleibt immer erhalten. Die Sichtbarkeit (privat, nicht gelistet, öffentlich) wählst du selbst; Standard ist privat.

Die Nutzung von Informationen aus Google-APIs durch Fog Scout richtet sich nach der [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy) einschliesslich der Limited-Use-Anforderungen.

## Kontakt

Fragen und Hinweise: über die Issues dieses Repositorys (<https://github.com/sarujansa/fog-scout/issues>).

---

# Privacy Policy – Fog Scout

Fog Scout is an open-source program for Windows that runs locally on your PC. There is no server, no account, no telemetry and no advertising. Everything the program stores (settings, round history, statistics) lives in its own folder on your PC. This document lists everything the program sends anywhere – each item can be switched off on its own or is active only when you click.

| Feature | Where to | What | When |
|---|---|---|---|
| Updates | GitHub (`github.com`) | `git fetch` of this repository | At start (can be disabled) and on "Check for updates now" |
| "Server" tab | AWS GameLift (`amazonaws.com`, `api.aws`) | Ping (ICMP or UDP beacon), DNS lookups | Only in the "Server" tab or while "Connected to" runs |
| Official match data | No connection of its own | Your browser, with a userscript, saves the match data that stats.deadbydaylight.com shows you as a file in your download folder; the program only reads that file | Only with the userscript you install yourself |
| OBS | Only `127.0.0.1` (your own PC) | Commands to OBS Studio over obs-websocket | Only with recording enabled |
| Discord Rich Presence | Only the local Discord client (IPC pipe) | Map, role, lobby state | Only when enabled, with your own application ID |
| Spotify "Up next" | Spotify Web API (`api.spotify.com`, `accounts.spotify.com`) | Login (OAuth 2 PKCE), reading the queue – never controlling | Only when enabled and after your login |
| YouTube upload | Google (`accounts.google.com`, `oauth2.googleapis.com`, `www.googleapis.com`) | See below | Only when enabled, or per file on click |
| Search with Claude (since 1.26) | Anthropic (`api.anthropic.com`) | Your search question and the fixed names of the program's settings, pages and actions (only texts that stand verbatim in the program – since 1.28 never status lines, error messages, paths, pings or statistics); never rounds, maps, killers or game data. Your own API key is stored encrypted with the Windows Data Protection API (DPAPI); when that is not available it is kept for the current session only and not stored. Never in a backup, the log or the diagnosis | Only when enabled and only when you pick "Ask Claude" in the search |
| Clip editor with Claude (since 1.27) | Anthropic (`api.anthropic.com`) | Your wish and the cut as numbers (times, speed, fades, export type, your own short texts, times of your F8 marks) – no picture, no file name, no map, no killer | Only with "Use Claude in the clip editor" ticked and only on "Suggest" |
| Open the stats page after the game | Your default browser opens `stats.deadbydaylight.com` (the program itself sends nothing) | – | Only with the tick "Open the stats page when DBD is closed" (off by default), at the earliest 15 s after DBD was closed and a round was played – never while DBD runs |

The program never touches Dead by Daylight: no input, no access to the game process or game files. It reads screen pixels, window information and – if you want – system values (CPU/GPU load and temperature).

**Credentials on this PC:** API key (Claude), OBS password, Spotify and YouTube login and the YouTube client secret are stored in `settings.json` only encrypted with the Windows Data Protection API (DPAPI, bound to your Windows account). When it is not available, the value only lasts until you quit and is not stored – never as clear text. Values from versions before 1.28 (Base64 only) are encrypted once on the start; if that is not possible they stay and the log names the setting (never the value). None of these values is in a backup (export), the log or the diagnosis; since 1.28 the YouTube queue (upload addresses, file paths) is not exported either.

**"Copy diagnosis"** puts a text on the clipboard that you pass on yourself: program, Python and Qt version, window and overlay state (positions, sizes), the last detection and end-of-round checks, counters and times of the settings and services, server addresses masked. Other programs appear only as a kind and window class ("anderes Programm [class]"), never with a window title; your home folder shows as `~` (since 1.28). No credentials, no song titles, no Claude questions.

## YouTube upload (Google user data)

The YouTube upload is off by default. If you switch it on:

- **Requested scope:** `https://www.googleapis.com/auth/youtube.upload` – the program can upload videos to your channel and nothing else. Only if you enable "Sort uploads into playlists" does the login also ask for `https://www.googleapis.com/auth/youtube`; of that the program uses exclusively listing your own playlists (title and ID, for the choice) and sorting the video just uploaded into the chosen playlist. It reads no other data from your Google account or channel; the answers it evaluates are the access tokens, the video ID of the uploaded video and that playlist list.
- **Sent** are the video file from your recordings folder and a title and description the program builds from map, role/killer, date and length. No player names, no other data.
- **Stored** are Google's refresh token together with the client ID and client secret of your own OAuth client – encrypted with the Windows Data Protection API (DPAPI) in the file `settings.json` on your PC. These values never go into a backup or an export. "Disconnect YouTube" deletes them; you can also revoke the access at any time at <https://myaccount.google.com/permissions>.
- **Sharing:** none. The data goes only to Google and otherwise stays on your PC. There is no server of the program, no analytics, no advertising.
- **Control:** every upload can be removed from the queue; the local file is always kept. You choose the visibility (private, unlisted, public); the default is private.

Fog Scout's use of information received from Google APIs adheres to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

## Contact

Questions and remarks: through the issues of this repository (<https://github.com/sarujansa/fog-scout/issues>).
