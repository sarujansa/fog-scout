# Fog Scout – Optimierung 1.25 bis 1.25.3 (Abschlussbericht)

> **Historische Momentaufnahme** (Stand laut Dokument: 3. November 2026, PR #299). Die Angaben zu Version, offenen Punkten und Merge-Status gelten für diesen Tag; spätere Änderungen stehen in `HISTORY.md`.

**Auftrag:** „Fog Scout – umfassende Produkt-, UI/UX-, Funktions- und Performance-Optimierung“ (Phasen 0 bis 10).

**Stand:** 3. November 2026, Zweig `claude/funny-feynman-gt5t6n`, PR senisinx/fog-scout#299 – **nicht gemergt**.

`IMPROVEMENTS_REPORT.md` (1.22.3–1.23.1) und `PHASE2_REPORT.md` (1.24–1.24.7) bleiben unverändert. Dieser Bericht ist eine neue Datei, um keinen vorhandenen Bericht zu überschreiben.

## 0. Ausgangslage, Vorgehen, Bestandsaufnahme

### Phase 0 – Sicherheit

- **Ausgangspunkt:** Arbeitsbaum sauber, Zweig `claude/funny-feynman-gt5t6n`, HEAD `3232a00`.
- **Stand der Basis:** PR 299 ist offen, `main` steht auf `eb94fec`. Gearbeitet wird auf dem Stand von PR 299, weil die beiden letzten Durchgänge sonst kollidieren würden.
- **Entscheidungen von Saru am Anfang:**
  - Je Arbeitspaket ein Commit und ein Push auf diesen Zweig, **kein Merge**. Grund: Der Cloud-Container ist flüchtig; ohne Push wäre die Arbeit gefährdet.
  - Die Navigation behält acht Seiten und Strg+1 … 9; sie wird nur geschärft.
- **Ablauf:** keine destruktiven Git-Befehle, keine fremden Änderungen. Die Vergleichsbasis liegt als eigener Worktree auf `3232a00` im Scratchpad.
- **Baseline:** Suite **1222 bestanden, 37 übersprungen, 0 fehlgeschlagen**, pyflakes ohne Befund, Screenshots in 27 Varianten (Dunkel/Hell/OLED × 100/125/150 % × 1100×760/1280×800/1600×1000).

### Phase 1 – Architektur

Die Architektur ist in `CLAUDE.md` (Abschnitt „Architektur“) je Datei beschrieben. Hier nur der Überblick:

```
__main__ → splash → App (app.py + Mixins app_*)
            │  events-Queue ← Worker-Thread (Erkennung: capture → detector/ocr → matchend/lobby)
            │                 ← Recorder-Thread (OBS), ConnectionWatch, Uploader, MediaWatcher …
            ├─ uimodel (Tk-ähnliches Modell) → app_qt.ui_state → qt_pages/qt_views (Qt zeichnet)
            ├─ Overlay: overlay_win32/overlay_qt + skin + layout (rein) + app_place/app_sysinfo
            └─ Daten: config (settings.json), history/official (JSONL, LineCache), obsrec-Indizes
```

**Bewertung:**

- **Gut gelöst, nicht umbauen:**
  - Trennung Modell → Qt, reine Logikmodule mit Tests.
  - Ereignisse aller Threads über eine Queue in den GUI-Thread.
  - Seiten erst bei Bedarf bauen, Caches mit klaren Schlüsseln.
  - 1222 Tests.
- **Gekoppelt, aber bewusst:** Die Mixins von `App` teilen sich Zustand (`self.settings`, `self.recorder` …). Ein Umbau hätte hohes Regressionsrisiko ohne Nutzen für den Spieler – nicht angefasst.
- **Hohes Regressionsrisiko:** Rundenende-Erkennung, Overlay-Platzierung, Speicherkern der Editor-Projekte, hosts-Datei. In diesem Durchgang **nicht berührt**.

### Phase 1 – Audit und Priorisierung

**Grundlage:**

- Die offenen Listen der beiden letzten Berichte (`IMPROVEMENTS_REPORT.md` D, `PHASE2_REPORT.md` 5 und 7).
- Die neuen Screenshots; jeder Punkt wurde im Code bzw. am Bild nachgeprüft.
- Die zwölf Kriterien je Seite waren in den beiden letzten Durchgängen schon systematisch geprüft. Hier sind nur die Punkte aufgeführt, die danach noch offen waren oder neu gefunden wurden.

| Prio | Bereich | Problem (geprüft) | Lösung | Nutzen | Risiko | Stand |
|---|---|---|---|---|---|---|
| P1 | Alle Eingabefelder | Platzhaltertext 3,3:1 (hell) – **Ursache gefunden:** Setzt das Stylesheet `color`, nimmt Qt für Platzhalter die Textfarbe mit 50 % Alpha; die Palette kam nie an | `placeholder-text-color` im Stylesheet | Suchfelder lesbar | gering | 1.25 |
| P1 | Alle Seiten | Scroll-Griffe 1,1–1,5:1, Kasten-Griffe 1,3:1, Map-Balken 2,4/2,8:1 – man sieht nicht, dass/wo eine Liste scrollt | Token `handle` (≥ 3:1 auf Seite und Karte) | Orientierung | gering | 1.25 |
| P1 | Aufnahmen | ★ ⚑ ▶ als Unicode aus beliebiger Schrift – zweimal zurückgestellt | `SignsDelegate`: gezeichnete Glyphen, Tooltip in Worten | Konsistenz | mittel | 1.25.1 |
| P1 | Performance | Klicks/Suchen kurz nach dem Start warteten bis 198 ms auf den Seitenaufbau im Hintergrund | Vorbauen pausiert nach Eingaben | spürbar schneller | gering | 1.25.1 |
| P2 | Maps | Realm-Name „Hawkins National Laborat…“ bei scrollender Liste; Zähler 3,3:1 | Breite nach Zähler, Dim-Farbe | Lesbarkeit | gering | 1.25 |
| P2 | Reiter | Rahmen mit offenen Ecken (100/125 %), Karten doppelt gerahmt | Linie statt Rahmen | ruhiger | gering | 1.25 |
| P2 | Navigation | Marke als „(“ gezeichnet | gerader Balken | Präzision | gering | 1.25 |
| P2 | Statistik | Fehlende Match-Daten dreimal untereinander erklärt | einmal, mit Knopf | weniger Rauschen | gering | 1.25.1 |
| P2 | Einstellungen | 14 Hotkeys in einem Block | Gruppen Karte/Erkennung/Aufnahmen | Auffindbarkeit | gering | 1.25.2 |
| P2 | Aufnahmen | „Ursache: ConnectionRefusedError“ | Ursache in Worten | verständlich | gering | 1.25.2 |
| P2 | Speicher | `cache/maps_dark` wuchs mit jeder Stil-Version und jedem geänderten Bild | `mapstyle.prune` | Plattenplatz | gering | 1.25.3 |
| P3 | Overlay | „Spielbild“ in der Vorschau 2,2:1 | 5,1:1 | Lesbarkeit | gering | 1.25.2 |
| P3 | Einstellungen | „1 Dateien“, Tooltip „1 Marken“ | Einzahl | Sprache | gering | 1.25 / 1.25.3 |
| P3 | diverse | siehe Abschnitt D | – | – | – | zurückgestellt |

**P0:** Es wurde kein Fehler mit Datenverlust oder Sicherheitsrisiko gefunden. Der einzige rote Check (CodeQL, Abschnitt C) ist ein eingeordneter Fehlalarm.

## A. Umgesetzte Verbesserungen

### UI/UX und Designsystem (1.25)

**Neues Token `handle`** in `qt_theme.colours()`:
- Berechnet von `_handle`: Dim über dem Seitengrund, nur so stark wie nötig für `HANDLE_CONTRAST` = 3:1 auf Seite **und** Karte (WCAG 1.4.11 für Bedienelemente).
- Gilt für Scroll-Griffe, die Griffe ⋮⋮ der Kästen und die Map-Balken der Statistik; Hover = Dim.
- Gemessen:

| Element | Hell vorher → nachher | Dunkel | OLED |
|---|---|---|---|
| Scroll-Griff auf Seite / Karte | 1,09:1 → 3,25 / 3,6:1 | 1,45:1 → 3,82 / 3,2:1 | 1,22:1 → 3,36 / 3,11:1 |
| Kasten-Griff | 1,44:1 → ≥ 3,25:1 | 1,25:1 → ≥ 3,2:1 | 1,31:1 → ≥ 3,11:1 |
| Map-Balken | 2,4:1 → 3,6:1 | 2,8:1 → 3,2:1 | 3,9:1 → 3,11:1 |
| Platzhaltertext auf dem Eingabefeld (Suche, Log-Filter) | 3,3:1 → 6,0:1 (Dim) | 4,2:1 → 6,0:1 | 4,47:1 → 7,6:1 |

- **Realm-Liste:** Zähler in Dim statt in der Platzhalterrolle; der Name ist nur noch um die Breite des Zählers gekürzt, nicht um feste 36 px. „Hawkins National Laboratory“ ist bei scrollender Liste wieder ganz lesbar (Bild 1280×800).
- **Navigation:** Die Marke der aktiven Seite ist ein gerader Balken.
- **Reiter (Statistik, Aufnahmen):** Unter der Reiterzeile eine Linie statt eines gerundeten Rahmens. Der Rahmen hatte offene Ecken und rahmte die Karten darin ein zweites Mal.

### Statistik (1.25.1)

- Der Satz zur Heatmap „Killer × Map“ nennt keinen Einstellungspfad mehr.
- Die Zeile darunter erklärt mit Knopf, wie man die Match-Daten einrichtet. Vorher stand derselbe Grund dreimal untereinander.

### Aufnahmen (1.25.1, 1.25.2)

- **Statusspalte von Runden und Clips:** Stern, Fahne und Abspielzeichen sind gezeichnete Glyphen im Stil des Fensters (`qt_views.SignsDelegate`).
  - Der Zelltext bleibt, also bleiben Sortieren, Kopieren und Tests unverändert.
  - Beim Darüberfahren erscheint die Bedeutung in Worten („behalten (nie aufgeräumt) · 2 Marken · auf YouTube“).
- **OBS nicht erreichbar:** Die Karte nennt die Ursache in Worten, z. B. „OBS läuft nicht, oder sein WebSocket-Server ist aus“ statt `ConnectionRefusedError`.

### Einstellungen (1.25, 1.25.2)

- **Hotkeys in Gruppen:** „Karte im Spiel“, „Erkennung“, „Aufnahmen“ (`HOTKEY_GROUPS`).
  - Schlüssel, Belegungen und die Suche sind unverändert.
  - Paare wie Grösser/Kleiner stehen untereinander.
- **Sicherung:** „1 Datei“ statt „1 Dateien“.

### Overlay (1.25.2)

- Die Beschriftung „Spielbild“ in der Vorschau ist lesbar (5,1:1 statt 2,2:1).
- Das Overlay im Spiel ist **nicht** verändert.

### Navigation und Übersicht

- Die Struktur bleibt (Entscheidung von Saru).
- Die Übersicht wurde gegen die Fragen des Auftrags geprüft; alle sind schon beantwortet, mit vorhandenen Daten:

| Frage | Antwort auf der Übersicht |
|---|---|
| Läuft Fog Scout korrekt? Ist DBD offen? | Status unten in der Navigation bzw. unter dem Titel |
| Zustand der Erkennung | Karte „Funktionen“ |
| Erkannte Map | Kopf der Seite |
| Rundenzeit | Kachel |
| OBS verbunden / nimmt auf | „Aufnahmen mit OBS – nimmt auf / bereit / OBS nicht verbunden“ |
| Warnungen | Navigation und Funktionen, in Farbe und Worten |

- Deshalb kamen keine neuen Elemente dazu.

### Neue Funktionen

- **Keine.** Die Prüffelder des Auftrags (Onboarding, Quick Actions, Diagnose, Personalisierung, Statistik, Maps, Integrationen) wurden gegen den Bestand geprüft.
  - Quick Actions gibt es seit 1.14 (Funktionen-Karte).
  - Die Fehlerhilfen kamen in 1.24.x dazu, die Map-Notizen und eigenen Bilder in 1.8.54/1.22.1, der Export mit Filtern in 1.8.91.
- Neue Funktionen mit klarem Nutzen und geringem Risiko blieben nicht übrig; Abschnitt D nennt die bewusst zurückgestellten.

### Architektur

- **Keine Umbauten.** Neue Teile:
  - **Token:** `handle`.
  - **Funktionen:** `SignsDelegate`/`sign_words`, `cause_words`, `mapstyle.prune`.
  - **Konstanten:** `WARM_QUIET_S`, `HOTKEY_GROUPS`.
- Datenformate, Einstellungsschlüssel, Hotkeys, Migrationen, Update/Autostart/Tray und Overlay-Lebenszyklus sind unverändert.

## B. Performance

**Methode:**

- **Messaufbau:** A = `3232a00` (vor diesem Durchgang, Worktree), B = `0611495` (1.25.3) – verschränkt gemessen, je Lauf ein eigener Prozess.
- **Umgebung:** Linux-Container, 4 CPUs, Python 3.13.18, Qt offscreen, Daten von `tools/bench.py`, 3. 11. 2026.
- **Angabe:** Median (Spannweite) in ms; Prozent = (B − A) / A.
- **Grenzen:** geteilter Cloud-Rechner, keine GPU, kein Windows. Die Werte gelten **nicht** für Windows; dort ist nichts gemessen.

| Messpunkt | vorher (A) | nachher (B) | n | Bewertung |
|---|---|---|---|---|
| Start gesamt | 516,6 (471,5–614,7) | 516,8 (457,8–618,9) | 20 | gleich |
| Import / App gebaut | 333,3 / 151,4 | 333,8 / 157,4 | 20 | im Rauschen |
| Speicher nach dem Start (RSS) | 188,9 MB | 188,9 MB | 20 | gleich |
| Klick → Handler, Median / Max | 0,2 / 2,1 | 0,2 / 0,3 | 6 | Max kleiner |
| **Map-Suche kurz nach dem Start**, je Eingabe (c / co / coal / xyz / leer / midwich / leer) | 120,9 / 155,6 / 63,6 / 128,3 / 122,0 / 67,1 / 40,9 | 51,0 / 23,7 / 18,6 / 18,5 / 35,1 / 36,2 / 30,6 | 12 | **−25 bis −86 %** |
| Statistik `_stats_render`, 5000 Runden | 8,44 (7,21–9,32) | 8,34 (7,10–9,15) | 6 | gleich |
| Statistik Ereignisse danach | 10,55 (7,71–11,74) | 2,46 (2,03–2,77) | 6 | −77 % (Vorbauen pausiert) |
| Übersicht `_qt_refresh` | 0,23 (0,19–0,30) | 0,19 (0,17–0,41) | 6 | gleich |
| Aufnahmen rendern, 300 | 8,1 (7,6–11,8) | 8,2 (7,6–9,8) | 6 | gleich |
| Leerlauf-CPU eingeschwungen | 1,5 % eines Kerns | 1,5 % | 4 | gleich |
| Leerlauf-RSS | 238,1 MB | 237,7 MB | 4 | gleich |
| Erste Seitenbesuche ohne Vorbauen (Bau + Füllen) | Übersicht 2,5 · Maps 127,6 · Overlay 338,1 · Statistik 162,0 · Aufnahmen 170,9 · Server 100,5 · Einstellungen 379,7 · Log 61,6 | 2,9 · 125,5 · 336,3 · 158,1 · 175,2 · 108,6 · 387,8 · 70,8 | 8 | gleich (Spannen überlappen) |

**Map-Suche:**

- Gemessen mit `ab_search2`: Eingabe über `_qt_post` wie im echten Suchfeld, 150 ms Tipp-Pause, gemessen wird die Rechenzeit der Ereignisschleife je Eingabe.
- Gewinn: Das Vorbauen der Seiten (`_qt_warm`) setzt nach einer Eingabe 0,4 s aus. Die ersten Sekunden nach dem Start reagieren damit sofort.
- Danach ist das Vorbauen fertig, und beide Stände sind gleich.

**Hinweis zum Szenario „pages“ von `tools/bench.py`:**

- Die ersten Besuche schwankten zwischen A und B um −29 % bis +49 %, z. B. Einstellungen 248 gegen 371 ms.
- Ursache: Ob das Vorbauen eine Seite schon vor dem Besuch gebaut hat, hängt vom Zeitpunkt ab.
- Mit abgeschaltetem Vorbauen (letzte Zeile der Tabelle) sind alle Seiten gleich teuer. Das ist also kein Effekt des Codes.

**Nicht gemessen:**

- Kaltstart unter Windows, Zeit bis zum ersten sichtbaren Fenster auf echter Hardware.
- CPU während der Erkennung im Spiel, Speicher nach Stunden Laufzeit.
- Clip-Editor mit echten Aufnahmen.
- Diese Werte brauchen Windows und DBD. Zuletzt gemessen in 1.16.1 bzw. 1.22.4 (`HISTORY.md`); dieser Durchgang hat die betroffenen Pfade nicht verändert.

## C. Tests

**Je Paket:** volle Suite und `pyflakes fogscout tests tools`:

| Stand | bestanden | übersprungen | fehlgeschlagen |
|---|---|---|---|
| Baseline `3232a00` | 1222 | 37 | 0 |
| 1.25 | 1222 | 37 | 0 – nach einem Test, der „1 Dateien“ erwartete (angepasst) |
| 1.25.1 | 1225 | 37 | 0 |
| 1.25.2 | 1226 | 37 | 0 |
| 1.25.3 | 1227 | 37 | 0 |

**Neue Tests:**
- `test_placeholders_grips_and_handles_are_readable_in_every_theme`: alle Themen × Hell/Dunkel/OLED plus eigene Farbe; schlägt ohne die Änderung nachweislich fehl.
- `test_status_signs_are_drawn_glyphs_with_words`
- `test_the_page_warm_up_waits_while_the_user_clicks_or_types`
- `test_the_hotkeys_tab_lists_every_hotkey_once_in_groups`
- `test_the_style_cache_keeps_only_the_current_version_and_newest_source`

**Bewusst geänderte Tests** (geändertes Verhalten, nicht abgeschwächt):
- Sicherung: „1 Datei,“ statt „1 Dateien“.
- Aufnahme-Karte: Ursache in Worten statt `ConnectionRefusedError`.

**Übersprungen:** dieselben 37 wie in der Baseline (Windows-only, echtes ffmpeg/node je nach Umgebung).

**CI:**
- `19894c7` (1.25) und `e0ba389` (1.25.1): Tests unter Linux und Windows grün, auf echten Runnern.
- 1.25.2 und 1.25.3 laufen beim Schreiben dieses Berichts; das Ergebnis steht in der PR-Beschreibung.
- **CodeQL:** Ein roter Sammel-Check besteht seit `06573af`: „weak hashing of sensitive data“ in `obsrec.auth_string`.
  - Eingeordnet als Fehlalarm: Das ist die obs-websocket-5-Anmeldung, die das Protokoll so vorschreibt, und die Zeile ist seit 1.4 unverändert. Begründung in `PHASE2_REPORT.md` § 11.
  - Den Alert in GitHub schliessen muss Saru.

**Sichtprüfung:**
- Screenshots in 27 Varianten sowie Hell/Dunkel mit den Akzenten Blutrot und Blau, selbst angesehen.
- Zusätzlich die Reiter Hotkeys und Statistik, Ausschnitte der Statusspalte und der Realm-Liste; Kontraste gerechnet.

**Nicht durchführbar** (kein Windows, kein DBD, kein OBS im Container):
- Map-Erkennung live, Overlay im Spiel, Hotkeys, Match-Ende, Rundentimer im Match.
- OBS-Verbindung und Aufnahmen, Tray/Autostart/Updates.
- Diese Prüfungen sind **nicht** durchgeführt. Die Windows-CI deckt natives Overlay, Hinweisfenster, Hotkey-Registrierung und windows-capture ab.

### Abschlussaudit (Phase 9)

- **Besser oder nur anders?**
  - Kontraste: gemessen besser.
  - Statussymbole: einheitlich, mit Worten.
  - Hotkeys: auffindbarer.
  - OBS-Fehler: verständlich.
  - Map-Suche nach dem Start: gemessen schneller.
- **Reiterlinie** statt Rahmen: eine Geschmacksfrage. Sie behebt aber die offenen Ecken nachweislich und spart den doppelten Rahmen. Behalten.
- **Neue Komplexität:** ein Delegate (60 Zeilen), eine Prune-Funktion (40 Zeilen), sonst Werte. Keine neuen Abhängigkeiten, Threads oder Datenformate.
- **Eigene Durchsicht des Diffs:**
  - Ein Fund: Der neue Tooltip sagte „1 Marken“; behoben in 1.25.3.
  - Kein Fund zu harten Regeln: kein Netz, kein Prozesszugriff, keine Spieldateien.
  - Gelöscht wird nur im eigenen `cache/maps_dark` und nur mit eigenem Namensmuster.
- **Unabhängige Agenten-Prüfung:** diesmal nicht durchgeführt (Nutzungslimit beim letzten Durchgang). Der Diff ist klein: 19 Dateien, +323/−34 ohne Doku.
- **Zurückzunehmen:** nichts.

## D. Nicht umgesetzte Empfehlungen

| Punkt | Begründung |
|---|---|
| Reglerknopf und -spur in OLED (1,3:1) | Die Regler zeichnet Qts Fusion-Stil aus der Palette; ein eigener QSS-Regler ändert die Geometrie aller Regler (auch `CapSlider` mit Grenzmarke) – eigene Prüfung am echten Fenster nötig |
| Zwei Chevron-Stile in der Filterzeile der Statistik | Die Auswahllisten zeichnet Qt, „Filter“ ist ein Knopf mit gezeichnetem Zeichen; Vereinheitlichung bräuchte eigene Combobox-Pfeile für alle Seiten |
| „F8“ fest in ~12 Texten | Betrifft nur umbelegte Clip-Tasten; Tooltip-Schlüssel hängen an den Beschriftungen – eigener Schritt |
| Kachelbild vor dem Laden als dunkles Feld (Hell) | Gewollt: die Karten liegen auf dem dunklen Medien-Hintergrund (`media_bg`), das Feld ist sein Platzhalter |
| Navigation umbauen / „Log“ → „Diagnose“ | Entscheidung von Saru: Struktur behalten; die Seite heisst weiter „Log“, ihr Zweck steht in der Zeile unter dem Titel |
| Server-Seite bei 1280×800: letzte Zeile am Fensterrand | Die Seite scrollt; kein Inhalt geht verloren |
| Export mit Fortschritt, Setup-Fussleiste, Maps-Klickverzögerung | Export < 1 s (gemessen 1.23); die anderen sind Bedienentscheidungen für Saru |
| onnxruntime/urllib später laden | Früher gemessen ohne belegbaren Gewinn (`IMPROVEMENTS_REPORT.md` D) |
| Neue Funktionen (Favoriten, Befehlspalette …) | Kein Nutzen über das Vorhandene hinaus (Suche Strg+F, „Zuletzt gespielt“, Funktionen-Karte) |

## E. Geänderte Dateien

| Datei | Änderung |
|---|---|
| `fogscout/qt_theme.py` | Token `handle`, `_handle`, `HANDLE_CONTRAST`; `placeholder-text-color`; Scroll-Griffe; Navigationsmarke; Reiterlinie |
| `fogscout/qt_views.py` | `SignsDelegate`, `sign_words`, `SIGNS`; `MapBars` mit `handle`; Heatmap-Hinweis; `BAR_NEUTRAL` entfernt |
| `fogscout/qt_pages.py` | `Grip` mit `handle` |
| `fogscout/qt_maps.py` | `RealmDelegate`: Zählerfarbe, Breite |
| `fogscout/qt_window.py` | `HOTKEY_GROUPS`, Spec der Hotkeys |
| `fogscout/qt_preview.py` | Beschriftung „Spielbild“ |
| `fogscout/app_qt.py` | `WARM_QUIET_S`, `signs` im Tabellenzustand |
| `fogscout/app_recordings.py` | `CAUSES`/`cause_words`, `_dbdms_signs` |
| `fogscout/app_settings.py` | Einzahl der Sicherung |
| `fogscout/mapstyle.py`, `fogscout/app.py` | `prune`, Aufruf vor `warm` |
| `fogscout/i18n_en.py`, `fogscout/__init__.py` | Texte, Version 1.25.3 |
| `tests/test_qt.py`, `tests/test_uimodel.py`, `tests/test_mapstyle.py`, `tests/test_recordings_page.py` | Tests (siehe C) |
| `README.md`, `README.en.md`, `HISTORY.md`, `CLAUDE.md` | Doku je Version |

## F. Bekannte Probleme und offene Windows-/Spieltests

1. **Am Windows-PC ansehen, bei 100/125/150 %:**
   - Scroll-Griffe und Kasten-Griffe sichtbar, aber nicht aufdringlich.
   - Platzhalter der Suche lesbar.
   - Reiter mit Linie.
   - Die Navigationsmarke gerade.
2. **Aufnahmen:** Statusspalte mit Stern/Fahne/Abspielzeichen; Tooltip beim Darüberfahren.
3. **OBS schliessen → Seite Aufnahmen:** Ursache in Worten.
4. **Einstellungen › Hotkeys:** drei Gruppen; eine Taste ändern und speichern.
5. **Kartenstil umschalten:** `cache/maps_dark` behält nur aktuelle Dateien. Die Log-Datei nennt einmal „Kartenstil-Cache: N alte Bilder entfernt“.
6. **Offen aus früheren Berichten:** CodeQL-Alert schliessen, Reglerkontrast in OLED, siehe D.

## G. Git-Zustand

- **Zweig:** `claude/funny-feynman-gt5t6n`, Ausgangscommit `3232a00` (PR 299 nach Phase 2; `main` = `eb94fec`).
- **Commits** (Autor = GitHub-Konto des Nutzers, wie in `CLAUDE.md` festgelegt):
  - `19894c7` 1.25
  - `e0ba389` 1.25.1
  - `f5ce9eb` 1.25.2
  - `0611495` 1.25.3
  - dieser Bericht mit Doku-Nachtrag
- **Push:** Alle Commits sind nach `origin` gepusht; PR 299 enthält sie. **Nicht gemergt.**
- **Uncommittete Änderungen:** keine nach dem Doku-Commit.
- Mess-/Screenshot-Skripte und Bilder liegen nur im Scratchpad der Sitzung, nicht im Repository.
