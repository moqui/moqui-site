#!/usr/bin/env python3
"""Import HiveMind wiki pages from moqui.org into docs/md and docs/attachment.

Authentication (read-only exporter account) comes from the environment:

    MOQUI_WIKI_USER
    MOQUI_WIKI_PASSWORD

Page lists are public (/m/alldocs/{space}). Source is the server-rendered
EditWikiPage form at /apps/hm/EditWikiPage (not the /qapps Vue shell).
Attachments are listed on /apps/hm/wiki and downloaded from the public
/docs/attachment/{wikiPageId}/{filename} URLs.
"""
from __future__ import annotations

import argparse
import base64
import html as htmlmod
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_MD = ROOT / "docs" / "md"
DOCS_ATT = ROOT / "docs" / "attachment"
MANIFEST_PATH = ROOT / "docs" / "manifest.json"
CACHE_DIR = Path(os.environ.get("MOQUI_WIKI_CACHE", "/tmp/moqui-wiki-import"))

BASE = "https://moqui.org"
UA = "moqui-site-wiki-import/1.0 (+https://github.com/moqui/moqui-site)"

SPACES = [
    {"id": "moqui", "title": "Moqui Community"},
    {"id": "framework", "title": "Moqui Framework"},
    {"id": "mantle", "title": "Mantle Business Artifacts"},
    {"id": "apps", "title": "Moqui Applications"},
]

CODE_PH = "@@MDCODE%d@@"
INLINE_PH = "@@MDINLINE%d@@"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class FetchError(Exception):
    pass


class Session:
    def __init__(self, user: str | None, password: str | None, delay: float):
        self.user = user
        self.password = password
        self.delay = delay
        self.last_request = 0.0
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )

    def get(self, url: str, auth: bool = False, binary: bool = False, retries: int = 4):
        last_err = None
        for attempt in range(retries):
            wait = self.delay - (time.time() - self.last_request)
            if wait > 0:
                time.sleep(wait)
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": "*/*" if binary else "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                },
            )
            if auth:
                if not self.user or not self.password:
                    raise FetchError("MOQUI_WIKI_USER / MOQUI_WIKI_PASSWORD are required")
                token = base64.b64encode(f"{self.user}:{self.password}".encode()).decode()
                req.add_header("Authorization", "Basic " + token)
            try:
                with self.opener.open(req, timeout=60) as resp:
                    data = resp.read()
                    ctype = resp.headers.get("Content-Type", "")
                    self.last_request = time.time()
                    if binary:
                        return data, ctype, resp.status
                    text = data.decode("utf-8", errors="replace")
                    if _looks_like_challenge(text):
                        raise FetchError("Cloudflare challenge page from %s" % url)
                    return text, ctype, resp.status
            except urllib.error.HTTPError as exc:
                self.last_request = time.time()
                body = exc.read() if exc.fp else b""
                if exc.code in (429, 500, 502, 503, 504) and attempt + 1 < retries:
                    time.sleep(1.5 * (attempt + 1))
                    last_err = exc
                    continue
                raise FetchError("HTTP %s for %s: %s" % (exc.code, url, body[:200])) from exc
            except urllib.error.URLError as exc:
                if attempt + 1 < retries:
                    time.sleep(1.5 * (attempt + 1))
                    last_err = exc
                    continue
                raise FetchError("URL error for %s: %s" % (url, exc)) from exc
        raise FetchError("Failed %s: %s" % (url, last_err))


def _looks_like_challenge(text: str) -> bool:
    head = text[:4000].lower()
    return (
        "cf-browser-verification" in head
        or "cdn-cgi/challenge-platform" in head
        or ("just a moment" in head and "cloudflare" in head)
        or "attention required! | cloudflare" in head
    )


# ---------------------------------------------------------------------------
# HTML parsers
# ---------------------------------------------------------------------------

class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(htmlmod.unescape(href))


class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs: dict[str, str] = {}
        self.textareas: dict[str, str] = {}
        self._ta_name: str | None = None
        self._ta_chunks: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "input":
            name = d.get("name")
            if name:
                self.inputs[name] = htmlmod.unescape(d.get("value") or "")
        elif tag == "textarea":
            self._ta_name = d.get("name") or d.get("id")
            self._ta_chunks = []

    def handle_endtag(self, tag):
        if tag == "textarea" and self._ta_name is not None:
            self.textareas[self._ta_name] = "".join(self._ta_chunks)
            self._ta_name = None

    def handle_data(self, data):
        if self._ta_name is not None:
            self._ta_chunks.append(data)


def parse_alldocs(html: str, space: str) -> list[str]:
    """Return pagePath values ('' for the space root), decoded, unique, stable order."""
    p = LinkCollector()
    p.feed(html)
    prefix = "/m/docs/" + space
    seen: set[str] = set()
    out: list[str] = []
    for href in p.hrefs:
        path = urllib.parse.urlparse(href).path.rstrip("/")
        if path == prefix:
            page_path = ""
        elif path.startswith(prefix + "/"):
            rest = path[len(prefix) + 1 :]
            page_path = "/".join(_decode_seg(seg) for seg in rest.split("/") if seg)
        else:
            continue
        if page_path in seen:
            continue
        seen.add(page_path)
        out.append(page_path)
    if "" not in seen:
        out.insert(0, "")
    return out


def _decode_seg(seg: str) -> str:
    try:
        seg = urllib.parse.unquote(seg)
    except Exception:
        pass
    return seg.replace("+", " ")


def parse_edit_html(html: str) -> dict:
    p = FormParser()
    p.feed(html)
    page_text = p.textareas.get("pageText")
    if page_text is None:
        for key, val in p.textareas.items():
            if key and "pageText" in key:
                page_text = val
                break
    if page_text is None:
        page_text = ""
    wiki_type = (p.inputs.get("wikiType") or "").strip().lower()
    if not wiki_type:
        m = re.search(r'id="EditPageForm_wikiType"[^>]*value="([^"]*)"', html)
        if m:
            wiki_type = m.group(1).strip().lower()
    is_create = (p.inputs.get("isCreate") or "").lower() in ("true", "1", "y")
    seq = p.inputs.get("sequenceNum") or "50"
    try:
        sequence_num = int(seq)
    except ValueError:
        sequence_num = 50
    return {
        "pageText": page_text.replace("\r\n", "\n").replace("\r", "\n"),
        "wikiType": wiki_type,
        "pageName": p.inputs.get("pageName") or "",
        "pagePath": p.inputs.get("pagePath") or "",
        "sequenceNum": sequence_num,
        "isCreate": is_create,
    }


def parse_wiki_view(html: str) -> dict:
    wiki_page_id = ""
    m = re.search(r"\bID:\s*(\d+)\b", html)
    if m:
        wiki_page_id = m.group(1)
    if not wiki_page_id:
        m = re.search(r"wikiPageId=(\d+)", html)
        if m:
            wiki_page_id = m.group(1)
    atts = []
    seen = set()
    for m in re.finditer(r"/docs/attachment/([^/]+)/([^\"'?#\s>]+)", html):
        pid, filename = m.group(1), urllib.parse.unquote(m.group(2))
        key = (pid, filename)
        if key in seen:
            continue
        seen.add(key)
        atts.append({"wikiPageId": pid, "filename": filename})
        if not wiki_page_id:
            wiki_page_id = pid
    for m in re.finditer(r"filename=([^&\"']+)", html):
        filename = urllib.parse.unquote(m.group(1))
        if not wiki_page_id:
            continue
        key = (wiki_page_id, filename)
        if key in seen:
            continue
        if filename in ("", "true", "false"):
            continue
        seen.add(key)
        atts.append({"wikiPageId": wiki_page_id, "filename": filename})
    return {"wikiPageId": wiki_page_id, "attachments": atts}


# ---------------------------------------------------------------------------
# Confluence wiki markup -> GFM
# ---------------------------------------------------------------------------

def sniff_wiki_type(text: str, hinted: str) -> str:
    if hinted in ("cwiki", "confluence", "md", "markdown", "html"):
        return "cwiki" if hinted in ("cwiki", "confluence") else ("md" if hinted in ("md", "markdown") else hinted)
    sample = text.lstrip()[:800]
    if re.search(r"^h[1-6]\.\s", sample, re.M) or "{toc" in sample or "{code" in sample:
        return "cwiki"
    return "md"


def _code_lang(params: str | None) -> str:
    if not params:
        return ""
    params = params.strip().rstrip(";")
    m = re.search(r"brush:\s*([A-Za-z0-9_+-]+)", params)
    if m:
        return m.group(1).lower()
    lang = ""
    for part in params.split("|"):
        part = part.strip()
        if part.lower().startswith("language="):
            return part.split("=", 1)[1].strip().lower()
        if "=" not in part and part.lower() not in (
            "collapse",
            "linenumbers",
            "firstline",
            "theme",
            "borderstyle",
            "title",
        ):
            lang = part
    return lang.lower()


def _fence_for(text: str) -> str:
    longest = 0
    cur = 0
    for ch in text:
        if ch == "`":
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0
    n = max(3, longest + 1)
    return "`" * n


def confluence_to_markdown(text: str, space: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks: list[str] = []
    inlines: list[str] = []

    def stash_block(body: str, lang: str = "") -> str:
        fence = _fence_for(body)
        lang = lang or ""
        chunk = fence + lang + "\n" + body.rstrip("\n") + "\n" + fence
        idx = len(blocks)
        blocks.append(chunk)
        return CODE_PH % idx

    def stash_inline(body: str) -> str:
        fence = "`"
        if "`" in body:
            n = max(2, body.count("`") + 1)
            fence = "`" * n
            chunk = fence + " " + body + " " + fence
        else:
            chunk = "`" + body + "`"
        idx = len(inlines)
        inlines.append(chunk)
        return INLINE_PH % idx

    def code_repl(m: re.Match) -> str:
        return stash_block(m.group(2).strip("\n"), _code_lang(m.group(1)))

    # Inline {{monospace}} first so "{{code}}" cannot be parsed as a {code} macro.
    text = re.sub(r"\{\{([^{}]+)\}\}", lambda m: stash_inline(m.group(1)), text)
    text = re.sub(r"\{code(?::([^}]*))?\}(.*?)\{code\}", code_repl, text, flags=re.S)
    text = re.sub(
        r"\{noformat(?::[^}]*)?\}(.*?)\{noformat\}",
        lambda m: stash_block(m.group(1).strip("\n")),
        text,
        flags=re.S,
    )

    def admon_repl(m: re.Match) -> str:
        kind = m.group(1).capitalize()
        inner = m.group(2).strip()
        lines = ["> **%s:**" % kind]
        if inner:
            for line in inner.split("\n"):
                lines.append("> " + line if line else ">")
        return "\n".join(lines)

    for name in ("note", "info", "warning", "tip", "panel"):
        text = re.sub(
            r"\{" + name + r"(?::[^}]*)?\}(.*?)\{" + name + r"\}",
            admon_repl,
            text,
            flags=re.S | re.I,
        )
    text = re.sub(r"\{anchor:[^}]*\}", "", text)
    text = re.sub(r"\{color:[^}]*\}(.*?)\{color\}", r"\1", text, flags=re.S)
    text = re.sub(r"\{(?:section|column)(?::[^}]*)?\}", "", text)
    text = re.sub(r"\{toc(?::[^}]*)?\}", "[TOC]", text)

    def img_repl(m: re.Match) -> str:
        name = m.group(1).strip()
        return "![%s](%s)" % (name, name)

    text = re.sub(r"!([^!|\n]+)(?:\|[^!\n]*)?!", img_repl, text)

    def link_repl(m: re.Match) -> str:
        body = m.group(1)
        if re.match(r"(?i)^TOC(?:\s|$)", body.strip()):
            return m.group(0)
        parts = [p.strip() for p in body.split("|")]
        if len(parts) == 1:
            label, target = parts[0], parts[0]
        else:
            label, target = parts[0], parts[1]
        return "[%s](%s)" % (label, _resolve_href(target, space))

    text = re.sub(r"\[([^\]\n]+)\]", link_repl, text)
    text = _convert_tables(text)
    # Lists before headings: Confluence numbered items are "# item" which would
    # look like Markdown ATX headings if h1. were already converted.
    text = _convert_lists(text)
    text = re.sub(r"^h([1-6])\.\s+(.*)$", lambda m: ("#" * int(m.group(1))) + " " + m.group(2), text, flags=re.M)
    text = re.sub(r"^----+$", "---", text, flags=re.M)
    text = re.sub(r"^bq\.\s+(.*)$", r"> \1", text, flags=re.M)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"**\1**", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+)_(?!\w)", r"*\1*", text)
    text = re.sub(r"\\\\\s*$", "  ", text, flags=re.M)

    for i, chunk in enumerate(inlines):
        text = text.replace(INLINE_PH % i, chunk)
    for i, chunk in enumerate(blocks):
        text = text.replace(CODE_PH % i, chunk)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _convert_tables(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        if not _is_table_line(lines[i]):
            out.append(lines[i])
            i += 1
            continue
        block = []
        while i < len(lines) and _is_table_line(lines[i]):
            block.append(lines[i])
            i += 1
        out.extend(_gfm_table(block))
    return "\n".join(out)


def _is_table_line(line: str) -> bool:
    s = line.lstrip()
    return s.startswith("|") and not s.startswith("|=")


def _split_row(line: str) -> tuple[bool, list[str]]:
    s = line.strip()
    header = s.startswith("||")
    if header:
        if s.startswith("||"):
            s = s[2:]
        if s.endswith("||"):
            s = s[:-2]
        cells = [c.strip() for c in s.split("||")]
    else:
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        cells = [c.strip() for c in s.split("|")]
    return header, cells


def _gfm_table(block: list[str]) -> list[str]:
    rows = []
    any_header = False
    width = 1
    for line in block:
        header, cells = _split_row(line)
        any_header = any_header or header
        width = max(width, len(cells) or 1)
        rows.append((header, cells))
    for idx, (header, cells) in enumerate(rows):
        if len(cells) < width:
            rows[idx] = (header, cells + [""] * (width - len(cells)))
    def fmt(cells: list[str]) -> str:
        return "| " + " | ".join(c.replace("\n", " ") for c in cells) + " |"
    sep = "| " + " | ".join("---" for _ in range(width)) + " |"
    out = []
    if rows and rows[0][0]:
        out.append(fmt(rows[0][1]))
        out.append(sep)
        for header, cells in rows[1:]:
            out.append(fmt(cells))
    elif any_header:
        header_row = next(cells for header, cells in rows if header)
        out.append(fmt(header_row))
        out.append(sep)
        for header, cells in rows:
            if not header:
                out.append(fmt(cells))
    else:
        out.append("| " + " | ".join(" " for _ in range(width)) + " |")
        out.append(sep)
        for _, cells in rows:
            out.append(fmt(cells))
    return out


def _convert_lists(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    list_re = re.compile(r"^([#\*]+)(?:\s+|$)(.*)$")
    for line in lines:
        m = list_re.match(line)
        if not m:
            out.append(line)
            continue
        markers, rest = m.group(1), m.group(2)
        depth = len(markers)
        kind = "ul" if markers[-1] == "*" else "ol"
        indent = "  " * (depth - 1)
        bullet = "- " if kind == "ul" else "1. "
        out.append(indent + bullet + rest)
    return "\n".join(out)


def _resolve_href(target: str, space: str) -> str:
    t = target.strip()
    if not t:
        return t
    if t.startswith("#"):
        return "#" + slugify(t[1:])
    if t.startswith("mailto:"):
        return t
    if re.match(r"^https?://", t, re.I):
        return normalize_moqui_url(t)
    if t.startswith("/"):
        return normalize_moqui_url("https://moqui.org" + t)
    return "/docs/%s/%s" % (space, "/".join(seg.replace(" ", "+") for seg in t.split("/")))


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = s.replace("'", "").replace('"', "")
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "section"


def normalize_moqui_url(url: str) -> str:
    m = re.match(r"^https?://(?:www\.)?moqui\.org(/m)?/docs(/.*)?$", url, re.I)
    if m:
        rest = m.group(2) or ""
        return "/docs" + rest
    m = re.match(r"^https?://(?:www\.)?moqui\.org/m/docs(/.*)?$", url, re.I)
    if m:
        rest = m.group(1) or ""
        return "/docs" + rest
    m = re.match(r"^https?://(?:www\.)?moqui\.org/javadoc(/.*)?$", url, re.I)
    if m:
        rest = m.group(1) or ""
        return "/javadoc" + rest if rest else "/javadoc/"
    if url.startswith("/m/docs"):
        return "/docs" + url[len("/m/docs") :]
    return url


def normalize_markdown(text: str, space: str) -> str:
    def repl_url(m: re.Match) -> str:
        return normalize_moqui_url(m.group(0))

    text = re.sub(r"https?://(?:www\.)?moqui\.org(?:/m)?/docs[^\s)\]>]*", repl_url, text)
    text = re.sub(r"https?://(?:www\.)?moqui\.org/javadoc[^\s)\]>]*", repl_url, text)
    text = text.replace("](/m/docs/", "](/docs/")
    text = re.sub(r"\{toc(?::[^}]*)?\}", "[TOC]", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not text.endswith("\n"):
        text += "\n"
    return text


def leftover_markers(text: str) -> list[str]:
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    body = re.sub(r"`[^`]+`", "", body)
    hits = []
    for label, rx in (
        ("h-heading", r"^h[1-6]\.\s"),
        ("{toc}", r"\{toc\b"),
        ("{code}", r"\{code\b"),
        ("{noformat}", r"\{noformat\b"),
        ("{{monospace}}", r"\{\{"),
    ):
        if re.search(rx, body, re.M):
            hits.append(label)
    return hits


# ---------------------------------------------------------------------------
# Paths / manifest
# ---------------------------------------------------------------------------

def md_path(space: str, page_path: str) -> Path:
    if not page_path:
        return DOCS_MD / space / "index.md"
    return DOCS_MD / space / (page_path + ".md")


def cache_path(space: str, page_path: str) -> Path:
    slug = "_root" if not page_path else page_path.replace("/", "__")
    return CACHE_DIR / space / (slug + ".json")


def parent_path(page_path: str) -> str | None:
    if page_path == "":
        return None
    if "/" not in page_path:
        return ""
    return page_path.rsplit("/", 1)[0]


def tree_order(pages: list[dict]) -> list[dict]:
    by_parent: dict[str | None, list[dict]] = {}
    for p in pages:
        by_parent.setdefault(parent_path(p["path"]), []).append(p)

    def sort_kids(kids: list[dict]) -> list[dict]:
        return sorted(kids, key=lambda x: (x.get("sequenceNum") if x.get("sequenceNum") is not None else 50, (x.get("title") or "").lower()))

    ordered: list[dict] = []

    def walk(parent: str | None):
        for child in sort_kids(by_parent.get(parent, [])):
            ordered.append(child)
            walk(child["path"])

    roots = by_parent.get(None, [])
    for root in sort_kids(roots):
        ordered.append(root)
        walk(root["path"])
    # orphans (missing parents)
    seen = {p["path"] for p in ordered}
    for p in pages:
        if p["path"] not in seen:
            ordered.append(p)
    return ordered


def title_for(space_title: str, page_path: str, page_name: str) -> str:
    if not page_path:
        return space_title
    if page_name:
        return page_name
    return page_path.rsplit("/", 1)[-1]


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

def edit_url(space: str, page_path: str) -> str:
    url = BASE + "/apps/hm/EditWikiPage?wikiSpaceId=" + urllib.parse.quote(space, safe="")
    if page_path:
        url += "&pagePath=" + urllib.parse.quote(page_path, safe="")
    return url


def wiki_view_url(space: str, page_path: str) -> str:
    url = BASE + "/apps/hm/wiki?wikiSpaceId=" + urllib.parse.quote(space, safe="")
    if page_path:
        url += "&pagePath=" + urllib.parse.quote(page_path, safe="")
    return url


def load_or_fetch_page(session: Session, space: str, page_path: str, convert_only: bool) -> dict:
    cpath = cache_path(space, page_path)
    if convert_only or cpath.exists():
        if cpath.exists():
            return json.loads(cpath.read_text(encoding="utf-8"))
        if convert_only:
            raise FetchError("No cache for %s/%s" % (space, page_path or "(root)"))
    edit_html, _, _ = session.get(edit_url(space, page_path), auth=True)
    parsed = parse_edit_html(edit_html)
    if parsed["isCreate"] or not parsed["pageText"]:
        # still try wiki view in case of empty published page
        pass
    view = {"wikiPageId": "", "attachments": []}
    try:
        view_html, _, _ = session.get(wiki_view_url(space, page_path), auth=True)
        view = parse_wiki_view(view_html)
    except FetchError as exc:
        print("  warn wiki view %s/%s: %s" % (space, page_path or "(root)", exc), file=sys.stderr)
    rec = {
        "space": space,
        "path": page_path,
        "pageName": parsed["pageName"] or (page_path.rsplit("/", 1)[-1] if page_path else ""),
        "wikiType": parsed["wikiType"],
        "sequenceNum": parsed["sequenceNum"],
        "pageText": parsed["pageText"],
        "wikiPageId": view.get("wikiPageId") or "",
        "attachments": view.get("attachments") or [],
        "isCreate": parsed["isCreate"],
    }
    cpath.parent.mkdir(parents=True, exist_ok=True)
    cpath.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    return rec


def download_attachment(session: Session, wiki_page_id: str, filename: str) -> Path:
    dest = DOCS_ATT / wiki_page_id / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = BASE + "/docs/attachment/%s/%s" % (
        urllib.parse.quote(wiki_page_id, safe=""),
        urllib.parse.quote(filename, safe=""),
    )
    data, _, _ = session.get(url, auth=False, binary=True)
    dest.write_bytes(data)
    return dest


def rewrite_local_images(md: str, attachments: list[dict], wiki_page_id: str) -> str:
    """Point bare image filenames at /docs/attachment/{id}/{file}."""
    names = {a["filename"]: a.get("wikiPageId") or wiki_page_id for a in attachments}
    if wiki_page_id:
        # also catch markdown images whose url is just the filename
        def repl(m: re.Match) -> str:
            alt, url = m.group(1), m.group(2)
            if url.startswith("/") or re.match(r"^https?://", url):
                return m.group(0)
            pid = names.get(url) or wiki_page_id
            return "![%s](/docs/attachment/%s/%s)" % (alt, pid, url)

        md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, md)
    return md


def convert_record(rec: dict) -> tuple[str, str, list[str]]:
    wiki_type = sniff_wiki_type(rec.get("pageText") or "", rec.get("wikiType") or "")
    raw = rec.get("pageText") or ""
    if wiki_type == "cwiki":
        md = confluence_to_markdown(raw, rec["space"])
    else:
        md = raw
    md = normalize_markdown(md, rec["space"])
    md = rewrite_local_images(md, rec.get("attachments") or [], rec.get("wikiPageId") or "")
    return md, wiki_type, leftover_markers(md)


def write_manifest(pages_by_space: dict[str, list[dict]]) -> None:
    manifest = {"spaces": SPACES, "pages": {}}
    for spec in SPACES:
        sid = spec["id"]
        ordered = tree_order(pages_by_space.get(sid, []))
        manifest["pages"][sid] = [{"path": p["path"], "title": p["title"]} for p in ordered]
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    user = os.environ.get("MOQUI_WIKI_USER") or args.user
    password = os.environ.get("MOQUI_WIKI_PASSWORD") or args.password
    session = Session(user, password, delay=args.delay)
    space_ids = args.spaces or [s["id"] for s in SPACES]
    space_title = {s["id"]: s["title"] for s in SPACES}

    pages_by_space: dict[str, list[dict]] = {sid: [] for sid in space_ids}
    errors: list[str] = []
    leftover_pages: list[str] = []
    type_counts = {"cwiki": 0, "md": 0, "other": 0}
    att_count = 0
    page_count = 0

    for space in space_ids:
        print("== space %s ==" % space)
        listing_html, _, _ = session.get(BASE + "/m/alldocs/" + space, auth=False)
        paths = parse_alldocs(listing_html, space)
        if args.limit:
            paths = paths[: args.limit]
        print("  %d pages" % len(paths))
        for page_path in paths:
            label = "%s/%s" % (space, page_path or "(root)")
            try:
                rec = load_or_fetch_page(session, space, page_path, convert_only=args.convert_only)
            except FetchError as exc:
                errors.append("%s: %s" % (label, exc))
                print("  FAIL fetch %s: %s" % (label, exc), file=sys.stderr)
                continue
            if rec.get("isCreate") and not rec.get("pageText"):
                errors.append("%s: edit screen looked like create (missing page)" % label)
                print("  FAIL missing %s" % label, file=sys.stderr)
                continue
            md, wiki_type, leftover = convert_record(rec)
            type_counts[wiki_type if wiki_type in type_counts else "other"] += 1
            dest = md_path(space, page_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(md, encoding="utf-8")
            page_count += 1
            title = title_for(space_title.get(space, space), page_path, rec.get("pageName") or "")
            pages_by_space[space].append(
                {
                    "path": page_path,
                    "title": title,
                    "sequenceNum": rec.get("sequenceNum", 50),
                }
            )
            for att in rec.get("attachments") or []:
                pid = att.get("wikiPageId") or rec.get("wikiPageId")
                fn = att.get("filename")
                if not pid or not fn:
                    continue
                try:
                    if not args.convert_only or not (DOCS_ATT / pid / fn).exists():
                        download_attachment(session, pid, fn)
                    att_count += 1
                except FetchError as exc:
                    errors.append("%s attachment %s: %s" % (label, fn, exc))
                    print("  FAIL att %s %s: %s" % (label, fn, exc), file=sys.stderr)
            extra = " leftover=%s" % ",".join(leftover) if leftover else ""
            if leftover:
                leftover_pages.append("%s (%s)" % (label, ", ".join(leftover)))
            print("  wrote %s [%s seq=%s]%s" % (dest.relative_to(ROOT), wiki_type, rec.get("sequenceNum"), extra))

    # keep unused spaces in the manifest so the viewer still lists them
    all_pages = {s["id"]: pages_by_space.get(s["id"], []) for s in SPACES}
    if args.spaces:
        # merge with existing manifest for spaces we did not touch
        if MANIFEST_PATH.exists():
            old = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            for spec in SPACES:
                sid = spec["id"]
                if sid not in pages_by_space or not pages_by_space[sid]:
                    old_pages = (old.get("pages") or {}).get(sid) or []
                    all_pages[sid] = [{"path": p["path"], "title": p["title"], "sequenceNum": 50} for p in old_pages]
    write_manifest(all_pages)

    print()
    print("pages=%d attachments=%d cwiki=%d md=%d" % (page_count, att_count, type_counts["cwiki"], type_counts["md"]))
    if leftover_pages:
        print("leftover confluence markers on %d pages:" % len(leftover_pages))
        for line in leftover_pages:
            print("  -", line)
    if errors:
        print("errors (%d):" % len(errors), file=sys.stderr)
        for line in errors:
            print("  -", line, file=sys.stderr)
        return 1
    return 0


def self_test() -> int:
    sample = """h1. Title

{toc}

This is *bold* and {{code}} and [Run and Deploy|https://www.moqui.org/docs/framework/Run+and+Deploy].

h2. Lists

# One
#* nested bullet
# Two

{code:brush: xml;}
<screen/>
{code}

|| A || B ||
| 1 | 2 |
"""
    md = confluence_to_markdown(sample, "framework")
    md = normalize_markdown(md, "framework")
    assert md.startswith("# Title\n"), md[:80]
    assert "[TOC]" in md
    assert "**bold**" in md
    assert "`code`" in md
    assert "](/docs/framework/Run+and+Deploy)" in md
    assert "```xml" in md
    assert "| A | B |" in md
    assert "1. One" in md
    assert "  - nested bullet" in md
    assert leftover_markers(md) == []
    print("self-test ok")
    print(md)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--delay", type=float, default=0.3, help="Seconds between HTTP requests")
    ap.add_argument("--limit", type=int, default=0, help="Max pages per space (0 = all)")
    ap.add_argument("--spaces", nargs="*", help="Subset of space ids")
    ap.add_argument("--convert-only", action="store_true", help="Reuse /tmp cache; do not fetch pages")
    ap.add_argument("--user", default="", help="Override MOQUI_WIKI_USER")
    ap.add_argument("--password", default="", help="Override MOQUI_WIKI_PASSWORD")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
