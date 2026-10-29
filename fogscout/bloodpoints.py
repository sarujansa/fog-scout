"""1.13 (user: "wenn nach einer Runde der Blutpunkte-Stand nicht erhöht wird, eine Meldung, dass ich das Cap erreicht
habe … merk dir nach jeder Runde, wie viele Blutpunkte man hat"): the bloodpoint balance from the currency bar top
right of the lobby, and the comparison before / after a round. Pure logic.

The worker reads the bar once a second while the lobby button (PLAY / CANCEL / READY) is on screen – the same OCR
the round end uses for "Lobby/Menü" (detector.OutOfMatchWatcher._currency, region detector.currency_box) – and
posts every reading; the app feeds them in here, says when a round starts (map banner) and when it was saved
(round end), and shows the result: an unchanged balance after a counted round means the round brought nothing –
the cap is reached. Everything stays local; the game is only looked at.

Why the lobby and not the result screen: there the counter may still be counting the round's points up, back in
the lobby they are credited. Why "unchanged" and not "balance ≥ 5 million": the cap (5 million since 8.2.0, 2
before) only limits the points from trials – tome and rift rewards push the balance above it, and a round then
adds nothing either; the balance itself says little, the missing gain says it all. A balance that fell (spent in
the bloodweb between the readings) says nothing; a reading needs CONFIRM_LOOKS identical looks in a row (one slip
of the OCR is never two the same); a round shorter than the statistics count (history.MIN_SECONDS) or a custom
game (no bloodpoints there) is never compared.
"""
from __future__ import annotations

import collections
import time
from dataclasses import dataclass

CONFIRM_LOOKS = 2           # identical readings in a row before a value counts
BEFORE_MAX_S = 15 * 60      # a reading older than this when the banner comes says nothing about the round
AFTER_MAX_S = 10 * 60       # … and the first reading after the end counts only within this time
CAP_FLOOR = 1_000_000       # an unchanged balance below this is no cap (it was never below a million: 1 → 2 → 5)
MAX_DIGITS = 9              # longer than any balance: a misread group
MIN_DIGITS = 3              # what _currency counts as a group
HISTORY_KEPT = 12           # confirmed changes kept for the diagnosis


def parse(text: str) -> int | None:
    """The bloodpoints in what ``_currency`` read ("1 499 484 | 4 628 | 823" – the counters left to right,
    bloodpoints first, then shards and cells): the first group's digits, or None."""
    first = str(text or "").split("|", 1)[0]
    digits = "".join(ch for ch in first if ch.isdigit())
    if not MIN_DIGITS <= len(digits) <= MAX_DIGITS:
        return None
    return int(digits)


def fmt(value: int) -> str:
    """5000000 → "5 000 000" – grouped like the game shows it."""
    return f"{int(value):,}".replace(",", " ")


@dataclass(frozen=True)
class RoundResult:
    """The balance before and after one counted round."""
    round_t: float          # start of the round (history key)
    before: int
    after: int

    @property
    def gain(self) -> int:
        return self.after - self.before

    @property
    def capped(self) -> bool:
        """The round brought nothing: the cap is reached (or the balance is above it)."""
        return self.after == self.before and self.after >= CAP_FLOOR


class BloodpointWatch:
    def __init__(self):
        self.balance: int | None = None      # last confirmed balance
        self.balance_t = 0.0                 # … when it was last confirmed (also unchanged)
        self.round_t: float | None = None    # start of the open round, None without one
        self.before: int | None = None       # balance when the open round started
        self.pending = None                  # (round_t, before, end_t): waits for the reading after the round
        self.last_text = ""                  # what the worker read last (diagnosis)
        self._last: int | None = None        # the reading being confirmed
        self._run = 0
        self.changes = collections.deque(maxlen=HISTORY_KEPT)   # (t, balance) of every confirmed change

    # ------------------------------------------------------------ readings
    def note(self, value: int | None, t: float, text: str = "") -> RoundResult | None:
        """One reading of the bar (``value`` from ``parse``, None = nothing readable). Returns the result of the last
        round once: with the first confirmed reading after its end."""
        if text:
            self.last_text = text
        if value is None:
            return None
        if value == self._last:
            self._run += 1
        else:
            self._last, self._run = value, 1
        if self._run < CONFIRM_LOOKS:
            return None
        if value != self.balance:
            self.changes.append((t, value))
        self.balance, self.balance_t = value, t
        pend, self.pending = self.pending, None
        if pend is None:
            return None
        round_t, before, end_t = pend
        if not end_t <= t <= end_t + AFTER_MAX_S:
            return None
        return RoundResult(round_t=round_t, before=before, after=value)

    # ------------------------------------------------------------ rounds
    def round_started(self, t: float):
        """The map banner: the balance read last (recent enough) is the one before the round."""
        self.pending = None
        self.round_t = t
        fresh = self.balance is not None and 0 <= t - self.balance_t <= BEFORE_MAX_S
        self.before = self.balance if fresh else None
        self._last, self._run = None, 0

    def round_ended(self, t: float, counts: bool = True):
        """The round was saved (``counts``: a normal round the statistics keep – no custom game, long enough).
        The next confirmed reading tells what it brought – CONFIRM_LOOKS fresh looks, the run from before the
        round does not carry over."""
        round_t, before, self.round_t, self.before = self.round_t, self.before, None, None
        self._last, self._run = None, 0
        if counts and round_t is not None and before is not None:
            self.pending = (round_t, before, t)

    # ------------------------------------------------------------ diagnosis
    def describe(self) -> str:
        clock = lambda t: time.strftime("%H:%M:%S", time.localtime(t))   # noqa: E731
        if self.balance is None:
            out = "noch nicht gelesen"
        else:
            out = f"Stand {fmt(self.balance)} ({clock(self.balance_t)})"
        if self.round_t is not None:
            out += f" · Runde offen, vorher {fmt(self.before) if self.before is not None else '–'}"
        if self.pending is not None:
            out += f" · wartet auf die Lesung nach der Runde (Ende {clock(self.pending[2])}, vorher {fmt(self.pending[1])})"
        if self.last_text:
            out += f" · zuletzt gelesen „{self.last_text}“"
        if self.changes:
            out += " · Änderungen " + ", ".join(f"{clock(t)} {fmt(v)}" for t, v in self.changes)
        return out
