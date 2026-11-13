#!/usr/bin/env python3
"""Render dist/macro-dot-map.html in a headless browser and check layout.

Usage: python3 scripts/render_check.py [--shots DIR]

Checks (V16):
  - no script errors on load
  - the page never scrolls sideways (phone and desktop)
  - at desktop widths (>= 1240px) the whole map fits
    without its own horizontal scroll, so no column is clipped (lesson L-011)
  - every chain button opens a panel with a script
  - headlines, category filters, and related-driver navigation work
Needs Playwright with Chromium: pip install playwright && playwright install chromium
Exit 0 = pass, 1 = fail, 2 = Playwright not available.
"""
import argparse, contextlib, functools, http.server, pathlib, shutil, sys, threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
VIEWS = [("phone-light", 400, "light"), ("phone-dark", 400, "dark"),
         ("tablet-light", 1000, "light"), ("desktop-light", 1300, "light"),
         ("desktop-dark", 1300, "dark"), ("wide-light", 1600, "light")]


@contextlib.contextmanager
def served_page():
    """Serve the exact built artifact locally, including on browsers blocking file URLs."""
    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                          ".html": "text/html; charset=utf-8"}

        def log_message(self, *args):
            pass

    handler = functools.partial(Handler, directory=str(ROOT / "dist"))
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}/macro-dot-map.html"
        finally:
            server.shutdown()
            thread.join()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", help="directory to save screenshots in")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("render_check: Playwright is not installed; do the readability check by hand (REVIEWER.md Step E)")
        return 2
    fails = []
    with served_page() as url, sync_playwright() as p:
        launch_options = {}
        if not pathlib.Path(p.chromium.executable_path).is_file():
            system_browser = shutil.which("chromium") or shutil.which("google-chrome")
            if system_browser:
                launch_options["executable_path"] = system_browser
        browser = p.chromium.launch(**launch_options)
        for name, width, scheme in VIEWS:
            page = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=scheme,
                                    reduced_motion="reduce")
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(url)
            if page.evaluate("document.characterSet") != "UTF-8":
                fails.append(f"{name}: build is not decoded as UTF-8")
            if "·" not in page.locator("#counts").inner_text():
                fails.append(f"{name}: Unicode labels are corrupted")
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > width:
                fails.append(f"{name}: page scrolls sideways ({sw}px > {width}px)")
            if width >= 1240:
                ov = page.evaluate("(()=>{const m=document.querySelector('.mapscroll');return m.scrollWidth-m.clientWidth})()")
                if ov > 1:
                    fails.append(f"{name}: map is clipped by {ov}px at desktop width")
                if page.locator("#map").bounding_box()["width"] < min(1640, width * .9):
                    fails.append(f"{name}: map does not use the full desktop width")
            n = page.evaluate("document.querySelectorAll('.chip').length")
            for i in range(n):
                page.click(f".chip >> nth={i}")
                if not page.evaluate("!!document.querySelector('#script') && document.querySelector('#script').textContent.length>100"):
                    fails.append(f"{name}: chain button {i + 1} did not open a script")
            headlines = page.locator(".news")
            for i in range(headlines.count()):
                headline = headlines.nth(i)
                title = headline.locator(".newsopen").inner_text()
                headline.locator(".newsopen").click()
                if page.locator("#panel h2").inner_text() != title:
                    fails.append(f"{name}: headline {i + 1} did not open")
                if page.locator(".node.on").count() == 0 or page.locator(".edge.on").count() != 0:
                    fails.append(f"{name}: headline {i + 1} incorrectly highlights its drivers")
                page.locator("#panel [data-n]").first.click()
                if not page.locator("#panel [data-h]").count():
                    fails.append(f"{name}: related driver lost its news links")
                else:
                    page.locator("#panel [data-h]").first.click()
                    if not page.locator("#panel .headline-summary").count():
                        fails.append(f"{name}: driver-to-headline navigation failed")
            for button in page.locator("#newsfilters button").all():
                category = button.inner_text()
                button.click()
                visible = page.locator(".news:visible")
                expected = headlines.count() if category == "All" else page.locator(f'.news[data-category="{category}"]').count()
                if visible.count() != expected:
                    fails.append(f"{name}: {category} filter shows the wrong stories")
            if headlines.count():
                page.locator("#newsfilters button").first.click()
            if width < 760:
                page.locator('[data-v="diagram"]').click()
                if not page.locator("#map").is_visible():
                    fails.append(f"{name}: phone diagram did not open")
                if page.evaluate("document.documentElement.scrollWidth") > width:
                    fails.append(f"{name}: phone diagram causes page overflow")
                page.locator('[data-v="list"]').click()
            if errs:
                fails.append(f"{name}: script errors {errs}")
            page.click(".chip >> nth=0")
            page.locator("#back-map").click()
            page.evaluate("scrollTo(0,0)")
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
