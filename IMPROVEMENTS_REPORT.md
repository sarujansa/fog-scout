# Fog Scout – Optimierung 1.22.3 bis 1.23.1 (Abschlussbericht)

> **Historische Momentaufnahme** (Stand laut Dokument: 2. November 2026, PR #298). Die Angaben zu Version, offenen Punkten und Merge-Status gelten für diesen Tag; spätere Änderungen stehen in `HISTORY.md`.

Auftrag: `prompt.md` (umfassende Produkt-, UI/UX-, Funktions- und Performance-Optimierung, Phasen 0–10).
Stand: 2. November 2026, Zweig `claude/funny-feynman-gt5t6n`, Pull Request senisinx/fog-scout#298 (nicht gemergt – Saru merged).

## 0. Ausgangslage, Vorgehen, Bestandsaufnahme

**Phase 0:**

- Ausgang war Version 1.22.2, Commit `06c9393` (= `main`); der Arbeitsbaum war sauber.
- Umfang: 119 Module, rund 57 000 Zeilen, 78 Testdateien. CI läuft auf Linux und Windows, dazu CodeQL.
- Git-Vorgabe von Saru: ein Commit je Arbeitspaket, Push und PR; gemergt wird nur auf sein Wort.

**Entscheidung: kein Rewrite.**

- Die Architektur (UI-Modell, Mixins von `App`, Qt-Seiten, ein Ereignis-Takt) ist tragfähig und an vielen Stellen schon gemessen optimiert (HISTORY 1.8.72, 1.16.1, 1.16.2, 1.17).
- Ein Umbau der 15 Mixins brächte mehr Risiko als Nutzen.
- Die Navigation mit acht Seiten passt zum Funktionsumfang. Eine Neuordnung bräche Gewohnheiten und Strg+1…9 ohne erkennbaren Gewinn.
- Verbessert wurden deshalb gezielt Auffindbarkeit, Begriffe, Zustände, Lesbarkeit und messbare Engpässe.

**Bestandsaufnahme (Phase 1, priorisiert):**

- Drei getrennte Untersuchungen: Architektur und Performance, UI/UX, Design.
- Jeder Kernbefund wurde im Code nachgeprüft.
- „Status“ in der Tabelle nennt das Paket, das den Befund behoben hat.

| Prio | Bereich | Befund | Status |
|---|---|---|---|
| P1 | Theme Hell | Abspielkopf im Editor weiss auf weiss (1,0:1), Marken 2,2:1, Statusfarben und Ping-Werte 2,3–2,5:1, Farbring im Bild-Editor weiss auf weiss | behoben (1.22.3) |
| P1 | Komponenten | deaktivierte Primärknöpfe sahen aktiv aus (ID-Regel schlug `:disabled`), gedrückt = Hover, Fokus unsichtbar bei ID-Knöpfen/Segmenten/Editor-Suche, Hell-Hover Gold/Grün 4,0–4,2:1 | behoben (1.22.3) |
| P1 | Performance (Windows) | `find_folder` fragt 26 Laufwerksbuchstaben je Aufruf, mehrfach je Aufnahmen-Render und im Recorder-Thread | behoben (1.22.4) |
| P1 | Performance | Seite Aufnahmen las Index/Clips/Screenshots und fragte OBS weiter, wenn das Fenster im Infobereich lag | behoben (1.22.4) |
| P1 | Reaktion | Klicks warteten bis zum nächsten 50-ms-Takt (Median 24 ms, max. 77–96 ms) | behoben (1.22.4) |
| P1 | Begriffe | „Overlay ein/aus“ (Hotkey, Tray), „Overlay ausblenden“ (Übersicht) blendeten nur die Karte aus; „Overlay ausschalten“ = Hauptschalter – drei Bedeutungen | behoben (1.23) |
| P1 | Rückfragen | alle Rückfragen mit „OK“ und OK als Standard, auch beim Löschen | behoben (1.23) |
| P1 | Suche | Log › „Erweitert“ zugeklappt und für Strg+F unsichtbar | behoben (1.23) |
| P1 | Server | angehakte Regionen sahen angewendet aus, wirken aber erst nach „Auswahl anwenden“ | behoben (1.23) |
| P2 | Tabellen | Doppelklick/Enter auf Aufnahmen und Clips ohne Wirkung | behoben (1.23) |
| P2 | Montage | „Als Montage öffnen …“ nur im Rechtsklick-Menü | behoben (1.23) |
| P2 | Übersetzung | „Vorgabe“ (Lage) und „Vorlage“ (Layout) beide „Preset“ | behoben (1.23) |
| P2 | Statistik | „Verlauf löschen“ unklar, ohne Runden passierte nichts | behoben (1.23) |
| P2 | Sichtbarer Fehler | Kachel-Knopf „Match-Daten einrichten …“ bei 1280 px beidseitig abgeschnitten („atch-Daten einrichten“) | behoben (1.23) |
| P2 | Sichtbarer Fehler | Aufnahme-Karte wiederholte „OBS nicht erreichbar – läuft OBS …“ im Detail | behoben (1.23) |
| P2 | Design | keine zentralen Schrift-/Radius-/Abstandsskalen, Kartenränder 14-mal kopiert | behoben (1.23.1) |
| P2 | Performance | onnxruntime/urllib vor dem Fenster importiert; Downloads-Scan im GUI-Thread | gemessen, bewusst nicht geändert (siehe D) |
| P2 | Text | „F8“ fest in ~12 Texten, auch wenn die Clip-Taste umbelegt ist | zurückgestellt (D) |
| P2 | Overlay-Seite | zweispaltig erst ab 1080 px Inhaltsbreite (`SPLIT_FROM`) | zurückgestellt (D) |
| P3 | diverse | Export ohne Fortschritt/Abbrechen, Hotkeys ungruppiert, Setup-Fussleiste, Klickverzögerung Maps, Cache `maps_dark` ohne Aufräumen, Log-Filter 4×/s, Unicode-Symbole als Icons, „Neu seit …“ deutsch in der englischen Oberfläche | zurückgestellt (D) |

## A. Umgesetzte Verbesserungen

### UI/UX und Design

**Lesbarkeit im hellen Modus (1.22.3).**

- Bis dahin nahmen die Qt-Seiten die Overlay-Farben `theme.DOT`, die für Schwarz gedacht sind, auch auf weissem Grund.
- Neu sind Zustandsfarben je Modus (`qt_theme.STATE`): ok/warn/err/info, Abspielkopf, Marken, Medienhintergrund und Auswahltext.
- Sie gelten für Statuspill, Kachelwerte, Timeline, Overlay-Vorschau, Bild-Editor, Reglermarke, Navigations-Warnpunkt und die Ping-Spalte des Servers.
- Kontraste, berechnet mit `qt_theme.contrast` – Text ≥ 4,5:1, Linien ≥ 3:1, auch auf der eigenen Pill-Tönung:

| Element | vorher | nachher |
|---|---|---|
| Statusfarben (hell) | 2,3–3,7:1 | 7,1–7,9:1 |
| Abspielkopf (hell) | 1,0:1 | 17:1 |
| Marken (hell) | 2,2:1 | 5,2:1 |
| Log-Zeitstempel (Hell und Dunkel) | 3,3:1 | 6,0:1 |
| Hover der Akzentknöpfe Gold/Grün (hell) | 4,0/4,2:1 | 6,6:1 |

**Knopfzustände.**

- Ein deaktivierter Primärknopf hat keine Akzentfläche mehr; offscreen geprüft: Pixel alt = Akzent, neu transparent.
- „Gedrückt“ unterscheidet sich jetzt von „Hover“; roter Löschen-Text darauf bleibt bei 6,4:1.
- Sichtbarer Tastaturfokus für `#rowplay`, die Suche in der Navigation, Segmente und die Editor-Suche.
- Der Clip-Editor übernimmt die Schriftgrösse des Fensters.

**Rückfragen (1.23).**

- Der Knopf sagt, was passiert: Löschen, Anwenden, Freigeben, Zurücksetzen, Importieren, Markieren, Trotzdem beenden, Alle löschen.
- Wo Daten verloren gehen oder ersetzt werden, ist der Knopf rot und der Fokus liegt auf „Abbrechen“. Qt macht den fokussierten Dialogknopf zum Standard, Enter bricht also ab.
- Betroffen sind zwölf Rückfragen.

**Sichtbare Fehler aus den Screenshots (1.23).**

- Kachel-Knöpfe kürzen am Ende mit „…“ (`ElideButton`), der volle Text steht im Tooltip.
- Die Aufnahme-Karte nennt nur noch die Ursache („Ursache: ConnectionRefusedError“).

### Navigation und Auffindbarkeit

- Die Suche (Strg+F) findet zugeklappte Bereiche über Namen und Inhalt (Debug-Bilder, Fensteraufnahme, Scans, Rundenende) und klappt sie beim Hinspringen auf. Betrifft Log › Erweitert.
- Die Seitenstruktur bleibt unverändert (Begründung in Abschnitt 0).

### Maps

- Keine Änderung.
- Erster Besuch 135 ms, wiederholter Besuch 17 ms (Linux offscreen).
- Die gemeldete Klickverzögerung der Kacheln ist zurückgestellt (D).

### Overlay

- Begriffe: „Karte ein/aus“ (Hotkey, Infobereich) und „Karte ausblenden/einblenden“ (Übersicht) für die Karte der Runde, „Overlay aus-/einschalten“ für alles im Spiel.
- Hotkey-Belegungen und Einstellungen sind unverändert.
- Overlay-Seite: „Vorgabe“ heisst jetzt „Position“ (im Englischen vorher doppelt „Preset“).
- Das Overlay im Spiel ist nicht verändert; die harten Regeln bleiben unberührt.

### Statistik

- „Verlauf löschen“ heisst jetzt „Alle Runden löschen …“ (Einstellungen › Allgemein › Sicherung).
- Die Rückfrage hat einen roten Knopf und nennt die Sicherungskopie.
- Ohne gespeicherte Runden erscheint ein Hinweis statt nichts.

### Aufnahmen

- Doppelklick oder Enter auf eine Aufnahme oder einen Clip spielt ihn ab.
- Bei zwei oder mehr markierten Zeilen erscheint „Als Montage öffnen …“ als Knopf.
- Die Seite liest bei verstecktem Fenster nichts mehr.
- Der Ordner wird höchstens alle 5 s über alle Laufwerksbuchstaben gesucht.

### Einstellungen

- Zurücksetzen und Importieren fragen mit rotem Knopf.
- „Alle Runden löschen …“ ist klar benannt.

### Server

- Eine gelbe Zeile „Nicht angewendet – N Änderungen …“ erscheint, solange die Häkchen von der hosts-Datei abweichen.

### Neue Funktionen

- Bewusst keine grossen.
- Nur Doppelklick/Enter und der Montage-Knopf, die vorhandene Funktionen leichter erreichbar machen (Auftrag: keine Feature-Flut).

### Architektur

- `qt_theme`:
  - `STATE` und `set_dark`/`current_dark`/`current_zoom`;
  - `readable`, `blend`, `dot_colour`, `pill_style`;
  - Skalen `TYPE`, `RADIUS`, `PAD_CARD`.
- Modell und Qt:
  - Modell-Label `Note.TLabel` (gelber Hinweis);
  - Treeview-Aktion `_dbdms_open` (Doppelklick/Enter);
  - `qt_views.ElideButton`.
- `_ask(…, ok_text=, danger=)`, rückwärtskompatibel.
- `App._poll_soon`/`_drain_events`: Klicks werden sofort verarbeitet, nie verschachtelt.
- `Recorder.folder()` mit Cache (`FOLDER_TTL_S`).
- Neues Messwerkzeug `tools/bench.py`: reproduzierbar, Kindprozesse auf Wegwerf-Ordnern, keine Nutzerdaten.
- Keine neuen Abhängigkeiten, keine Änderungen an Datenformaten (`settings.json`, `rounds.jsonl`/`official.jsonl`, Projekte, Indizes), keine Hotkey-Änderungen.

### Korrekturen aus dem Abschlussaudit (1.23.1)

Die unabhängige Prüfung des Gesamt-Diffs hat sechs Befunde gemeldet; alle sind behoben und mit Tests abgesichert.

- Die Auswahl in der Editor-Mediathek nutzte die neue, dunklere Pressed-Farbe und war kaum sichtbar. Jetzt hat sie einen eigenen Token `sel_bg`.
- Eine Lösch-Rückfrage mit DBD im Vordergrund liess den Fokus auf dem roten Knopf. Jetzt liegt er immer auf „Abbrechen“.
- Doppelklick innerhalb einer Mehrfachauswahl spielte die erste markierte Zeile ab. Jetzt spielt er die angeklickte.
- Ohne Häkchen riet der Server-Hinweis zu „Auswahl anwenden“, das dann ablehnt. Jetzt erscheint ein eigener Text.
- Ein fehlendes Laufwerk blieb 5 s gemerkt, sodass eine Runde direkt nach dem Einstecken nicht aufgenommen worden wäre. Jetzt wird es nicht mehr gemerkt.
- Schieberegler und Ziehgesten lösten nach der Klick-Beschleunigung eine Fensteraktualisierung je Mausereignis aus: 55 % statt 34 % CPU. Jetzt wird gedrosselt; Werte in Abschnitt B.

## B. Performance

**Methode.**

- Werkzeug: `tools/bench.py`, im Repository und reproduzierbar.
- Umgebung: Linux-Container, Python 3.13, PySide6 6.11.2 offscreen. **Es sind keine Windows-Zeiten** – sie vergleichen alt und neu auf derselben Maschine.
- Ablauf: Jedes Szenario läuft in einem eigenen Kindprozess auf einem Wegwerf-Ordner (Maps/Modelle verlinkt, synthetische Runden und Aufnahmen). Echte Nutzerdaten werden nicht berührt.
- Alt (1.22.2, Commit `06c9393`) und neu laufen **verschränkt**: abwechselnd im selben Zeitraum, je 6 Läufe, der Start mit 16 Läufen. Angegeben ist der Median.
- Warum verschränkt: Zwei getrennte Serien hintereinander zeigten scheinbare Verschlechterungen, zum Beispiel beim zweiten Besuch der Übersicht 6 → 21 ms. Eine Bisektion über die Paket-Commits zeigte dann für den unveränderten Ausgangsstand selbst 6, 19 und 21 ms. Solche Unterschiede sind Rauschen, kein Code-Effekt.

| Messpunkt | vorher (1.22.2) | nachher (1.23.1) | Bedingungen | Ergebnis |
|---|---|---|---|---|
| Klick im Fenster bis zum Handler, Median | 24,4 ms | 0,2 ms | 40 Klicks im Abstand von 137 ms, laufende Ereignisschleife | **−99 %** |
| … Maximum | 95,5 ms | 1,9 ms (nach Drosselung 6,7 ms) | ebenso | **−93 bis −98 %** |
| Ordnersuche `find_folder` (Windows: 26 Laufwerksbuchstaben je Aufruf), Aufnahmen-Seite sichtbar | 5 je 10 s | 2 je 10 s | 300 Aufnahmen, 100 Clips | **−60 %** (Aufrufe gezählt; Windows-Zeit je Aufruf nicht gemessen) |
| … Fenster versteckt, Seite gewählt | 9 je 10 s | 1–2 je 10 s | ebenso | **−83 %** |
| Neuberechnungen der Aufnahmenliste bei verstecktem Fenster | 1 je 10 s | 0 | ebenso | **entfällt** |
| Regler ziehen (Post alle 8 ms): Fensteraktualisierungen | ~200/s | 198–207/s | Seite Overlay, 3 s, je 3 Läufe | unverändert (1.23 ohne Drosselung: 360–385/s) |
| … CPU eines Kerns | 33–35 % | 34–37 % | ebenso | unverändert (1.23 ohne Drosselung: 55–57 %) |
| Start gesamt (Import + `App()` + erster Leerlauf) | 552 ms (IQR 535–583) | 548 ms (IQR 535–601) | 16 Läufe verschränkt | **keine messbare Änderung** |
| Speicher nach dem Start (RSS) | 189,3 MB | 189,4 MB | ebenso | unverändert |
| Leerlauf, eingeschwungen (25 s nach dem Start) | 1,6 % eines Kerns | 1,6 % | Übersicht sichtbar, 10 s | unverändert |
| Leerlauf, erste 10 s (Seiten werden im Hintergrund gebaut) | 7,1 % | 7,0 % | ebenso | unverändert |
| RSS nach dem Leerlauf | 236,8 MB | 237,1 MB | ebenso | unverändert (+0,1 %) |
| Statistik rendern, 5000 Runden | 8,3 ms | 7,8 ms | 10 Renders | im Rauschen |
| Aufnahmenliste rendern, 300 Einträge | 8,5 ms | 8,9 ms | 10 Renders | im Rauschen |
| Seitenwechsel, erster Besuch (Overlay / Einstellungen / Aufnahmen / Statistik / Maps) | 440 / 306 / 228 / 191 / 147 ms | 443 / 304 / 191 / 196 / 117 ms | je 6 Läufe | ohne systematische Änderung |
| Seitenwechsel, zweiter Besuch (alle 8 Seiten) | 10–45 ms | 14–33 ms | je 6 Läufe | ohne systematische Änderung (±40 % in beide Richtungen) |
| Rückkopplung durch sofortige Klicks | – | 0 Klick-Ereignisse ohne Eingabe auf allen 8 Seiten | je 4 s Leerlauf | keine Schleife |

**Geprüft und bewusst nicht geändert (gemessen):**

- onnxruntime verzögert laden: netto im Rauschen, zurückgenommen.
- Downloads-Scan: 1,2 ms je 20 s bei 3000 Dateien.

**Nicht gemessen:**

- Zeiten unter Windows, darunter die tatsächliche Dauer einer Laufwerksabfrage und `EnumWindows`.
- Erkennung und OCR: unverändert, nicht Teil dieser Arbeit.
- Overlay im Spiel, OBS-Abläufe.
- Verhalten mit echter GPU/HDR.

## C. Tests

**Ausgeführt:**

- `python -m pyflakes fogscout tests tools`: sauber.
- `python -m pytest -q tests` auf Linux, vollständig nach jedem Paket.
  - Letzter vollständiger Lauf vor der HISTORY-Zeile: 1198 bestanden, 1 fehlgeschlagen, 37 übersprungen.
  - Der eine Fehlschlag war `test_the_real_history_ends_with_the_current_version`, weil die HISTORY-Zeile zu 1.23.1 noch fehlte.
  - Nach dem Ergänzen sind die Doku-Wächter (`test_whatsnew.py`, `test_history.py`, 30 Tests) grün.
- GitHub Actions für die Pakete 1 und 2: Linux (pyflakes + pytest) und Windows (pytest inkl. `tests/test_windows.py`) grün; beide Jobs liefen mit echtem Runner.
- **Pakete 3 und 4 waren in CI rot (Linux, Windows grün):** `test_a_tile_button_ends_in_dots_when_the_tile_is_narrow`.
  - Mit DejaVu Sans, der Schrift im Linux-Runner, kürzt Qts `elidedText` einen Text, der genau in seine Breite passt („…einrichten…“).
  - Lokal mit Inter fiel das nicht auf. Lokal nachgestellt: 46 von 104 Schrift/Grössen-Kombinationen sind betroffen.
  - Behoben in 1.23.1 (`ELIDE_SLACK`). Der Test prüft die CI-Schrift jetzt ausdrücklich: mit dem alten Code rot, mit dem neuen grün.
  - Der Fehler wirkte sich auch für Nutzer aus: Kachel-Knöpfe wären unnötig gekürzt worden.
- **Danach war der Windows-Job rot:** `test_a_question_that_deletes_says_so_and_keeps_the_data_on_enter`.
  - Unter Windows setzt eine Rückfrage, die ohne Aktivierung erscheint (DBD vorne), den Fokus nicht auf „Abbrechen“.
  - Folge: Enter auf dem fokussierten roten Knopf hätte gelöscht.
  - Behoben: Bei `danger` ist der rote Knopf nicht mehr „autoDefault“, Enter drückt immer „Abbrechen“.
  - Der Test drückt jetzt Enter auf dem roten Knopf: mit dem alten Code löscht er, mit dem neuen bricht er ab.
- Im selben Log stand eine harmlose Fehlermeldung „Internal C++ object already deleted“. Ursache war ein Timer zum Hervorheben eines Suchtreffers, der nach dem Schliessen des Fensters feuerte (vorhandener Code). Er ist jetzt an sein Widget gebunden.

**Übersprungen:** 37 Tests, nur unter Windows ausführbar.

- 23 „Windows only“
- 12 „Windows file-system semantics“
- 2 „Windows share modes“

Sie laufen im Windows-Job der CI.

**Neue Tests:** 14 Testfunktionen; jede ist ausgeführt gegen den alten Code rot geprüft. Dazu kommen erweiterte Prüfungen in bestehenden Tests: `test_colour_themes_stay_readable` (alle Themes × OLED), `test_qt_uses_the_original_palette`, Ordner-Cache, Klick-Drosselung, Doppelklick in einer Markierung, Server ohne Häkchen. Auch die Erweiterungen aus dem Audit sind ohne die Korrektur rot (11 Fehlschläge).

- Theme: Kontraste aller Themes × OLED inklusive Hover, Zustandsfarben, Pill-Tönung, Abspielkopf/Marken, Auswahl, `sel_bg`; `readable()`; deaktivierter Primärknopf per Pixel; Stylesheet-Skalen.
- Rückfragen: Verb, rot, Fokus auf Abbrechen, auch ohne Aktivierung.
- Bedienung: Doppelklick/Enter (Qt-Tabelle und App), Montage-Knopf, `ElideButton`.
- Seiten: Server-Hinweis inklusive „keine Region“, Suche findet und öffnet „Erweitert“, „Alle Runden löschen …“, OBS-Ursache.
- Performance: Ordner-Cache (inklusive Laufwerk wieder eingesteckt), Aufnahmen-Seite bei verstecktem Fenster, sofortiger Klick mit Drosselung und Thread-Regel.

**Visuell (offscreen):**

- Alle 8 Seiten in 7 Varianten (Dunkel/Hell/OLED, Akzente Gold/Blau/Grün, 1280×800, 1100×760 mit 125 %, 1600×1000 mit 90 %), alt gegen neu.
- Dazu der Editor im Hell-Modus vorher/nachher, Server-Hinweis und Lösch-Rückfrage.
- Ergebnis: keine Layout-Regression gefunden.

**Nicht durchführbar (hier kein Windows, kein Spiel):** Overlay im Spiel, Erkennung im echten Match, OBS, Tray, Autostart, echte Windows-Zeiten – siehe Abschnitt F.

**Bekannte Risiken:**

- Die Drosselung `SOON_GAP_S` lässt einen Klick, der binnen 50 ms nach einer Klick-Aktualisierung kommt, wie früher auf den 50-ms-Takt warten.
- Die Begriffsänderungen (Karte/Overlay) können anfangs ungewohnt sein; die Belegungen sind unverändert.

## Abschlussaudit (Phase 9)

**Besser oder nur anders?**

- Messbar besser: Lesbarkeit im hellen Modus (Kontraste in Abschnitt A), Klick-Reaktion (−99 %), Hintergrundlast bei verstecktem Fenster.
- Sichtbare Fehler sind behoben: abgeschnittener Kachel-Knopf, doppelte OBS-Meldung, unsichtbarer Abspielkopf.
- Optisch bleibt die Oberfläche bewusst ruhig. Die Tokens ändern nichts Sichtbares, sie verhindern künftige Abweichungen.

**Leichter zu finden?**

- „Erweitert“ ist über die Suche erreichbar.
- Die Montage ist ein Knopf.
- Doppelklick tut das Naheliegende.
- Die Navigation selbst ist unverändert; das war eine bewusste Entscheidung (Abschnitt 0).

**Neue Komplexität:**

- Ein zweiter Weg in die Ereignisverarbeitung (`_poll_soon`) mit Drosselung.
- Ein Cache mit Ablaufzeit in `Recorder.folder()`.
- Beides ist dokumentiert (CLAUDE.md), getestet und gemessen.

**Funktionen erhalten?**

- Ja. Alle Tests sind grün.
- Keine Formate, Einstellungen oder Hotkey-Belegungen wurden geändert.
- Die harten Regeln sind unberührt: kein neuer Netz-, Prozess- oder Dateizugriff.

**Zurückgenommen:**

- onnxruntime verzögert laden (kein Gewinn).
- Die ungedrosselte Klick-Beschleunigung (Rechenlast beim Ziehen).

**Selbst gefunden durch die eigene Messung:** Die getrennten Serien täuschten Verschlechterungen vor. Deshalb wurde verschränkt nachgemessen; Ergebnis in Abschnitt B.


## D. Nicht umgesetzte Empfehlungen

| Punkt | Begründung |
|---|---|
| onnxruntime erst im Worker-Thread laden | Gemessen: Import 377 → 320 ms, aber `App()` 155 → 190 ms, weil der Thread parallel lädt und den GIL hält. Netto 555 → 541 ms bei einer Streuung von 545–656 ms je Lauf – kein belegbarer Gewinn, daher zurückgenommen. |
| urllib/http erst bei Bedarf laden | ~20 ms Importzeit, betrifft aber sechs Module (Spotify, YouTube, Discord, Statistik …). Lohnt den Umbau erst zusammen mit einer Messung unter Windows. |
| Downloads-Scan (offizielle Match-Daten) in einen Thread | Gemessen 1,2 ms je Scan bei 3000 Dateien, alle 20 s – kein Thread nötig. Unter Windows/OneDrive ungemessen. |
| „F8“ dynamisch in allen Texten | ~12 Texte und Tooltip-Schlüssel; betrifft nur umbelegte Clip-Tasten. Eigener kleiner Schritt mit `_tip_lookup`. |
| Overlay-Seite schon ab ~860 px zweispaltig (`SPLIT_FROM`) | Braucht Prüfung der Vorschau bei 1100×760 am echten Fenster; ohne diese Prüfung ist das Risiko eines zu engen Layouts zu hoch. |
| Export-Fortschritt mit Abbrechen, Hotkeys in Gruppen, Fussleiste des Setups, Maps-Klickverzögerung | Sinnvoll, aber jeweils eigene Bedienentscheidungen; nicht ohne Rückfrage an Saru. |
| Cache `cache/maps_dark` aufräumen, Log-Filter cachen, `DashboardView`-Schlüssel ohne `id()` | Kleine Gewinne ohne gemessenen Engpass. |
| Unicode-Symbole (▶ ★ ⚑ ↻) durch gezeichnete Icons ersetzen | Optischer Umbau über viele Seiten, Risiko für Tooltips und Tests; eigener Auftrag. |
| „Neu seit …“ (HISTORY.md) in der englischen Oberfläche deutsch | HISTORY ist bewusst deutsch; eine englische Fassung wäre ein Dokumentationsauftrag. |
| Navigation umbauen, Seiten zusammenlegen | Bewusst nicht (Abschnitt 0). |

## E. Geänderte Dateien

| Datei | Änderung |
|---|---|
| `fogscout/qt_theme.py` | `STATE` (Zustandsfarben je Modus), `set_dark`/`current_dark`/`current_zoom`, `readable`/`blend`/`dot_colour`/`pill_style`, QSS-Zustände (`#primary:disabled`/`:pressed`, Fokus), Skalen `TYPE`/`RADIUS`/`PAD_CARD` |
| `fogscout/qt_editor.py`, `qt_timeline.py`, `qt_image.py`, `qt_preview.py`, `qt_library.py` | Editor-Stylesheet mit Zoom und Skalen, Abspielkopf/Marken/fehlende Aufnahme aus dem Theme, Farbring und Vorschau-Hinweis je Modus, Auswahl der Mediathek `sel_bg` |
| `fogscout/qt_views.py` | `ElideButton`, FactBox-Werte lesbar, Tabellen: `itemActivated` → „open“ |
| `fogscout/qt_pages.py` | `MessageBox.ask(ok_text, danger)`, Modell-Hinweis `note`, `CapSlider`-Farbe, `PAD_CARD` |
| `fogscout/qt_window.py` | `apply_theme` → `set_dark`, Suche findet Falten und klappt sie auf, `show_question` mit 5 Feldern |
| `fogscout/app.py`, `app_qt.py` | `_poll_soon`/`_drain_events` (sofortige Klicks, gedrosselt `SOON_GAP_S`), `_ask(ok_text, danger)`, Modell-Knoten `note`/`open` |
| `fogscout/obsrec.py` | `Recorder.folder()` mit Cache `FOLDER_TTL_S` (fehlendes Laufwerk nie gemerkt) |
| `fogscout/app_recordings.py` | `_rec_tab_tick` nur bei sichtbarem Fenster, Doppelklick, Montage-Knopf, OBS-Ursache, Rückfragen |
| `fogscout/app_server.py` | Hinweis „Nicht angewendet“, Rückfragen mit Verb |
| `fogscout/app_stats.py`, `app_settings.py`, `app_overlay.py`, `app_hotkeys.py`, `overview.py`, `tray.py` | Begriffe, „Alle Runden löschen …“, Rückfragen |
| `fogscout/i18n_en.py`, `tooltip.py`, `uimodel.py`, `theme.py` | Übersetzungen, Tooltips, `Note.TLabel`, Log-Zeitstempelfarben |
| `tools/bench.py` (neu) | Messwerkzeug |
| `tests/…` | 14 neue Testfunktionen und erweiterte bestehende Prüfungen, siehe C |
| `README.md`, `README.en.md`, `CLAUDE.md`, `HISTORY.md` | Doku je Paket |

## F. Bekannte Probleme und offene Windows-/Spieltests

Ohne Windows-Rechner und Spiel nicht geprüft – bitte am PC durchgehen:

1. **Hell-Modus:** Statusanzeige oben rechts, Ping-Farben auf der Seite Server, Werte der Kacheln „Heute“, Abspielkopf und Marken im grossen Editor, Farbfelder im Bild-Editor.
2. **Primärknöpfe:** deaktiviert grau statt Akzentfarbe (z. B. Einrichtung, Editor „Exportieren“ ohne Clip); gedrückt sichtbar dunkler; Tab-Taste zeigt den Fokus auf ▶-Knöpfen in den Tabellen.
3. **Klicks:** Knöpfe und Häkchen reagieren spürbar sofort; Regler auf der Seite Overlay ziehen ohne Ruckeln und ohne mehr CPU als vorher (Task-Manager).
4. **Aufnahmen:** mit dem Aufnahme-Laufwerk als externem Datenträger (T7) abziehen und wieder anstecken – die Seite zeigt den Ordner nach dem Einstecken sofort wieder; eine Runde direkt danach wird aufgenommen.
5. **Doppelklick/Enter** auf eine Aufnahme und einen Clip spielt ihn ab; zwei markieren → „Als Montage öffnen …“ erscheint.
6. **Rückfragen:** „Aufnahme löschen“ – roter Knopf „Löschen“, Enter bricht ab; dasselbe mit DBD im Vordergrund (z. B. Beenden während einer hängenden Sicherung).
7. **Begriffe:** Hotkey Strg+Alt+M und Infobereich „Karte ein/aus“ blenden nur die Karte aus; „Overlay ausschalten“ in der Übersicht alles.
8. **Server:** eine Region abhaken – gelbe Zeile „Nicht angewendet – 1 Änderung“; alle abhaken – „Keine Region angehakt …“; „Auswahl anwenden“ (UAC) – Zeile verschwindet.
9. **Suche:** Strg+F „Debug“ → springt zu Log › Erweitert und klappt es auf.
10. **Übersicht bei 1280 px Breite** ohne Stats-Daten: der Knopf in der Kachel „Ø Kills“ endet auf „…“, Tooltip zeigt den vollen Text.
11. **Editor-Mediathek im Dunkelmodus:** die markierte Aufnahme ist deutlich hervorgehoben.

**Bekannte Einschränkungen:**

- „F8“ steht fest in einigen Texten, auch wenn die Clip-Taste umbelegt ist (D).
- Die Karte „Neu seit …“ zeigt die deutschen HISTORY-Sätze auch in der englischen Oberfläche (D).
- Alle Zeiten in Abschnitt B stammen aus Linux offscreen.

## G. Git-Zustand

**Zweig und Ausgang:**

- Zweig: `claude/funny-feynman-gt5t6n`.
- Ausgangscommit: `06c9393` (1.22.2, = `main` beim Start).

**Commits:** unter dem Namen des Nutzers, ein Commit je Arbeitspaket.

| Commit | Inhalt |
|---|---|
| `77bfd46` | 1.22.3: Messbasis, Lesbarkeit und Knopfzustände |
| `a7e19af` | 1.22.4: Klicks sofort, Ordner-Cache, Aufnahmen-Seite nur sichtbar |
| `68a5d37` | 1.23: Begriffe, Rückfragen, Doppelklick, Server-Hinweis |
| `f6aba5d` | Design-Tokens |
| `8ba6ccc` | 1.23.1: Audit-Korrekturen und dieser Bericht |
| `8f3c31a` | 1.23.1: Kachel-Knopf bei CI-Schrift, Timer an Widget |
| `007525b` | Bericht: Commit-Tabelle |
| letzter Commit | Enter bei Lösch-Rückfragen immer „Abbrechen“ (CI Windows) |

**Push:** Alle Commits sind nach `origin/claude/funny-feynman-gt5t6n` gepusht. Pull Request senisinx/fog-scout#298 ist offen, **nicht gemergt** – Saru merged.

**Arbeitsbaum:** Nach dem letzten Commit gibt es keine uncommitteten Änderungen.

**Nicht im Repository:** Messdaten, Screenshots und Hilfsskripte liegen nur im Scratchpad der Sitzung.
