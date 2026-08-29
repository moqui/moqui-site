#!/usr/bin/env python3
"""Local preview server with GitHub Pages-style 404.html fallback.

Missing extensionless paths (and .html) are served from /404.html so
/docs/framework and similar documentation URLs work the same way they
will on GitHub Pages. Real files such as .md, .json, and images still
404 if they are absent.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import posixpath
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        rel = posixpath.normpath(urllib.parse.unquote(parsed.path)).lstrip("/")
        full = os.path.join(ROOT, rel)
        if os.path.isdir(full):
            index = os.path.join(full, "index.html")
            if os.path.isfile(index):
                return SimpleHTTPRequestHandler.do_GET(self)
        if os.path.isfile(full):
            return SimpleHTTPRequestHandler.do_GET(self)
        ext = os.path.splitext(rel)[1]
        if ext in ("", ".html"):
            qs = parsed.query
            self.path = "/404.html" + (("?" + qs) if qs else "")
        return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print("Serving %s at http://127.0.0.1:%s/" % (ROOT, port))
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
