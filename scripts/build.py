#!/usr/bin/env python3
"""Build dist/macro-dot-map.html from data/map.json + src/template.html.

Usage: python3 scripts/build.py
The build embeds precomputed edge paths and sign positions, plus a content
hash that release_check.py compares against the approved review.
It also writes index.html: the same page wrapped in a full HTML document,
served by GitHub Pages at https://podor.org/macro-dot-map/.
"""
import hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import mapgeo  # noqa: E402


def content_hash():
    h = hashlib.sha256()
    for rel in ("data/map.json", "src/template.html"):
        h.update((ROOT / rel).read_bytes())
    return h.hexdigest()


def main():
    data = json.loads((ROOT / "data/map.json").read_text(encoding="utf-8"))
    for e in data["edges"]:
        segs = mapgeo.edge_segments(data, e)
        e["d"] = mapgeo.segments_to_d(segs)
        x, y = mapgeo.sign_position(data, e)
        e["sx"], e["sy"] = round(x, 1), round(y, 1)
    digest = content_hash()
    data["meta"]["contentHash"] = digest
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
    if "/*__DATA__*/null" not in tpl:
        sys.exit("template is missing the /*__DATA__*/null placeholder")
    html = tpl.replace("/*__DATA__*/null", payload).replace("__CONTENT_HASH__", digest)
    out = ROOT / "dist/macro-dot-map.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    head, sep, body = html.partition("</style>")
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f"{head}{sep}\n</head>\n<body>{body}</body>\n</html>\n")
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"built {out.relative_to(ROOT)} and index.html  content_hash={digest}")


if __name__ == "__main__":
    main()
