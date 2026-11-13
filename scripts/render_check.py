#!/usr/bin/env python3
"""Render dist/macro-dot-map.html in a headless browser and check layout.

Usage: python3 scripts/render_check.py [--shots DIR]

Checks (V16):
  - no script errors on load
  - the page never scrolls sideways (phone and desktop)
  - at desktop widths (>= 1240px) the whole map fits
    without its own horizontal scroll, so no column is clipped (lesson L-011)
  - the initial page contains only the unfiltered map
  - every connection remains solid without arrows or sign markers in every state
  - every node opens a floating details card with reachable sources and close/Escape
  - desktop selection keeps all five map columns visible and other cards clickable
  - compact layouts reserve space below the map and survive viewport resizing
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



def check_connections(page, name, fails):
    issues = page.locator("#map").evaluate("""svg => {
        const edges = [...svg.querySelectorAll('.edge')];
        return {
            count: edges.length === DATA.edges.length,
            markers: !!svg.querySelector('marker, .sign, [marker-start], [marker-mid], [marker-end]'),
            solid: edges.every(e => {
                const s = getComputedStyle(e);
                return s.strokeDasharray === 'none' && s.markerStart === 'none'
                    && s.markerMid === 'none' && s.markerEnd === 'none';
            })
        };
    }""")
    if not issues["count"] or issues["markers"] or not issues["solid"]:
        fails.append(f"{name}: connections are missing or include dashes, arrows or sign markers")


def check_details_layout(page, name, width, fails):
    check_connections(page, name, fails)
    canvas = page.locator("#map-canvas").bounding_box()
    details = page.locator("#details").bounding_box()
    viewport = page.viewport_size
    if (details["x"] < 1 or details["y"] < 1
            or details["x"] + details["width"] > viewport["width"] - 1
            or details["y"] + details["height"] > viewport["height"] - 1):
        fails.append(f"{name}: floating details card lacks outer spacing or leaves the viewport")
    appearance = page.locator("#details").evaluate("""e => {
        const s = getComputedStyle(e);
        return parseFloat(s.borderTopLeftRadius) >= 12 && s.boxShadow !== 'none';
    }""")
    if not appearance:
        fails.append(f"{name}: details card has lost its rounded corners or shadow")
    close = page.locator("#close-details").bounding_box()
    if (close["x"] < details["x"] or close["y"] < details["y"]
            or close["x"] + close["width"] > details["x"] + details["width"]
            or close["y"] + close["height"] > details["y"] + details["height"]):
        fails.append(f"{name}: close button is outside the floating details card")
    content = page.locator("#panel").evaluate("""e => {
        const before = e.scrollTop;
        e.scrollTop = e.scrollHeight;
        const panel = e.getBoundingClientRect();
        const links = e.querySelectorAll('.src a');
        const last = links.length ? links[links.length - 1].getBoundingClientRect() : null;
        const visible = !!last && last.top >= panel.top - 1 && last.bottom <= panel.bottom + 1;
        e.scrollTop = before;
        return {overflow: e.scrollWidth - e.clientWidth, visible,
            signs: [...e.querySelectorAll('.direction')].some(d => /[+−-]/.test(d.textContent))};
    }""")
    if content["overflow"] > 1 or not content["visible"]:
        fails.append(f"{name}: card content clips horizontally or its final source is unreachable")
    if content["signs"]:
        fails.append(f"{name}: details show a +/− connection marker")
    if width >= 1100:
        if canvas["x"] + canvas["width"] > details["x"] + 1:
            fails.append(f"{name}: right details pane overlaps the map")
        if page.locator("#map-canvas").evaluate("e => e.scrollWidth - e.clientWidth") > 1:
            fails.append(f"{name}: opening details clips the desktop map")
        for box in page.locator("#map .node").all():
            b = box.bounding_box()
            if (b["x"] < canvas["x"] - 1 or b["y"] < canvas["y"] - 1
                    or b["x"] + b["width"] > canvas["x"] + canvas["width"] + 1
                    or b["y"] + b["height"] > canvas["y"] + canvas["height"] + 1):
                fails.append(f"{name}: a map card is outside the visible canvas with details open")
                break
    elif canvas["y"] + canvas["height"] > details["y"] + 1:
        fails.append(f"{name}: compact details pane overlaps the map")
    if page.locator(".dim").count():
        fails.append(f"{name}: opening details dims the overview")
    if page.locator('dialog, [aria-modal="true"]').count():
        fails.append(f"{name}: details use a modal overlay")


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
            if page.locator("main > :not(svg)").count() or page.locator("#details").is_visible():
                fails.append(f"{name}: the initial page is not map-only")
            if page.locator(".dim, .node.sel").count():
                fails.append(f"{name}: initial map hides drivers behind a selection")
            check_connections(page, name, fails)
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
            closed_canvas = page.locator("#map-canvas").bounding_box()
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
                check_details_layout(page, name, width, fails)
                expected_edges = page.evaluate("id => DATA.edges.filter(e=>e.from===id||e.to===id).length", node_id)
                if page.locator(".edge.on").count() != expected_edges:
                    fails.append(f"{name}: {expected} highlights the wrong connections")
                page.locator("#close-details").click()
                page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
            for start, targets in (("nvidia", ("overcap", "semis", "breadth")),
                                   ("issuance", ("overcap",))):
                page.locator(f'#map [data-node="{start}"]').click()
                for target in targets:
                    page.locator(f'#panel [data-node-link="{target}"]').click()
                    expected = page.evaluate("id => DATA.nodes[id].label", target)
                    if page.locator("#detail-title").inner_text() != expected:
                        fails.append(f"{name}: consolidated AI link to {target} failed")
                page.keyboard.press("Escape")
                page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
            page.locator('#map [data-node="nvidia"]').focus()
            page.keyboard.press("Enter")
            if page.locator("#detail-title").inner_text() != "NVIDIA CEO resigns":
                fails.append(f"{name}: keyboard node activation failed")
            page.keyboard.press("Escape")
            page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
            page.locator('#map [data-node="nvidia"]').click()
            # A second card must be selectable directly while details remain open.
            page.locator('#map [data-node="coreweave"]').click()
            if page.locator("#detail-title").inner_text() != "CoreWeave earnings":
                fails.append(f"{name}: selecting another map card did not update the pane")
            check_details_layout(page, name, width, fails)
            if a.shots:
                out = pathlib.Path(a.shots)
                out.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out / f"{name}-details.png"), full_page=True)
            page.locator("#close-details").click()
            page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
            restored = page.locator("#map-canvas").bounding_box()
            if abs(restored["width"] - closed_canvas["width"]) > 1 or abs(restored["height"] - closed_canvas["height"]) > 1:
                fails.append(f"{name}: closing details did not restore the full map area")
            if page.locator('[data-node="leadership"]').count():
                fails.append(f"{name}: the merged leadership node is still rendered")
            check_connections(page, name, fails)
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
        page = browser.new_page(viewport={"width": 1300, "height": 900}, reduced_motion="reduce")
        page.goto(url)
        page.locator('#map [data-node="nvidia"]').click()
        for width in (1000, 400, 1100, 1300):
            page.set_viewport_size({"width": width, "height": 900})
            check_details_layout(page, f"resize-{width}", width, fails)
            if page.locator("#detail-title").inner_text() != "NVIDIA CEO resigns":
                fails.append(f"resize-{width}: selection was lost during resize")
        page.close()
        browser.close()
    for f in fails:
        print("FAIL   V16", f)
    print(f"render_check: {len(fails)} failures across {len(VIEWS)} views")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
