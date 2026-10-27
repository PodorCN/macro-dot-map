# Changelog

## 2026-10-27 (version 3, fixes for reviews 2026-10-26-002 and 2026-10-27-001)
Max asked for the two blockers to be fixed and the update released. Regenerated again from release a1b264d (data as of Oct 26). Review 2026-10-27-001 failed this draft because it said the Oct 26 close "changed nothing material", but on Oct 26 Meta launched a ~$35B stock offering (L-010 recurred). The map now includes it.

Blockers fixed:
- **L-013 (recurred):** every source hosted on Yahoo, Investing.com or TradingView now names its real publisher, and V18 passes.
  - `yahoo_chips` → "24/7 Wall St. via Yahoo Finance" (tier 2).
  - `inv_nasdaq` and `inv_cad` are Investing.com staff articles (bylines Anuron Mitra and Jaiveer Shekhawat), so they carry `publisher: Investing.com`.
  - `edge_kimi` (The Edge, could not be opened to check the byline) is replaced by The Next Web, Jul 17 (tier 2). It confirms Kimi K3, the selloff and the DeepSeek comparison.
- **L-014:** edge `y10-semis` → `unsourced` (dashed). Its only source was a StockStory piece about Yelp, and no tier-1/2 source states the link for this episode. That source is removed.

Minors fixed (from record 002):
- The `bonds` script now says "AI-spending worries hit tech", not "growth fears".
- The `gold` say line no longer contradicts the chain.
- The Lam fact now uses Lam's own words.
- The Hormuz conflict fact adds Trading Economics' "near prewar levels".
- The `hormuz` keepReason now says "claimed" Houthi strikes.
- Removed "AI euphoria" from `factor` and the unsupported TSX clause from `canada`.
- Fixed the name of the Investing.com Nasdaq source.

Still open (minor): `semis` shows only the Oct 22 one-day move (no weekly SOX return found); the Seeking Alpha RSP page is undated; CNBC pages could not be opened.

Fix for review 2026-10-27-001:
- **Blocker (L-010):** `aicapex` adds Meta's Oct 26 equity raise (SEC FWP; Proactive): ~$35B of offerings ($22.5B common and ~$12.5B mandatory convertible preferred) and a planned ~$60B at-the-market program, alongside investment-grade debt.
  - The `fund` script was re-tested and rewritten. Bond supply still holds as one channel, since Meta also uses investment-grade debt, but the script now says the funding mix (bonds or stock) is the thing to watch.
  - A Yahoo-hosted article on the share move (by Fiona Craig, no original publisher named) was not used.
- Minors:
  - The `oil` fact names the contract (front-month futures). AP's $110.74 is most likely the next contract after the Oct 25 roll.
  - The `inflation-fed` edge says "oil-driven" instead of "sticky".
  - The 24/7 Wall St. source keeps tier 2: it is an established financial news publisher with named reporters, and the fact used quotes Lam executives directly.
  - `y10` stays at FRED's latest close (5.00%, Oct 23), because FRED has not posted Oct 26.
  - `semis` keeps only the SOX one-day move. RIA's −16.4% three-week figure uses SMH, and one proxy per node applies (L-007).

> **2026-10-26: not released.** The update failed review twice that day (2026-10-26-001 and 2026-10-26-002), so per AGENT.md section 10 it stopped and v2 stayed live. The failed work stayed on `claude/jolly-curie-dpktl1` (commit d38dfcf), because this session can only push to that branch.

## 2026-10-26 (version 3, regenerated after review 2026-10-26-001 FAIL)
First daily data update since v2. The first draft (commit b9191a5) failed review with 3 blockers and 3 majors. This version was regenerated from the last release (a1b264d) with every finding fixed, and every item of the same type was re-checked: every chain against the latest week, every source's publisher and tier, every sourced edge's evidence, and every headline status claim.

Updated (all `price`, `policy` and `weekly` nodes, plus `sbcorr`):
- `hormuz`: now "Disrupted since Feb 28; October attacks at a war high". Lloyd's List: at least 28 confirmed attacks in October as of Oct 22, the most of the war. **The sources disagree on traffic, and the node now says so** (Lloyd's "relatively elevated" vs Reuters "largely shut", L-015). The Houthi strikes on the East-West pipeline (Oct 26) are given as claims that Saudi Arabia did not confirm.
- `oil`: Brent ~$109–110 → ~$115 on Oct 26, after settling at $116.72 on Oct 23, a six-month high, +6.24% on the week (The National). WTI $103.27. The 2026 peak of $126.41 on Apr 30 was re-checked.
- `inflation`: US CPI 3.7% in September, gasoline over half of the monthly rise (BLS). UMich 1-yr 4.6% → 4.7% (October final). Canada CPI 3.1% (Statistics Canada).
- `fed`: 3.75–4.00% after the Sep 16 hike (Fed statement). Next decision Oct 28, with a hold expected and December hike odds above 80% (CME FedWatch via Trading Economics).
- `y10`: **Correction.** The 2026 high was 5.31% on Oct 5, the highest close since May 2002, not 5.23% in late September (FRED DGS10). The yield fell to 4.96% on Oct 22 as investors bought Treasuries in the tech selloff, and was 5.00% on Oct 23.
- `realy`: 10-yr TIPS 2.66% on Oct 23, from 1.72% on Feb 27, with a 2.95% peak on Oct 5 (FRED DFII10).
- `gold`: ~$4,114 → ~$4,017, near a three-month low. The record was $5,608 in January (Trading Economics). Added Jefferies via Kitco: rising TIPS yields helped drive gold about 25% below its peak.
- `credit`: HY OAS 3.29% → 3.38% on Oct 23. It hit 3.40% on Oct 22, the widest since Mar 30 (FRED). CCC 12.78% (tier 3) → 13.56% (FRED), the widest since at least 2023. Added that CoreWeave bonds yielded near 15% in mid-October (CNBC).
- `semis`: SOX −11.41% for the week to Oct 16 (tier 3) → SOX −6.7% on Oct 22, chip stocks' worst day since June 23, on AI financing worries after Meta's negative free cash flow (RIA, Investing.com). Lam Research's supply warning the same day is listed as a second cause.
- `aicapex`: Meta $125–145B → $135–145B (Meta Q3 release). Free cash flow turned negative (−$2.1B), and the shares fell nearly 7% on Oct 22 (CNBC).
- `boc`: 2.25% since Oct 29, 2025 (Bank of Canada). About 81% market odds of a hike on Oct 28 (InvestingLive), and 19 of 34 economists in a Reuters poll expect one (Reuters via Yahoo). Jobs −68,000 and 6.5% unemployment now come from Statistics Canada instead of a broker blog.
- `energy`: XLE +52.6% (tier 3) → +58.14% YTD through Oct 23 (Yahoo Finance). The FactSet wording now matches the source.
- `cad`: 1.3993 on Oct 23, down from the 2026 high of 1.4273 on Oct 14 (FRED DEXCAUS).
- `breadth`: equal weight is now measured with a named equal-weight proxy (L-016). RSP rose 3.5% over the past month while the S&P 500 fell 0.4%, on track for the biggest outperformance since April 2009 (Seeking Alpha). Removed the tier-3 Oct 12–16 fact and the unsourced "YTD roughly tied" line.
- `sbcorr`: **regime change.** It was "most positive since 1999" (a Nationwide piece from June). It now reads: positive for most of 2026, with the 60-day correlation at +0.56 in early June. On Oct 22, SPY fell 1.2% while long Treasuries rose 1.9%, and the 20-day SPY–TLT correlation fell to −0.30, ending the week at −0.24 (RIA, Investing.com).
- `factor`: the headline is now Confluence's sourced Q3 result (value, yield and quality beat momentum). The tier-3 Goldman +55% was removed.
- Edges:
  - `oil-energy` now cites OilPrice: energy led S&P earnings growth "thanks in large part to higher oil prices".
  - `inflation-boc` cites Reuters (the hike is to stop energy inflation spreading).
  - `realy-gold` cites Kitco/Jefferies (real yields).
  - `y10-sbcorr` cites AQR and RIA.
  - `oil-inflation` adds BLS, and `hormuz-oil` adds The National.
- Source tiers: Reuters read on Investing.com or Yahoo is tier 2 (L-013). The mislabelled "Yahoo Finance" BoC piece (really Baystreet) was dropped.

Retired:
- `metacompute`, last value "Meta Compute announced Jul 1, 2026", with its edge `metacompute-overcap`. Reason: it is 117 days old and no tier-1 coverage in the last 14 days ties it to a market move (AGENT.md 5.2 rule 1). The overbuild doubt stays on `overcap` through `cheapai`.
- Sources removed as unused: lite, disp, mitrade, tt_credit, cnn_10y, yahoo_hike, mt_wti, oilprice, cnbc_hy, bnn, cnn_meta, intel, nation, datap, biggo.

Not re-verified today (within TTL; `asOf` left at 2026-10-20): `cheapai`, `issuance`, `overcap`, `factor`.

Chains:
- `bonds` is renamed "Is the bond hedge back?" and rewritten: bonds stopped hedging while oil drove inflation, and the hedge returned on the Oct 22 tech selloff.
- `ai` now follows its four edges (cheap models → demand doubt → semis → equal weight and quality) and uses the RSP figures.
- `fund` adds Meta's negative free cash flow and the Oct 22 share drop.
- `gold` adds that the latest leg is Fed pricing, while real yields eased in October.
- `canada` uses the 81% odds.
- `quality` dates CoreWeave to mid-October.
- No V15 weak-number warnings remain.

Warnings left open:
- V07 `hormuz` event is 240 days old. Kept: October has the most Hormuz attacks of the war, and Houthi strikes on Saudi export routes lifted Brent to a six-month high on Oct 23.
- Lesson flags: L-015 on `hormuz` (the disagreement is now stated) and L-012 on `semis`, `sbcorr` and `bonds`. These are the rewritten texts, which now match the latest week.

Watch next: the Fed and the BoC both decide on Oct 28, so `fed`, `boc`, `cad`, `y10`, `gold` and `sbcorr` need a refresh on Oct 29. Microsoft, Alphabet and Amazon report this week (`aicapex`).

## 2026-10-21 (version 2, design refresh)
Design-only release requested by Max: the page now uses the Thematic Tracker house style. `data/map.json` is byte-identical to the 2026-10-20 release, so no fact, link, sign or chain changed.
- New look: black masthead with the red-square brand, date rule, Georgia headline, monospace kickers, square boxes, no web fonts. Light and dark themes.
- Chain steps in the side panel use the Thematic Tracker event-chain pattern (numbered steps, the final effect shown filled).
- Column headers are numbered 01–05 because the map reads left to right as a causal sequence.
- Side panel is 350px from 1240px and 400px from 1500px, so the full map still fits at desktop width (L-011; render_check 0 failures across 6 views).
- `scripts/build.py` also writes `index.html`, the same page as a full HTML document, for GitHub Pages at https://podor.org/macro-dot-map/. `dist/macro-dot-map.html` is unchanged in role and is still what the artifact publishes.
- Follow-up (Max): removed the headline and intro paragraph; the page now opens on the chain picker.
- Phone layout (under 760px): chain picker in two columns, the reading panel comes right after it, and the map defaults to a list of drivers grouped by stage (tap one to open it). A List / Diagram switch brings back the full diagram.
- "Driven by" and "Drives" names in the panel are now links that open that driver.
- Follow-up (Max): the page is full width (no 1480px cap). Tapping a selected box again clears it; the panel then lists the chains.

Warnings left open: unchanged from version 2 (V07 `hormuz`, V07 `metacompute`, three V15 weak-source script numbers); see below.

## 2026-10-20 (version 2)
Restructure into a maintained project; no market data changed from version 1.
- Content moved to `data/map.json`; the page is built from `src/template.html`.
- Reasoning-based links and facts are labelled "unsourced" instead of 自己推理 (L-008).
- Each fact now has its own sources and a basis: sourced, verify (tier-3 only) or unsourced.
- Fixed two pairs of overlapping +/− markers (L-009): moved markers on `aicapex-issuance`, `fed-realy` and `y10-semis`, and swapped the positions of `gold` and `credit`.
- Fixed the map being clipped at desktop width with the side panel open (L-011): side panel now appears from 1240px and is 360px wide.
- Credit value now also states 329 bp, so the "330 basis points" in the quality script is backed by the map.
- Added validator, render check, release gate, AGENT.md, REVIEWER.md and the lessons ledger.

Warnings left open:
- V07 `hormuz` event is 234 days old: kept because the disruption is ongoing (Houthi attacks in October).
- V07 `metacompute` event is 111 days old: kept as the origin of the overcapacity narrative still driving semis; re-assess by 2026-11-15.
- V15 scripts use numbers resting only on tier-3 sources: energy +52% and CA jobs −68,000 (canada chain), Goldman basket +55% (quality chain). Each is tagged "verify" on the page. Replace with tier-1 sources at the next update.

## 2026-10-20 (version 1)
First version, built in chat from the day's fact-check of a market commentary. Six chains: bonds, gold, AI funding, AI repricing, Canada, quality.
