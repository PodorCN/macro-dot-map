# Macro Dot Map

An interactive cause-and-effect map of what is driving markets right now: the oil shock, inflation, rates, AI, credit, gold and FX, through to portfolio construction. It is built for buy-side interview prep. Pick a chain to walk through a story step by step and get a ready-to-say 60-second answer, or tap any box to see what drives it and what it drives. Every number links to its source.

Live page: https://podor.org/macro-dot-map/ (GitHub Pages, serves `index.html`). The claude.ai artifact URL in `meta.artifactUrl` is a legacy mirror and is not updated by the daily run.

The map fills the page width, with dated headlines and a reading panel underneath. Select a headline to highlight related drivers, or filter by AI, Macro, Markets or Policy. Reporting links to its source; watch questions are labelled as reasoning. Driver panels also link to related headlines.

Headlines live in `data/map.json` alongside the map. Each has an `id`, `title`, reporting `date`, `category`, `summary`, reasoning-only `watch`, related `nodes`, source keys in `src`, and evidence `basis`. `meta.headlinesAsOf` records when the news was checked; `meta.asOf` still dates the map’s prices and chain scripts. A newer headline does not refresh those values. The page displays both dates when they differ. V21 validates the news references, dates and evidence; the existing map freshness and release gates remain in force.

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

## Legend on the page

- Solid line: the link is stated by a tier-1 or tier-2 source.
- Dashed line: unsourced, our own reasoning.
- "verify" tag: the only source is a blog, Substack or aggregator.
- `+` the two move the same way; `−` they move in opposite directions.
