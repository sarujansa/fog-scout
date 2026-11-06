"""Choices several mixins of the App share (1.38.36, project review ARCH-1): the selectable values of the overlay,
system values, music, statistics periods and hotkeys. Before, the mixins imported them from each other
(app_overlay from app_sysinfo and app_spotify, app_recordings from app_stats …); now none imports another
(guard tests/test_mixins.py). The mixins re-export their names, so ``from .app_sysinfo import SELECTABLE`` keeps
working. Pure – only texts marked for translation (N_).
"""
from __future__ import annotations

from .i18n import N_

# from app_sysinfo
HUD_SIDES = [("off", N_("Aus")), ("above", N_("Direkt über der Karte (wandert mit)")),
             ("left", N_("Links oben (über der Karte)")), ("right", N_("Rechts oben")),
             ("custom", N_("Eigene Position (mit der Maus verschieben)"))]

# from app_sysinfo
BAR_ALIGNS = [("left", N_("Links")), ("centre", N_("Mittig")), ("right", N_("Rechts"))]     # 1.2.8

# from app_sysinfo
PRESET_LABELS = [("left", N_("Alles links")), ("right", N_("Alles rechts")),           # 1.2.9 (layoutmem.PRESETS)
                 ("spread", N_("Verteilt: Karte links, Werte rechts")),
                 ("standard", N_("Standard (wie ausgeliefert)"))]                         # 1.2.17 (config.DEFAULTS)

# from app_sysinfo
HUD_ROW_LABELS = [("cpu", N_("Zeile CPU (Temperatur, Last)")), ("gpu", N_("Zeile GPU (Temperatur, Last)")),
                  ("spot", N_("Zeile Hotspot / GPU-Speicher (HWiNFO)")), ("vram", N_("Zeile VRAM")),
                  ("ram", N_("Zeile RAM"))]

# from app_sysinfo
MEDIA_SPOTS = [("below", N_("Unter den Systemwerten")), ("under_today", N_("Unter „Heute“")),
               ("bottom_right", N_("Rechts unten im Balken")), ("bottom_left", N_("Links unten im Balken")),
               ("custom", N_("Eigene Position (mit der Maus verschieben)"))]

# from app_sysinfo
TODAY_SPOTS = [("below", N_("Unter den Systemwerten")), ("under_music", N_("Unter der Musik")),
               ("bottom_right", N_("Rechts unten im Balken")), ("bottom_left", N_("Links unten im Balken")),
               ("custom", N_("Eigene Position (mit der Maus verschieben)"))]

# from app_sysinfo
OPACITY_KEYS = {"hud": "hud_opacity", "today": "today_opacity", "music": "media_opacity",   # 1.2.7; else "opacity"
                "text": "info_opacity",      # 1.8.24: the lines as their own element
                "inputs": "inputs_opacity"}  # 1.39: the input card

# from app_sysinfo
MEDIA_STYLES = [("big", N_("Gross – Cover oben, Titel darunter")), ("compact", N_("Kompakt – Cover links"))]

# from app_sysinfo
MAP_SCALE = (15, 90)                        # size of the map, percent of the game height

# from app_sysinfo
# 1.64.9 (user: one size for what was picked instead of three sliders): the elements of the preview
SELECTABLE = (("map", N_("Karte")), ("text", N_("Infos und Schrift (Name, Timer, Bilanz, Server)")),
              ("hud", N_("Systemwerte")), ("today", N_("Heute")), ("music", N_("Musik")),
              ("inputs", N_("Eingaben")))                                                     # 1.39

# from app_inputs (1.39): the input card's place and device
INPUT_SPOTS = [("bottom_left", N_("Links unten im Balken")), ("bottom_right", N_("Rechts unten im Balken")),
               ("custom", N_("Eigene Position (mit der Maus verschieben)"))]
INPUT_LAYOUTS = [("auto", N_("Automatisch (zuletzt benutztes Gerät)")), ("keyboard", N_("Tastatur und Maus")),
                 ("gamepad", N_("Gamepad"))]

# from app_overlay
# 1.8.24: where the map's lines (timer, record, server) go – an element of their own, or drawn with the map as before
INFO_SPOTS = [("below", N_("Eigenes Element unter der Karte")), ("above", N_("Eigenes Element über der Karte")),
              ("custom", N_("Eigenes Element, eigene Position")), ("inside", N_("Mit der Karte verbunden, unten")),
              ("inside_top", N_("Mit der Karte verbunden, oben"))]     # 1.8.34

# from app_spotify
MEDIA_NEXT_SPOTS = [("below", N_("Unter dem Lied")), ("right", N_("Rechts neben dem Lied"))]

# from app_spotify
MEDIA_NEXT_N = (1, 5)                      # tracks shown

# from app_stats
STATS_PERIODS = [("all", N_("Gesamter Zeitraum")), ("day", N_("Heute")), ("7d", N_("Letzte 7 Tage")),
                 ("30d", N_("Letzte 30 Tage")), ("week", N_("Diese Woche")), ("month", N_("Dieser Monat")),
                 ("year", N_("Dieses Jahr"))]

# from app_hotkeys
HOTKEY_LABELS = [("toggle_overlay", N_("Karte ein/aus")), ("next_variant", N_("Layout-Variante")),
                 ("scan_now", N_("Bildschirm scannen")), ("prev_map", N_("Vorherige Map")),
                 ("next_map", N_("Nächste Map")), ("bigger", N_("Grösser")), ("smaller", N_("Kleiner")),
                 ("edit_position", N_("Mit Maus verschieben")), ("rotate_map", N_("Karte drehen")),
                 ("next_floor", N_("Etage wechseln")), ("reject_map", N_("Falsch erkannt")),
                 ("mark_clip", N_("Clip-Marke setzen")), ("record_toggle", N_("Aufnahme starten/stoppen")),
                 ("record_pause", N_("Aufnahme pausieren/weiter"))]                      # 1.15
