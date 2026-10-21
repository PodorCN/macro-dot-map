# Lessons ledger

Every mistake that reached a draft or a release, the rule it taught, and the guard that now catches it. Reviewers check every lesson on every review (`lessons_checked` in the review record, enforced by `release_check.py` R4). A lesson is never deleted. When a lesson recurs, its occurrence count goes up and its guard is upgraded one level: manual → pattern → validator check.

Guard levels:
- **validator**: an automated check in `scripts/validate.py` (strongest)
- **pattern**: a regex in `reviews/lesson_patterns.json`; the reviewer must acknowledge each hit
- **manual**: a line in the REVIEWER.md procedure

---

### L-001 — "Record high" without checking the peak
- **What happened:** The draft commentary called Brent at $110 "another record high" for the year. The 2026 intraday high was $126.41 on Apr 30, so $110 was only a five-month high.
- **Rule:** Any record, peak or "highest" claim must name the peak it beats and its date, taken from a source.
- **Guard:** pattern (`record high`, `all-time high`, `new high`, `highest ever`) + manual (Step B).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-002 — Event placed in the wrong month
- **What happened:** The Meta compute news was placed "around April or May". Meta Compute was announced on Jul 1, 2026; Zuckerberg had only hinted at it in May.
- **Rule:** Every event needs an `eventDate` from a dated source. Distinguish the announcement from earlier hints.
- **Guard:** validator (V07 requires `eventDate` on event nodes) + manual (Step B: open the source and confirm the date).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-003 — Event attributed to the wrong actor
- **What happened:** The July "cheap Chinese model" chip selloff was attributed to DeepSeek. It was Moonshot's Kimi K3; DeepSeek's market-moving releases came on other dates.
- **Rule:** The named company, person or model must match the source text exactly. "Compared to X" is not "caused by X".
- **Guard:** manual (Step B: check the named actor in the source).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-004 — Utilities called an oil winner
- **What happened:** Utilities were described as a clear winner alongside energy. They fell about 6% in September; they trade on rates and AI power demand, not oil.
- **Rule:** Only list a sector as a winner for a stated period, with its return, and only link it to a driver its source names.
- **Guard:** pattern (`utilities`).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-005 — "Risk parity" used for concentration risk
- **What happened:** The commentary said "risk parity" when the point was that the cap-weighted index is concentrated.
- **Rule:** Risk parity is an allocation method that equalizes risk contribution. Use "concentration risk" or "diversification" for index concentration.
- **Guard:** pattern (`risk parity`).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-006 — Sector leadership without a period
- **What happened:** "Most sectors are green except tech" was true for October but the reverse of September, when tech was the only sector up.
- **Rule:** Every sector, breadth or factor claim states its period (week ending, month, YTD).
- **Guard:** pattern (`this month`, `all sectors`, `most sectors`, `every sector`) + V12 (script numbers must exist on the chain).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-007 — Same move quoted with different proxies
- **What happened:** Tech's loss for the week of Oct 12–16 was quoted as −4.82% in one place and −7.70% in another, from different proxies (S&P 500 IT vs XLK).
- **Rule:** Name the proxy (XLK, SOX, RSP, S&P 500 IT) and use one proxy per node.
- **Guard:** pattern (tech sector + %) + manual (Step B).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-008 — Internal label shown on the page
- **What happened:** v1 showed the Chinese label 自己推理 on the page for reasoning-based links. The page is English, and the label should be "unsourced".
- **Rule:** Reasoning is marked with `basis: "unsourced"`, which renders as "unsourced" and a dashed line. No CJK text in display fields.
- **Guard:** validator (V05 basis enum, V06 no CJK text).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-009 — Overlapping +/− markers shipped
- **What happened:** v1 drew the markers for `aicapex-issuance` and `metacompute-overcap` on top of each other, and the same for `realy-gold` and `y10-credit`. Nobody noticed until the validator was written.
- **Rule:** No marker within 20px of another or inside a node box; no edge through a non-endpoint box.
- **Guard:** validator (V11 geometry checks).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-010 — Major driver left out of the story
- **What happened:** The draft explained the 10-year yield move with inflation expectations only and left out the September Fed hike, the first in over three years.
- **Rule:** The research sweep covers every area in AGENT.md section 3 on every run; the reviewer asks what a PM would expect to see.
- **Guard:** manual (AGENT.md section 3 sweep, REVIEWER.md Step D "missed drivers").
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-011 — Map clipped at desktop width
- **What happened:** In v1, at about 1300px wide with the side panel open, the map needed its own sideways scroll and the Portfolio column was cut off ("Quality > moment…", "Equal vs cap weig…"). Found in the v2 baseline screenshots.
- **Rule:** With the side panel visible, the whole map fits without sideways scrolling. Look at the rendered page before every release.
- **Guard:** validator (V16 in `scripts/render_check.py`, run by `release_check.py` R7).
- **First seen:** 2026-10-20 · **Occurrences:** 1
