#!/usr/bin/env python3
"""Release gate. Publishing is allowed only if this exits 0.

Usage: python3 scripts/release_check.py [--today YYYY-MM-DD]

Checks, in order:
  R1 validate.py reports 0 errors for today's date.
  R2 dist/macro-dot-map.html was built from the current data and template.
  R3 a review record in reviews/records/ has verdict PASS for this exact content hash.
  R4 that review lists every lesson ID in reviews/LESSONS.md under lessons_checked.
  R5 that review acknowledges every lesson flag raised by validate.py.
  R6 no later review for the same hash says FAIL.
  R7 render_check.py passes (or, if Playwright is unavailable, the review
     record says render_check: manual).
"""
import argparse, datetime as dt, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            fm[k.strip()] = v
    return fm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args()
    fails = []

    r = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), "--today", a.today], capture_output=True, text=True)
    report = json.loads((ROOT / "build/validate-report.json").read_text(encoding="utf-8"))
    h = report["content_hash"]
    if r.returncode != 0 or report["errors"]:
        fails.append(f"R1 validator has {len(report['errors'])} errors")

    dist = ROOT / "dist/macro-dot-map.html"
    if not dist.exists() or f'content="{h}"' not in dist.read_text(encoding="utf-8"):
        fails.append("R2 dist/macro-dot-map.html is missing or stale; run scripts/build.py")

    lesson_ids = re.findall(r"^### (L-\d{3})", (ROOT / "reviews/LESSONS.md").read_text(encoding="utf-8"), re.M)
    records = sorted((ROOT / "reviews/records").glob("*.md"))
    matching = [(p, fm) for p in records if (fm := front_matter(p)) and fm.get("content_hash") == h]
    if not matching:
        fails.append(f"R3 no review record for content_hash {h}")
    else:
        p, fm = matching[-1]
        if fm.get("verdict") != "PASS":
            fails.append(f"R3/R6 latest review for this hash ({p.name}) is {fm.get('verdict')}")
        checked = set(fm.get("lessons_checked") or [])
        missing = [x for x in lesson_ids if x not in checked]
        if missing:
            fails.append(f"R4 {p.name} did not check lessons {missing}")
        ack = set(fm.get("lessons_acknowledged") or [])
        flagged = sorted({f["lesson"] for f in report["lesson_flags"]})
        unack = [x for x in flagged if x not in ack]
        if unack:
            fails.append(f"R5 {p.name} did not acknowledge lesson flags {unack}")

    rc = subprocess.run([sys.executable, str(ROOT / "scripts/render_check.py")], capture_output=True, text=True)
    if rc.returncode == 1:
        fails.append("R7 render_check.py failed:\n" + rc.stdout.strip())
    elif rc.returncode == 2:
        if not (matching and matching[-1][1].get("render_check") == "manual"):
            fails.append("R7 Playwright unavailable and the review record does not say render_check: manual")

    if fails:
        print("RELEASE BLOCKED")
        for f in fails:
            print("  -", f)
        return 1
    print(f"RELEASE OK  content_hash={h}  review={matching[-1][0].name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
