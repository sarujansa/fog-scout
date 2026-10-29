"""Lobby: search, waiting time and role from the worker, notifications (sound + own window).

Mixin of App (app.py) – the methods use App's attributes; split out of app.py unchanged."""
from __future__ import annotations

import logging
import time

from . import bloodpoints, history
from .capture import IS_WIN, foreground_root, is_game_window
from .i18n import _
from .lobby import killer_label, resolve_killer
from .textnorm import fmt_duration

log = logging.getLogger("fogscout")


class LobbyInfo:
    def _notify_flags_changed(self):
        for key, v in self.notify_vars.items():
            self.settings.set(key, bool(v.get()))
        self._save_soon()

    def _notify(self, title, text, force=False):
        """Sound + own notification window (lobby found, countdown) – only local, nothing goes to the game."""
        if (not force and self.settings.get("notify_background_only", True) and not self.simulate
                and self.game is not None):
            fg = foreground_root()
            if is_game_window(fg):
                return                                   # DBD is in front: the player sees it anyway
        try:
            if IS_WIN:
                import winsound
                winsound.PlaySound("SystemNotification", winsound.SND_ALIAS | winsound.SND_ASYNC)
            else:
                self.root.bell()
        except Exception:
            log.debug("notify sound", exc_info=True)
        # own window instead of a Windows notification: those are swallowed by "Do not disturb",
        # which Windows turns on by itself while a game runs
        self.toast.show(title, text)

    # ---------------------------------------------------------- 1.13: bloodpoint balance (cap reached?)
    def _bp_reading(self, d):
        """A reading of the bloodpoint counter from the lobby (worker, once a second while the lobby button is on
        screen). The watch confirms it; the first confirmed one after a counted round says what the round brought –
        nothing: the cap is reached (log line, and sound + window unless switched off – also with DBD in front, that
        is where the player is), else a log line. The balance after the round goes to the saved round."""
        res = self.bloodpoints.note(d.get("value"), d.get("t") or time.time(), d.get("text") or "")
        if res is None:
            return
        after = bloodpoints.fmt(res.after)
        if res.capped:
            self._log(_("Blutpunkte unverändert: {bp} vor und nach der Runde – das Cap ist erreicht, die Punkte "
                        "dieser Runde sind verfallen.", bp=after), "Erkennung")
            if self.settings.get("bp_cap_notify", True):
                self._notify(_("Blutpunkte-Cap erreicht"),
                             _("{bp} BP vor und nach der Runde – im Blutnetz ausgeben, sonst bringt auch die "
                               "nächste Runde nichts.", bp=after), force=True)
        elif res.gain > 0:
            self._log(_("Blutpunkte: +{gain} in dieser Runde, Stand {bp}.", gain=bloodpoints.fmt(res.gain),
                        bp=after), "Erkennung")
        else:
            self._log(_("Blutpunkte: Stand {bp} nach der Runde, vorher {before}.", bp=after,
                        before=bloodpoints.fmt(res.before)), "Erkennung")
        try:
            history.set_balance(self._hist_path(), res.round_t, res.after)
        except OSError as e:
            self._report_once("history", f"{e}")

    # ---------------------------------------------------------- lobby: search, waiting time, role
    def _killer_of(self, name):
        """Killer name as read -> the killer (own assignments of skins / new killers)."""
        return resolve_killer(name, self.settings.get("killer_aliases", {}))

    def _role_name(self, role):
        return {"killer": _("Killer"), "survivor": _("Survivor")}.get(role, "")

    def _queue_text(self, now):
        q = self._queue
        role = self._role_name(q.get("role"))
        if q.get("role") == "killer" and q.get("killer"):
            role = killer_label(self._killer_of(q["killer"]))                 # "Nurse" says more than "Killer"
        if q["state"] == "search" and q.get("since"):
            text = _("Suche läuft: {time}", time=fmt_duration(max(0.0, now - q["since"])))
            if q.get("crossplay_off") and self.settings.get("farming_crossplay", True):
                text += " · " + _("Farming")
            return text + (f" · {role}" if role else "")
        f = q.get("found") or q.get("used")          # lobby found / the round it led to
        if q["state"] == "custom" or (f is not None and f.custom):
            return _("Custom Game")
        if f is not None:
            parts = ([_("Rolle: {role}", role=role)] if role else []) + \
                ([_("Wartezeit {time}", time=fmt_duration(f.wait))] if f.wait is not None else []) + \
                ([_("Farming")] if f.crossplay_off and self.settings.get("farming_crossplay", True) else [])
            return " · ".join(parts)
        return ""

    def _queue_event(self, d):
        prev, what = self._queue, d.get("what")
        if what == "search":
            self._queue = {"state": "search", "since": d.get("since"), "role": d.get("role") or prev.get("role"),
                           "killer": d.get("killer") or prev.get("killer", ""),
                           "crossplay_off": d.get("crossplay_off")}
            if prev.get("state") != "search":
                self._log(_("Suche nach einem Match gestartet."), "Erkennung")
        elif what == "cancel":
            self._queue = {"state": "idle"}
            self._log(_("Suche abgebrochen."), "Erkennung")
        elif what == "left":                             # back on PLAY: an unused lobby must not stick
            if prev.get("found") is not None:
                self._log(_("Lobby verlassen – sie zählt für keine Runde."), "Erkennung")
            self._queue = {"state": "idle"}
        elif what == "found" and d.get("found") is not None:
            f = d["found"]
            self._queue = {"state": "custom" if f.custom else "lobby", "role": f.role, "killer": f.killer, "found": f}
            if not f.custom and self.settings.get("lobby_notify", True):
                self._notify(_("Lobby gefunden"), (_("nach {time}", time=fmt_duration(f.wait)) + " – "
                                                   if f.wait is not None else "") + _("READY drücken."))
            if f.custom:
                self._log(_("Custom Game – keine Wartezeit."), "Erkennung")
            else:
                who = f" ({self._role_name(f.role)}{', ' + self._killer_of(f.killer) if f.killer else ''})" if f.role else ""
                if f.wait is not None:
                    self._log(_("Lobby gefunden nach {time}{role}.", time=fmt_duration(f.wait), role=who), "Erkennung")
                else:
                    self._log(_("Lobby gefunden{role}.", role=who), "Erkennung")
                off, on = f.cross_looks
                looks = _("{off} von {n} Blicken mit Kreuz", off=off, n=off + on) if off + on else _("letzter Blick")
                if f.crossplay_off and self.settings.get("farming_crossplay", True):
                    self._log(_("Crossplay ist aus ({looks}) – die nächste Runde zählt als Farming-Runde.",
                                looks=looks), "Erkennung")
                elif f.crossplay_off is None and self.settings.get("farming_crossplay", True):
                    self._log(_("Crossplay-Anzeige nicht lesbar – die Runde zählt nicht als Farming (Ausschnitt in "
                                "debug/lobby)."), "Erkennung")
                elif self.settings.get("farming_crossplay", True):
                    self._log(_("Crossplay ist an ({looks}) – keine Farming-Runde.", looks=looks), "Erkennung")
        elif what == "remind":
            if self.settings.get("lobby_remind", True):
                self._notify(_("Lobby startet gleich"), _("Noch {n} s – READY ist noch nicht gedrückt.",
                                                           n=int(d.get("seconds") or 0)))
                self._log(_("Lobby-Countdown läuft ab, READY ist noch nicht gedrückt."), "Erkennung")
        else:
            self._queue = dict(prev, role=d.get("role") or prev.get("role"),
                               killer=d.get("killer") or prev.get("killer", ""),
                               crossplay_off=d.get("crossplay_off", prev.get("crossplay_off")))
