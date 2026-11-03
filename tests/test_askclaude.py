"""1.26: the optional question to Claude (askclaude.py) – no network: a fake opener records the request."""
import io
import json
import queue
import urllib.error

import pytest

from fogscout import askclaude

KEY = "sk-ant-api03-" + "x" * 40


class _Reply(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeOpener:
    def __init__(self, reply=None, error=None):
        self.reply, self.error, self.requests = reply, error, []

    def open(self, req, timeout=None):
        self.requests.append((req, timeout))
        if self.error is not None:
            raise self.error
        return _Reply(json.dumps(self.reply).encode("utf-8"))


def _answer(answer, ids, stop="end_turn"):
    return {"type": "message", "stop_reason": stop,
            "content": [{"type": "text", "text": json.dumps({"answer": answer, "ids": ids})}]}


@pytest.fixture
def opener(monkeypatch):
    def make(**kw):
        o = FakeOpener(**kw)
        monkeypatch.setattr(askclaude, "OPENER", o)
        return o
    return make


CATALOGUE = [("s:size", "Eigene Grösse zurücksetzen (Overlay)"), ("p:overlay", "Overlay"), ("a:scan", "Scannen")]


def test_the_request_goes_only_to_the_api_with_the_question_and_the_catalogue(opener):
    o = opener(reply=_answer("Unter Overlay die Grösse ändern.", ["s:size", "p:overlay"]))
    answer, ids = askclaude.ask(KEY, "wie mache ich die Karte grösser?", CATALOGUE)
    assert answer == "Unter Overlay die Grösse ändern." and ids == ["s:size", "p:overlay"]
    (req, timeout), = o.requests
    assert req.full_url == "https://api.anthropic.com/v1/messages" and req.get_method() == "POST"
    assert timeout == askclaude.HTTP_TIMEOUT
    headers = {k.lower(): v for k, v in req.header_items()}
    assert headers["x-api-key"] == KEY and headers["anthropic-version"] == askclaude.API_VERSION
    body = json.loads(req.data.decode("utf-8"))
    assert set(body) == {"model", "max_tokens", "fallbacks", "system", "output_config", "messages"}
    assert body["model"] == askclaude.MODEL and body["output_config"]["format"]["type"] == "json_schema"
    text = body["messages"][0]["content"]
    assert "wie mache ich die Karte grösser?" in text and "s:size\tEigene Grösse zurücksetzen (Overlay)" in text


def test_the_question_and_the_catalogue_are_cut_to_their_limits(opener):
    o = opener(reply=_answer("", []))
    big = [(f"s:{i}", f"Setting {i}") for i in range(askclaude.MAX_CATALOGUE + 50)]
    askclaude.ask(KEY, "x" * 1000, big)
    text = json.loads(o.requests[0][0].data.decode("utf-8"))["messages"][0]["content"]
    assert text.count("\n") <= askclaude.MAX_CATALOGUE + 4
    assert "x" * askclaude.MAX_QUESTION in text and "x" * (askclaude.MAX_QUESTION + 1) not in text


def test_only_known_ids_are_taken_at_most_five_without_repeats():
    reply = _answer("ok", ["s:size", "rm -rf", "s:size", "p:overlay", "a:scan", "x", "y"])
    assert askclaude.parse(reply, [i for i, _t in CATALOGUE])[1] == ["s:size", "p:overlay", "a:scan"]
    many = [f"s:{i}" for i in range(9)]
    assert askclaude.parse(_answer("", many), many)[1] == many[:askclaude.MAX_IDS]


def test_a_broken_answer_or_a_refusal_is_an_error_not_a_crash():
    with pytest.raises(askclaude.AskError) as e:
        askclaude.parse({"stop_reason": "end_turn", "content": [{"type": "text", "text": "kein JSON"}]}, [])
    assert e.value.kind == "bad"
    with pytest.raises(askclaude.AskError) as e:
        askclaude.parse({"stop_reason": "refusal", "content": []}, [])
    assert e.value.kind == "refused"


@pytest.mark.parametrize("code,body,kind", [(401, {}, "auth"), (403, {}, "auth"), (429, {}, "rate"),
                                            (400, {"error": {"message": "Your credit balance is too low"}}, "quota"),
                                            (500, {}, "net")])
def test_http_errors_have_a_kind(opener, code, body, kind):
    err = urllib.error.HTTPError(askclaude.ENDPOINT, code, "x", {}, io.BytesIO(json.dumps(body).encode()))
    opener(error=err)
    with pytest.raises(askclaude.AskError) as e:
        askclaude.ask(KEY, "frage", CATALOGUE)
    assert e.value.kind == kind


def test_no_network_is_net(opener):
    opener(error=urllib.error.URLError("offline"))
    with pytest.raises(askclaude.AskError) as e:
        askclaude.ask(KEY, "frage", CATALOGUE)
    assert e.value.kind == "net"


def test_a_key_looks_like_one():
    assert askclaude.valid_key(KEY) and askclaude.valid_key("  " + KEY + " ")
    assert not askclaude.valid_key("") and not askclaude.valid_key("sk-ant-") and not askclaude.valid_key("abc" * 10)


def test_the_asker_thread_posts_answers_and_errors_and_keeps_no_question(opener):
    o = opener(reply=_answer("Hier.", ["a:scan"]))
    got = queue.Queue()
    a = askclaude.Asker(lambda kind, **kw: got.put((kind, kw)))
    a.start()
    a.ask(KEY, "scannen?", CATALOGUE)
    kind, kw = got.get(timeout=10)
    assert kind == "answer" and kw == {"answer": "Hier.", "ids": ["a:scan"], "question": "scannen?"}
    o.error = urllib.error.URLError("offline")
    a.ask(KEY, "nochmal?", CATALOGUE)
    kind, kw = got.get(timeout=10)
    assert kind == "error" and kw["error"] == "net"
    a.stop()
    a.join(timeout=10)
    line = a.diag_line()
    assert "gefragt 2" in line and "nochmal" not in line and KEY not in line
