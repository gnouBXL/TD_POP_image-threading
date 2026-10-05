#!/usr/bin/env python3
"""Fast lookups in the TouchDesigner documentation (docs.derivative.ca).

Pages are fetched as raw wikitext (index.php?title=X&action=raw), which is far
more compact than the HTML, and cached in ~/.cache/td_docs.

    td_doc.py params "GLSL POP"          opType + every parameter (Python name, type, label, menu values)
    td_doc.py summary "Feedback POP"     the long description, wiki markup stripped
    td_doc.py raw "Write a GLSL POP"     raw wikitext (pipe into grep)
    td_doc.py grep "Write a GLSL POP" TDDimension   lines matching a regex, with context
    td_doc.py search "line strip info"   full-text search, page titles
    td_doc.py category POPs              all pages of a category
    td_doc.py methods "POP Class"        members and methods of a Python class page
    td_doc.py index out.md "Category:POPs" | page...   regenerate a reference index
"""

import json
import signal
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

BASE = "https://docs.derivative.ca"
CACHE = os.path.expanduser("~/.cache/td_docs")


def _ctx():
    for path in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"),
                 "/root/.ccr/ca-bundle.crt"):
        if path and os.path.exists(path):
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()


def _get(url):
    # The site rejects the default Python-urllib user agent (HTTP 403).
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"})
    with urllib.request.urlopen(req, context=_ctx(), timeout=30) as r:
        return r.read().decode("utf-8")


def raw(title, follow=True):
    title = title.replace(" ", "_")
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, title.replace("/", "%2F") + ".wiki")
    if os.path.exists(path):
        text = open(path, encoding="utf-8").read()
    else:
        try:
            text = _get(f"{BASE}/index.php?title={urllib.parse.quote(title)}&action=raw")
        except Exception as e:  # 404 = no such page
            raise SystemExit(f"{title}: {e}")
        open(path, "w", encoding="utf-8").write(text)
    m = re.match(r"#REDIRECT \[\[([^\]]+)\]\]", text)
    if follow and m:
        return raw(m.group(1))
    return text


def strip(s):
    s = re.sub(r"<syntaxhighlight[^>]*>", "\n```\n", s)
    s = s.replace("</syntaxhighlight>", "\n```\n")
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", s)
    s = re.sub(r"'''|''|<[^>]+>", "", s)
    return s


def op_type(text):
    m = re.search(r"\|opType=(\S+)", text)
    return m.group(1) if m else "?"


def params(text):
    """[(name, type, label, [(menuName, menuLabel)], summary)]"""
    out = []
    for blk in re.split(r"\{\{Parameter\n", text)[1:]:
        def g(k):
            m = re.search(r"\|" + k + r"=([^|\n]*)", blk)
            return m.group(1).strip() if m else ""
        name = g("parName")
        if not name:
            continue
        items = [(n.strip(), l.strip()) for l, n in
                 re.findall(r"\|itemLabel=([^|\n]*)\n\s*\|itemName=([^|\n]*)", blk) if n.strip()]
        summ = re.search(r"\|parSummary=(.*?)\|parItems", blk, re.S)
        out.append((name, g("parType"), g("parLabel"), items,
                    re.sub(r"\s+", " ", strip(summ.group(1))).strip() if summ else ""))
    return out


def summary(text):
    m = re.search(r"\|long=(.*?)\n\s*\}\}", text, re.S)
    return strip(m.group(1)).strip() if m else strip(text)[:3000]


def first_sentence(text):
    m = re.search(r"\|short=(.*?)\n\s*\|", text, re.S)
    s = (m.group(1) if m else "").strip() or summary(text)
    s = re.sub(r"\s+", " ", strip(s))
    return re.split(r"(?<=\.)\s", s)[0][:300]


def category(name):
    url = (f"{BASE}/api.php?action=query&list=categorymembers&cmlimit=500&format=json"
           f"&cmtitle=Category:{urllib.parse.quote(name)}")
    return [m["title"] for m in json.loads(_get(url))["query"]["categorymembers"]]


def search(q):
    url = f"{BASE}/api.php?action=query&list=search&srlimit=20&format=json&srsearch={urllib.parse.quote(q)}"
    return [r["title"] for r in json.loads(_get(url))["query"]["search"]]


def index_entry(title):
    text = raw(title)
    lines = [f"### {title} — `{op_type(text)}`"]
    s = first_sentence(text)
    if s:
        lines.append(s)
    ps = []
    for name, typ, _, items, _ in params(text):
        menu = typ in ("Menu", "StrMenu") and items and not any(n.startswith(name) for n, _ in items)
        ps.append(f"`{name}({'|'.join(n for n, _ in items)})`" if menu else f"`{name}`")
    if ps:
        lines.append("Params: " + ", ".join(ps))
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    cmd, args = argv[1], argv[2:]
    if cmd == "params":
        text = raw(args[0])
        print("opType:", op_type(text))
        for name, typ, label, items, summ in params(text):
            print(f"{name} [{typ}] {label}" + (f" — {summ}" if summ else ""))
            for n, l in items:
                print(f"    {n}  ({l})")
    elif cmd == "summary":
        print(summary(raw(args[0])))
    elif cmd == "raw":
        print(raw(args[0]))
    elif cmd == "grep":
        lines = raw(args[0]).splitlines()
        rx = re.compile(args[1], re.I)
        for i, line in enumerate(lines):
            if rx.search(line):
                print(f"--- {i}")
                print("\n".join(lines[max(0, i - 3): i + 8]))
    elif cmd == "search":
        print("\n".join(search(" ".join(args))))
    elif cmd == "category":
        print("\n".join(category(args[0])))
    elif cmd == "methods":
        text = raw(args[0])
        for m in re.finditer(r"\|(name|call)=([^\n|]*)", text):
            print(m.group(2).strip())
    elif cmd == "index":
        out, sources = args[0], args[1:]
        titles = []
        for s in sources:
            titles += category(s.split(":", 1)[1]) if s.startswith("Category:") else [s]
        titles = sorted(t for t in titles if not t.startswith("Category:"))
        with open(out, "w", encoding="utf-8") as f:
            for t in titles:
                try:
                    f.write(index_entry(t) + "\n")
                except SystemExit as e:
                    print(e, file=sys.stderr)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet when piped into head
    main(sys.argv)
