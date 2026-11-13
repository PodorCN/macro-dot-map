# Macro Dot Map

An interactive cause-and-effect map of what drives markets: jobs, wages, oil, inflation, AI, Treasury financing and rates through to asset prices and portfolio effects. The website displays only the diagram. Click a node to highlight its connections and show dated facts, mechanisms and sources in a floating card on the right. The map fits beside the card and stays clickable; closing details returns it to full width. Compact screens reserve space below the pannable map for details. The card has rounded corners, outer spacing and a shadow, and leaves the diagram visible.

Live page: https://podor.org/macro-dot-map/ (GitHub Pages serves `index.html`). The legacy claude.ai artifact URL is not updated by the daily run.

New headlines belong directly in the map. Each update must also review the entire graph for overlapping mechanisms, missing connections, repeated facts and chains that can be merged. The source data retains chain scripts for internal logic/numeric checks; the page has no chain picker, permanent reading panel, news section, masthead, legend or footer.

Keep useful coverage across all five columns, including currency translation and duration effects alongside equity concentration and stock–bond hedging. The expansion budget allows 32 nodes, at most seven per column, 40 connections and eight internal stories; dated evidence and meaningful connections still decide what belongs.

## How it stays current and clean

| Role | Instructions | Job |
|---|---|---|
| Updater | [AGENT.md](AGENT.md) | Daily research sweep, refresh and retire facts, decide on additions, keep the map small |
| Reviewer | [REVIEWER.md](REVIEWER.md) | Independent fact, logic and readability check; PASS or FAIL; maintains the lessons ledger |

Nothing is released without a PASS review for the exact content hash. `scripts/release_check.py` enforces that.

Past mistakes are kept in [reviews/LESSONS.md](reviews/LESSONS.md). Every review re-checks all of them. When a mistake recurs, its guard is upgraded until it is caught automatically.

## Layout

```
data/map.json              all content: nodes, edges, chains, sources, layout
src/template.html          page shell
scripts/build.py           builds dist/macro-dot-map.html and index.html (computes all paths)
index.html                 the built page as a full HTML document, for GitHub Pages
scripts/validate.py        content and geometry checks V01–V15
scripts/render_check.py    headless-browser layout check V16
scripts/release_check.py   release gate R1–R7
reviews/LESSONS.md         mistake ledger
reviews/lesson_patterns.json  risky phrasings that need a reviewer's eye
reviews/records/           one file per review, never edited afterwards
CHANGELOG.md               daily changes, including what was retired and why
```

## Commands

```
python scripts/build.py           # build the page
python scripts/validate.py        # content checks (add --today YYYY-MM-DD to test a date)
python scripts/render_check.py    # layout checks (needs: pip install playwright && playwright install chromium)
python scripts/release_check.py   # must print RELEASE OK before publishing
```

## Map notation

- Every connection is solid, with no arrowhead or +/− marker.
- Click a node for "Driven by" and "Drives" links, with direction explained in words.
- "sourced" means a tier-1 or tier-2 source states the link; "unsourced" means our own reasoning.
- "verify" means the only source is a blog, Substack or aggregator.
