#!/usr/bin/env python3
"""Build dist/macro-dot-map.html from data/map.json + src/template.html.

Usage: python3 scripts/build.py
The build embeds precomputed edge paths and sign positions, plus a content
hash that release_check.py compares against the approved review.
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
    print(f"built {out.relative_to(ROOT)}  content_hash={digest}")


if __name__ == "__main__":
    main()
