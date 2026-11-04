"""1.33.5 (review S9): the one HTTP opener of the program – standard library only (spotify.py, ytupload.py,
askclaude.py and relupdate.py use it; each keeps its own ``OPENER`` the tests replace).

Redirects are followed only to https (1.33.1 audit M-2, until now only for updates), and a redirect to another host
never carries the request's ``Authorization``/``Cookie`` along – urllib's own handler copies every header of the
request to the new address, so a token for Spotify, Google or Anthropic would go wherever a redirect pointed."""
from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request

SECRET_HEADERS = ("authorization", "cookie", "x-api-key", "proxy-authorization")


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    """https only; credentials stay with the host they were meant for."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not str(newurl).lower().startswith("https://"):
            raise urllib.error.URLError(f"Weiterleitung ohne HTTPS abgelehnt: {newurl}")
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and _host(newurl) != _host(req.full_url):
            for name in list(new.headers):
                if name.lower() in SECRET_HEADERS:
                    del new.headers[name]
            for name in list(new.unredirected_hdrs):
                if name.lower() in SECRET_HEADERS:
                    del new.unredirected_hdrs[name]
        return new


def _host(url: str) -> str:
    return (urllib.parse.urlsplit(str(url)).hostname or "").lower()


def opener():
    """A new opener: system proxy as every urllib call, redirects through ``SafeRedirect``."""
    return urllib.request.build_opener(SafeRedirect)
