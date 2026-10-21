#!/usr/bin/env python3
"""Mechanical checks for the Macro Dot Map.

Usage: python3 scripts/validate.py [--today YYYY-MM-DD]

Exit code 0 = no errors (warnings and lesson flags may still exist).
Exit code 1 = at least one error; the map must not be released.

Every check has an ID (V01...). LESSONS.md refers to these IDs, so when a
past mistake gets an automated guard, the guard is listed here and in the
lesson. Writes build/validate-report.json for release_check.py.
"""
import argparse, collections, datetime as dt, hashlib, json, math, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import mapgeo  # noqa: E402

# ---- readability budget (change only with an approved review that says why) ----
CAPS = {
    "nodes_total": 22, "nodes_per_column": 5, "edges_total": 26, "chains_total": 7,
    "chain_edges_min": 3, "chain_edges_max": 6, "facts_min": 1, "facts_max": 4,
    "label": 19, "tag": 22, "value": 60, "fact": 220, "why": 110, "say": 170,
    "chain_name": 34, "script_words_min": 50, "script_words_max": 140, "topics_max": 5,
}
TTL_DAYS = {"price": 4, "weekly": 8, "monthly": 35, "policy": 50, "event": 60, "structural": 120}
EVENT_RETIRE_DAYS = 90
NODE_KEYS = {"label", "tag", "layer", "y", "kind", "asOf", "value", "facts", "say"}
EDGE_KEYS = {"id", "from", "to", "sign", "why", "src", "basis"}
CHAIN_KEYS = {"key", "name", "edges", "script", "topics"}
BASES = {"sourced", "weak", "unsourced"}
CJK = re.compile(r"[㐀-鿿　-〿＀-￯]")
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)")

errors, warnings, flags = [], [], []


def err(cid, msg):
    errors.append(f"{cid} {msg}")


def warn(cid, msg):
    warnings.append(f"{cid} {msg}")


def numbers(text):
    out = []
    for m in NUM.finditer(text):
        try:
            out.append(float(m.group(1).replace(",", "")))
        except ValueError:
            pass
    return out


def supported(n, pool):
    if 1900 <= n <= 2100 and float(n).is_integer():
        return n in pool
    return any(abs(n - m) <= 0.1 * max(abs(m), 1e-9) for m in pool)


def check_basis(where, basis, src, sources):
    if basis not in BASES:
        err("V05", f"{where}: basis '{basis}' must be one of {sorted(BASES)}")
        return
    tiers = [sources[k]["tier"] for k in src if k in sources]
    if basis == "unsourced" and src:
        err("V05", f"{where}: unsourced items must have an empty src list")
    if basis == "sourced" and not any(t <= 2 for t in tiers):
        err("V05", f"{where}: 'sourced' needs at least one tier-1 or tier-2 source (else use 'weak')")
    if basis == "weak":
        if not tiers:
            err("V05", f"{where}: 'weak' needs at least one source")
        elif any(t <= 2 for t in tiers):
            err("V05", f"{where}: has a tier-1/2 source, so basis should be 'sourced'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=dt.date.today().isoformat())
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.today)
    data = json.loads((ROOT / "data/map.json").read_text(encoding="utf-8"))
    L, N, E, C, S, M = (data[k] for k in ("layout", "nodes", "edges", "chains", "sources", "meta"))

    # V01 schema
    for nid, n in N.items():
        miss = NODE_KEYS - n.keys()
        if miss:
            err("V01", f"node {nid}: missing {sorted(miss)}")
    for e in E:
        miss = EDGE_KEYS - e.keys()
        if miss:
            err("V01", f"edge {e.get('id')}: missing {sorted(miss)}")
    for c in C:
        miss = CHAIN_KEYS - c.keys()
        if miss:
            err("V01", f"chain {c.get('key')}: missing {sorted(miss)}")
    for k, s in S.items():
        if not {"name", "url", "tier"} <= s.keys():
            err("V01", f"source {k}: needs name, url, tier")
        elif s["tier"] not in (1, 2, 3):
            err("V01", f"source {k}: tier must be 1, 2 or 3")
    if errors:
        return finish(data, today)

    # V02 references
    EB = {e["id"]: e for e in E}
    if len(EB) != len(E):
        err("V02", "duplicate edge ids")
    for e in E:
        for end in ("from", "to"):
            if e[end] not in N:
                err("V02", f"edge {e['id']}: unknown node '{e[end]}'")
        if e["sign"] not in ("+", "−"):
            err("V02", f"edge {e['id']}: sign must be '+' or '−' (U+2212)")
        for k in e["src"]:
            if k not in S:
                err("V02", f"edge {e['id']}: unknown source '{k}'")
    for nid, n in N.items():
        if not 0 <= n["layer"] < len(L["columns"]):
            err("V02", f"node {nid}: layer out of range")
        for f in n["facts"]:
            for k in f["src"]:
                if k not in S:
                    err("V02", f"node {nid}: unknown source '{k}'")
    for c in C:
        for eid in c["edges"]:
            if eid not in EB:
                err("V02", f"chain {c['key']}: unknown edge '{eid}'")
    if M.get("defaultChain") not in {c["key"] for c in C}:
        err("V02", "meta.defaultChain is not a chain key")
    if errors:
        return finish(data, today)

    # V03 budget
    if len(N) > CAPS["nodes_total"]:
        err("V03", f"{len(N)} nodes > cap {CAPS['nodes_total']}: retire one before adding")
    per_col = collections.Counter(n["layer"] for n in N.values())
    for col, cnt in per_col.items():
        if cnt > CAPS["nodes_per_column"]:
            err("V03", f"column '{L['layers'][col]}' has {cnt} nodes > {CAPS['nodes_per_column']}")
    if len(E) > CAPS["edges_total"]:
        err("V03", f"{len(E)} edges > cap {CAPS['edges_total']}")
    if len(C) > CAPS["chains_total"]:
        err("V03", f"{len(C)} chains > cap {CAPS['chains_total']}")
    for c in C:
        if not CAPS["chain_edges_min"] <= len(c["edges"]) <= CAPS["chain_edges_max"]:
            err("V03", f"chain {c['key']}: {len(c['edges'])} edges, allowed {CAPS['chain_edges_min']}-{CAPS['chain_edges_max']}")
        if len(c["topics"]) > CAPS["topics_max"]:
            err("V03", f"chain {c['key']}: more than {CAPS['topics_max']} topics")
    for nid, n in N.items():
        if not CAPS["facts_min"] <= len(n["facts"]) <= CAPS["facts_max"]:
            err("V03", f"node {nid}: {len(n['facts'])} facts, allowed {CAPS['facts_min']}-{CAPS['facts_max']}")
    used = {k for n in N.values() for f in n["facts"] for k in f["src"]} | {k for e in E for k in e["src"]}
    for k in S:
        if k not in used:
            warn("V03", f"source {k} is not used; remove it")

    # V04 text lengths
    def ln(where, text, cap):
        if len(text) > cap:
            err("V04", f"{where}: {len(text)} chars > {cap}")
    for nid, n in N.items():
        ln(f"node {nid} label", n["label"], CAPS["label"])
        ln(f"node {nid} tag", n["tag"], CAPS["tag"])
        ln(f"node {nid} value", n["value"], CAPS["value"])
        ln(f"node {nid} say", n["say"], CAPS["say"])
        for i, f in enumerate(n["facts"]):
            ln(f"node {nid} fact {i + 1}", f["text"], CAPS["fact"])
    for e in E:
        ln(f"edge {e['id']} why", e["why"], CAPS["why"])
    for c in C:
        ln(f"chain {c['key']} name", c["name"], CAPS["chain_name"])
        w = len(c["script"].split())
        if not CAPS["script_words_min"] <= w <= CAPS["script_words_max"]:
            err("V04", f"chain {c['key']}: script has {w} words, allowed {CAPS['script_words_min']}-{CAPS['script_words_max']}")

    # V05 sourcing basis
    for nid, n in N.items():
        for i, f in enumerate(n["facts"]):
            check_basis(f"node {nid} fact {i + 1}", f["basis"], f["src"], S)
        if not any(f["basis"] != "unsourced" for f in n["facts"]):
            err("V05", f"node {nid}: needs at least one fact with a source")
    for e in E:
        check_basis(f"edge {e['id']}", e["basis"], e["src"], S)
    urls = collections.Counter(s["url"] for s in S.values())
    for k, s in S.items():
        if not s["url"].startswith("https://"):
            err("V14", f"source {k}: url must start with https://")
        if urls[s["url"]] > 1:
            err("V14", f"source {k}: duplicate url")

    # V06 display text must be English, no internal labels (lesson L-008)
    def texts():
        for nid, n in N.items():
            yield f"node {nid}", " ".join([n["label"], n["tag"], n["value"], n["say"]] + [f["text"] for f in n["facts"]])
        for e in E:
            yield f"edge {e['id']}", e["why"]
        for c in C:
            yield f"chain {c['key']}", " ".join([c["name"], c["script"]] + c["topics"])
    for where, t in texts():
        if CJK.search(t):
            err("V06", f"{where}: contains CJK text; display text is English and reasoning is marked with basis 'unsourced'")

    # V07 freshness
    asof = dt.date.fromisoformat(M["asOf"])
    if asof > today:
        err("V07", f"meta.asOf {asof} is in the future")
    for nid, n in N.items():
        d = dt.date.fromisoformat(n["asOf"])
        if d > asof:
            err("V07", f"node {nid}: asOf {d} is after meta.asOf {asof}")
        ttl = TTL_DAYS.get(n["kind"])
        if ttl is None:
            err("V07", f"node {nid}: kind must be one of {sorted(TTL_DAYS)}")
            continue
        age = (today - d).days
        if age > ttl:
            err("V07", f"node {nid}: {n['kind']} data is {age} days old (TTL {ttl}); refresh it or retire the node")
        if n["kind"] == "event":
            if "eventDate" not in n:
                err("V07", f"node {nid}: event nodes need eventDate")
            else:
                ev_age = (today - dt.date.fromisoformat(n["eventDate"])).days
                if ev_age > EVENT_RETIRE_DAYS and not n.get("keepReason"):
                    err("V07", f"node {nid}: event is {ev_age} days old; retire it or add keepReason")
                elif ev_age > EVENT_RETIRE_DAYS:
                    warn("V07", f"node {nid}: event is {ev_age} days old, kept because: {n['keepReason']}")

    # V08 orphans and chain coverage
    deg = collections.Counter()
    for e in E:
        deg[e["from"]] += 1; deg[e["to"]] += 1
    in_chain = {x for c in C for eid in c["edges"] for x in (EB[eid]["from"], EB[eid]["to"])}
    for nid in N:
        if deg[nid] == 0:
            err("V08", f"node {nid}: has no edges; connect it or remove it")
        elif nid not in in_chain:
            warn("V08", f"node {nid}: not part of any chain")

    # V09 chains are connected stories
    for c in C:
        es = [EB[x] for x in c["edges"]]
        adj = collections.defaultdict(set)
        for e in es:
            adj[e["from"]].add(e["to"]); adj[e["to"]].add(e["from"])
        start = es[0]["from"]; seen = {start}; stack = [start]
        while stack:
            for nx in adj[stack.pop()]:
                if nx not in seen:
                    seen.add(nx); stack.append(nx)
        if seen != set(adj):
            err("V09", f"chain {c['key']}: edges do not form one connected story")
        if N[es[-1]["to"]]["layer"] < 2 and N[es[-1]["from"]]["layer"] < 2:
            warn("V09", f"chain {c['key']}: ends before reaching policy, markets or portfolio")

    # V10 no cycles except explicit feedback edges
    g = collections.defaultdict(list)
    for e in E:
        if e.get("route") != "feedback":
            g[e["from"]].append(e["to"])
    state = {}
    def dfs(u, path):
        state[u] = 1
        for v in g[u]:
            if state.get(v) == 1:
                err("V10", "cycle without route 'feedback': " + " → ".join(path + [v]))
            elif not state.get(v):
                dfs(v, path + [v])
        state[u] = 2
    for u in list(N):
        if not state.get(u):
            dfs(u, [u])
    for e in E:
        if e.get("route") == "feedback" and N[e["to"]]["layer"] >= N[e["from"]]["layer"]:
            err("V10", f"edge {e['id']}: feedback edges must point to an earlier column")

    # V11 geometry
    vw, vh = L["viewBox"]
    boxes = {nid: mapgeo.node_box(data, nid) for nid in N}
    for nid, b in boxes.items():
        if b[0] < 0 or b[1] < L["headerY"] + 10 or b[2] > vw or b[3] > vh:
            err("V11", f"node {nid}: box is outside the drawing area")
    for col in range(len(L["columns"])):
        ys = sorted((N[n]["y"], n) for n in N if N[n]["layer"] == col)
        for (y1, a), (y2, b) in zip(ys, ys[1:]):
            if y2 - y1 < L["nodeH"] + 18:
                err("V11", f"nodes {a} and {b}: less than 18px apart vertically")
    signs = {}
    for e in E:
        segs = mapgeo.edge_segments(data, e)
        own = {e["from"], e["to"]}
        hit = set()
        for p in mapgeo.sample(segs):
            if not (0 <= p[0] <= vw and 0 <= p[1] <= vh):
                err("V11", f"edge {e['id']}: leaves the drawing area"); break
            for nid, b in boxes.items():
                if nid not in own and nid not in hit and mapgeo.inside(mapgeo.node_box(data, nid, 3), p):
                    hit.add(nid)
        for nid in sorted(hit):
            err("V11", f"edge {e['id']}: passes through node '{nid}'; add or adjust 'via', or move a node")
        signs[e["id"]] = mapgeo.sign_position(data, e)
    for eid, p in signs.items():
        for nid in N:
            b = mapgeo.node_box(data, nid, 10)
            if mapgeo.inside(b, p):
                err("V11", f"edge {eid}: its +/− marker overlaps node '{nid}'")
    ids = list(signs)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if math.dist(signs[a], signs[b]) < 20:
                err("V11", f"edges {a} and {b}: +/− markers overlap")
    for nid, n in N.items():  # rough text-fit estimate
        if len(n["label"]) * 7.6 > L["nodeW"] - 20:
            err("V11", f"node {nid}: label likely overflows its box")
        if len(n["tag"]) * 6.4 > L["nodeW"] - 20:
            err("V11", f"node {nid}: tag likely overflows its box")

    # V12 every number in a script is backed by the map's own data
    def pool(node_ids, edge_list):
        out = []
        for nid in node_ids:
            n = N[nid]
            out += numbers(n["value"]) + numbers(n["tag"]) + [x for f in n["facts"] for x in numbers(f["text"])]
        for e in edge_list:
            out += numbers(e["why"])
        return out
    for c in C:
        es = [EB[x] for x in c["edges"]]
        nodes = {x for e in es for x in (e["from"], e["to"])}
        p = pool(nodes, es)
        weak_pool = [x for nid in nodes for f in N[nid]["facts"] if f["basis"] == "weak" for x in numbers(f["text"])]
        for x in numbers(c["script"]):
            if not supported(x, p):
                err("V12", f"chain {c['key']}: script number {x:g} is not in any node or edge on this chain")
            elif supported(x, weak_pool) and not supported(x, [y for y in p if y not in weak_pool]):
                warn("V15", f"chain {c['key']}: script number {x:g} rests only on a 'weak' (verify) source")
    for nid, n in N.items():
        p = pool([nid], [])
        for x in numbers(n["say"]):
            if not supported(x, p):
                err("V12", f"node {nid}: say-line number {x:g} is not in its value or facts")

    # V13 lesson patterns: known risky phrasings need reviewer acknowledgement
    pats = json.loads((ROOT / "reviews/lesson_patterns.json").read_text(encoding="utf-8"))
    for where, t in texts():
        for p in pats:
            if re.search(p["pattern"], t, re.I):
                flags.append({"lesson": p["lesson"], "where": where, "rule": p["rule"]})

    return finish(data, today)


def finish(data, today):
    h = hashlib.sha256()
    for rel in ("data/map.json", "src/template.html"):
        h.update((ROOT / rel).read_bytes())
    report = {"content_hash": h.hexdigest(), "today": today.isoformat(),
              "errors": errors, "warnings": warnings, "lesson_flags": flags}
    out = ROOT / "build/validate-report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    for f in flags:
        print(f"FLAG    {f['lesson']} at {f['where']}: {f['rule']}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings, {len(flags)} lesson flags. content_hash={report['content_hash']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
