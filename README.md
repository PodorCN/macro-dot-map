# Macro Dot Map

An interactive cause-and-effect map of what is driving markets right now: the oil shock, inflation, rates, AI, credit, gold and FX, through to portfolio construction. It is built for buy-side interview prep. Pick a chain to walk through a story step by step and get a ready-to-say 60-second answer, or tap any box to see what drives it and what it drives. Every number links to its source.

Live page: https://claude.ai/artifact/GnDR8esNpiSLzq6ki3r8dT

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
scripts/build.py           builds dist/macro-dot-map.html (computes all paths)
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
python3 scripts/build.py           # build the page
python3 scripts/validate.py        # content checks (add --today YYYY-MM-DD to test a date)
python3 scripts/render_check.py    # layout checks (needs: pip install playwright && playwright install chromium)
python3 scripts/release_check.py   # must print RELEASE OK before publishing
```

## Legend on the page

- Solid line: the link is stated by a tier-1 or tier-2 source.
- Dashed line: unsourced, our own reasoning.
- "verify" tag: the only source is a blog, Substack or aggregator.
- `+` the two move the same way; `−` they move in opposite directions.
