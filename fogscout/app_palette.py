"""Mixin of App (1.26, user: "wenn man was sucht soll sich das GUI verdunkeln und Vorschläge anhand der Suche geben
(evtl. Claude API Key benutzen?)"): the command palette's entries and what a pick does, and the optional question to
Claude (askclaude) with its settings card under Einstellungen → Verbindungen.

Entries (palette.Entry, ids stable across openings): the settings the window's search finds (``s:``), the pages
(``p:``), the maps of the catalogue (``m:``), the actions that can do something now (``a:``) and the last rounds
(``r:``). Claude gets only the settings, pages and actions (id + title) – never maps, rounds or anything of the
game (CLAUDE.md, harte Regel „Claude-Suche“)."""
from __future__ import annotations

import threading
import time
import webbrowser

from . import askclaude, i18n, overview, palette, spotify
from . import uimodel as ui
from .i18n import _

ROUNDS_KEPT = 50          # the last rounds offered
CLAUDE_KINDS = ("setting", "page", "action")     # what Claude may see (titles of the program's own texts)


class PaletteMixin:
    # ---------------------------------------------------------- entries
    def _palette_actions(self) -> list:
        acts = overview.actions(self)
        out = []
        for key in ("confirm", "scan", "choose", "toggle", "rotate", "reject", "layout", "floor", "power"):
            v = acts.get(key)
            if v:
                out.append((key, v[1]))
        out.append(("test", self.test_btn.cget("text") if hasattr(self, "test_btn") else _("Overlay testen")))
        out.append(("edit", self.edit_btn.cget("text") if hasattr(self, "edit_btn") else _("Mit der Maus verschieben")))
        if self.settings.get("rec_on") or self.settings.get("rec_folder"):
            rec = getattr(self, "recorder", None)
            out.append(("record", _("Aufnahme stoppen") if rec is not None and rec.recording else _("Aufnahme starten")))
            out.append(("clip", _("Clip speichern")))
        out += [("update", _("Jetzt nach Updates suchen")), ("diagnose", _("Diagnose kopieren")),
                ("setup", _("Einrichtung starten"))]
        return [palette.Entry("action", "a:" + key, title, action=key) for key, title in out]

    def _palette_pages(self) -> list:
        from .qt_common import PAGE_SUBTITLES
        from .qt_window import PAGES
        return [palette.Entry("page", "p:" + key, _(label), _(PAGE_SUBTITLES.get(key, "")), action="page", arg=key,
                              words=i18n.other(_(label)))
                for key, label in PAGES]

    def _palette_settings(self) -> list:
        return self.qt.setting_entries()

    def _palette_maps(self) -> list:
        lang = i18n.current()
        out = []
        for mid, m in self.catalog.maps.items():
            try:
                v = m.image_for(1)[1]
            except Exception:
                v = 1
            realm = m.realm_names.get(lang) or m.realm_names.get("en") or m.realm
            words = " ".join(list(m.names.values()) + list(m.realm_names.values()) + list(m.aliases or ()))
            out.append(palette.Entry("map", "m:" + mid, m.names.get(lang) or m.name, realm, action="map",
                                     arg=(mid, v), alt="show", words=words))
        return out

    def _palette_rounds(self) -> list:
        try:
            rows = overview.last_rounds(self, ROUNDS_KEPT)
        except Exception:
            return []
        out = []
        for r in rows:
            when = time.strftime("%d.%m.%Y %H:%M", time.localtime(r.t))
            out.append(palette.Entry("round", "r:" + repr(r.t), r.map, when + (" · " + r.text if r.text else ""),
                                     action="round", arg=r.t, alt="recording" if r.recording else ""))
        return out

    def _palette_build(self) -> list:
        entries = []
        for part in (self._palette_actions, self._palette_pages, self._palette_settings, self._palette_maps,
                     self._palette_rounds):
            try:
                entries += part()
            except Exception:
                import logging
                logging.getLogger("fogscout").exception("Suche: Einträge")
        self._palette_by_id = {e.id: e for e in entries}
        return entries

    def _claude_ready(self) -> bool:
        return bool(self.settings.get("claude_on", False)) and askclaude.valid_key(self._claude_key())

    def _claude_key(self) -> str:
        return spotify.unprotect(self.settings.get("claude_key", "") or "")

    # ---------------------------------------------------------- events of the palette
    def _palette_event(self, action, arg):
        if action == "palette_open":
            self._qt_event("search_open")             # the pages filled, the window's search index new
            self.qt.palette_entries(self._palette_build(), recent=self.settings.get("palette_recent") or [],
                                    claude=self._claude_ready())
        elif action == "palette_pick":
            entry_id, alt = arg
            e = getattr(self, "_palette_by_id", {}).get(entry_id)
            if e is None:
                return
            self.settings.set("palette_recent", palette.remember(self.settings.get("palette_recent") or [], e.id))
            self._save_soon()
            self.qt.palette_entries(self.qt._palette_entries, recent=self.settings.get("palette_recent"))
            self._palette_run(e, bool(alt))
        elif action == "palette_ask":
            self._palette_ask(str(arg or ""))

    def _palette_run(self, e, alt: bool):
        q = self.qt
        if e.action == "found":
            q.go_to_found(e.arg)
        elif e.action == "page":
            q.show_page(e.arg)
        elif e.action == "map":
            mid, v = e.arg
            if mid not in self.catalog.maps:
                return
            if alt:
                self.show_map(mid, int(v), "manual")
            else:
                q.show_page("maps")
                q.maps.open_big((mid, int(v)))
        elif e.action == "round":
            if alt:
                self._show_round_recording(e.arg)
            else:
                self._show_round(e.arg)
        else:
            {"scan": self.scan_now, "rotate": self.rotate_map, "toggle": self.toggle_overlay,
             "power": self.toggle_overlay_master, "reject": self.reject_detection, "confirm": self._confirm_unsure,
             "layout": self.next_variant, "floor": self.next_floor, "choose": lambda: q.show_page("maps"),
             "test": self.test_overlay, "edit": self.toggle_edit, "record": self.record_toggle,
             "clip": self.mark_clip, "diagnose": self.show_diagnose, "setup": lambda: q.show_setup(True),
             "update": self._palette_update}.get(e.action, lambda: None)()

    def _palette_update(self):
        self.qt.show_page("settings")
        self._qt_refresh(force=True)
        self.qt.reveal("settings", "st.upd_btn")
        self.check_update()

    # ---------------------------------------------------------- Claude
    def _palette_ask(self, question: str):
        if not question.strip():
            return
        if not self.settings.get("claude_on", False):
            return
        key = self._claude_key()
        if not askclaude.valid_key(key):
            self.qt.palette.show_error(_("Kein API-Key – unter Einstellungen › Verbindungen › Claude eintragen."))
            return
        catalogue = [(e.id, e.title + (f" ({e.sub})" if e.sub else ""))
                     for e in getattr(self, "_palette_by_id", {}).values() if e.kind in CLAUDE_KINDS]
        self._asker().ask(key, question, catalogue)

    def _asker(self):
        a = getattr(self, "asker", None)
        if a is None:                         # started on the first question only
            a = self.asker = askclaude.Asker(lambda kind, **kw: self.events.put(("claude", kind, kw)))
            a.start()
        return a

    def _claude_event(self, kind, data):
        if kind in ("test_ok", "test_err"):
            self.cl_status_var.set(_("Claude: Key funktioniert.") if kind == "test_ok"
                                   else self._claude_words(data.get("error", "net")))
            return
        p = getattr(getattr(self, "qt", None), "palette", None)
        if p is None or not p.isVisible() or p.field.text().strip() != str(data.get("question", "")).strip():
            return                            # closed or typed on meanwhile: the answer is stale
        if kind == "answer":
            p.show_answer(data.get("answer", ""), data.get("ids") or [])
        else:
            p.show_error(self._claude_words(data.get("error", "net")))

    @staticmethod
    def _claude_words(kind: str) -> str:
        return {"auth": _("Claude: Der API-Key wird nicht angenommen – unter Einstellungen › Verbindungen prüfen "
                         "(„API-Key holen“ öffnet die Anthropic Console)."),
                "rate": _("Claude: Zu viele Anfragen – gleich noch einmal versuchen."),
                "quota": _("Claude: Kein Guthaben mehr auf dem API-Konto – Einstellungen › Verbindungen › "
                          "„Guthaben aufladen“."),
                "refused": _("Claude hat die Frage abgelehnt."),
                "bad": _("Claude hat unverständlich geantwortet.")}.get(
            kind, _("Claude ist nicht erreichbar – keine Internetverbindung?"))

    # ---------------------------------------------------------- settings card (Einstellungen → Verbindungen)
    def _claude_card(self, more):
        cc = self._reg("st.more.claude", ui.LabelFrame(more, text=_("Claude (Suche)"), padding=8))
        cc.pack(fill="x", pady=(8, 0))
        self.cl_on_var = ui.BooleanVar(value=bool(self.settings.get("claude_on", False)))
        self._reg("st.more.cl_on", ui.Checkbutton(cc, text=_("In der Suche Claude fragen können"),
                                                   variable=self.cl_on_var, command=self._claude_setting)).pack(anchor="w")
        row = ui.Frame(cc)
        row.pack(fill="x", pady=(4, 0))
        self._reg("st.more.cl_key.label", ui.Label(row, text=_("API-Key"))).pack(side="left")
        self.cl_key_var = ui.StringVar(value=self._claude_key())
        self.cl_key_var.trace_add("write", lambda *a: self._claude_setting())
        key = self._reg("st.more.cl_key", ui.Entry(row, textvariable=self.cl_key_var, width=34))
        key._dbdms_secret = True
        key.pack(side="left", padx=6)
        self._reg("st.more.cl_test", ui.Button(row, text=_("Key prüfen"), command=self._claude_test)).pack(side="left")
        self._reg("st.more.cl_clear", ui.Button(row, text=_("Key löschen"),
                                                 command=lambda: self.cl_key_var.set(""))).pack(side="left", padx=(6, 0))
        row2 = ui.Frame(cc)                       # 1.26.1: straight to the Anthropic Console's pages
        row2.pack(fill="x", pady=(4, 0))
        self._reg("st.more.cl_keys", ui.Button(row2, text=_("API-Key holen"),
                                                command=lambda: webbrowser.open(askclaude.CONSOLE_KEYS))).pack(side="left")
        self._reg("st.more.cl_billing", ui.Button(row2, text=_("Guthaben aufladen"),
                                                   command=lambda: webbrowser.open(askclaude.CONSOLE_BILLING))
                  ).pack(side="left", padx=(6, 0))
        self.cl_status_var = ui.StringVar(value="")
        self._reg("st.more.cl_status", ui.Label(cc, textvariable=self.cl_status_var, wraplength=420,
                                                 style="Dim.TLabel")).pack(anchor="w", pady=(4, 0))
        self._reg("st.more.cl_text", ui.Label(cc, text=_(
            "Findet die Suche (Strg+F) nichts Passendes, kann sie Claude fragen – nur wenn du die Zeile „Claude fragen“ "
            "wählst, nie beim Tippen. Gesendet werden nur deine Frage und die Namen der Einstellungen, Seiten und "
            "Aktionen von Fog Scout an api.anthropic.com – nie Runden, Maps, Killer, Pfade oder Spieldaten. Claude "
            "schlägt nur Einträge vor; ausgeführt wird erst, was du wählst. Dafür einen eigenen API-Key aus der "
            "Anthropic Console eintragen („API-Key holen“). Die API wird getrennt von einem Claude-Abo abgerechnet: "
            "jede Frage kostet etwas von deinem Guthaben in der Console („Guthaben aufladen“, dort lässt sich auch "
            "ein Ausgabenlimit setzen). Der Key liegt "
            "verschlüsselt auf diesem PC und steht nie in der Sicherung, im Log oder in der Diagnose."),
            style="Dim.TLabel", wraplength=420)).pack(anchor="w", pady=(4, 0))
        self._claude_setting(save=False)

    def _claude_setting(self, save=True):
        key = self.cl_key_var.get().strip()
        if save:
            self.settings.set("claude_on", bool(self.cl_on_var.get()))
            self.settings.set("claude_key", spotify.protect(key))
            self._save_soon()
        if not key:
            self.cl_status_var.set(_("Claude: kein API-Key eingetragen.") if self.cl_on_var.get() else "")
        elif not askclaude.valid_key(key):
            self.cl_status_var.set(_("Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-)."))
        else:
            self.cl_status_var.set(_("Claude: Key eingetragen.") if self.cl_on_var.get()
                                   else _("Claude: Key eingetragen, Suche mit Claude ist aus."))
        q = getattr(self, "qt", None)
        if q is not None and hasattr(q, "palette_entries"):
            q.palette_entries(q._palette_entries, claude=self._claude_ready())

    def _claude_test(self):
        """One small request with a one-line catalogue – says whether the key works (and costs next to nothing)."""
        key = self.cl_key_var.get().strip()
        if not askclaude.valid_key(key):
            self._claude_setting(save=False)
            return
        self.cl_status_var.set(_("Claude: prüfe den Key …"))

        def work():
            try:
                askclaude.ask(key, "Overview", [("p:overview", "Overview")])
                self.events.put(("claude", "test_ok", {}))
            except askclaude.AskError as e:
                self.events.put(("claude", "test_err", {"error": e.kind}))
            except Exception:
                self.events.put(("claude", "test_err", {"error": "bad"}))
        threading.Thread(target=work, daemon=True, name="claude-test").start()

    def _claude_diag(self) -> str:
        """For the diagnosis: on/off, a key set, counts – never the key, never a question."""
        a = getattr(self, "asker", None)
        return (f"Claude-Suche: an={bool(self.settings.get('claude_on'))}, Key gesetzt={bool(self._claude_key())}, "
                + (a.diag_line() if a is not None else "noch nicht gefragt"))
