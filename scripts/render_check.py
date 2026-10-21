#!/usr/bin/env python3
"""Render dist/macro-dot-map.html in a headless browser and check layout.

Usage: python3 scripts/render_check.py [--shots DIR]

Checks (V16):
  - no script errors on load
  - the page never scrolls sideways (phone and desktop)
  - at desktop widths (>= 1240px, side panel visible) the whole map fits
    without its own horizontal scroll, so no column is clipped (lesson L-011)
  - every chain button opens a panel with a script
Needs Playwright with Chromium: pip install playwright && playwright install chromium
Exit 0 = pass, 1 = fail, 2 = Playwright not available.
"""
import argparse, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VIEWS = [("phone-light", 400, "light"), ("phone-dark", 400, "dark"),
         ("tablet-light", 1000, "light"), ("desktop-light", 1300, "light"),
         ("desktop-dark", 1300, "dark"), ("wide-light", 1600, "light")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", help="directory to save screenshots in")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("render_check: Playwright is not installed; do the readability check by hand (REVIEWER.md Step E)")
        return 2
    url = (ROOT / "dist/macro-dot-map.html").resolve().as_uri()
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, width, scheme in VIEWS:
            page = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=scheme)
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(url)
            page.wait_for_timeout(500)
            if errs:
                fails.append(f"{name}: script errors {errs}")
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > width:
                fails.append(f"{name}: page scrolls sideways ({sw}px > {width}px)")
            if width >= 1240:
                ov = page.evaluate("(()=>{const m=document.querySelector('.mapscroll');return m.scrollWidth-m.clientWidth})()")
                if ov > 1:
                    fails.append(f"{name}: map is clipped by {ov}px at desktop width")
            n = page.evaluate("document.querySelectorAll('.chip').length")
            for i in range(n):
                page.click(f".chip >> nth={i}")
                if not page.evaluate("!!document.querySelector('#script') && document.querySelector('#script').textContent.length>100"):
                    fails.append(f"{name}: chain button {i + 1} did not open a script")
            page.click(".chip >> nth=0")
            if a.shots:
                out = pathlib.Path(a.shots)
                out.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out / f"{name}.png"), full_page=True)
            page.close()
        browser.close()
    for f in fails:
        print("FAIL   V16", f)
    print(f"render_check: {len(fails)} failures across {len(VIEWS)} views")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
