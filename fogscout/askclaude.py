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
MODEL = "claude-opus-5-5"            # the current default model; effort low keeps the answer quick
EFFORT = "low"
FALLBACK_BETA = "server-side-fallback-2026-07-01"   # a declined request is retried server-side ("default")
MAX_TOKENS = 1024
HTTP_TIMEOUT = 20.0
MAX_IDS = 5
MAX_QUESTION = 300                   # characters of the question sent at most
MAX_CATALOGUE = 600                  # entries sent at most
KEY_PREFIX = "sk-ant-"
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


def valid_key(key: str) -> bool:
    k = str(key or "").strip()
    return k.startswith(KEY_PREFIX) and len(k) >= 20 and " " not in k


def _opener():
    global OPENER
    if OPENER is None:
        from .net import opener                    # 1.33.5 (S9): https-only redirects, no token to another host
        OPENER = opener()
    return OPENER


def request_body(system: str, content: str, schema: dict, max_tokens: int = MAX_TOKENS) -> dict:
    """1.27: one Messages request with a structured answer (``schema``) – shared by the search and the editor."""
    return {"model": MODEL, "max_tokens": max_tokens, "fallbacks": "default", "system": system,
            "output_config": {"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
            "messages": [{"role": "user", "content": content}]}


def body(question: str, catalogue) -> dict:
    """The search's request body. ``catalogue``: [(id, title)] – only the program's own entries."""
    lines = "\n".join(f"{i}\t{t}" for i, t in list(catalogue)[:MAX_CATALOGUE])
    return request_body(SYSTEM, f"Catalogue:\n{lines}\n\nQuestion: {str(question or '').strip()[:MAX_QUESTION]}",
                        SCHEMA)


def headers(key: str) -> dict:
    return {"x-api-key": str(key).strip(), "anthropic-version": API_VERSION, "anthropic-beta": FALLBACK_BETA,
            "content-type": "application/json"}


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


def send(key: str, payload: dict) -> dict:
    """POST ``payload`` to ENDPOINT; the reply as a dict, or AskError with its kind."""
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"), headers=headers(key),
                                 method="POST")
    try:
        with _opener().open(req, timeout=HTTP_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
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


def request(key: str, system: str, content: str, schema: dict, max_tokens: int = MAX_TOKENS) -> dict:
    """1.27: one structured request – the answer's JSON object, or AskError."""
    return reply_json(send(key, request_body(system, content, schema, max_tokens)))


def ask(key: str, question: str, catalogue) -> tuple[str, list[str]]:
    """The search: one request; (answer, ids) or AskError."""
    catalogue = list(catalogue)
    return parse(send(key, body(question, catalogue)), [i for i, _t in catalogue])


class Asker(threading.Thread):
    """One question at a time in the background; a newer question replaces one still waiting. ``post(kind, **kw)``
    gets ("answer", answer=, ids=, question=) or ("error", error=, question=)."""

    def __init__(self, post):
        super().__init__(daemon=True, name="askclaude")
        self._post = post
        self._jobs = queue.Queue()
        self.asked = self.answered = self.failed = 0          # for the diagnosis (counts only)
        self.last_error = ""

    def ask(self, key: str, question: str, catalogue):
        while True:                                            # only the newest question counts
            try:
                self._jobs.get_nowait()
            except queue.Empty:
                break
        self._jobs.put((key, question, list(catalogue)))

    def stop(self):
        self._jobs.put(None)

    def run(self):
        while True:
            job = self._jobs.get()
            if job is None:
                return
            key, question, catalogue = job
            self.asked += 1
            try:
                answer, ids = ask(key, question, catalogue)
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
