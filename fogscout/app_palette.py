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

from . import askclaude, i18n, launch, overview, palette, spotify, statsclaude
from . import uimodel as ui
from .i18n import N_, _

ROUNDS_KEPT = 50          # the last rounds offered
CLAUDE_KINDS = ("setting", "page", "action")     # what Claude may see (titles of the program's own texts)
# 1.36 (user: costs shown, model selectable): the models offered, cheapest last (askclaude.MODELS/PRICES)
MODEL_LABELS = (("opus", N_("Opus 5.5 – am genauesten")), ("sonnet", N_("Sonnet 5.5 – halber Preis")),
                ("haiku", N_("Haiku 5.5 – am günstigsten")))


def usd(value: float) -> str:
    """An estimated amount in dollars as the language writes it ("0,04 $" / "$0.04"); under a cent "< 0,01 $"."""
    v = max(0.0, float(value or 0.0))
    num = "0.00" if v == 0 else ("< 0.01" if v < 0.01 else f"{v:.2f}")
    return (num.replace(".", ",") + " $") if i18n.current() == "de" else ("$" + num if v >= 0.01 or v == 0
                                                                         else "< $0.01")


def _fixed(text: str) -> bool:
    """A fixed program text – also "Position (Musik)": a fixed text with the fixed name of its tab."""
    t = str(text or "").strip()
    if i18n.is_program_text(t):
        return True
    if t.endswith(")") and " (" in t:
        head, _sep, tail = t[:-1].rpartition(" (")
        return i18n.is_program_text(head) and i18n.is_program_text(tail)
    return False


def claude_catalogue(entries) -> tuple[list, dict]:
    """1.28 (audit F1, Datenschutz): what the Claude search may send – a positive list. An entry goes only when
    (1) it is a setting, page or action, (2) its widget kind allows it (``Entry.static``, set by the window only for
    tick boxes, buttons, titles, sliders and tabs – never labels, which hold status lines, paths, pings, statistics)
    and (3) its title and sub are verbatim the program's own texts (i18n.is_program_text). The ids are opaque
    ("e1" …) so no entry text travels twice. Returns ([(id, text)], {id: entry id})."""
    out, ids = [], {}
    for e in entries:
        if e.kind not in CLAUDE_KINDS or not e.static or not _fixed(e.title) or (e.sub and not _fixed(e.sub)):
            continue
        cid = f"e{len(out) + 1}"
        ids[cid] = e.id
        out.append((cid, e.title + (f" ({e.sub})" if e.sub else "")))
    return out, ids


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
        out.append(("edit", self.edit_btn.cget("text") if hasattr(self, "edit_btn") else _("Anordnen")))
        if self.settings.get("rec_on") or self.settings.get("rec_folder"):
            rec = getattr(self, "recorder", None)
            out.append(("record", _("Aufnahme stoppen") if rec is not None and rec.recording else _("Aufnahme starten")))
            out.append(("clip", _("Clip speichern")))
        out += [("update", _("Jetzt nach Updates suchen")), ("diagnose", _("Diagnose kopieren")),
                ("setup", _("Einrichtung starten"))]
        if self._claude_stats_ready():                 # 1.36: fixed statistics questions (claude_stats on)
            out += [("claude_week", _("Claude: Woche zusammenfassen")),
                    ("claude_build", _("Claude: Welcher Build läuft am besten?"))]
        return [palette.Entry("action", "a:" + key, title, action=key, static=i18n.is_program_text(title))
                for key, title in out]

    def _palette_pages(self) -> list:
        from .qt_common import PAGE_SUBTITLES
        from .qt_window import PAGES
        return [palette.Entry("page", "p:" + key, _(label), _(PAGE_SUBTITLES.get(key, "")), action="page", arg=key,
                              words=i18n.other(_(label)), static=True)
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

    def _claude_stats_ready(self) -> bool:
        """1.35: the search may also ask Claude about the summed-up round values."""
        return bool(self.settings.get("claude_stats", False)) and askclaude.valid_key(self._claude_key())

    def _claude_key(self) -> str:
        """The key in use: one typed this session that could not be stored encrypted (1.28), else the stored one."""
        return getattr(self, "_claude_session_key", "") or spotify.unprotect(self.settings.get("claude_key", "") or "")

    def _claude_stored_words(self) -> str:
        """1.28 (audit F2): says honestly how the key is kept – never „verschlüsselt“ when it is not."""
        stored = self.settings.get("claude_key", "") or ""
        if getattr(self, "_claude_session_key", ""):
            return _("nur für diese Sitzung – die Windows-Verschlüsselung ist nicht verfügbar")
        if spotify.is_legacy(stored):
            return _("unverschlüsselt gespeichert (alt)")
        if spotify.is_encrypted(stored) and spotify.unprotect(stored):
            return _("verschlüsselt gespeichert")
        return ""

    # ---------------------------------------------------------- events of the palette
    def _palette_event(self, action, arg):
        if action == "palette_open":
            self._qt_event("search_open")             # the pages filled, the window's search index new
            self.qt.palette_entries(self._palette_build(), recent=self.settings.get("palette_recent") or [],
                                    claude=self._claude_ready(), stats=self._claude_stats_ready())
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
        elif action == "palette_ask_stats":
            self._palette_ask_stats(str(arg or ""))

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
             "update": self._palette_update, "claude_week": lambda: self._palette_ask_fixed("week"),
             "claude_build": lambda: self._palette_ask_fixed("build")}.get(e.action, lambda: None)()

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
            self.qt.palette.show_error(_("Kein API-Key – unter Einstellungen → Verbindungen → Claude eintragen."))
            return
        catalogue, self._claude_ids = claude_catalogue(getattr(self, "_palette_by_id", {}).values())
        if not catalogue:                     # nothing fixed to offer: nothing is sent
            self.qt.palette.show_error(_("Claude hat nichts Passendes gefunden."))
            return
        self._asker().ask(key, question, catalogue)

    def _palette_ask_stats(self, question: str):
        """1.35: a statistics question – the question and statsclaude.summary (counts and rates per group, never a
        single round, never a name) go to Claude once; the answer comes back as plain text."""
        if not question.strip() or not self._claude_stats_ready():
            return
        try:
            j = self._joined()
            data = statsclaude.summary(j.rounds, j.off)
        except Exception:
            import logging
            logging.getLogger("fogscout").exception("Claude: Statistik zusammenfassen")
            self.qt.palette.show_error(_("Die Statistik liess sich nicht zusammenfassen – Details im Log."))
            return
        if not data.get("rounds"):
            self.qt.palette.show_error(_("Noch keine Runden – Claude hätte nichts zum Auswerten."))
            return
        self._asker().ask_stats(self._claude_key(), question, data)

    def _palette_ask_fixed(self, kind: str):
        """1.36: "Woche zusammenfassen" / "Welcher Build läuft am besten?" – the palette opens again with the
        question in its field and Claude's answer below it; sent like a statistics question (statsclaude)."""
        if not self._claude_stats_ready():
            return
        question = (_("Fasse meine Woche im Vergleich zur letzten zusammen: was lief besser, was schlechter?")
                    if kind == "week" else
                    _("Welche meiner Perks laufen am besten – getrennt nach Killer und Survivor?"))
        q = self.qt
        q.palette.open(q._palette_entries, q._palette_recent, q._palette_claude, text=question)
        try:
            j = self._joined()
            data = (statsclaude.week(j.rounds, j.off, time.time()) if kind == "week"
                    else statsclaude.summary(j.rounds, j.off))
        except Exception:
            import logging
            logging.getLogger("fogscout").exception("Claude: Statistik zusammenfassen")
            q.palette.show_error(_("Die Statistik liess sich nicht zusammenfassen – Details im Log."))
            return
        rounds = (data["this_week"]["rounds"] + data["last_week"]["rounds"]) if kind == "week" else data["rounds"]
        if not rounds:
            q.palette.show_error(_("Noch keine Runden – Claude hätte nichts zum Auswerten."))
            return
        q.palette.show_waiting()
        self._asker().ask_stats(self._claude_key(), question, data)

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
        if kind == "stats":                                 # 1.35: a statistics answer – plain text, no rows
            p.show_answer(data.get("answer", "") or _("Claude hat keine Antwort gegeben."), [])
        elif kind == "answer":
            ids = getattr(self, "_claude_ids", {})          # 1.28: the opaque ids back to the entries
            p.show_answer(data.get("answer", ""), [ids[i] for i in data.get("ids") or [] if i in ids])
        else:
            p.show_error(self._claude_words(data.get("error", "net")))

    @staticmethod
    def _claude_words(kind: str) -> str:
        return askclaude.error_text(kind)

    # ---------------------------------------------------------- settings card (Einstellungen → Verbindungen)
    def _claude_card(self, more):
        cc = self._reg("st.more.claude", ui.LabelFrame(more, text=_("Claude"), padding=8))
        cc.pack(fill="x", pady=(8, 0))
        self.cl_on_var = ui.BooleanVar(value=bool(self.settings.get("claude_on", False)))
        self._reg("st.more.cl_on", ui.Checkbutton(cc, text=_("In der Suche Claude fragen können"),
                                                   variable=self.cl_on_var, command=self._claude_setting)).pack(anchor="w")
        self.cl_editor_var = ui.BooleanVar(value=bool(self.settings.get("claude_editor", False)))     # 1.27
        self._reg("st.more.cl_editor", ui.Checkbutton(cc, text=_("Im Clip-Editor Claude nutzen"),
                                                       variable=self.cl_editor_var,
                                                       command=self._claude_setting)).pack(anchor="w")
        # 1.35 (user's release of 3.11.2026): pictures and summed-up round values – one switch per function
        self.cl_image_var = ui.BooleanVar(value=bool(self.settings.get("claude_image", False)))
        self._reg("st.more.cl_image", ui.Checkbutton(cc, text=_("Bilder im Bild-Editor an Claude schicken"),
                                                      variable=self.cl_image_var,
                                                      command=self._claude_setting)).pack(anchor="w")
        self.cl_frame_var = ui.BooleanVar(value=bool(self.settings.get("claude_frame", False)))
        self._reg("st.more.cl_frame", ui.Checkbutton(cc, text=_("Standbilder aus Aufnahmen im Clip-Editor an Claude "
                                                                "schicken"),
                                                      variable=self.cl_frame_var,
                                                      command=self._claude_setting)).pack(anchor="w")
        self.cl_stats_var = ui.BooleanVar(value=bool(self.settings.get("claude_stats", False)))
        self._reg("st.more.cl_stats", ui.Checkbutton(cc, text=_("In der Suche Statistik-Fragen an Claude stellen"),
                                                      variable=self.cl_stats_var,
                                                      command=self._claude_setting)).pack(anchor="w")
        self._reg("st.more.cl_privacy", ui.Label(cc, text=_(
            "Bilder können Spielernamen zeigen – sie gehen nur auf deinen Klick „Vorschlagen“ an Claude, verkleinert "
            "und nur im Speicher; bereits zensierte Bereiche bleiben zensiert. Statistik-Fragen senden nur Zähler "
            "und Quoten je Rolle, Killer, Map, Region und Tageszeit – keine einzelne Runde, keine Namen von "
            "Spielern."), style="Dim.TLabel", wraplength=420)).pack(anchor="w", pady=(2, 0))
        mr = ui.Frame(cc)                         # 1.36: the model for every Claude request
        mr.pack(fill="x", pady=(6, 0))
        self._reg("st.more.cl_model.label", ui.Label(mr, text=_("Modell"))).pack(side="left")
        labels = dict(MODEL_LABELS)
        self.cl_model_var = ui.StringVar(value=_(labels.get(self.settings.get("claude_model", "opus"),
                                                            labels["opus"])))
        mcb = self._reg("st.more.cl_model", ui.Combobox(mr, textvariable=self.cl_model_var, state="readonly",
                                                         width=28, values=[_(t) for _k, t in MODEL_LABELS]))
        mcb.pack(side="left", padx=6)
        mcb.bind("<<ComboboxSelected>>", lambda e: self._claude_setting())
        self.cl_cost_var = ui.StringVar(value="")
        self._reg("st.more.cl_cost", ui.Label(cc, textvariable=self.cl_cost_var, wraplength=420,
                                               style="Dim.TLabel")).pack(anchor="w", pady=(2, 0))
        self._claude_cost_show()
        row = ui.Frame(cc)
        row.pack(fill="x", pady=(4, 0))
        self._reg("st.more.cl_key.label", ui.Label(row, text=_("API-Key"))).pack(side="left")
        self._claude_session_key = ""
        self._claude_loaded = self._claude_key()      # 1.28: the key is written only when the field really changes
        self.cl_key_var = ui.StringVar(value=self._claude_loaded)
        self.cl_key_var.trace_add("write", lambda *a: self._claude_setting())
        key = self._reg("st.more.cl_key", ui.Entry(row, textvariable=self.cl_key_var, width=34))
        key._dbdms_secret = True
        key.pack(side="left", padx=6)
        self._reg("st.more.cl_test", ui.Button(row, text=_("Key prüfen"), command=self._claude_test)).pack(side="left")
        self._reg("st.more.cl_clear", ui.Button(row, text=_("Key löschen"),
                                                 command=self._claude_clear)).pack(side="left", padx=(6, 0))
        row2 = ui.Frame(cc)                       # 1.26.1: straight to the Anthropic Console's pages
        row2.pack(fill="x", pady=(4, 0))
        self._reg("st.more.cl_keys", ui.Button(row2, text=_("API-Key holen"),
                                                command=lambda: launch.open_url(askclaude.CONSOLE_KEYS))).pack(side="left")
        self._reg("st.more.cl_billing", ui.Button(row2, text=_("Guthaben aufladen"),
                                                   command=lambda: launch.open_url(askclaude.CONSOLE_BILLING))
                  ).pack(side="left", padx=(6, 0))
        self.cl_status_var = ui.StringVar(value="")
        self._reg("st.more.cl_status", ui.Label(cc, textvariable=self.cl_status_var, wraplength=420,
                                                 style="Dim.TLabel")).pack(anchor="w", pady=(4, 0))
        self._reg("st.more.cl_text", ui.Label(cc, text=_(
            "Jedes Häkchen ist eine Stelle, an der Claude auf deinen Klick hilft – nie von selbst, nie beim "
            "Tippen: die Suche (Zeile „Claude fragen“: deine Frage und die Namen der Einstellungen, Seiten und "
            "Aktionen), Statistik-Fragen (Zähler und Quoten), der Clip-Editor („Mit Claude bearbeiten“: deine "
            "Bitte und der Schnitt als Zahlen, mit Häkchen auch ein Standbild) und der Bild-Editor (Reiter "
            "„Claude“: deine Bitte und das Bild). Claude schlägt nur vor; ausgeführt wird erst, was du wählst oder "
            "mit „Übernehmen“ bestätigst. Nie gesendet werden Runden, Maps, Killer, Pfade, Dateinamen, Server oder "
            "Log. Dafür einen eigenen API-Key aus der Anthropic Console eintragen („API-Key holen“); die API wird "
            "getrennt von einem Claude-Abo aus Guthaben bezahlt („Guthaben aufladen“, dort auch ein Ausgabenlimit) "
            "– die Kosten je Frage schätzt das Programm aus der Antwort und zählt sie je Monat zusammen. Der Key "
            "wird mit der Windows-Verschlüsselung auf diesem PC gespeichert (geht das nicht, gilt er nur bis zum "
            "Beenden) und steht nie in der Sicherung, im Log oder in der Diagnose."),
            style="Dim.TLabel", wraplength=420)).pack(anchor="w", pady=(4, 0))
        self._claude_setting(save=False)

    def _claude_setting(self, save=True):
        key = self.cl_key_var.get().strip()
        if save:
            self.settings.set("claude_on", bool(self.cl_on_var.get()))
            self.settings.set("claude_editor", bool(self.cl_editor_var.get()))
            for k, var in (("claude_image", self.cl_image_var), ("claude_frame", self.cl_frame_var),
                           ("claude_stats", self.cl_stats_var)):
                self.settings.set(k, bool(var.get()))
            picked = next((k for k, t in MODEL_LABELS if _(t) == self.cl_model_var.get()), "opus")
            self.settings.set("claude_model", picked)
            askclaude.set_model(picked)
            if key != self._claude_loaded:        # 1.28 (audit F2b): a switch never overwrites the stored key
                self._claude_store(key)
            self._save_soon()
        on = any(v.get() for v in (self.cl_on_var, self.cl_editor_var, self.cl_image_var, self.cl_frame_var,
                                   self.cl_stats_var))
        stored = self.settings.get("claude_key", "") or ""
        if not key and stored and not spotify.unprotect(stored):
            self.cl_status_var.set(_("Claude: Der gespeicherte Key ist auf diesem PC nicht lesbar – bitte neu "
                                     "eintragen oder „Key löschen“."))
        elif not key:
            self.cl_status_var.set(_("Claude: kein API-Key eingetragen.") if on else "")
        elif not askclaude.valid_key(key):
            self.cl_status_var.set(_("Claude: Das sieht nicht wie ein API-Key aus (beginnt mit sk-ant-)."))
        else:
            words = self._claude_stored_words()
            text = (_("Claude: Key eingetragen.") if on
                    else _("Claude: Key eingetragen, Claude ist überall aus."))
            self.cl_status_var.set(text + (" " + _("({how})", how=words) if words else ""))
        q = getattr(self, "qt", None)
        if q is not None and hasattr(q, "palette_entries"):
            q.palette_entries(q._palette_entries, claude=self._claude_ready(), stats=self._claude_stats_ready())

    def _claude_store(self, key: str):
        """Writes a newly typed key encrypted; without the Windows encryption it is kept for this session only and
        the stored value stays as it was (never clear text, never Base64)."""
        self._claude_loaded = key
        if not key:
            self._claude_session_key = ""
            self.settings.set("claude_key", "")
            return
        try:
            self.settings.set("claude_key", spotify.protect(key))
            self._claude_session_key = ""
        except spotify.CannotProtect:
            self._claude_session_key = key
            self._log(_("Claude: API-Key gilt nur bis zum Beenden – die Windows-Verschlüsselung ist nicht verfügbar, "
                       "darum wird er nicht gespeichert."), "System")

    def _claude_clear(self):
        """„Key löschen“: removes the stored key too – also one this PC cannot read."""
        self._claude_session_key = ""
        self._claude_loaded = ""
        self.settings.set("claude_key", "")
        self.cl_key_var.set("")
        self._claude_setting()

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

    def _claude_editor_key(self) -> str:
        """1.27: the key for the clip editor – "" while the user has not allowed Claude there (or no valid key)."""
        key = self._claude_key()
        return key if self.settings.get("claude_editor", False) and askclaude.valid_key(key) else ""

    # ---------------------------------------------------------- 1.36: what the requests cost (estimate)
    def _claude_cost_tick(self):
        """A tick step: the cost of replies since the last tick into this month's total (settings, this PC)."""
        new = askclaude.METER.take()
        if new <= 0:
            return
        month = time.strftime("%Y-%m")
        spent = {k: v for k, v in (self.settings.get("claude_spent") or {}).items()
                 if isinstance(k, str) and isinstance(v, (int, float)) and not isinstance(v, bool)}
        spent[month] = float(spent.get(month, 0.0)) + new
        self.settings.set("claude_spent", dict(sorted(spent.items())[-12:]))      # the last twelve months
        self._save_soon()
        self._claude_cost_show()

    def _claude_cost_show(self):
        var = getattr(self, "cl_cost_var", None)
        if var is None:
            return
        m = askclaude.METER
        month = float((self.settings.get("claude_spent") or {}).get(time.strftime("%Y-%m"), 0.0) or 0.0)
        var.set(_("Kosten (Schätzung nach Listenpreis): diese Sitzung {session} bei {n} Anfragen, diesen Monat "
                  "{month}. Abgerechnet wird in der Anthropic Console.", session=usd(m.usd), n=m.requests,
                  month=usd(month)))

    def _claude_image_key(self) -> str:
        """1.35: the key for the screenshot editor – "" while the user has not allowed pictures there."""
        key = self._claude_key()
        return key if self.settings.get("claude_image", False) and askclaude.valid_key(key) else ""

    def _claude_diag(self) -> str:
        """For the diagnosis: on/off, a key set, counts – never the key, never a question."""
        a = getattr(self, "asker", None)
        return (f"Claude: Suche an={bool(self.settings.get('claude_on'))}, "
                f"Editor an={bool(self.settings.get('claude_editor'))}, "
                f"Bilder an={bool(self.settings.get('claude_image'))}, "
                f"Standbilder an={bool(self.settings.get('claude_frame'))}, "
                f"Statistik an={bool(self.settings.get('claude_stats'))}, Key gesetzt={bool(self._claude_key())}, "
                f"Modell={askclaude.current_model()}, Anfragen={askclaude.METER.requests}, "
                f"Kosten≈{askclaude.METER.usd:.3f} $, aus Cache={askclaude.METER.cached_tokens} Token, "
                + (a.diag_line() if a is not None else "noch nicht gefragt"))
