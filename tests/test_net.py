"""1.33.5 (review S9): one HTTP opener for every web request – redirects only to https, and credentials never follow
a redirect to another host (urllib's own handler copies all headers to the new address)."""
import urllib.error
import urllib.request

import pytest

from fogscout import askclaude, net, relupdate, spotify, ytupload


def _redirect(req, url, code=302):
    return net.SafeRedirect().redirect_request(req, None, code, "Found", {}, url)


def test_a_redirect_to_plain_http_is_refused():
    req = urllib.request.Request("https://api.spotify.com/v1/me/player/queue")
    with pytest.raises(urllib.error.URLError):
        _redirect(req, "http://example.com/x")


def test_the_token_stays_with_its_host_on_a_redirect():
    req = urllib.request.Request("https://api.spotify.com/v1/x", headers={"Authorization": "Bearer secret",
                                                                        "Accept": "application/json"})
    req.add_unredirected_header("Cookie", "a=b")
    same = _redirect(req, "https://api.spotify.com/v1/y")
    assert same.get_header("Authorization") == "Bearer secret"              # the same host keeps it
    other = _redirect(req, "https://evil.example.com/steal")
    assert other.get_header("Authorization") is None and other.get_header("Cookie") is None
    assert other.get_header("Accept") == "application/json"                 # everything else goes along
    key = urllib.request.Request("https://api.anthropic.com/v1/messages", headers={"x-api-key": "sk-ant-x"})
    assert _redirect(key, "https://other.example.com/", code=302).get_header("X-api-key") is None


@pytest.mark.parametrize("mod", [spotify, ytupload, askclaude])
def test_every_web_client_builds_its_opener_from_net(mod, monkeypatch):
    monkeypatch.setattr(mod, "OPENER", None)
    built = mod._opener()
    assert any(isinstance(h, net.SafeRedirect) for h in built.handlers)
    assert not any(type(h) is urllib.request.HTTPRedirectHandler for h in built.handlers)


def test_the_updater_uses_it_too():
    assert any(isinstance(h, net.SafeRedirect) for h in relupdate._opener().handlers)
