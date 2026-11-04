"""1.26 (user: "Vorschläge anhand der Suche … evtl. Claude API Key benutzen?" – freigegeben: lokal immer, Claude nur
optional mit eigenem Key, Standard aus): the palette asks Claude which of Fog Scout's own entries fit a question
("wie mache ich die Karte grösser?").

Rules (CLAUDE.md, harte Regel „Claude-Suche“):
- Only on an explicit request of the user (Enter on "Claude fragen …"), never per key press.
- Only ENDPOINT (api.anthropic.com, HTTPS). Sent: the question and the catalogue of the program's own entries
  (id + title of settings, pages, actions) – never rounds, maps played, killers, paths, servers or game data.
- The answer is used only as ids that exist in that catalogue (``parse``); nothing Claude writes is run.
- The key is DPAPI-protected (spotify.protect) and never logged; the question is never logged either.
- Only the standard library (urllib), like spotify.py and ytupload.py.
"""
from __future__ import annotations

import json
import queue
import threading
import urllib.error
import urllib.request

ENDPOINT = "https://api.anthropic.com/v1/messages"
API_VERSION = "2026-10-21"
MODEL = "claude-opus-5-5"            # the default model; effort low keeps the answer quick
# 1.36 (user: costs shown, model selectable): the models the user can pick (setting claude_model) and their list
# prices in $ per million tokens – input, output, cache read (a cache write costs 1.25 × input). An estimate only:
# the API bills; Anthropic's prices can change (checked 2026-10). Haiku: prompts up to 100 000 tokens.
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
PRICES = {"claude-opus-5-5": (4.0, 20.0, 0.20), "claude-sonnet-5-5": (2.0, 10.0, 0.20),
          "claude-haiku-5-5": (0.10, 0.50, 0.01)}
CACHE_WRITE = 1.25
FALLBACK_MODELS = ("claude-opus-5-5", "claude-sonnet-5-5")   # the server-side fallback ("default"); not on Haiku
_model = [MODEL]                     # the picked model (set_model); one list cell – the asking threads only read it
EFFORT = "low"
FALLBACK_BETA = "server-side-fallback-2026-07-01"   # a declined request is retried server-side ("default")
MAX_TOKENS = 1024
HTTP_TIMEOUT = 20.0
IMAGE_TIMEOUT = 60.0                 # 1.35: a request with a picture uploads more and takes longer
MAX_IDS = 5
MAX_QUESTION = 300                   # characters of the question sent at most
MAX_CATALOGUE = 600                  # entries sent at most
KEY_PREFIX = "sk-ant-"
# 1.35 (user's release of 3.11.2026: pictures on a click, one switch per function): a picture goes only as a JPEG
# made in memory, its long side at most IMAGE_SIDE px (what the model looks at anyway – more only costs), never a file
IMAGE_SIDE = 1568
IMAGE_QUALITY = 85
MAX_IMAGE_BYTES = 3_000_000          # the encoded picture at most (the API takes 5 MB per picture)
# 1.26.1 (user: "einen Button, dass man direkt auf die Seite kommt"): the Anthropic Console's pages, opened in the
# default browser on a click only (like ytupload.CONSOLE) – the program itself sends nothing there
CONSOLE_KEYS = "https://platform.claude.com/settings/keys"
CONSOLE_BILLING = "https://platform.claude.com/settings/billing"

SYSTEM = ("You help users of Fog Scout, a desktop companion app for the game Dead by Daylight, find things in the "
          "app. You get the user's question and a catalogue of the app's settings, pages and actions as lines "
          "'id<TAB>title'. Pick up to five catalogue entries that best answer the question, best first, and write "
          "one short sentence in the language of the question that tells the user what to do. Use only ids from "
          "the catalogue; if nothing fits, return no ids and say so.")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["answer", "ids"],
          "properties": {"answer": {"type": "string"},
                         "ids": {"type": "array", "items": {"type": "string"}}}}

OPENER = None                        # urllib opener; the tests set a fake one


class AskError(Exception):
    """``kind``: auth (key wrong), rate (too many requests), quota (credit used up), net, bad (answer unusable),
    refused (the model declined)."""

    def __init__(self, kind: str, detail: str = ""):
        super().__init__(detail or kind)
        self.kind = kind


def set_model(key: str) -> str:
    """1.36: the model for every request from now on ("opus" | "sonnet" | "haiku"; anything else = the default)."""
    _model[0] = MODELS.get(str(key or ""), MODEL)
    return _model[0]


def current_model() -> str:
    return _model[0]


def cost_usd(model: str, usage: dict) -> float:
    """1.36: what a reply cost at list price, from its ``usage`` (input, cache write/read, output tokens)."""
    p_in, p_out, p_read = PRICES.get(model, PRICES[MODEL])
    u = usage if isinstance(usage, dict) else {}

    def n(k):
        v = u.get(k)
        return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else 0.0
    return (n("input_tokens") * p_in + n("cache_creation_input_tokens") * p_in * CACHE_WRITE
            + n("cache_read_input_tokens") * p_read + n("output_tokens") * p_out) / 1e6


class Meter:
    """1.36: what the requests of this session cost (estimate at list price) – every ``send`` adds its reply's
    usage; the App takes the new amount once a second for the month's total. Counts only, never a question."""

    def __init__(self):
        self._lock = threading.Lock()
        self.requests = 0
        self.usd = 0.0
        self.cached_tokens = 0               # input tokens read from the cache (what caching saved)
        self._untaken = 0.0

    def add(self, model: str, usage) -> float:
        c = cost_usd(model, usage)
        read = (usage or {}).get("cache_read_input_tokens") if isinstance(usage, dict) else 0
        with self._lock:
            self.requests += 1
            self.usd += c
            self._untaken += c
            self.cached_tokens += int(read) if isinstance(read, int) and read > 0 else 0
        return c

    def take(self) -> float:
        """The cost added since the last take (0.0 when nothing was asked)."""
        with self._lock:
            c, self._untaken = self._untaken, 0.0
        return c


METER = Meter()


def cached(text: str) -> dict:
    """1.36: a text block the API may keep for five minutes – the part of a request that does not change between
    questions (the search's catalogue, the statistics summary). A second question within five minutes reads it at a
    twentieth of the price; the first pays a quarter more. Too short a block is simply not cached."""
    return {"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}


def valid_key(key: str) -> bool:
    k = str(key or "").strip()
    return k.startswith(KEY_PREFIX) and len(k) >= 20 and " " not in k


def _opener():
    global OPENER
    if OPENER is None:
        from .net import opener                    # 1.33.5 (S9): https-only redirects, no token to another host
        OPENER = opener()
    return OPENER


def image_block(img) -> dict:
    """1.35: a PIL picture as an image content block – RGB, the long side at most IMAGE_SIDE, JPEG in memory,
    base64 without line breaks. Nothing is written to disk. ValueError when it stays too large."""
    import base64
    import io

    from PIL import Image
    pic = img.convert("RGB")
    if max(pic.size) > IMAGE_SIDE:
        pic = pic.copy()
        pic.thumbnail((IMAGE_SIDE, IMAGE_SIDE), Image.LANCZOS)
    buf = io.BytesIO()
    pic.save(buf, "JPEG", quality=IMAGE_QUALITY)
    data = buf.getvalue()
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("picture too large")
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                        "data": base64.standard_b64encode(data).decode("ascii")}}


def request_body(system: str, content, schema: dict, max_tokens: int = MAX_TOKENS, images=(), model=None) -> dict:
    """1.27: one Messages request with a structured answer (``schema``) – shared by the search and the editor.
    1.35: ``images`` (image blocks from ``image_block``) go before the text, as the API recommends. 1.36: ``content``
    may be a list of text blocks (``cached`` for the fixed part); ``model`` default = the picked one; the
    server-side fallback only where the model has it."""
    model = model or current_model()
    blocks = list(images)
    text = list(content) if isinstance(content, (list, tuple)) else [{"type": "text", "text": content}]
    user = blocks + text if blocks or isinstance(content, (list, tuple)) else content
    body = {"model": model, "max_tokens": max_tokens, "system": system,
            "output_config": {"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
            "messages": [{"role": "user", "content": user}]}
    if model in FALLBACK_MODELS:
        body["fallbacks"] = "default"
    return body


def body(question: str, catalogue) -> dict:
    """The search's request body. ``catalogue``: [(id, title)] – only the program's own entries. 1.36: the catalogue
    is its own cached block (the same for every question), the question comes after it."""
    lines = "\n".join(f"{i}\t{t}" for i, t in list(catalogue)[:MAX_CATALOGUE])
    return request_body(SYSTEM, [cached(f"Catalogue:\n{lines}"),
                                 {"type": "text", "text": f"Question: {str(question or '').strip()[:MAX_QUESTION]}"}],
                        SCHEMA)


def headers(key: str, fallback: bool = True) -> dict:
    h = {"x-api-key": str(key).strip(), "anthropic-version": API_VERSION, "content-type": "application/json"}
    if fallback:
        h["anthropic-beta"] = FALLBACK_BETA
    return h


def reply_json(reply: dict) -> dict:
    """The JSON object of a structured answer (AskError refused/bad otherwise)."""
    if reply.get("stop_reason") == "refusal":
        raise AskError("refused")
    text = "".join(b.get("text", "") for b in reply.get("content") or () if b.get("type") == "text")
    try:
        data = json.loads(text)
    except ValueError:
        raise AskError("bad") from None
    if not isinstance(data, dict):
        raise AskError("bad")
    return data


def parse(reply: dict, known) -> tuple[str, list[str]]:
    """(answer, ids) from the API's reply – ids only from ``known``, at most MAX_IDS, no repeats."""
    data = reply_json(reply)
    known = set(known)
    ids = []
    for i in data.get("ids") or ():
        if isinstance(i, str) and i in known and i not in ids:
            ids.append(i)
    return str(data.get("answer") or "").strip()[:400], ids[:MAX_IDS]


def send(key: str, payload: dict, timeout: float = HTTP_TIMEOUT) -> dict:
    """POST ``payload`` to ENDPOINT; the reply as a dict, or AskError with its kind."""
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"),
                                 headers=headers(key, "fallbacks" in payload), method="POST")
    try:
        with _opener().open(req, timeout=timeout) as r:
            reply = json.loads(r.read().decode("utf-8"))
        if isinstance(reply, dict):                      # 1.36: what it cost (estimate), also for a refusal
            METER.add(str(payload.get("model") or MODEL), reply.get("usage"))
        return reply
    except urllib.error.HTTPError as e:
        code = e.code
        try:
            err = json.loads(e.read().decode("utf-8")).get("error") or {}
        except (ValueError, OSError, AttributeError):
            err = {}
        if code in (401, 403):
            raise AskError("auth") from None
        if code == 429:
            raise AskError("rate") from None
        if code == 402 or "credit" in str(err.get("message", "")).lower():
            raise AskError("quota") from None
        raise AskError("net", f"HTTP {code}") from None
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        raise AskError("net", type(e).__name__) from None
    except ValueError:
        raise AskError("bad") from None


def request(key: str, system: str, content, schema: dict, max_tokens: int = MAX_TOKENS, images=()) -> dict:
    """1.27: one structured request – the answer's JSON object, or AskError. 1.35: with ``images``."""
    return reply_json(send(key, request_body(system, content, schema, max_tokens, images),
                           IMAGE_TIMEOUT if images else HTTP_TIMEOUT))


def ask(key: str, question: str, catalogue) -> tuple[str, list[str]]:
    """The search: one request; (answer, ids) or AskError."""
    catalogue = list(catalogue)
    return parse(send(key, body(question, catalogue)), [i for i, _t in catalogue])


class Asker(threading.Thread):
    """One question at a time in the background; a newer question replaces one still waiting. ``post(kind, **kw)``
    gets ("answer", answer=, ids=, question=), 1.35 ("stats", answer=, question=) or ("error", error=, question=)."""

    def __init__(self, post):
        super().__init__(daemon=True, name="askclaude")
        self._post = post
        self._jobs = queue.Queue()
        self.asked = self.answered = self.failed = 0          # for the diagnosis (counts only)
        self.last_error = ""

    def _put(self, job):
        while True:                                            # only the newest question counts
            try:
                self._jobs.get_nowait()
            except queue.Empty:
                break
        self._jobs.put(job)

    def ask(self, key: str, question: str, catalogue):
        self._put(("search", key, question, list(catalogue)))

    def ask_stats(self, key: str, question: str, data: dict):
        """1.35: a statistics question with the summed-up round values (statsclaude.summary)."""
        self._put(("stats", key, question, data))

    def stop(self):
        self._jobs.put(None)

    def run(self):
        while True:
            job = self._jobs.get()
            if job is None:
                return
            what, key, question, extra = job
            self.asked += 1
            try:
                if what == "stats":
                    from . import statsclaude
                    reply = request(key, statsclaude.SYSTEM, statsclaude.blocks(question, extra), statsclaude.SCHEMA,
                                    statsclaude.MAX_TOKENS)
                    self.answered += 1
                    self.last_error = ""
                    self._post("stats", answer=statsclaude.answer(reply), question=question)
                    continue
                answer, ids = ask(key, question, extra)
            except AskError as e:
                self.failed += 1
                self.last_error = e.kind
                self._post("error", error=e.kind, question=question)
                continue
            except Exception:                                  # never let the thread die
                self.failed += 1
                self.last_error = "bad"
                self._post("error", error="bad", question=question)
                continue
            self.answered += 1
            self.last_error = ""
            self._post("answer", answer=answer, ids=ids, question=question)

    def diag_line(self) -> str:
        """For the diagnosis: counts and the last error kind – never the key, never a question."""
        return f"gefragt {self.asked}, beantwortet {self.answered}, Fehler {self.failed}" + \
            (f" (zuletzt {self.last_error})" if self.last_error else "")
