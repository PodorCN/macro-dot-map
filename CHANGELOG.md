# Changelog

## 2026-10-26 (version 3)
First daily data update since v2. Every `price`, `policy` and `weekly` node was past or near its TTL, so all of them were refreshed. Where a number could be taken from primary data (FRED, BLS, Statistics Canada, Federal Reserve, Meta IR), it was.

Updated:
- `hormuz`: still the root shock. Lloyd's List: at least 28 confirmed attacks around Hormuz in October as of Oct 22, the most of the war. Reuters, Oct 26: the Houthis claim strikes on Saudi East-West pipeline pumping stations (not confirmed by Riyadh). The Houthi-only October fact (oilprice) was replaced.
- `oil`: Brent ~$109–110 → ~$115 on Oct 26, after settling at $116.72 on Oct 23, a six-month high, +6.24% on the week (The National). WTI $103.27. The 2026 peak of $126.41 on Apr 30 was re-checked (InvestingLive).
- `inflation`: UMich 1-yr 4.6% (Sept) → 4.7% (Oct final, umich.edu). Added US CPI 3.7% y/y for September, with gasoline over half of the monthly rise (BLS), and Canada CPI 3.1% (Statistics Canada).
- `fed`: "Hiked in Sept" → 3.75–4.00% after the Sep 16 hike (Fed statement). The next decision is Oct 28, and markets expect a hold with odds of a December hike above 80% (CME FedWatch via Trading Economics). **Refresh the day after Oct 28.**
- `y10`: **Correction.** "Peaked at 5.23% in late Sept, highest since 2007" was superseded: FRED DGS10 shows a 2026 closing high of 5.31% on Oct 5, the highest close since May 2002. The yield was 5.00% on Oct 23. The 2026 start is now 4.19% (FRED), replacing 4.15% (CNN). The `fund` chain was rewritten to match.
- `realy`: "Rising since Feb" → 10-yr TIPS 2.66% on Oct 23, from 1.72% on Feb 27, with a 2.95% peak on Oct 5 (FRED DFII10).
- `gold`: ~$4,114 → ~$4,017 on Oct 26, after a three-month low just under $4,000. The record was $5,608 in January 2026 (Trading Economics, FXStreet). Removed the tier-3 Mitrade fact.
- `credit`: HY OAS 3.29% → 3.38% on Oct 23. It hit 3.40% on Oct 22, the widest since Mar 30 (FRED). CCC 12.78% (tier 3) → 13.56% (FRED BAMLH0A3HYC), wider than at any point since at least 2023. Added CoreWeave bonds near 15% (CNBC, Oct 14).
- `semis`: SOX −11.41% for the week to Oct 16 (tier 3) → SOXX −6% on Oct 22 after Lam Research's supply-constraint warning (Yahoo Finance). The node now states that this leg was a supply squeeze, not weaker demand.
- `aicapex`: Meta $125–145B → $135–145B (Meta Q3 release, Oct 21). Added that free cash flow turned negative (−$2.1B) and the shares fell nearly 7% (CNBC).
- `boc`: hike odds from a tier-3 broker blog → 78% futures odds for Oct 28 and a Reuters poll majority expecting a hike (Yahoo Finance, Oct 26). Jobs −68,000 and 6.5% unemployment are now sourced to Statistics Canada. **Refresh the day after Oct 28.**
- `energy`: XLE +52.6% YTD (tier 3) → +58.14% YTD through Oct 23 (Yahoo Finance). Added FactSet: Q3 blended growth is 29.5%, helped by energy estimate revisions.
- `cad`: "~1.43 then eased" → 1.3993 on Oct 23, down from the 2026 high of 1.4273 on Oct 14 (FRED DEXCAUS).
- `breadth`: replaced the tier-3 Oct 12–16 fact and the unsourced "YTD roughly tied" line with AP's figures for the week to Oct 23: Russell 2000 +2%, S&P 500 −0.5%, Nasdaq −0.7%.
- Edges: `inflation-boc` text now uses 3.1% CPI and the Oct 28 hike pricing. `oil-inflation` adds BLS, `hormuz-oil` adds The National.

Added: nothing. Retired: no nodes or edges. Sources removed as unused: lite, disp, mitrade, tt_credit, cnn_10y, yahoo_hike, mt_wti, oilprice, cnbc_hy, bnn, cnn_meta.

Not re-verified today (all within TTL; `asOf` left at 2026-10-20): `cheapai`, `metacompute`, `issuance`, `overcap`, `sbcorr`, `factor`.

Chains: every script was rewritten with today's numbers. `gold` now uses TIPS 2.66% vs 1.72%, gold near $4,000 against the $5,608 record, and the December hike odds. `quality` drops the tier-3 Goldman +55% and uses the FRED HY/CCC spreads and CoreWeave. `canada` now rests on tier-1/2 numbers (XLE 58%, CPI 3.1%, jobs −68,000, 78% hike odds, USD/CAD below 1.40). `ai` explains that the Oct 22 drop was supply-driven. All three V15 weak-number warnings from v2 are resolved.

Warnings left open:
- V07 `hormuz` event is 240 days old. Kept: October has the most Hormuz attacks of the war, and Houthi strikes on Saudi export routes lifted Brent to a six-month high on Oct 23.
- V07 `metacompute` event is 117 days old. Kept as the origin of the overbuild fear that neocloud debt stress keeps alive; re-assess by 2026-11-15.

Watch next: the Fed and the BoC both decide on Oct 28, so `fed`, `boc`, `cad`, `y10` and `gold` need a refresh on Oct 29. Microsoft, Alphabet and Amazon report this week, which bears on `aicapex`.

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
