# AGENT.md — Updating the Macro Dot Map

You are the **updater**. Your job is to keep the Macro Dot Map current every trading day while keeping it as clean, small and rigorous as it is now. A separate **reviewer** (see `REVIEWER.md`) must approve your work before anything is released.

The map is an interview-prep tool for a buy-side multi-asset analyst. A reader should be able to follow the diagram and explain how today's market stories connect, with dated facts and sources available by clicking each node. **Readability is a feature.**

**User preference, 2026-11-13:** Actively add new market-moving headlines **to the macro map itself** as nodes with meaningful transmission links, and remove old headlines when their relevance fades or a newer event supersedes them. Do not create a separate headline section, news feed or card list. Treat this as ongoing curation: proactively look for additions and retirements on every update without waiting for the user to name each event. Keep the map large and readable; use the evidence, connection and budget rules below to choose what earns a place.

**Whole-map review, on every update:** Reassess the entire graph, including unchanged nodes, edges and chains. Look for shared mechanisms, missing connections and opportunities to merge overlapping nodes or stories. Do not keep appending isolated boxes. Record what was merged, reconnected, retired or deliberately kept separate, and why. The user specifically asked for this after finding three disconnected AI transmission boxes in column 02.

**Coverage preference, 2026-11-13:** The user asked for more content in every column. Broaden the map beyond AI and oil with connected macro drivers, transmission stages, rates, asset outcomes and portfolio effects. The reviewed expansion budget is 32 nodes, at most 7 per column, 40 connections and 8 internal chains. New material still needs dated evidence and a defensible role in a complete path; related observations should move into their own useful stages instead of being duplicated. Keep all-solid connections and a floating details window that never reflows the map. Increase the drawing's height when needed and preserve readable compact-screen panning; never add cards by shrinking their text.

**Presentation preference, revised 2026-11-13:** The user requested a full visual redesign, clearer redrawn connections, and details that do not affect the overall layout. Keep a map-only canvas with all drivers and links visible initially; integrated map labels/date are allowed, while separate news sections, chain pickers and page chrome stay absent. Use readable themed cards and routed, rounded orthogonal connections. Every connection stays solid with no arrowhead or +/− marker. Colours group related mechanisms, not evidence strength or a positive/negative investment view; details retain source/basis and direction in words.

**Details must never reflow the map.** The user confirmed that the full details window obscured the map. Default every map-card click to a compact summary (at most 288px wide and 180px high) containing the title and core value. A visible “Read details” button explicitly expands facts, dates, mechanisms and sources; “Collapse” returns to the small summary. Map clicks return to compact mode, while links followed inside full details can stay expanded. Do not remove any source or qualification from the expanded view.

Use a fixed, draggable non-modal window outside canvas layout. Opening, expanding, collapsing, switching, moving and closing it must preserve canvas/SVG dimensions, node positions and map scroll; do not auto-pan the diagram. Search around the selected and visible nodes as well as viewport corners, strongly avoid covering the selected/connected cards, and consider active paths and map labels. Prefer clear space rather than a fixed corner. Full details may cover some of the map only after an explicit expansion. Pointer/keyboard movement, viewport clamping, a visible close control, scrollable full content and Escape/focus restoration remain required. No separate sidebar/lower row, modal, backdrop, whole-canvas dimming or hidden graph content.

**Selection contrast, 2026-11-13:** The selected card must stand out clearly from an unselected or hovered card: use a strong filled theme colour, contrasting text and a heavier border. Connected cards use a lighter treatment, active links stand out and nonincident links may recede while staying visible. Unrelated card text stays fully readable; do not dim the whole canvas. Keep this distinction clear in both light and dark modes; selection must not move the map.

---

## 0. Before you touch anything

1. Read `reviews/LESSONS.md` in full. Every lesson there is a mistake that already happened once. Repeating one is an automatic review failure.
2. Read the most recent file in `reviews/records/`. If it is a FAIL, your first job is to fix every finding in it.
3. Read `CHANGELOG.md` (the last 5 entries) so you know what changed recently and why.
4. Note today's date. All freshness rules use it.

---

## 1. Repository map

| Path | What it is | Who edits it |
|---|---|---|
| `data/map.json` | **The only content file.** Nodes, edges, chains, sources, layout. | Updater |
| `src/template.html` | The page shell. Reads the data, draws the map. | Only with a reviewed reason (design change) |
| `scripts/build.py` | Builds `dist/macro-dot-map.html` and computes all edge paths. | Rarely |
| `scripts/mapgeo.py` | Shared geometry used by build and validate. | Rarely |
| `scripts/route_map.py` | Assigns clear ports and orthogonal lanes; saves reviewed waypoints. | Run after graph/layout changes |
| `scripts/validate.py` | Mechanical checks V01–V15 and V17–V20 (V17/V18 source tiers and publishers on syndicating hosts, V19 research sweep log in the changelog, V20 a script's cause must not post-date the move it explains). | Reviewer adds checks when lessons recur |
| `scripts/render_check.py` | Headless-browser layout check V16 (needs Playwright). | Reviewer adds checks when lessons recur |
| `scripts/release_check.py` | The release gate (R1–R7). | Rarely |
| `dist/macro-dot-map.html` | The built page that gets published. Never edit by hand. | build.py |
| `reviews/LESSONS.md` | Ledger of past mistakes and their guards. | Reviewer |
| `reviews/lesson_patterns.json` | Risky phrasings that require reviewer acknowledgement. | Reviewer |
| `reviews/records/` | One file per review, never deleted or edited after the fact. | Reviewer |
| `reviews/RELEASES.md` | One row per release: the commit to roll back to. | Updater, after release |
| `CHANGELOG.md` | What changed each day, including what was retired and why. | Updater |

The published page lives at the URL in `meta.artifactUrl`. Always update that same artifact; never create a new one.

---

## 2. The daily run, in order

1. **Prepare** (section 0).
2. **Research sweep** (section 3). Collect today's facts with sources and dates into a scratch note. Do not edit `map.json` yet.
3. **Refresh** every node whose data has changed or whose TTL has expired (section 5). Update `value`, `tag`, `facts`, `asOf`.
4. **Retire** what is stale or no longer a live driver (section 5).
5. **Add new headlines to the map** (section 6). Actively evaluate the strongest new stories, give material events their own nodes and transmission links, and replace weaker or superseded headlines when needed.
6. **Review the whole map, consolidate and reconnect** (section 4.5). Check all five columns and every edge and chain, including unchanged items. Merge overlapping mechanisms, connect related stages where the mechanism is defensible, and rewrite affected scripts and references. This is required on every update, not only when adding a node or reaching the budget.
7. Set `meta.asOf` to today and bump `meta.version` by 1.
8. Run:
   ```
   python scripts/build.py
   python scripts/validate.py
   ```
   On this Windows host there is no `python3`: use `python` (3.14). Playwright and Chromium are installed for it, so V16 runs automatically.
   Fix every ERROR. Read every WARN and FLAG and either fix it or be ready to justify it in the changelog.
9. **Look at the page.** Run `python scripts/render_check.py --shots <scratch dir>` (V16: script errors, page overflow, clipped desktop map, mobile panning and node-detail interactions). Then open the desktop and phone screenshots yourself and check nothing overlaps or is clipped. The validator only approximates text width; your eyes are the final check.
10. **Write the changelog entry** (section 9).
11. **Hand off to the reviewer** (section 10). Do not publish.
12. On **PASS**: run `python scripts/release_check.py`. Only if it prints `RELEASE OK`, publish and commit (section 11).
13. On **FAIL**: regenerate (section 10). Never publish a version the gate blocks.

---

## 3. Research sweep

Search every item below every run. Prefer tier-1 sources. Record for each fact: the number, its date, the source URL, and the exact wording that supports it.

| Area | What to check | Feeds node(s) |
|---|---|---|
| Geopolitics and oil | Hormuz and Gulf flows, attacks on infrastructure, OPEC+ decisions, Brent and WTI levels, YTD peak | `hormuz`, `oil` |
| Inflation | US CPI and PCE releases, UMich expectations, Canada CPI | `inflation` |
| Fed | Last decision, next meeting date, market pricing, key speeches | `fed` |
| Bank of Canada | Last decision, next date, CA jobs and CPI, hike or cut odds | `boc` |
| Rates | US 10-year level and 2026 high, real yields (TIPS), auction and issuance news | `y10`, `realy`, `issuance` |
| Credit | ICE BofA HY OAS (FRED), CCC spreads, notable defaults | `credit` |
| FX and gold | USD/CAD, DXY, gold spot and 1-month change | `cad`, `gold` |
| Equities | S&P sector returns for the week and YTD (name the proxy), SOX, equal vs cap weight, Nasdaq-100 | `energy`, `semis`, `breadth` |
| Factors | Momentum, value, quality performance (Confluence, MSCI, Goldman via reputable press) | `factor` |
| AI | Hyperscaler capex guidance, model releases that move chip stocks, compute leasing deals | `aicapex`, `cheapai`, `metacompute`, `overcap` |
| Portfolio | Stock–bond correlation measures, 60/40 commentary from asset managers | `sbcorr` |
| Earnings | FactSet weekly earnings insight: blended growth, concentration | `breadth`, `energy` |

**Source tiers** (set `tier` in `sources`):

- **Tier 1**: primary data and top financial press. FRED, central banks (federalreserve.gov, bankofcanada.ca), statistics agencies, exchanges, company filings, FactSet, S&P DJI, Confluence, MSCI, Bloomberg, Reuters, WSJ, FT, CNBC, BNN Bloomberg, CNN Business, AQR and similar primary research.
- **Tier 2**: reputable secondary sources. Yahoo Finance, Fortune, Investing.com news, Trading Economics, Macrotrends, OilPrice, asset-manager commentary, regional press syndicating Bloomberg or Reuters.
- **Tier 3**: blogs, Substack recaps, broker blogs, aggregators, AI-written finance sites. Usable only as `weak` evidence, shown on the page as "verify".

Rules:

- Never fill a number from memory. If you cannot find a source today, keep the old value only if it is still within its TTL; otherwise retire the fact.
- Prefer the original publisher. If a tier-3 page cites Bloomberg, find the Bloomberg piece.
- When two sources disagree, use the tier-1 one, and if both are tier 1, say so in the fact ("estimates range from X to Y").
- Dates matter as much as numbers. Every event needs the date it happened, taken from a dated source.

---

## 4. How to connect the dots

The map has five columns, left to right: **Shock → Transmission → Policy & rates → Markets → Portfolio**. Causation flows left to right. A node belongs in the column of its role, not its asset class (oil is "Transmission" because it carries the shock to inflation and to energy stocks).

### 4.1 What an edge means

An edge `A → B` says: *a change in A changes B, through a mechanism you can name.* It is not "A and B moved together."

Every edge must pass all four tests:

1. **Mechanism test.** You can name the channel. Use one of:
   - *cost* (input prices, borrowing costs),
   - *price/discount rate* (valuation, real yields),
   - *policy reaction* (central bank responds),
   - *supply/demand* (bond issuance, chip demand),
   - *substitution/opportunity cost* (gold vs real yields),
   - *risk appetite/flows* (rotation, crowding),
   - *currency* (rate differentials, commodity FX).
2. **Sentence test.** `why` explains cause → mechanism → effect in at most 110 characters, in plain words.
3. **Sign test.** `+` if A up means B up; `−` (Unicode minus U+2212) if A up means B down. Check the sign against the direction the chain describes.
4. **Evidence test.**
   - `basis: "sourced"`: a tier-1 or tier-2 source states this causal link for the current episode (not just the two facts separately).
   - `basis: "weak"`: only tier-3 sources state it.
   - `basis: "unsourced"`: it is our own reasoning. Textbook links are allowed but must be marked unsourced, and `src` must be empty. Details label them "unsourced"; their map lines are solid like every other connection, as requested by the user.

### 4.2 Edge shape rules

- Prefer edges between adjacent columns. Long edges clutter the map.
- An edge that skips a column needs a route through gaps between nodes. For the orthogonal layout, run `scripts/route_map.py` to assign explicit ports and waypoints; V11 checks the exact rounded paths. Legacy layouts can use a `via` y-value.
- Edges within a column connect neighbours only, unless `route: "side"`.
- A loop (B eventually affects A) is allowed only as one explicit `route: "feedback"` edge pointing to an earlier column (V10). Keep at most two feedback edges on the whole map.
- The page omits +/− markers. Retain `sign` and any existing `signAt` positions for data integrity and the conservative V11 geometry checks; do not loosen those checks for this presentation preference.

### 4.3 Chains

A chain is a story an interviewer could ask about ("Why is gold falling?"). Rules:

- 3–6 edges, forming one connected path from a shock or policy node to a markets or portfolio node.
- The name is the question or claim, in at most 34 characters.
- The `script` is a ready-to-say answer of 50–140 words (about 60 seconds). It:
  - opens with the conclusion,
  - walks the chain in order, one number per step at most,
  - uses only numbers that appear in that chain's nodes or edges (V12 enforces this; rounding within 10% is fine),
  - ends with a portfolio implication or what to watch.
- At most 8 chains. Every node should sit on at least one chain (V08 warns if not).

### 4.4 Nodes

- `label` at most 19 characters, `tag` at most 22. The tag is the single most useful number or date.
- `value` is the headline fact shown in the panel, at most 60 characters.
- 1–4 `facts`, each at most 220 characters, each with its own `src` and `basis`.
- `say` is one sentence the reader can say out loud.
- `kind` sets the freshness rule (section 5). `event` nodes also need `eventDate`.
- In the redesigned map, `tone` groups related mechanisms: `labour`, `duration`, `energy`, `ai` or `risk`. Assign a matching edge tone when adding a connection. Colour does not replace an evidence label or encode the causal sign.

---

### 4.5 Whole-map review and consolidation

After each content update, review the complete diagram before finalizing it:

- Read every column for overlapping concepts and repeated facts. Group candidates by their actual mechanism, not merely by company name or a shared label such as "AI".
- Trace all stories from shock through transmission to markets and portfolio effects. Connect upstream constraints to downstream risks where the mechanism is defensible; distinguish causal links from co-movement and mark inferred links unsourced.
- Merge nodes that serve the same transmission role. Preserve distinct stages, measures and material event headlines: financing pressure can feed execution risk, while an event, its mechanism and its market outcome can still need separate boxes.
- Reassess chain overlap after a node merge. Combine stories that now repeat the same path, remove retired IDs everywhere, deduplicate facts and sources, and retain material qualifications and counterpoints.
- Check the whole layout again after rewiring, including unchanged paths. Connections remain solid without arrowheads or sign markers. Write the merge/reconnection decisions and reasons for keeping other candidates distinct in the changelog.

This review must happen on every update even if there are no additions and the graph is below its cap. Do not claim a whole-map review after checking only the edited neighborhood.

---

## 5. Freshness and retirement

### 5.1 TTL by kind (V07 enforces)

| kind | Meaning | TTL | Typical nodes |
|---|---|---|---|
| `price` | Levels that move daily | 4 days | oil, y10, gold, credit, cad |
| `weekly` | Weekly or YTD performance | 8 days | energy, semis, breadth |
| `monthly` | Monthly data or slow measures | 35 days | inflation, realy, sbcorr, factor |
| `policy` | Rates and decisions | 50 days, and always refresh the day after a meeting | fed, boc |
| `event` | Something that happened on a date | 60 days since last confirmed relevant | hormuz, cheapai, metacompute |
| `structural` | Slow trends | 120 days | aicapex, issuance, overcap |

A node past its TTL is a validator ERROR. Refresh it with a sourced fact, or retire it.

### 5.2 When to retire

Retire a node, edge or chain when any of these is true:

1. **It is no longer moving markets.** No tier-1 coverage in the last 14 days connects it to a market move. For events older than 90 days, the validator blocks release unless `keepReason` explains why it still matters. Re-justify `keepReason` every run; if you cannot, retire.
2. **It has been superseded.** A newer event tells the same story better (a newer model release replaces an older one). Update the node rather than adding a second one.
3. **The mechanism broke.** The sign flipped or the link stopped holding. Example: if bonds start rallying when stocks fall, the "positive correlation" chain must be rewritten, not kept.
4. **It is needed for budget.** A stronger new item is displacing it (section 6).

When you retire something:

- Delete it from `map.json`, along with edges and chain steps that depended on it. Fix any chain that drops below 3 edges, or retire that chain too.
- Remove sources no longer used (V03 warns).
- Record it in `CHANGELOG.md` under **Retired**, with the reason and the last value.

Old values are never kept on the page. The page shows today's picture; the changelog keeps the history.

---

## 6. Deciding whether new information goes in

Actively curate the map's headlines. A distinct, material new event should become a visible node with a clear path to markets or portfolio implications. Refresh an existing node when the news is simply a new value for the same driver. Do not bury a new market-moving event only in another node's facts or commentary when it deserves its own place on the map.

On every update:

- Research and score the strongest new headline candidates, including company events that can transmit into broader markets (for example, NVIDIA's CEO departure).
- Add qualifying headlines directly to the graph and include them in a chain. Distinguish the sourced event from inferred effects; mark reasoning that reporting has not established as `unsourced` with empty citations, and show that label in details. All map lines remain solid.
- Reassess the oldest and weakest event headlines. Remove or replace items whose market relevance has faded, whose mechanism no longer holds, or whose story is better represented by a newer event. Clean up dependent links, scripts and unused sources.
- If the graph is at its budget, compare incoming headlines with existing ones and retire a weaker or superseded item instead of silently keeping the old lineup. Do not raise a cap just to avoid choosing.
- Record candidates added, updated, retired or rejected and the concrete reasons in the changelog. Never invent an event or a causal claim to fill space.

These headlines belong in the macro map, not in a separate news section. The existing research and retirement checks still apply.

A new node must pass every gate:

1. **Material.** It moved an asset class or changed policy expectations, reported by at least one tier-1 source with numbers.
2. **Connected.** It has at least one edge in and one edge out that pass the four edge tests. Shocks need only an edge out; terminal portfolio effects need only an edge in, as in the existing five-column design. If you cannot draw its edges, it does not belong.
3. **Not redundant.** It is not another example of an existing node.
4. **Interview-useful.** A PM could reasonably ask about it this month.

Then score it 0–3 on each of materiality, recency, connectivity and interview value (maximum 12). Add it only if:

- it scores **8 or more**, and
- there is room under the budget (V03: 32 nodes, 7 per column, 40 edges, 8 chains), **or** it scores higher than the weakest existing node, which you then retire. Score the existing nodes the same way and write both scores in the changelog.

A new chain must tell a story none of the existing chains tells. If it overlaps an existing chain by more than half its edges, extend or rewrite that chain instead.

New edges between existing nodes follow the same edge tests. Do not add an edge just because two things are both in the news.

---

## 7. Layout procedure

- Keep the existing positions unless a change is needed. Readers learn where things are.
- Preserve the five-column stage order. Column positions, card size and spacing live in `layout`; change them only for an explicit reviewed design reason.
- Keep at least 18px between boxes in a column (V11). Current node height is 70, so centres must be at least 88 apart.
- Place a node near the nodes it connects to, so edges stay short and do not cross boxes.
- After any move/addition, run `python scripts/route_map.py`, then build and validate, and inspect the rendered page. Never hand-adjust a waypoint to hide a causal connection. Orthogonal endpoint, axis-alignment, box-clearance and conservative sign-position guards remain enforced.

---

## 8. Writing style

- English only on the page (V06). Plain, short sentences. Name things the way a market professional would say them out loud.
- Numbers with units and dates: "$110", "5.23%", "Oct 16". Use the minus sign "−" for negatives.
- Say which period a performance number covers (week, month, YTD) and which proxy (XLK, SOX, RSP).
- No hype words ("soaring", "plunging") unless quoting a move that large.
- Never state something more strongly than the source does.

---

## 9. Changelog entry

Add at the top of `CHANGELOG.md`:

```
## YYYY-MM-DD (version N)
Sweep to YYYY-MM-DD:            (= meta.asOf; V19 checks this block)
- Geopolitics and oil: <latest dated event or data point, and where it went on the map or why not>
- Inflation: ...
- Fed: ...
- Bank of Canada: ...
- Rates: ...
- Credit: ...
- FX and gold: ...
- Equities: ...
- Factors: ...
- AI: <dated equity-side item>; <dated debt-side item>   (one ';' clause per side)
- Portfolio: ...
- Earnings: ...
Updated: node — old → new (source)
Added: node or edge — score X/12 — why
Retired: node or edge — last value — why
Chains: what changed in which script
Whole-map review: candidates merged, reconnected or kept distinct across all five columns, with reasons
Warnings left open: V-code — justification
```

---

## 10. Hand-off, and what to do on FAIL

- The reviewer must be a separate agent or session that has **not** seen your reasoning. Give it only the repository and the instruction "Review today's update using REVIEWER.md." Do not summarize your work for it beyond the changelog.
- **FAIL means regenerate, not patch.** Start from the last approved data (`git checkout <commit of the last row in reviews/RELEASES.md> -- data/map.json`), then redo the run with every finding fixed. Re-check every item of the same type as each finding, not just the one quoted. (If the reviewer found one wrong date, re-verify every date.)
- After two FAILs in one day, stop. The last released version stays live. Commit your work on a branch named `failed/YYYY-MM-DD` and leave a note at the top of `CHANGELOG.md` saying the day's update was not released and why.

---

## 11. Publish and commit (only after `RELEASE OK`)

1. `python scripts/release_check.py` must print `RELEASE OK`.
2. Publishing is the git push itself: GitHub Pages serves `index.html` from `main` at https://podor.org/macro-dot-map/. `dist/macro-dot-map.html` is committed as the artifact copy. `meta.artifactUrl` is a legacy claude.ai mirror and is not updated by this process.
3. Commit everything (data, dist, index.html, changelog, review record) in one commit: `update: YYYY-MM-DD vN`.
4. Push the commit; GitHub Pages redeploys within about a minute. Then add a row to `reviews/RELEASES.md` (date, version, commit, content hash, review id) in a second commit and push it. That file, not git tags, is the record of what was released, because tag pushes can be blocked.

---

## 12. Never

- Never publish without `RELEASE OK`.
- Never edit `dist/` by hand or edit a review record.
- Never weaken a validator check or raise a cap to make your update pass. Budget changes need a reviewed design reason recorded in a review record.
- Never mark your own reasoning as sourced, or a tier-3 source as sourced.
- Never keep a number you could not re-verify after its TTL.
- Never add a node without its edges, or an edge without a mechanism.
