# Fog Scout – Phase 2: Produkt-Redesign 1.24 bis 1.24.7 (Abschlussbericht)

> **Historische Momentaufnahme** (Stand laut Dokument: 3. November 2026, PR #299). Die Angaben zu Version, offenen Punkten und Merge-Status gelten für diesen Tag; spätere Änderungen stehen in `HISTORY.md`.

Auftrag: `prompt_phase2.md` („Entwicklungsphase 2: Produkt-Redesign, moderne Benutzeroberfläche, UX und gezielte Funktionsentwicklung“), acht Arbeitspakete.
Stand: 3. November 2026, Zweig `claude/funny-feynman-gt5t6n`, Pull Request senisinx/fog-scout#299 – **nicht gemergt**, der Merge bleibt Saru vorbehalten.

## 1. Ausgangszustand und untersuchte Architektur

**Git und Tests:**

- Ausgang war `main` = `eb94fec`: der Merge von PR #298, Version 1.23.1, Phase 1 vollständig integriert.
- Der Arbeitsbaum war sauber.
- Ausgangsstand der Tests: **1199 bestanden, 37 übersprungen, 0 fehlgeschlagen** (`pytest -q tests`, Linux, offscreen).

**Untersuchte Architektur:**

- **UI-Modell:** `uimodel.py` (Tk-ähnlich), daraus `app_qt.ui_layout`/`ui_state`. Qt zeichnet es über `qt_pages.AutoPage`/`FormPage`/`show_control`.
- **Handgemachte Seiten:** Übersicht (`OverviewPage`) und Maps (`MapsPage`).
- **Hauptfenster:** `qt_window.MainWindow` mit Navigation, Suche (Strg+F), Strg+1…9 und Seiten, die erst bei Bedarf gebaut werden.
- **Theme:** Tokens in `qt_theme` (`STATE`, `TYPE`, `RADIUS`, `PAD_CARD`). Gezeichnete Symbole in `qt_icons` (24er-Raster, bisher nur im Editor).
- **Weitere Module:** Status `status.user_state`; die Übersicht als reines Modell in `overview.py`.

Darauf wurde aufgebaut, statt ein zweites System daneben zu stellen.

**Audit** (je Seite, Screenshots in 27 Varianten = 3 Grössen × 3 Skalierungen × Dark/Light/OLED, jeder Befund im Code geprüft):

| Seite | Befund (vorher) | Paket |
|---|---|---|
| Hülle | Keine Marke, kein globaler Status (der Pill stand nur auf der Übersicht), unten leere Seitenleiste, kein Seitenzweck | 2 |
| Alle | Unicode als Symbole (↻ ▸ ✕ ▶ ← ▾/▴ ● ⏸ ⚑), kein `primary` im Modell, keine gemeinsame Darstellung leerer Zustände | 2, 3, 5 |
| Übersicht | „Schnell ein/aus“ ohne Zustand (OBS erreichbar? HWiNFO? Spotify angemeldet?), 6 von 10 Kacheln „–“ ohne Match-Daten, „Scannen“ immer Hauptaktion | 2, 3 |
| Maps | Suche ohne Treffer = leeres Raster | 3 |
| Overlay | `SPLIT_FROM` 1080: im 1280-px-Fenster liegen die Reiter unter der Vorschau (Scrollen zu jeder Einstellung) | 4 |
| Statistik | 4 von 8 Dashboard-Kacheln „–“ ohne Match-Daten; Hinweise mit ⚠/✓ im Text; leere Auswahl ohne Hinweis auf „Filter zurücksetzen“ | 4 |
| Aufnahmen | „Aufnahme ist aus.“ und „Aufnahmen sind aus.“ doppelt; Warnzeile nicht gelb; „OBS nicht erreichbar“ ohne Fehlerfarbe und ohne nächsten Schritt; Tabelle ohne Treffer bleibt leer | 5 |
| Server | „Auswahl anwenden“ nicht als Hauptaktion; unlesbare hosts-Datei nur Klartext, Knöpfe aktiv | 5 |
| Einstellungen | Fehler von „Verbindung testen“ grau wie ein Hinweis | 5 |
| Log | Leeres oder ganz gefiltertes Log = leere Fläche | 5 |

## 2. Redesign-Ziel und Designentscheidungen

**Ziel:** ein ruhiges Desktop-Werkzeug mit eigener Identität, kein Web-Dashboard. Der Spieler sieht auf jeder Seite, was Fog Scout gerade tut, und bei einem Problem den nächsten Schritt.

**Entscheidungen:**

- **Kein Rewrite, kein zweites Designsystem.**
  - Die bestehenden Tokens (`STATE` mit geprüftem Kontrast ≥ 4,5:1, `TYPE`, `RADIUS`, `PAD_CARD`) und `qt_icons` wurden erweitert.
  - Navigation, acht Seiten, Strg+1…9 und die Suche bleiben, damit Gewohnheiten nicht brechen.
- **Akzentfarbe nur für Zustand und Hauptaktion.**
  - Je Ansicht höchstens ein gefüllter Knopf (`ui.primary`).
  - Die Übersicht hat nur dann eine Hauptaktion, wenn der Spieler handeln muss: „Stimmt“ bei unsicherer Map, „Map wählen …“ bei ausgeschalteter Automatik.
  - „Scannen“ ist Notbehelf, nicht Hauptaktion.
- **Zustand nie nur über Farbe.**
  - `ui.level` setzt die Qt-Eigenschaft `state` (ok/warn/err/off) immer an einem Label, das den Zustand auch in Worten nennt.
  - Grün, Gelb und Rot kommen aus `qt_theme.STATE`, geprüft für Dark, Light und OLED.
- **Gezeichnete Symbole statt Unicode.**
  - Neue Glyphen im `qt_icons`-Raster: star, warning, chevron_right/down/up, rotate, record, back, external.
  - `ui.glyph(w, name)` → `qt_common.set_glyph`: Farben des aktiven Themas, neu gesetzt nur bei Änderung.
  - Die Suche erkennt eine zugeklappte Falte jetzt an der Eigenschaft `glyph`, nicht mehr am Zeichen „▸“.
- **Keine leeren Kacheln.**
  - Ein Wert, den es nicht gibt, bekommt keine Kachel mit „–“.
  - Stattdessen sagt **ein** Satz, was fehlt und wie man es bekommt („Match-Daten einrichten …“).
- **Subtiler DBD-Bezug.**
  - Der Kompass des Programmsymbols steht in der Markenzeile – seit 1.24.7 in Textfarbe, denn der Akzent markiert nur Zustand und Hauptaktion.
  - Die Gold-Akzente bleiben.
  - Keine Glow-Effekte, kein Glas, keine Emojis.

## 3. Vorher/Nachher je Seite

| Seite | Vorher | Nachher |
|---|---|---|
| Hülle | Navigation ohne Kopf und Fuss | Markenzeile (Kompass + „Fog Scout“); unten `NavStatus`: Punkt + Zustand in Worten (höchstens zwei Zeilen, der ganze Text im Tooltip) auf **jeder** Seite, ein Fehler mit Warnzeichen statt Punkt, Klick/Enter → Übersicht; schmales Fenster: nur das Zeichen, dafür steht der Zustand in Worten unter dem Titel der Übersicht; unter jedem Seitentitel eine Zeile Zweck (`PAGE_SUBTITLES`, DE/EN) |
| Übersicht | Status-Pill; „Scannen“ immer gold; „Schnell ein/aus“ nur Häkchen; Kacheln „–“; „Heute“ zeigte höchstens 5 von bis zu 7 Fakten | Pill weg (Status unten in der Navigation); Hauptaktion nur bei Handlungsbedarf; Knöpfe mit Symbolen; Karte **„Funktionen“** mit Zustand je Häkchen („aktiv“, „wartet auf DBD“, „OBS nicht erreichbar“, „HWiNFO fehlt“, „Anmeldung nötig“, sonst „an“), genau unter dem Text des Häkchens; Heute/Diese Woche ohne Kacheln ohne Wert, alle Fakten von „Heute“ als Kachel, Wochenkacheln in Rasterbreite; Kachel „Stats-Seite“ ohne „–“ mit „Einrichten …“ |
| Maps | Suche ohne Treffer = leeres Raster; „← Zurück“ | Satz „Keine Map passt zu „…““ + Knopf „Suche leeren“; „Zurück“ mit gezeichnetem Pfeil |
| Overlay | 1280-px-Fenster: Reiter unter der Vorschau | ab 940 px Seitenbreite (1280-px-Fenster) Vorschau + Werkzeuge links, Reiter rechts – keine Einstellung mehr unter dem Falz; 1100-px-Fenster unverändert |
| Statistik | 4 Kacheln „–“; „⚠ Nicht gezählt …“/„✓ …“ in einem Label | nur Kacheln mit Daten + eine Zeile, was fehlt (mit „Match-Daten einrichten …“, solange nie eingerichtet); „Nicht gezählt …“ als gelber Hinweis, Gerettetes schlicht, ohne Zeichen; Spielzeit „58,3 h“ mit Komma; „Filter“ mit Chevron, „Stats-Seite öffnen“ mit Symbol für extern; leere Auswahl verweist auf „Filter zurücksetzen“ |
| Aufnahmen | „● Nimmt auf“, „⏸ Pausiert“, „⚑ 2 Marken“; „OBS nicht erreichbar“ in Textfarbe; zweimal „aus“ | Zeile in Zustandsfarbe (Aufnahme grün, Pause/F8 ohne Puffer gelb, OBS weg rot) mit Worten ohne Zeichen; Warnzeile gelb; Knopf „Verbindung prüfen …“ bei OBS weg, „Clip speichern (F8)“ dann gesperrt wie „Aufnahme starten“; Karte versteckt, solange Aufnahmen aus sind (ein Text statt zwei); leere Runden-/Clip-Tabelle: „Keine Aufnahme passt zu den Filtern oben.“ |
| Server | „Auswahl anwenden“ wie die anderen Knöpfe; hosts-Fehler grau, Knöpfe aktiv | „Auswahl anwenden“ als Hauptaktion; hosts-Fehler, Ping- und Anwende-Fehler rot; unlesbare hosts-Datei sperrt „Auswahl anwenden“ und „Alles freigeben“ (Ping bleibt) |
| Einstellungen | OBS-Testergebnis immer grau | grün bei Erfolg, rot bei jedem Fehler, den der Recorder als Fehler meldet (OBS nicht erreichbar, Passwort falsch, kein obs-websocket …), gelb bei sonstigen Hinweisen (Tonquelle, Puffer, Laufwerk) |
| Log | leere Fläche bei leerem/ganz gefiltertem Log; „▸ Erweitert“ | Platzhalter „Keine Zeilen – das Log ist leer, oder Suche und Kategorien blenden alles aus.“; „Erweitert“ mit gezeichnetem Chevron (die Suche klappt die Falte weiter auf) |

## 4. Neue oder verbesserte Funktionen (Paket 6, priorisiert)

1. **Globaler Status in der Navigation** (1.24): was Fog Scout tut, auf jeder Seite; dieselben Worte wie der Tray-Punkt (`App._user_state`, gemeinsam genutzt).
2. **Funktionen mit Zustand und nächstem Schritt** (1.24.1, `overview.switch_state`):
   - Der Zustand kommt nur aus Werten, die das Programm ohnehin hat: Worker-Status, Recorder, Verbindungsanzeige, Systemwerte, Mediensteuerung, Discord, Spotify, YouTube.
   - Es gibt keine neuen Abfragen, keine neuen Threads und kein Netz.
   - „Aufnahmen mit OBS“: Ein Zustand von der Seite Aufnahmen gilt nur `OBS_STATE_FRESH_S` = 60 s lang; sonst antwortet der Recorder selbst (`Recorder.obs_ready`: „bereit“ bzw. „OBS nicht verbunden“, solange DBD läuft), ohne DBD „wartet auf DBD“ – nie „bereit“ ohne Wissen (1.24.5).
   - „Systemwerte“: „HWiNFO fehlt“ nach der Lesung von jetzt, frühestens wenn auch das Log es sagt (`HWINFO_WAIT_S`), oder sofort, wenn HWiNFO schon lief und jetzt fehlt (1.24.5).
3. **Leere Zustände mit Handlung** (1.24.1–1.24.3): Map-Suche, Statistik ohne Match-Daten, gefilterte Tabellen, Log.
4. **Hauptaktionen** (1.24/1.24.3): „Stimmt“ bzw. „Map wählen …“ in der Übersicht, „Auswahl anwenden“ auf der Seite Server.
5. **Fehler mit nächstem Schritt** (1.24.3): „Verbindung prüfen …“ bei OBS weg; gesperrte hosts-Aktionen bei unlesbarer Datei.

## 5. Bewusst nicht umgesetzt

| Vorschlag | Grund |
|---|---|
| Befehlspalette | Strg+F findet schon jede Einstellung, jeden Reiter und jede Seite; eine zweite Suche wäre doppelt |
| Favoriten (Maps) | kein Nutzerwunsch, „Zuletzt gespielt“ deckt den häufigsten Weg ab |
| Fortschrittsanzeige beim Export | Export unter 1 s gemessen (Phase 1, 1.23) – ein Balken würde nur flackern |
| Statusspalte der Aufnahmen (★ ⚑N ▶) als gezeichnete Symbole | braucht einen eigenen Delegate für `Table`; die Legende unter der Tabelle erklärt die Zeichen, Nutzen kleiner als Risiko in dieser Phase |
| ⚠/✓ im Abgleich unter Einstellungen › Match-Daten | eine Liste in einem Label; Aufteilen in Warn-/Info-Zeilen zurückgestellt |
| Navigation neu ordnen / Seiten zusammenlegen | bricht Gewohnheiten und Strg+1…9, ohne erkennbaren Gewinn (wie Phase 1) |

## 6. Performance vorher/nachher

**Methode:**

- Abwechselnd gemessen (A/B/A/B …, je Lauf ein eigener Prozess, gleiche Zeitspanne, gleiche Last). A = `main` `eb94fec` (git worktree), B = Arbeitsbaum 1.24.7.
- B war `879f9b0` plus die F8-Änderung aus `2077617`, die während der Messung dazukam. Sie ändert nur den Zustand eines Knopfs.
- Werkzeuge: `tools/bench.py` (Szenarien startup, pages, overview, stats, recordings, latency, idle, folder) über ein A/B-Skript; dazu zwei Zerlegungen im Prozess (Maps-Erstbesuch, Übersicht, Statistik) und die Maps-Suche.
- Angegeben sind Median und Spannweite (min–max) in ms, Prozent = (B − A) / A · 100.
- **Umgebung:** Linux-Container, 4 CPUs, Python 3.13.18, Kernel 6.18.44, Qt offscreen, Daten von `tools/bench.py` (300 bzw. 5000 Runden, 40 Aufnahmen), 3. 11. 2026.
- **Grenzen:** Geteilter Cloud-Rechner ohne festen Takt. Die Spannen sind breit (der Start streut um ±20 %) und überlappen sich fast überall. Offscreen ohne GPU, ohne Windows, ohne DBD. Windows-Werte können abweichen.

**Start** (n = 20 je Baum):

| Wert | A | B | Δ |
|---|---|---|---|
| Import | 365,8 (288,0–419,9) | 370,9 (290,7–410,1) | +1 % |
| App gebaut | 167,9 (129,6–212,9) | 187,5 (134,8–205,8) | +12 % |
| bis Leerlauf | 27,2 (21,6–53,0) | 27,6 (17,9–44,5) | +1 % |
| **gesamt** | **576,5 (440,2–640,1)** | **570,3 (461,8–647,7)** | **−1 %** |
| Speicher (RSS, MB) | 189,5 | 189,2 | 0 % |

Ein erster Lauf mit n = 10 ergab 544,9 gegen 630,8 ms (A 460–2700, B 484–828 ms). Mit n = 20 verschwand der Unterschied, er war Rauschen.

**Seiten, Klicks, Leerlauf** (n = 6, Leerlauf n = 4):

| Wert | A | B | Δ |
|---|---|---|---|
| Erster Besuch Übersicht | 3,5 (3,1–21,9) | 2,6 (0,6–4,2) | −27 % |
| Erster Besuch Maps | 136,3 (99,4–155,5) | 127,5 (113,6–169,2) | −6 % |
| Erster Besuch Overlay | 470,8 (312,0–533,7) | 430,5 (385,8–512,1) | −9 % |
| Erster Besuch Statistik | 197,4 (60,6–240,8) | 190,7 (84,0–233,4) | −3 % |
| Erster Besuch Aufnahmen | 208,3 (171,3–297,4) | 207,7 (192,6–287,8) | 0 % |
| Erster Besuch Server | 92,0 (86,4–148,8) | 82,0 (69,3–94,7) | −11 % |
| Erster Besuch Einstellungen | 296,2 (236,8–355,1) | 247,0 (209,1–315,9) | −17 % |
| Erster Besuch Log | 48,6 (28,6–62,4) | 58,0 (45,7–74,1) | +20 % |
| Zweiter Besuch (8 Seiten) | 13,7–40,7 | 12,3–39,9 | −45 … +28 %, Spannen überlappen |
| Klick → Handler (Median / Max) | 0,2 / 3,0 | 0,2 / 2,9 | 0 % |
| Übersicht aktualisieren (Median) | 0,1 (0,1–0,2) | 0,2 (0,1–0,3) | +0,1 ms |
| Statistik rendern, 5000 Runden | 6,8 (5,6–10,2) | 8,7 (6,5–14,2) | +28 % |
| Aufnahmen rendern, 300 | 7,8 (7,3–13,6) | 8,8 (7,9–12,0) | +13 % |
| Leerlauf CPU (% eines Kerns) | 7,1 (6,4–7,6) | 7,0 (6,1–7,3) | −2 % |
| Leerlauf CPU eingeschwungen | 1,5 | 1,5 | 0 % |
| Leerlauf RSS (MB) | 236,9 | 238,5 | +0,7 % (+1,6 MB) |
| Laufwerksabfragen `find_folder` | 1–2 | 1–2 | gleich |

**Zerlegung im Prozess** (n = 6):

| Wert | A | B | Δ |
|---|---|---|---|
| Maps erster Besuch gesamt | 134,2 (91,7–149,7) | 117,5 (76,4–144,1) | −12 % |
| Übersicht `_qt_refresh` | 0,18 (0,15–0,22) | 0,20 (0,19–0,29) | +0,02 ms |
| Übersicht Modell | 0,04 | 0,05 | +0,01 ms |
| Statistik `_stats_render` | 8,44 (7,53–11,58) | 9,02 (7,82–11,39) | +7 % |
| Statistik `_qt_refresh` | 0,65 (0,52–0,74) | 0,66 (0,56–0,76) | +2 % |

**Statistik nachgeprüft:** Die Mediane liegen bei B um 7 bis 28 % höher, die Spannen überlappen sich. Darum wurde zusätzlich ein Profil je Baum gemessen (cProfile, 40 Renders, Eigenzeit je Funktion addiert).

- Summe 17,9 ms (A) gegen 18,4 ms (B), +3 %.
- Die grössten Unterschiede: ein Ausreisser in `history.load_lost` (0,006 → 0,282 ms je Render, gleiche Aufrufzahl) und Bilddekodierung des Vorschau-Threads im selben Prozess (11 → 26 Dekodierungen).
- Gemessene Phase-2-Kosten: nur eine Schleife über alle Runden für den Satz zu verknüpften Custom Games. Seit `952098a` läuft sie nur, wenn es Verknüpfungen gibt.
- Ein Lauf danach (`ab_split`, n = 6) ergab 7,64 gegen 8,76 ms – weiterhin überlappend.
- **Ergebnis:** keine nachweisbare Mehrarbeit im Code. Ein Rest von bis zu ~1 ms je Statistik-Render ist nicht ausgeschlossen. Er tritt nur beim Neuzeichnen der Statistik auf (Filterwechsel, neue Runde), nicht im Takt.

**Maps-Suche:** Zeit vom Suchtext bis zum ruhigen Raster, n = 12, 1280×800.

| Eingabe | A | B |
|---|---|---|
| c | 24,8 (11,0–62,6) | 24,0 (15,6–54,7) |
| co | 19,6 (7,7–31,3) | 23,3 (9,0–61,6) |
| coal | 8,6 (4,3–30,5) | 9,8 (5,1–97,9) |
| xyz (kein Treffer) | 4,6 (2,8–36,2) | 10,7 (7,1–32,9) |
| leer | 27,3 (14,0–40,4) | 46,3 (26,3–163,5) |
| midwich | 8,7 (4,2–78,0) | 11,3 (6,2–110,1) |
| leer | 22,4 (11,9–153,5) | 93,2 (15,7–197,8) |

- Das Profil der leeren Suche zeigt in beiden Bäumen dasselbe Muster: Der Hintergrund-Timer `_qt_warm` baut und styled währenddessen andere Seiten (`_style_page` → `setStyleSheet`), je nach Zeitpunkt mitten in der Messung. Das erklärt die Ausreisser bis 198 ms.
- Isoliert gemessen (20× „midwich“ → leer im selben Prozess): A 48,7 ms (32,2–162,6), B 50,5 ms (36,4–248,4), also +4 % im Rauschen.
- Mehrkosten aus Phase 2 bei „xyz“: die Zeile „Keine Map passt …“ wird gezeigt (Text setzen, Widget einblenden).

**Gesamtbild:** Start, Leerlauf, Klicklatenz und die ersten Seitenbesuche liegen im Rauschen von `main` oder darunter. Die Übersicht kostet je Takt +0,02 bis 0,1 ms für die Funktionen-Karte, das sind bei 4 Takten/s unter 0,05 % eines Kerns. Bei Statistik und Maps-Suche gibt es höhere Mediane mit stark überlappenden Spannen. Profile zeigen keinen Phase-2-Code als Ursache, ein kleiner Rest ist nicht ausgeschlossen. Der Leerlauf-Speicher liegt +1,6 MB höher (neue Widgets und Glyphen-Pixmaps).

**Messung 1.24.4 → 1.24.5:**
- Die erste A/B-Messung fand messbare Mehrkosten im Takt: `set_glyph` baute bei jedem Aufruf die Palette, und `getattr` auf fehlende Namen an PySide-Widgets kostete 3,7 µs.
- Behoben in 1.24.5 (`ab_split`, n = 6 je Lauf, A = `main` im selben Lauf):
  - Übersicht aktualisieren: 0,30 → 0,21 ms (`main` 0,19 bzw. 0,19 ms).
  - Statistik `_qt_refresh`: 0,92 → 0,72 ms (`main` 0,66 bzw. 0,63 ms).
- Die Werte oben sind die Endmessung auf 1.24.7.

## 7. Tests

- **Ausgangsstand:** 1199 bestanden, 37 übersprungen, 0 fehlgeschlagen.
- **Je Paket vor dem Commit:** volle Suite `DBDMS_LANG=de QT_QPA_PLATFORM=offscreen python -m pytest -q tests` und `python -m pyflakes fogscout tests tools` (ohne Befund):

  | Paket | bestanden | übersprungen | fehlgeschlagen |
  |---|---|---|---|
  | 2 (1.24) | 1205 | 37 | 0 |
  | 3 (1.24.1) | 1209 | 37 | 0 |
  | 4 (1.24.2) | 1211 | 37 | 0 |
  | 5+6 (1.24.3) | 1215 | 37 | 0 |
  | 8, eigene Durchsicht (1.24.4) | nur gezielt: 29 + 20 (Übersicht, Navigation, Doku-Wächter) | – | 0 |
  | 7, Performance-Fix (vor den Prüfbefunden) | 1215 | 37 | 0 |
  | 8, Prüfbefunde (1.24.5) | 1218 | 37 | 0 |
  | 8, zweite Prüfung (1.24.6) | 1221 | 37 | 0 |
  | 8, visuelle QA (1.24.7, `879f9b0` und `2077617`) | 1222 | 37 | 0 |
  | 8, Abkürzung Statistik (`952098a`) | gezielt `test_qt` + `test_uimodel`: 213 | – | 0 |

- **Übersprungen:** dieselben 37 wie im Ausgangsstand – Windows-only (`tests/test_windows.py`, natives Overlay, Hotkeys, windows-capture), echtes ffmpeg und `node` je nach Umgebung.
- **Neue Tests (Auswahl):**
  - `test_the_navigation_shows_the_name_and_the_state_on_every_page`
  - `test_the_state_reaches_the_foot_of_the_navigation_on_every_page`
  - `test_a_model_button_can_be_the_main_action_and_carry_a_drawn_sign`
  - `test_every_page_says_what_it_is_for_under_its_title`
  - `test_the_new_signs_are_drawn`
  - `test_the_overview_draws_a_main_action_only_when_the_player_has_to_act`
  - `test_each_feature_says_whether_it_works_now_and_what_is_missing`
  - `test_the_feature_card_writes_the_state_under_each_box`
  - `test_the_overview_drops_tiles_that_would_only_say_nothing`
  - `test_a_search_without_a_hit_says_so_and_offers_to_clear_it`
  - `test_the_dashboard_has_no_tile_that_would_only_say_nothing`
  - `test_the_statistics_say_once_what_the_stats_page_would_add_instead_of_tiles_of_nothing`
  - `test_an_unreadable_hosts_file_is_an_error_and_locks_apply_and_release`
  - `test_the_obs_line_in_the_settings_is_coloured_by_what_it_says`
  - `test_an_empty_table_and_an_empty_log_say_why`
  - `test_a_table_the_filters_empty_says_so`
  - `test_the_recorder_says_whether_obs_is_ready_for_the_running_game` (1.24.5)
  - `test_signs_made_before_the_theme_follow_it_and_another_screen_scale` (1.24.5)
  - `test_linked_custom_games_are_not_called_unlinked` (1.24.5)
  - `test_obs_away_at_dbd_start_is_marked_as_a_failure`, `test_a_model_label_level_reaches_the_qt_property`, `test_obs_away_with_recordings_off_but_a_folder_keeps_the_next_step` (1.24.6)
  - `test_the_overview_fixes_of_the_visual_qa` (1.24.7: Heute mit sieben Kacheln, Kachel „Stats-Seite“, Wochenraster, Kompass und Statuszeichen auf der Symbolspalte); erweitert: Funktionen-Karte (Einzug = Lage des Häkchen-Texts, „an“), F8 bei OBS weg gesperrt
- **Bewusst geänderte bestehende Tests** (Verhalten geändert, nicht abgeschwächt):
  - Filter-Knopf: Text ohne ▾/▴, das Zeichen wird geprüft.
  - Kontextmenü: „Drehen“.
  - Split-Schwelle der Overlay-Seite: neue Schranke 860 < `SPLIT_FROM` ≤ 1000.
  - Aufnahme-Karte: Zeilen ohne ●/⏸/⚑, dazu Stufe, Knopf und versteckte Karte.
  - Status unten in der Navigation: Vergleich ohne Zeilenumbruch, weil `_two_lines` die Zeilen jetzt selbst setzt.
  - Log-Platzhalter: neuer Text.
  - Funktionen: ein eingeschalteter Schalter ohne Zustand erwartet jetzt „an“ statt nichts (1.24.7).
  - Spielzeit: `play_time(7200)` erwartet „2,0 h“ (Komma im Deutschen, 1.24.7).
- **Gefunden, nicht geändert:** `test_page_keys_never_get_in_the_way_of_typing` schlägt fehl, wenn `tests/test_uimodel.py` **vor** `tests/test_qt.py` läuft.
  - Das passiert auch auf `main` (`eb94fec`), ist also nicht neu.
  - In der normalen Reihenfolge (CI) ist der Test grün.
  - Ursache vermutlich Fokus/aktives Fenster aus einem früheren App-Test (Strg+3 erreicht das neue Fenster nicht).
- **CI:** Linux und Windows sowie CodeQL siehe Abschnitt 11.

### Unabhängige Prüfung (Paket 8)

- **Vorgehen:** Ein eigener Agent las den ganzen Diff seit `eb94fec`, ohne etwas auszuführen. Jeder Befund wurde danach im Code nachgeprüft, bevor er behoben wurde.
- **Ohne Befund:**
  - Attributnamen in `switch_state`: alle vorhanden.
  - Harte Regeln: kein Netz, kein Prozess- oder Dateizugriff, nichts Sensibles im Log.
  - Übersetzungen und Tooltips: vollständig.
  - Abgeschwächte Tests: keine.
- **Aufgeräumt:** Tooltip und Übersetzung „✕“ werden nicht mehr gebraucht.

| # | Schwere | Befund (im Code bestätigt) | Behebung (1.24.5) | Test |
|---|---|---|---|---|
| 1 | MEDIUM | Zeichen auf Übersicht und Maps entstehen vor `apply_theme`. Im hellen Modus trugen sie die Dunkel-Farbe (≈ 1,3:1), ein Themenwechsel zeichnete sie nicht neu | `_glyph_args` + `refresh_glyphs` in `MainWindow._signs_paint` | `test_signs_made_before_the_theme_follow_it_and_another_screen_scale` |
| 2 | MEDIUM | „Aufnahmen mit OBS – bereit“ ohne Wissen: nur die Seite Aufnahmen fragt OBS | `Recorder.obs_ready`; „OBS nicht verbunden“; ohne DBD „wartet auf DBD“ | `test_the_recorder_says_whether_obs_is_ready_for_the_running_game`, `test_each_feature_says_whether_it_works_now_and_what_is_missing` |
| 3 | LOW | Falsches Passwort und andere `ObsError` erschienen in den Einstellungen gelb statt rot | Flag `err` im Statusereignis | `test_the_recorder_thread_survives_errors`, `test_the_obs_line_in_the_settings_is_coloured_by_what_it_says` |
| 4 | LOW | Schmale Navigation zeigte den Zustand nur über die Farbe | Warnzeichen bei Fehler; der Zustand in Worten auf der Übersicht | `test_the_navigation_shows_the_name_and_the_state_on_every_page` |
| 5 | LOW | Aufnahme-Karte rot mit „Verbindung prüfen …“, obwohl Aufnahmen absichtlich aus sind | `rec_card_level(…, rec_on=)` | `test_the_recording_card_text_follows_obs_state` |
| 6 | LOW | Der 1.24.4-Fix „Punkt nach Bildschirmwechsel“ wirkte nicht, weil nichts das Neuzeichnen auslöste | `QEvent.DevicePixelRatioChange` → `_signs_paint`; die HISTORY-Zeile 1.24.4 berichtigt | wie 1 |
| 7 | LOW | Der Log-Platzhalter nannte nach „Leeren“ die Filter als Grund | neutraler Text | `test_an_empty_table_and_an_empty_log_say_why` |
| 8 | LOW | Ein fehlgeschlagener Ping gab „Auswahl anwenden“ trotz unlesbarer hosts-Datei frei; „Keine Region hat geantwortet“ war ungefärbt | `_srv_lock`; die Meldung gelb | `test_an_unreadable_hosts_file_is_an_error_and_locks_apply_and_release` |
| 9 | LOW | Der Status unten hatte keine Zeilengrenze | `NavStatus._two_lines` | Navigationstest |
| 10 | LOW | „HWiNFO fehlt“ erschien in der ersten Sekunde; nach dem Schliessen von HWiNFO stand dort weiter „aktiv“ | Lesung von jetzt + `_hwinfo_told` | `test_each_feature_says_whether_it_works_now_and_what_is_missing` |
| 11 | LOW | Verknüpfte Custom Games hiessen „keinem Match zugeordnet“ | Prüfung über `c.off` statt über die Kill-Paare | `test_linked_custom_games_are_not_called_unlinked` |

### Zweite unabhängige Prüfung (1.24.6)

- **Vorgehen:** Workflow `review-1245` über `b788e8c..a40dc67`. Vier Prüfrichtungen, je Befund drei Gegenprüfer, 61 Agenten.
- **Ergebnis:** 19 Befunde, davon 16 von mindestens zwei Gegenprüfern bestätigt (2 MEDIUM, 14 LOW). Jeder wurde im Code nachgeprüft und behoben.
- **Wichtigste Befunde:**
  - `Recorder.obs_ready` las „eingerichtet“ statt „verbunden“. Nach einer Einstellungsänderung stand „OBS nicht verbunden“, ein geschlossenes OBS blieb „bereit“. Jetzt aus `_reachable` (letzte Verbindung in `_client`).
  - OBS-Fehler beim DBD-Start und am Rundenende sind jetzt rot (`err` auch bei `_warn` und Leerlauf-`ObsError`).
  - Aufnahme-Karte bei ausgeschalteten Aufnahmen, aber gesetztem Ordner: gelb statt still.
  - Verknüpfte Custom Games bekommen einen eigenen Satz.
  - `_signs_paint` zeichnet auch die Navigationssymbole und den schmalen Suchknopf neu.
  - `NavStatus._two_lines` kürzt auch die erste Zeile.
  - `set_glyph` ohne Import im Aufruf.
- **Abgelehnt** (Mehrheit der Gegenprüfer): 3 Befunde, Einzelheiten in `HISTORY.md` 1.24.6.

### Visuelle Prüfung (1.24.7)

- **Vorgehen:** Workflow `visual-qa-phase2`. Nach-Bilder aller acht Seiten in 27 Varianten (Dunkel/Hell/OLED × 100/125/150 % × 1100×760/1280×800/1600×1000) plus Zusatzzustände (schmales Fenster, Fehlerstatus, Maps ohne Treffer). Je Seite ein Prüfer, je Fund drei Gegenprüfer.
- **Ergebnis:** 51 Funde, 42 bestätigt (6 MEDIUM, 36 LOW), 9 ohne Bestätigung – 8 davon nur, weil ihre Gegenprüfung ausfiel. Laut Gegenprüfern waren 13 neu aus Phase 2, 27 bestanden schon vorher, 2 unklar.
- **Ausfälle:** 26 Gegenprüfungen (Seite Aufnahmen, Zusatzzustände) brachen am Nutzungslimit ab. Diese 9 Funde habe ich selbst an den Bildern und im Code nachgeprüft.
  - Die Zusatzbilder „Maps ohne Treffer“ wurden mit „xyzq“ neu erstellt; die Suche „lery“ traf „Léry's Memorial Institute“.
  - Ergebnis der Nachprüfung: „Clip speichern (F8)“ aktiv trotz OBS weg stimmt → behoben.
  - Der Fund „Status im schmalen Fenster ohne Tooltip“ stimmt nicht: `status_btn.setToolTip` in `_status_paint`, Test `test_the_navigation_shows_the_name_and_the_state_on_every_page`.
  - Die übrigen sind dieselben Altbefunde wie auf anderen Seiten (Scrollleisten, Platzhalter, Reiter-Rahmen, ★ ⚑ ▶).

**Behoben in 1.24.7:**

| Fund | Schwere | Herkunft | Behebung |
|---|---|---|---|
| Zustandswörter der Funktionen-Karte 5 px links vom Text des Häkchens (fest 27 px) | MEDIUM | neu | Einzug = Breite des Häkchens + Abstand von `WrapCheck`, gemerkt je Thema/Zoom |
| Leeres Band und ungleiche Höhen unter Häkchen ohne Zustand | LOW | neu | eingeschaltet ohne Zustand = „an“ |
| Kompass, Statuszeichen und Navigationssymbole auf drei verschiedenen Linien | LOW | neu | `NAV_SIGN_X` (gemessene Mitte der Symbolspalte, x = 33); der Statuspunkt war vom Layout auf 7 px gequetscht → feste Breite. Nachgemessen: Kompass 26–39, Symbole 25–40, Statuszeichen 27–38 px |
| Kompass in Akzentfarbe (4 Funde auf 4 Seiten) | LOW | neu | Textfarbe |
| „Diese Woche“: zwei Kacheln je 672 px statt 261 px breit (1600 px) | LOW | neu | `TileGrid(stretch=False)` |
| Statistik: Hinweiszeile hell und 8 px unter der Karte | LOW | neu | gedimmt, Kartenabstand 12 px |
| „Heute“ hat 5 Kachel-Widgets für bis zu 7 Fakten – Aufnahmen und „Farming?“ fielen weg | MEDIUM | vorher | Kacheln nach Bedarf (`_today_tile`) |
| Knopf „Match-Daten einrichten …“ bei 1280 px abgeschnitten | MEDIUM | vorher | „Einrichten …“ (Tooltip unverändert ausführlich) |
| Kachel „Stats-Seite“ mit grossem „–“ | LOW | vorher | ohne Wert; `FactBox` blendet eine leere Wertzeile aus |
| „58.3 h gespielt“ im Deutschen | LOW | vorher | `dashboard.play_time` mit Komma |
| „Clip speichern (F8)“ aktiv bei OBS weg (selbst nachgeprüft) | – | vorher | gesperrt wie „Aufnahme starten“ |

**Bekannt, nicht behoben** (alle LOW, ausser wo genannt; drei sind neu aus Phase 2 und markiert, die übrigen bestanden schon vorher):

| Fund | Grund |
|---|---|
| Platzhaltertext (Suche, Log-Filter) unter 4,5:1 (Hell 3,3:1, Dunkel 4,2:1, OLED 4,47:1) | Qt-Palette `PlaceholderText`; betrifft alle Eingabefelder, gehört in eine eigene Kontrastrunde |
| Realm-Zähler auf Maps 3,3:1 (Hell), Realm-Name „Hawkins National Laborat…“ gekürzt, wenn die Liste scrollt (MEDIUM) | Delegate der Realm-Liste; Breite der Spalte fest – eigene Änderung an `qt_maps` |
| Scrollleisten-Griffe kaum sichtbar (1,1–1,5:1, auf der Overlay-Seite MEDIUM), Griffe ⋮⋮ der Karten 1,3–1,4:1, Regler-Knopf in OLED 1,3:1 | Farbe `hover` des Themas; eine Änderung trifft jede Seite und braucht eine eigene visuelle Prüfung |
| Markierung der aktiven Navigation als „(“ (border-left + border-radius) | Qt-Darstellung; ein eigener Strich bräuchte einen Delegate |
| Rahmen der Reiterflächen mit offenen Ecken, aktiver Reitertext 1–2 px höher, rechte Kanten der Statistik-Zeile nicht bündig | Qt-Stil von `QTabWidget::pane`; vorher genauso |
| Statusspalte ★ ⚑ ▶ der Aufnahmen als Unicode | eigener Delegate für `Table` (siehe Abschnitt 5) |
| Vorschau der Overlay-Seite: Beschriftung „Spielbild“ 2,2:1, Discord-Flächen 2,1:1 | gezeichnete Vorschau (`qt_preview`), eigene Änderung |
| Kachel „Aufnahmen“: Balkenspur kaum sichtbar, Detailzeile bricht mitten im Datum | Spurfarbe wie Scrollleisten; Text kommt aus `overview.recordings` |
| Diagrammtitel „Runden pro Tag“ grau und 8 px eingerückt; „Letzte Runden“ 5 px eingerückt; letzte Heute-Kachel 3 px kürzer | Diagramm-Widget bzw. Rahmen der Zeilen; Pixelkosmetik |
| Statistik: Kartenbalken 2,4:1 (Hell); zwei Chevron-Stile in einer Zeile (Auswahllisten vs. „Filter“) – **neu** | Balken: `qt_views.MapBars`; Chevron: die Auswahllisten zeichnet Qt, „Filter“ ist ein Knopf mit gezeichnetem Zeichen |
| Statistik: dieselbe Ursache in drei Texten untereinander (Killer × Map, Hinweiszeile, Fussnote) – **neu** | jede Karte erklärt sich allein, wenn der Nutzer nur sie sieht; Zusammenführen ändert drei Stellen und ihre Tests – zurückgestellt |
| Server bei 1280×800: Hinweiszeile vom Fensterrand angeschnitten – **neu** | die Seite scrollt; die Zeile Zweck kostet ~18 px |
| Server im Container: hosts-Spalte „–“ und gesperrte Knöpfe ohne Grund im Bild | Container ohne lesbare Windows-hosts-Datei; unter Windows zeigt die Seite den Status (siehe Abschnitt 9, Punkt 5) |
| Kartenbild vor dem Laden ein schwarzes Feld (Hell) | Ladezustand der Kacheln, vorher genauso |

## 8. Windows-/Spieltests

- **Nicht durchgeführt:** Die Umgebung ist ein Linux-Container ohne Windows, ohne DBD und ohne OBS. Echte Windows-, Spiel-, OBS- und Overlay-Tests liefen nicht.
- **Ersatz:** Geprüft wurden Offscreen-Qt-Rendering, die Testsuite und die Windows-CI-Läufe von GitHub Actions (`tests/test_windows.py`, siehe Abschnitt 11).

## 9. Offene Risiken und manuelle Prüfpunkte (am Windows-PC)

1. **Navigation:** Markenzeile und Status unten in Dark, Light und OLED. Bei einem Fenster unter 960 px nur Kompass und Punkt, Tooltip mit Status.
   - Status wechselt beim DBD-Start („wartet auf das Map-Banner“), beim Banner (Map-Name) und nach der Runde.
   - Klick und Enter öffnen die Übersicht.
2. **Übersicht › Funktionen:** Bei laufendem DBD „Automatische Erkennung – aktiv“, „Systemwerte – aktiv“ bzw. „HWiNFO fehlt“ ohne HWiNFO.
   - Ohne OBS und nach einem Besuch der Seite Aufnahmen: „OBS nicht erreichbar“. Nach dem Start von OBS verschwindet es spätestens nach 60 s.
   - Spotify bzw. YouTube ohne Anmeldung: „Anmeldung nötig“.
3. **Overlay-Seite** bei 1280×800, 100 % und 125 %: Vorschau links, Reiter rechts, nichts abgeschnitten (Windows-Schriften sind breiter als im Container).
4. **Aufnahmen:** OBS aus → rote Zeile und „Verbindung prüfen …“ führt zu Einstellungen › Aufnahmen. Aufnahme läuft → grüne Zeile; Pause → gelb.
5. **Server:** Kann die hosts-Datei nicht gelesen werden (z. B. gesperrt durch Virenscanner), ist der Status rot und „Auswahl anwenden“ gesperrt.
   - Danach normal: „Auswahl anwenden“ gold gefüllt.
   - UAC-Abbruch → Zeile nicht rot.
6. **Einstellungen › Aufnahmen › Verbindung testen:** grün bei Erfolg, rot ohne OBS.
7. **Log:** Suche ohne Treffer und „Leeren“ zeigen den Platzhalter.
8. **Heller Modus und Farbthemen:** In Hell, OLED und mit einer anderen Akzentfarbe sind die gezeichneten Zeichen auf Übersicht und Maps gut lesbar: „Zurück“, „Suche leeren“, das ✕ des Hinweises bei unbekannter Map, ▶ der letzten Runden. Ein Themenwechsel bei laufendem Programm zeichnet sie neu.
9. **Bildschirmwechsel:** Das Fenster auf einen Bildschirm mit anderer Skalierung ziehen (z. B. 100 % → 150 %). Kompass, Statuszeichen und Knopfzeichen bleiben scharf (`QEvent.DevicePixelRatioChange`).
10. **Schmales Fenster (< 960 px):** Unten in der Navigation nur das Zeichen, bei einem Fehler ein Warnzeichen. Die Übersicht zeigt den Zustand dann unter ihrem Titel in Worten.
11. **OBS beim DBD-Start nicht offen:** „Aufnahmen mit OBS“ zeigt „OBS nicht verbunden“. Nach dem Einrichten (spätestens nach 30 s, `RECHECK_S`) zeigt es „bereit“. Sind Aufnahmen ausgeschaltet, aber der Ordner bleibt gesetzt, ist die Aufnahme-Karte nicht rot.
12. **1.24.7 – Ausrichtung unter Windows:** Kompass, Statuszeichen und Navigationssymbole stehen auf einer Linie. `NAV_SIGN_X` ist offscreen gemessen (Rand 6 + 12 + 6 px des Qt-Stils). Unter Windows bei 100 %, 125 % und 150 % prüfen; weicht der Stil dort ab, ist es ein Wert.
    - Zustandswörter genau unter dem Text der Häkchen, auch bei grösserer Schrift (Einstellungen → Schriftgrösse).
    - Mit OBS geschlossen ist „Clip speichern (F8)“ gesperrt.
13. **Risiko:** Die Zustandswörter der Funktionen-Karte hängen an vorhandenen Attributen. Ein fehlendes Attribut ergibt keinen Zustand statt eines Fehlers – sichtbar falsch wäre höchstens ein fehlender Hinweis.

## 10. Geänderte Dateien und Architekturentscheidungen

- **Modell → Qt:**
  - `uimodel.primary`/`glyph`/`level`
  - `app_qt.ui_state` (`primary`, `glyph`, `level`, Treeview `empty`)
  - `qt_pages.show_control` (Objektname `primary`, `set_glyph`, Eigenschaft `state`)
  - `qt_views.Table.paintEvent` (Worte in leerer Tabelle), `LogView` (Platzhalter)
- **Hülle:**
  - `qt_window.NavStatus`, `MainWindow._brand_row`/`show_status`/`_status_paint`
  - `qt_common.page_head`/`PAGE_SUBTITLES`/`set_glyph`
  - `qt_theme` (QSS `navbrand`/`brandname`/`navstatus`/`subtitle`, `QLabel[state=…]` hinter allen Klassenregeln, Hover für Tabellenzeilen, `ICON`)
  - `qt_icons` (neue Glyphen)
- **Seiten:**
  - `overview.py` (`primary_action`, `switch_state`, `OBS_STATE_FRESH_S`, Kacheln ohne Wert)
  - `qt_pages.OverviewPage` (Funktionen-Karte)
  - `qt_maps.MapsPage` (`no_hits`, `clear_search`)
  - `qt_pages.SPLIT_FROM` 940
  - `dashboard.tiles`
  - `app_stats` (`stats_data_row`, Hinweise getrennt)
  - `app_recordings` (`rec_card_level`, `rec_obs_btn`, leere Tabellen)
  - `app_server` (Hauptaktion, Fehlerzustand)
  - `app_settings` (`_user_state`, `rec_status_level`)
- **1.24.5 (Messung und unabhängige Prüfung):**
  - `qt_theme.look_key()` als billiger Cache-Schlüssel der Themenfarben.
  - `qt_common.set_glyph(w, name, primary, tone)`: Schlüssel mit Pixelverhältnis, die Anfrage gemerkt in `_glyph_args`. `refresh_glyphs(root)` und `MainWindow._signs_paint` laufen bei `apply_theme` und bei `QEvent.DevicePixelRatioChange`.
  - Caches auf Qt-Widgets über `w.__dict__.get`, denn ein fehlender Name per `getattr` kostet 3,7 µs.
  - `obsrec.Recorder.obs_ready` und `_say(…, err=)` (Statusereignis `err`).
  - `app_server._srv_lock`, `NavStatus._two_lines` mit Warnzeichen, `OverviewPage.status_line`.
- **1.24.7 (visuelle Prüfung):**
  - `qt_window.NAV_SIGN_X` (Kompass und Statuszeichen auf der Symbolspalte), `NavStatus` mit fester Breite des Zeichens, Kompass in Textfarbe.
  - `qt_layouts.TileGrid(stretch=False)`, `qt_pages.OverviewPage._today_tile` (Kacheln nach Bedarf), Einzug der Zustandswörter aus `WrapCheck`.
  - `overview._setup_fact`, „an“ in `overview.switches`, `qt_views.FactBox` ohne leere Wertzeile.
  - `dashboard.play_time` mit Komma, `app_stats` Hinweiszeile gedimmt, `app_recordings` F8 bei OBS weg gesperrt.
- **Texte:**
  - `i18n_en.py`: jede neue Zeichenkette DE/EN; veraltete Einträge entfernt, Wächter grün.
  - `tooltip.py`: neue Knöpfe.
- **Doku:** `README.md`/`README.en.md` (Abschnitt „Neue Oberfläche“, Karte „Funktionen“), `CLAUDE.md` (eine Zeile), `HISTORY.md` (je Version eine Zeile).
- **Daten:** keine Änderung an Datenformaten, Einstellungsschlüsseln, Hotkeys oder Strg+1…9. Neue Werte liegen nur im Speicher; es gibt keine Migration.

## 11. Git, Commits, Push, PR

- **Zweig:** `claude/funny-feynman-gt5t6n`, Basis `main` = `eb94fec`.
- **Autor der Commits:** GitHub-Konto des Nutzers, laut CLAUDE.md.
- **Commits** (je Arbeitspaket einer):

  | Commit | Version | Inhalt |
  |---|---|---|
  | `b7761f3` | 1.24 | Paket 2: App-Hülle, Designsystem, gezeichnete Symbole |
  | `10ce87e` | 1.24.1 | Paket 3: Übersicht („Funktionen“) und Maps |
  | `4b114f7` | 1.24.2 | Paket 4: Overlay zweispaltig, Statistik ohne leere Kacheln |
  | `9125c80` | 1.24.3 | Pakete 5 und 6: Zustände in Farbe und Worten, leere Tabellen und Log |
  | `b788e8c` | 1.24.4 | Paket 8: eigene Durchsicht (veraltete OBS-Warnung) |
  | `a40dc67` | 1.24.5 | Pakete 7 und 8: Performance-Fix, Befunde der unabhängigen Prüfung, Windows-Testfix |
  | `ad4b74c` | 1.24.6 | Paket 8: Befunde der zweiten unabhängigen Prüfung |
  | `879f9b0` | 1.24.7 | Paket 8: Funde der visuellen Prüfung |
  | `2077617` | 1.24.7 | F8-Knopf bei OBS weg gesperrt (selbst nachgeprüfter Fund), README |
  | `952098a` | 1.24.7 | Statistik: Schleife über verknüpfte Custom Games nur mit Verknüpfungen (Endmessung) |
  | (dieser) | – | `PHASE2_REPORT.md` |

- **Push:** Jeder Commit wurde nach `origin` gepusht. GitHub meldet beim Push, dass das Repository umgezogen ist (Umleitung, siehe CLAUDE.md).
- **PR:** senisinx/fog-scout#299, offen, **nicht gemergt**.
- **CI:**
  - `b7761f3` bis `b788e8c` (1.24–1.24.4): Linux grün, **Windows rot** – in jedem dieser fünf Läufe derselbe eine Test (z. B. 1.24: 1 failed, 1127 passed, 114 skipped).
    - Der Test `test_the_overview_draws_a_main_action_only_when_the_player_has_to_act` (neu in 1.24) rief `overview_model(app, 1000.0, …)` auf; `datetime.timestamp()` einer Lokalzeit nahe 1970 wirft unter Windows `OSError 22`.
    - Ein Testfehler, kein Programmfehler: das Programm übergibt immer `time.time()`.
    - Bemerkt erst bei 1.24.4, behoben in `a40dc67`. Die Commits davor wurden nicht einzeln nachgeprüft – sie sind nicht einzeln auf `main` gedacht.
  - `a40dc67`: alle grün.
    - Linux-pytest: 1218 passed, 37 skipped.
    - Windows: 1137 passed, 118 skipped in 6:18 min auf einem echten Runner.
    - CodeQL sowie Analyze (python, javascript-typescript, actions): grün.
  - `ad4b74c` (1.24.6) und `879f9b0` (1.24.7): grün (Tests Linux + Windows, CodeQL).
  - `06573af` (Bericht): Linux, Windows und die drei CodeQL-Analysen grün.
    - Der zusammenfassende Check **„CodeQL“ ist rot**: „1 new alert including 1 high severity security vulnerability“ – *Use of a broken or weak cryptographic hashing algorithm on sensitive data*, `fogscout/obsrec.py:230` (`auth_string`).
    - Eingeordnet als **Fehlalarm, nicht geändert**:
      - Die Zeile ist die Anmeldung, die obs-websocket 5 vorschreibt: `base64(sha256(base64(sha256(Passwort + Salt)) + Challenge))`.
      - Das Programm speichert keinen Passwort-Hash; das Passwort liegt DPAPI-geschützt in den Einstellungen (seit 1.16.2).
      - Ein langsamer Hash wie bcrypt würde das Protokoll brechen – OBS würde die Anmeldung ablehnen.
      - Die Zeile ist seit 1.4 unverändert. Als „neu in diesem PR“ gilt sie, weil `Recorder._client` (geändert in 1.24.6: `_reachable`) auf dem Datenweg des Passworts liegt.
    - Offen für Saru: den Alert in GitHub (Security → Code scanning) als „False positive“ bzw. „Won't fix“ schliessen – eine Repo-Sicherheitsaktion, die ich nicht selbst ausführe.

## 12. Harte Projektregeln

**Keine Änderung an den harten Regeln aus `CLAUDE.md`:**

- Keine Eingaben ans Spiel, kein Zugriff auf den Spielprozess, keine Spieldateien.
- Keine neuen Netzwerkverbindungen in Erkennung oder Overlay, keine Telemetrie, keine Paketinhalte.
- Keine neuen Abhängigkeiten, keine neuen Threads, Timer oder Laufwerksabfragen.

**Zur Funktionen-Karte:** Sie liest nur Zustände, die schon im Speicher liegen. Medientitel, Server-IP und Tokens erscheinen in keinem neuen Text, keinem Log und keiner Diagnose.

**Daten im Repository:** Keine Screenshots, Testdaten oder Nutzerdaten committet. Die Bildschirmfotos liegen nur im Scratchpad der Sitzung.
