#!/usr/bin/env python3
"""Render dist/macro-dot-map.html in a headless browser and check layout.

Usage: python3 scripts/render_check.py [--shots DIR]

Checks (V16):
  - no script errors on load
  - the page never scrolls sideways (phone and desktop)
  - at desktop widths (>= 1240px) the whole map fits
    without its own horizontal scroll, so no column is clipped (lesson L-011)
  - the initial page contains only the unfiltered map
  - every node opens sourced details and closes by button/Escape
  - the consolidated AI path can be followed in the map details
  - compact screens can pan the readable diagram without page overflow
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
            if "02  " not in page.locator(".colhead").nth(1).text_content():
                fails.append(f"{name}: column labels did not render correctly")
            if page.locator("header, footer, #chains, #inspector, .legend, .stack, #headlines-sec").count():
                fails.append(f"{name}: page contains UI outside the map")
            if page.locator("main > :not(svg)").count() or page.locator("dialog").is_visible():
                fails.append(f"{name}: the initial page is not map-only")
            if page.locator(".dim, .node.sel").count():
                fails.append(f"{name}: initial map hides drivers behind a selection")
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > width:
                fails.append(f"{name}: page scrolls sideways ({sw}px > {width}px)")
            if width >= 1240:
                overflow = page.locator("#map-canvas").evaluate("e => e.scrollWidth - e.clientWidth")
                if overflow > 1:
                    fails.append(f"{name}: map is clipped by {overflow}px at desktop width")
            elif width < 760:
                moved = page.locator("#map-canvas").evaluate("e => {e.scrollLeft=e.scrollWidth;return e.scrollLeft}")
                if moved <= 0:
                    fails.append(f"{name}: readable mobile map cannot pan to later columns")
                page.locator("#map-canvas").evaluate("e => e.scrollLeft=0")
            ids = page.evaluate("Object.keys(DATA.nodes)")
            if page.locator("#map .node").count() != len(ids):
                fails.append(f"{name}: a driver is missing from the diagram")
            for node_id in ids:
                expected = page.evaluate("id => DATA.nodes[id].label", node_id)
                node = page.locator(f'#map [data-node="{node_id}"]')
                node.click()
                if not page.locator("#details").is_visible() or page.locator("#detail-title").inner_text() != expected:
                    fails.append(f"{name}: {expected} did not open its details")
                if not page.locator("#panel .src a").count():
                    fails.append(f"{name}: {expected} has no traceable sources")
                expected_edges = page.evaluate("id => DATA.edges.filter(e=>e.from===id||e.to===id).length", node_id)
                if page.locator(".edge.on").count() != expected_edges:
                    fails.append(f"{name}: {expected} highlights the wrong connections")
                page.locator("#close-details").click()
                page.wait_for_function("!document.querySelector('dialog').open && !document.querySelector('.node.sel')")
            for start, targets in (("nvidia", ("overcap", "semis", "breadth")),
                                   ("issuance", ("overcap",))):
                page.locator(f'#map [data-node="{start}"]').click()
                for target in targets:
                    page.locator(f'#panel [data-node-link="{target}"]').click()
                    expected = page.evaluate("id => DATA.nodes[id].label", target)
                    if page.locator("#detail-title").inner_text() != expected:
                        fails.append(f"{name}: consolidated AI link to {target} failed")
                page.keyboard.press("Escape")
                page.wait_for_function("!document.querySelector('dialog').open && !document.querySelector('.node.sel')")
            page.locator('#map [data-node="nvidia"]').focus()
            page.keyboard.press("Enter")
            if page.locator("#detail-title").inner_text() != "NVIDIA CEO resigns":
                fails.append(f"{name}: keyboard node activation failed")
            page.keyboard.press("Escape")
            page.wait_for_function("!document.querySelector('dialog').open && !document.querySelector('.node.sel')")
            page.locator('#map [data-node="nvidia"]').click()
            page.mouse.click(1, 1)
            page.wait_for_function("!document.querySelector('dialog').open && !document.querySelector('.node.sel')")
            if page.locator('[data-node="leadership"]').count():
                fails.append(f"{name}: the merged leadership node is still rendered")
            if page.evaluate("document.documentElement.scrollWidth") > width:
                fails.append(f"{name}: map navigation causes page overflow")
            if errs:
                fails.append(f"{name}: script errors {errs}")
            page.locator("#map-canvas").evaluate("e => {e.scrollLeft=0;e.scrollTop=0}")
            page.evaluate("document.activeElement.blur()")
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
