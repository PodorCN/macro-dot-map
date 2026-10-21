"""Shared geometry for the Macro Dot Map.

build.py uses it to compute every edge path and sign position, so the page
never computes layout itself. validate.py uses the same functions to check
for collisions, so what is validated is exactly what is drawn.
"""
import math


def node_center(data, nid):
    n = data["nodes"][nid]
    return data["layout"]["columns"][n["layer"]], n["y"]


def node_box(data, nid, pad=0.0):
    L = data["layout"]
    x, y = node_center(data, nid)
    w, h = L["nodeW"], L["nodeH"]
    return (x - w / 2 - pad, y - h / 2 - pad, x + w / 2 + pad, y + h / 2 + pad)


def edge_segments(data, e):
    """Return a list of absolute path segments for edge e."""
    L = data["layout"]
    W, H = L["nodeW"], L["nodeH"]
    ax, ay = node_center(data, e["from"])
    bx, by = node_center(data, e["to"])
    route = e.get("route")
    if route == "feedback":
        g, bot = L["feedback"]["gutterX"], L["feedback"]["bottomY"]
        sx, sy = ax - W / 2, ay + 12
        return [("M", sx, sy), ("L", g + 6, sy), ("Q", g, sy, g, sy + 8),
                ("L", g, bot - 8), ("Q", g, bot, g - 8, bot),
                ("L", bx + 8, bot), ("Q", bx, bot, bx, bot - 8),
                ("L", bx, by + H / 2 + 2)]
    if route == "side":
        x = ax + W / 2
        return [("M", x, ay + 12), ("C", x + 30, ay + 12, x + 30, by - 12, x + 2, by - 12)]
    if ax == bx:
        return [("M", ax, ay + H / 2),
                ("C", ax, ay + H / 2 + 20, bx, by - H / 2 - 20, bx, by - H / 2 - 2)]
    sx, tx = ax + W / 2, bx - W / 2 - 2
    if e.get("via") is not None:
        v = e["via"]
        return [("M", sx, ay), ("C", sx + 16, ay, sx + 16, v, sx + 34, v),
                ("L", tx - 34, v), ("C", tx - 16, v, tx - 16, by, tx, by)]
    m = (sx + tx) / 2
    return [("M", sx, ay), ("C", m, ay, m, by, tx, by)]


def segments_to_d(segs):
    def f(v):
        return ("%.1f" % v).rstrip("0").rstrip(".")
    return " ".join(s[0] + " ".join(f(v) for v in s[1:]) for s in segs)


def sample(segs, per_seg=60):
    pts = []
    cur = None
    for s in segs:
        cmd = s[0]
        if cmd == "M":
            cur = (s[1], s[2]); pts.append(cur); continue
        for i in range(1, per_seg + 1):
            t = i / per_seg
            if cmd == "L":
                p = (cur[0] + (s[1] - cur[0]) * t, cur[1] + (s[2] - cur[1]) * t)
            elif cmd == "Q":
                x1, y1, x, y = s[1:]
                p = ((1 - t) ** 2 * cur[0] + 2 * (1 - t) * t * x1 + t * t * x,
                     (1 - t) ** 2 * cur[1] + 2 * (1 - t) * t * y1 + t * t * y)
            else:  # C
                x1, y1, x2, y2, x, y = s[1:]
                mt = 1 - t
                p = (mt ** 3 * cur[0] + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * x,
                     mt ** 3 * cur[1] + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * y)
            pts.append(p)
        cur = (s[-2], s[-1])
    return pts


def point_at_fraction(segs, frac):
    pts = sample(segs)
    lens = [0.0]
    for a, b in zip(pts, pts[1:]):
        lens.append(lens[-1] + math.dist(a, b))
    target = lens[-1] * frac
    for i in range(1, len(lens)):
        if lens[i] >= target:
            a, b = pts[i - 1], pts[i]
            span = lens[i] - lens[i - 1] or 1
            k = (target - lens[i - 1]) / span
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
    return pts[-1]


def sign_position(data, e):
    frac = e.get("signAt", 0.62 if e.get("route") == "feedback" else 0.5)
    return point_at_fraction(edge_segments(data, e), frac)


def inside(box, p):
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]
