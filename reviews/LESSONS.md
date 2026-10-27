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
- **Recurred (2026-10-27, review 001):** the 2026-10-27 hand-off kept data as of Oct 26 and its changelog said "the Oct 26 close changed nothing material". On Oct 26 Meta launched a ~$35B stock offering (about $22.5B common plus $12.5B mandatory convertible preferred, SEC FWP; Reuters; AP) to fund its AI build-out, with up to $60B more planned. The map's `aicapex` node and its chain "The AI funding squeeze" left it out and still said hyperscalers fund the build-out by "borrowing heavily".
- **Rule:** The research sweep covers every area in AGENT.md section 3 on every run, up to the date in `meta.asOf`; the reviewer asks what a PM would expect to see. A chain about funding or a driver must include that driver's latest event, and its channel must still match it.
- **Recurred again (2026-10-27, review 002):** the fix for review 001 added Meta's offering but not the other lead story of the same asOf day. On Oct 26 Anthropic publicly filed its S-1 for a Nasdaq IPO (ticker ANT; reported raise of up to $100B; AP via BNN Bloomberg, CNBC). CNBC's Oct 26 wrap: "Stocks close higher as excitement over Anthropic IPO filing propels tech sector"; SOXX rose nearly 3%. The map still told the chip story only through the Oct 22 selloff (`semis`: "Chips had their worst day since June on Oct 22 as AI financing worries returned"), and the `fund` chain's "funding mix, bonds or stock" left out the largest AI equity raise in the pipeline. The changelog recorded no sweep of the AI and equities areas for Oct 26.
- **Recurred a third time (2026-10-27, review 003):** the fix for review 002 added Anthropic's IPO filing and logged the sweep, but the AI bullet listed only equity raises. It left out the debt side of AI funding on the same days. On Oct 25 Musk said SpaceX had closed $40B of debt for GPUs, and warned that "debt markets have almost entirely shut off access to money" for neoclouds without other revenue. CNBC, Fox Business (with Reuters) and Yahoo Finance covered this on Oct 26. The `fund` chain ("the funding mix, bonds or stock") still rested its bond channel on a Sep 26 CNBC piece. The `credit`/`quality` story ("AI borrowers are in focus") stopped at CoreWeave in mid-October.
- **Guard:** validator (V19: the newest `CHANGELOG.md` entry must contain `Sweep to YYYY-MM-DD:` equal to `meta.asOf`, with one bullet `- <Area>: ...` naming a dated finding for each of the 12 AGENT.md section 3 areas; since review 2026-10-27-003, the `AI` bullet must also have a dated `;`-separated clause on the debt side (debt, bond, loan, borrowing, credit) and one on the equity side (stock, equity, shares, IPO, offering)) + pattern (`funding squeeze`, `borrowing heavily`, `heavy issuance`, `AI debt`/`AI borrowing`, `bond supply`) + manual (REVIEWER.md Step D "missed drivers": the reviewer compares each sweep bullet with that day's tier-1 market wraps).
- **First seen:** 2026-10-20 · **Occurrences:** 4

### L-011 — Map clipped at desktop width
- **What happened:** In v1, at about 1300px wide with the side panel open, the map needed its own sideways scroll and the Portfolio column was cut off ("Quality > moment…", "Equal vs cap weig…"). Found in the v2 baseline screenshots.
- **Rule:** With the side panel visible, the whole map fits without sideways scrolling. Look at the rendered page before every release.
- **Guard:** validator (V16 in `scripts/render_check.py`, run by `release_check.py` R7).
- **First seen:** 2026-10-20 · **Occurrences:** 1

### L-012 — Chain rewritten with new numbers but its story not re-tested
- **What happened:** In the v3 draft (2026-10-26) every script got fresh numbers, but two chains kept a story the latest data no longer supports. `bonds` still said bonds aren't hedging, resting on a Nationwide 40-day correlation dated 06/10/2026 that was not re-verified, while Treasuries rallied as a haven on the October tech selloff days (Oct 14–15, Oct 22: Nasdaq −2.6%, 10-year closed below 5%). `ai` explained the Oct 22 chip drop as a supply squeeze, a cause that no edge on the chain carries (its edge is demand doubt → semis).
- **Rule:** Before rewriting a script, re-test the chain's mechanism against the latest week: the biggest moves must go the way the edges say, for the reason the edges say. If not, rewrite the chain or retire it (AGENT.md 5.2, rule 3). A node that carries a chain's key claim must be re-verified on the day the chain is rewritten.
- **Guard:** pattern (stock–bond correlation, "bonds aren't hedging", "supply squeeze", "rather than demand") + manual (REVIEWER.md Step C, "Does the story still hold given today's data?").
- **First seen:** 2026-10-26 · **Occurrences:** 1

### L-013 — Syndicated copy given the wire's tier, or the wrong publisher
- **What happened:** The v3 draft gave tier 1 to a Reuters story read on za.investing.com and an AP story read on finance.yahoo.com, against AGENT.md section 3 (Yahoo Finance, Investing.com and syndicating outlets are tier 2) and the existing `edge_kimi` precedent. The `yahoo_boc` source ("Yahoo Finance") is a Baystreet.ca article hosted on Yahoo, not Yahoo or Reuters reporting.
- **Recurred (2026-10-26, review 002):** the regenerated v3 still named two Yahoo-hosted pieces "Yahoo Finance". `yahoo_chips` (the Lam Research supply warning on `semis`) is a 24/7 Wall St. article by David Moadel. `yahoo_growth` (the only source for the sourced edge `y10-semis`, chain `fund`) is a StockStory piece about Yelp, by Radek Strnad. Both kept Yahoo's tier 2 instead of their own publisher's tier, so `y10-semis` was `sourced` on an AI-assisted stock-content site.
- **Rule:** Tier a source by the page you cite. A wire story on a syndicating host is tier 2; for tier 1, cite the original publisher's own URL. Name the original publisher in the source name and judge its own tier.
- **Guard:** validator (V17: sources on syndicating hosts cannot be tier 1; V18: an article on a syndicating host is named "<Publisher> via <Host>: ..." or carries a `publisher` field, copied from the byline, that its name starts with; tradingview.com added to the syndicating hosts) + manual (Step B: open each source and check the byline).
- **First seen:** 2026-10-26 · **Occurrences:** 2

### L-014 — "Sourced" edge whose source states only the facts
- **What happened:** Spot check on 2026-10-26: `oil-energy` ("higher realized prices lift producer earnings") is `sourced` to James Investment's September recap, which gives energy returns and FactSet earnings growth but does not link them to oil prices. It had passed review since v2.
- **Rule:** A `sourced` edge needs a tier-1/2 source that states the causal link itself. Otherwise add one that does, or mark the edge `unsourced`.
- **Guard:** manual (REVIEWER.md Step C, "Does a sourced edge's source actually state the causal link?"), now applied to spot-checked edges as well as new ones.
- **First seen:** 2026-10-26 · **Occurrences:** 1

### L-015 — Status claim contradicted by the node's own source
- **What happened:** The v3 `hormuz` value said "Hormuz largely shut since Feb 28". Its own Lloyd's List source (Oct 22) says "Hormuz traffic remains relatively elevated", and Trading Economics (Oct 26) says flows are recovering to near prewar levels. Reuters (Oct 26) still says "largely shut". The disagreement was not stated.
- **Rule:** A headline status (shut, closed, halted) must agree with every source on the node for today's date. When tier-1/2 sources disagree, say so (AGENT.md section 3).
- **Guard:** pattern (`largely shut`, `closed`, `near-closure`, `shut since`).
- **First seen:** 2026-10-26 · **Occurrences:** 1

### L-016 — Small caps used as a stand-in for equal weight
- **What happened:** The v3 `breadth` node ("Equal vs cap weight") replaced its equal-weight data with the Russell 2000 vs S&P 500 for the week to Oct 23, and the `ai` script concluded that this "argues for equal weight". Size and equal weighting are different exposures.
- **Rule:** A node measures the concept on its label. Equal vs cap weight needs an equal-weight proxy (RSP or S&P 500 Equal Weight), named, against the cap-weighted S&P 500 for a stated period.
- **Guard:** pattern (`small cap`, `Russell 2000`).
- **First seen:** 2026-10-26 · **Occurrences:** 1

### L-017 — A move credited to one chain edge when its source gives several causes
- **What happened:** The 2026-10-27 regenerated `ai` script said cheaper Chinese models raise doubts about chip demand, then: "Those doubts hit chip stocks: the SOX fell eight straight sessions to Oct 16." Its source (24/7 Wall St., Oct 17) says the run "was driven by oil, interest rates, and doubts about whether AI spending will pay off". It does not mention cheaper models or DeepSeek. The script made a multi-cause move look like proof of the chain's own mechanism.
- **Recurred (2026-10-27, review 004):** the fix for review 003 added SpaceX's $40B GPU debt to the `fund` script as "SpaceX closed $40B of GPU debt, adding to bond supply that helped push the 10-year to 5.31% on Oct 5". Musk announced the deal on Oct 25, and the FT first reported the talks on Oct 6, so it cannot have helped push the Oct 5 peak. The 10-year's source (CNBC, Sep 26) does not mention it. No source on the map says the deal is bonds or that it moved Treasury yields: the FT described ~$10B of bank loans and ~$30B of investment-grade debt led by Apollo, and Bloomberg reported an off-balance-sheet vehicle.
- **Rule:** When a script or fact says a move happened because of something, that cause must be in the move's source. If the source names several causes, say so, or use a move that the source ties to the chain's edge. Never state a cause more strongly than the source does (AGENT.md section 8). A cause must come before the move it explains: a new event can be the latest example of a channel, but it cannot be credited for a move dated before it.
- **Guard:** validator (V20: in a chain script, a sentence or clause with a causal phrase such as "drove", "helped push", "adding to" or "because of" that dates its effect must not name an event, via a proper noun from a fact starting `Mon DD:` on the chain's nodes, dated after that effect) + pattern (`those/these doubts hit…`, `straight sessions`, `losing run/streak`) + manual (REVIEWER.md Step C: "Does every claim in it appear in the chain's nodes or edges?", applied to causes as well as numbers).
- **First seen:** 2026-10-27 · **Occurrences:** 2

### L-018 — Chain script skips one of its edges
- **What happened:** The 2026-10-27 regenerated `ai` script dropped its old ending ("which argues for equal weight and for quality over momentum"). Now nothing in the script covers the chain's fourth edge, `semis-factor` (Semis & tech → Quality > momentum). The map highlights that step, but the 60-second answer never mentions it, and the script ends on a description rather than an implication.
- **Rule:** A chain's script walks every edge of the chain, in order, and ends with a portfolio implication or a watch item (AGENT.md 4.3). If an edge no longer belongs in the story, take it off the chain; do not leave it out of the script silently.
- **Guard:** manual (REVIEWER.md Step C: "follow the edges in order, and end with an implication"). A validator check was tried and dropped. Matching each edge's node label against the script gave false positives on today's data ("10-year" for "US 10-yr yield", "growth stocks" for "Semis & tech"). It needs per-node aliases in `data/map.json`, and the reviewer may not add them. Upgrade it if this lesson recurs.
- **First seen:** 2026-10-27 · **Occurrences:** 1

### L-019 — A clause taken from a review record, cited to sources that do not say it
- **What happened:** The fix for review 2026-10-27-004 added two clauses that came from that review record, not from the sources cited. First, the `issuance` fact now ends "talks were first reported on Oct 6". Its sources are `il_spacex` and `tnw_spacex`, and neither gives that date: The Next Web says only that the FT reported the talks "earlier this month". The date is right. The FT reported it on Tuesday Oct 6, as InvestingLive's Oct 7 piece says, but that piece is not on the map. Second, the `credit` fact says "Musk, who competes with neoclouds", and the `quality` script says "Musk, a competitor". Neither `tnw_spacex` nor `il_spacex` says this. Both say only that SpaceX would not buy any neoclouds and that its AI unit is its largest business.
- **Rule:** Every clause of a `sourced` fact, including a date, a "first reported" history or a statement about an actor's interest, must be stated by one of that fact's own cited sources. A review record is not a source. If a fix uses something a reviewer found, add the reviewer's source to `sources` and cite it, or leave the clause out.
- **Guard:** pattern (`first reported`, `competes with`, `a/its/their competitor/rival`) + manual (REVIEWER.md Step B: "open its source URL and confirm the source says it", applied to every added clause).
- **First seen:** 2026-10-27 · **Occurrences:** 1
