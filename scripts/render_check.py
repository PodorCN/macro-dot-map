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
  - every node opens a compact summary, with explicit expand/collapse and sources
  - selection preserves map dimensions, node positions and scroll position
  - floating cards support dragging, keyboard movement and responsive resizing
  - the AI, labour/currency and fiscal/duration paths can be followed
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


def map_snapshot(page):
    return page.evaluate("""() => {
        const canvas = document.getElementById('map-canvas');
        const rect = e => {const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
        return {canvas:rect(canvas),svg:rect(document.getElementById('map')),
            scroll:[canvas.scrollLeft,canvas.scrollTop],
            nodes:[...document.querySelectorAll('#map .node')].map(rect)};
    }""")


def check_map_stable(page, before, name, fails):
    after = map_snapshot(page)
    for key in before:
        def flatten(value):
            return [n for item in value for n in flatten(item)] if isinstance(value, list) else [value]
        if any(abs(a-b) > .5 for a,b in zip(flatten(before[key]), flatten(after[key]))):
            fails.append(f"{name}: details move or resize the map ({key})")


def check_details_layout(page, name, width, fails):
    check_connections(page, name, fails)
    # Read related rectangles in one browser task. A resize handler can move
    # the window between separate Playwright calls; mixed frames are invalid.
    geometry = page.evaluate("""() => {
        const rect=id=>{const r=document.getElementById(id).getBoundingClientRect();
            return {x:r.x,y:r.y,width:r.width,height:r.height}};
        return {canvas:rect('map-canvas'),details:rect('details'),expanded:document.getElementById('details').classList.contains('expanded'),manual:moved,
            close:rect('close-details'),viewport:{width:innerWidth,height:innerHeight}};
    }""")
    canvas, details, viewport = (geometry[k] for k in ("canvas", "details", "viewport"))
    if geometry["expanded"] and page.locator("#toggle-details").get_attribute("aria-expanded") != "true":
        fails.append(f"{name}: expanded details state is not accessible")
    if not geometry["expanded"]:
        if details["width"] > 288.5 or details["height"] > 180.5:
            fails.append(f"{name}: default summary is too large")
        if page.locator("#detail-body").is_visible() or page.locator("#toggle-details").get_attribute("aria-expanded") != "false":
            fails.append(f"{name}: full details open without an explicit request")
        selected = page.locator("#map .node.sel").bounding_box()
        overlap = (max(0, min(details["x"] + details["width"], selected["x"] + selected["width"]) - max(details["x"], selected["x"]))
                   * max(0, min(details["y"] + details["height"], selected["y"] + selected["height"]) - max(details["y"], selected["y"])))
        if overlap > 1 and not geometry["manual"]:
            fails.append(f"{name}: compact summary covers the selected node")
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
    close = geometry["close"]
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
        return {overflow: e.scrollWidth - e.clientWidth, visible:visible || !document.getElementById('details').classList.contains('expanded'),
            signs: [...e.querySelectorAll('.direction')].some(d => /[+−-]/.test(d.textContent))};
    }""")
    if content["overflow"] > 1 or not content["visible"]:
        fails.append(f"{name}: card content clips horizontally or its final source is unreachable")
    if content["signs"]:
        fails.append(f"{name}: details show a +/− connection marker")
    if page.locator("#details").evaluate("e => getComputedStyle(e).position") != "fixed":
        fails.append(f"{name}: details participate in the map layout")
    if width >= 1100:
        if page.locator("#map-canvas").evaluate("e => e.scrollWidth - e.clientWidth") > 1:
            fails.append(f"{name}: desktop map is clipped")
        for box in page.locator("#map .node").all():
            b = box.bounding_box()
            if (b["x"] < canvas["x"] - 1 or b["y"] < canvas["y"] - 1
                    or b["x"] + b["width"] > canvas["x"] + canvas["width"] + 1
                    or b["y"] + b["height"] > canvas["y"] + canvas["height"] + 1):
                fails.append(f"{name}: a desktop node is outside the map canvas")
                break
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
            if page.locator(".colnum").nth(1).text_content() != "02":
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
            if width < 1100:
                scale = page.locator("#map").evaluate("e => e.getScreenCTM().a")
                if scale < .9:
                    fails.append(f"{name}: expanded diagram shrinks compact-screen text instead of panning")
            closed_canvas = page.locator("#map-canvas").bounding_box()
            ids = page.evaluate("Object.keys(DATA.nodes)")
            if page.locator("#map .node").count() != len(ids):
                fails.append(f"{name}: a driver is missing from the diagram")
            for node_id in ids:
                expected = page.evaluate("id => DATA.nodes[id].label", node_id)
                node = page.locator(f'#map [data-node="{node_id}"]')
                node.scroll_into_view_if_needed()
                before = map_snapshot(page)
                node.click()
                check_map_stable(page, before, name, fails)
                if not page.locator("#details").is_visible() or page.locator("#detail-title").inner_text() != expected:
                    fails.append(f"{name}: {expected} did not open its details")
                if not page.locator("#panel .src a").count():
                    fails.append(f"{name}: {expected} has no traceable sources")
                check_details_layout(page, name, width, fails)
                page.locator("#toggle-details").click()
                check_map_stable(page, before, name, fails)
                if not page.locator("#detail-body").is_visible():
                    fails.append(f"{name}: full details are not reachable")
                check_details_layout(page, name, width, fails)
                page.locator("#toggle-details").click()
                check_map_stable(page, before, name, fails)
                check_details_layout(page, name, width, fails)
                expected_edges = page.evaluate("id => DATA.edges.filter(e=>e.from===id||e.to===id).length", node_id)
                if page.locator(".edge.on").count() != expected_edges:
                    fails.append(f"{name}: {expected} highlights the wrong connections")
                page.locator("#close-details").click()
                page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
                check_map_stable(page, before, name, fails)
            for start, targets in (("nvidia", ("overcap", "semis", "breadth")),
                                   ("issuance", ("overcap",)),
                                   ("jobs", ("wages", "fed", "front", "usd", "fx")),
                                   ("auction", ("supply", "term", "treasuries", "duration"))):
                page.locator(f'#map [data-node="{start}"]').click()
                page.locator("#toggle-details").click()
                before = map_snapshot(page)
                for target in targets:
                    page.locator(f'#panel [data-node-link="{target}"]').click()
                    expected = page.evaluate("id => DATA.nodes[id].label", target)
                    check_map_stable(page, before, name, fails)
                    if page.locator("#detail-title").inner_text() != expected:
                        fails.append(f"{name}: map connection to {target} failed")
                page.keyboard.press("Escape")
                page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
            page.locator('#map [data-node="nvidia"]').focus()
            page.keyboard.press("Enter")
            if page.locator("#detail-title").inner_text() != "NVIDIA CEO resigns":
                fails.append(f"{name}: keyboard node activation failed")
            page.keyboard.press("Escape")
            page.wait_for_function("document.getElementById('details').hidden && !document.querySelector('.node.sel')")
            page.locator('#map [data-node="nvidia"]').click()
            page.locator("#toggle-details").click()
            # The requested floating window may cover some nodes; uncovered
            # nodes must stay directly selectable without a backdrop or reflow.
            target = page.evaluate("""() => [...document.querySelectorAll('#map .node')].find(n => {
                const r=n.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2;
                return n.dataset.node!=='nvidia' && r.left>=0 && r.right<=innerWidth
                    && r.top>=0 && r.bottom<=innerHeight
                    && document.elementFromPoint(x,y)?.closest('[data-node]')===n;
            })?.dataset.node""")
            if not target:
                fails.append(f"{name}: no uncovered map card remains selectable")
            else:
                before_switch = map_snapshot(page)
                page.locator(f'#map [data-node="{target}"]').click()
                if page.locator("#details.expanded").count():
                    fails.append(f"{name}: a new map selection does not return to compact mode")
                expected = page.evaluate("id => DATA.nodes[id].label", target)
                if page.locator("#detail-title").inner_text() != expected:
                    fails.append(f"{name}: selecting an uncovered map card did not update details")
                check_map_stable(page, before_switch, name, fails)
            check_details_layout(page, name, width, fails)
            if a.shots:
                out = pathlib.Path(a.shots)
                out.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out / f"{name}-details.png"), full_page=True)
            before_expand = map_snapshot(page)
            page.locator("#toggle-details").click()
            check_details_layout(page, name, width, fails)
            check_map_stable(page, before_expand, name, fails)
            if a.shots:
                page.screenshot(path=str(out / f"{name}-expanded.png"), full_page=True)
            page.locator("#toggle-details").click()
            check_map_stable(page, before_expand, name, fails)
            # Pointer and keyboard movement affect only the floating card.
            before_drag = map_snapshot(page)
            handle = page.locator("#move-details")
            card_before = page.locator("#details").bounding_box()
            handle.focus()
            key = (("ArrowUp" if card_before["y"] > 60 else "ArrowDown") if width < 760
                   else ("ArrowLeft" if card_before["x"] > 60 else "ArrowRight"))
            page.keyboard.press(key)
            card_after = page.locator("#details").bounding_box()
            if abs(card_before["x"] - card_after["x"]) + abs(card_before["y"] - card_after["y"]) < 10:
                fails.append(f"{name}: keyboard movement of details failed")
            h = handle.bounding_box()
            start = (h["x"]+h["width"]/2, h["y"]+h["height"]/2)
            dy = 35 if card_after["y"] < 100 else -35
            page.mouse.move(*start)
            page.mouse.down()
            page.mouse.move(start[0], start[1]+dy, steps=5)
            page.mouse.up()
            dragged = page.locator("#details").bounding_box()
            if abs(dragged["y"] - card_after["y"]) < 10:
                fails.append(f"{name}: dragging details failed")
            check_map_stable(page, before_drag, name, fails)
            check_details_layout(page, name, width, fails)
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
            page.mouse.move(0, 0)
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
            # Check the browser's rendered resize state after its event and
            # placement callback, rather than an intermediate layout frame.
            page.evaluate("() => new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)))")
            check_details_layout(page, f"resize-{width}", width, fails)
            if page.locator("#detail-title").inner_text() != "NVIDIA CEO resigns":
                fails.append(f"resize-{width}: selection was lost during resize")
            before_close = map_snapshot(page)
            page.keyboard.press("Escape")
            check_map_stable(page, before_close, f"resize-{width}", fails)
            page.evaluate("openNode('nvidia')")
            check_map_stable(page, before_close, f"resize-{width}", fails)
            page.locator("#toggle-details").click()
            check_details_layout(page, f"resize-{width}-expanded", width, fails)
            check_map_stable(page, before_close, f"resize-{width}-expanded", fails)
            page.locator("#toggle-details").click()
            check_map_stable(page, before_close, f"resize-{width}-collapsed", fails)
        page.close()
        browser.close()
    for f in fails:
        print("FAIL   V16", f)
    print(f"render_check: {len(fails)} failures across {len(VIEWS)} views")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
