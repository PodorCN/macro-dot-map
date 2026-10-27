# Changelog

## 2026-10-27 (version 3, fixes for reviews 2026-10-27-002, -003 and -004)
**Released 2026-10-27** after review 2026-10-27-005 PASS (RELEASE OK, content hash b1992750…04b7). Open for the next update:
- Major (L-019): cite a source for "talks were first reported on Oct 6" on `issuance` (InvestingLive, Oct 7, on the FT report), or drop the clause.
- Minors:
  - Source "competes with neoclouds" / "a competitor" in `credit`/`quality`, and keep Musk's claim attributed to him.
  - The `ai` script's "momentum is crowded" is reasoning; mark it as such or source it.
  - The Anthropic IPO size still rests on The Herald Business.
  - Re-verify CNBC Sep 26 (`cnbc_10y`).
- The Fed and BoC decide Oct 28; refresh on Oct 29.

v3 failed review twice on Oct 27: 2026-10-27-001 (Meta's Oct 26 stock offering missing) and 2026-10-27-002 (Anthropic's Oct 26 IPO filing missing), both L-010; review 2026-10-27-003 then failed it for missing the debt side of AI funding (L-010) and two `ai` script problems (L-017, L-018); review 2026-10-27-004 failed it for a timing error in the `fund` script (L-017 again). AGENT.md section 10 says to stop after two FAILs in a day. **Max explicitly overrode that stop** ("keep fixing"), so this run continues with a full sweep. The data is rebuilt from release a1b264d by replaying the scripted edits in `reviews/updates/2026-10-26/` (`sh reviews/updates/2026-10-26/replay.sh` reproduces `data/map.json` exactly), so a diff against the previous draft shows only the reviewed fixes. Data as of Oct 26.

Sweep to 2026-10-26:
- Geopolitics and oil: Oct 26 Houthis claimed strikes on Saudi East-West pumping stations (Reuters); Brent settled $115.81 on Oct 26 after a six-month high of $116.72 on Oct 23. Zacks (Oct 26) also tied the Oct 23 spike to reports of a possible renewed US/Israeli strike on Iran; the map keeps The National's Houthi framing, which names the cause directly. On `hormuz`/`oil` (Oct 23 settle kept as the headline).
- Inflation: US Sept CPI 3.7% (BLS, Oct 14); UMich 1-yr 4.7% final (Oct 23); Canada Sept CPI 3.1% (Oct 19). US PCE is due Oct 30, after asOf. On `inflation`.
- Fed: Oct 27–28 meeting; hold expected and Dec hike odds above 80% (CME FedWatch via TE, Oct 26). On `fed`.
- Bank of Canada: Oct 28 decision; ~81% hike odds (InvestingLive, Oct 25); Reuters poll Oct 21–23 (19 of 34 expect a hike). On `boc`.
- Rates: 10-yr 5.00% on Oct 23 (FRED; Oct 26 not yet posted, ~4.98% intraday); TIPS 2.66% on Oct 23; Oct 26 $69B 2-year auction tailed 0.3 bp with indirect bidders at 45.7% (InvestingLive, C−). On `y10`/`realy`/`issuance`.
- Credit: HY OAS 3.38% and CCC 13.56% on Oct 23 (FRED, latest posted); CoreWeave bonds near 15% in mid-October. On `credit`.
- FX and gold: USD/CAD 1.3993 on Oct 23 (FRED); gold ~$4,017 on Oct 26 after a three-month low (TE). On `cad`/`gold`.
- Equities: Oct 26 S&P 500 +0.70% and Nasdaq +0.83% as Anthropic's IPO filing lifted tech; SOX +2.82% on Oct 26 and −12.2% from Sep 30 to Oct 26 (Investing.com data). Week to Oct 23: S&P −0.5%. On `semis`.
- Factors: Oct 22 investors rotated into defensive sectors and Treasuries as the Nasdaq fell 2.6% (Investing.com); RSP +3.5% vs S&P 500 −0.4% over the month to late October (Seeking Alpha); Q3 value/quality beat momentum (Confluence). On `breadth`/`factor`.
- AI: equity side, Oct 26 Anthropic filed for a Nasdaq IPO (ANT) reportedly seeking up to $100B, and Meta launched ~$35B of stock offerings (SEC); debt side, Oct 25 Musk said SpaceX closed $40B of GPU debt (talks first reported Oct 6) and that debt markets have almost shut for firms without substantial revenue outside AI data centers (InvestingLive, The Next Web); chips, Oct 22 Lam supply warning and Oct 19 DeepSeek update. On `aicapex`/`issuance`/`credit`/`overcap`/`semis`/`cheapai`.
- Portfolio: 20-day SPY–TLT correlation −0.24 at the Oct 23 close, after −0.30 on Oct 22 (RIA, Oct 24). On `sbcorr`.
- Earnings: FactSet Oct 23: Q3 blended growth 29.5% with 24% reported; Meta Q3 on Oct 21. Microsoft, Alphabet and Amazon report after asOf. On `energy`/`aicapex`.

Fix for review 2026-10-27-004:
- **Blocker (L-017, V20):** the `fund` script no longer credits the 10-year's Oct 5 peak to SpaceX's deal. Talks were first reported Oct 6 and the deal was announced Oct 25. The script now gives the peak to heavy borrowing for the build-out (the `issuance` facts), then says the funding has widened since: SpaceX's debt, Meta's stock sale and Anthropic's IPO.
- Minors:
  - `issuance`: the say line and value no longer call SpaceX's private debt "bonds", and the SpaceX fact gives the Oct 6 date.
  - Musk's wording now includes "substantial", and the `credit` fact says he competes with neoclouds. In `quality`, his reason (revenue concentration) is kept apart from "higher rates".
  - `ai`: the stated causes (oil, rates, AI-payoff doubts) apply only to the eight-session streak they describe. The `semis-factor` mechanism is spelled out: momentum is crowded in AI winners, so lean to equal weight and quality as it unwinds.
  - The scripted edits are now committed (`reviews/updates/2026-10-26/`).
  - The Anthropic IPO size ("reportedly up to $100B") rests on The Herald Business (tier 2, an AI-assisted translation of its own reporting). Nasdaq.com and NPR versions could not be opened. The ticker and revenue rest on Yahoo Finance.
  - AGENT.md §1 lists V20.

Warnings left open: V07 `hormuz` is 241 days old. Kept: October has the most Hormuz attacks of the war, and claimed Houthi strikes on Saudi export routes lifted Brent to a six-month high on Oct 23.

Fix for review 2026-10-27-003:
- **Blocker (L-010):** the debt side of AI funding is now on the map.
  - `issuance` adds SpaceX's $40B GPU debt (Oct 25) and the soft $69B 2-year auction (Oct 26).
  - `credit` adds Musk's warning that debt markets have "almost entirely shut off" money for firms without revenue outside AI data centers.
  - The `fund` script names both sides (equity: Meta, Anthropic; debt: SpaceX).
  - The `quality` script adds Musk's warning.
- **Major (L-017):** the `ai` script no longer credits the SOX streak to cheap-model doubts. It uses the source's own causes: oil, rates and doubts that AI spending will pay off.
- **Major (L-018):** the `ai` script covers all four edges again, including `semis-factor`, and ends with the implication (equal weight, quality over momentum).
- Minors:
  - `semis` now has a period return: SOX −12.2% from Sep 30 to Oct 26 and −15.7% over the eight-session streak (Investing.com historical data).
  - `overcap` asOf is Oct 26, and its say line reflects the counterpoint.
  - The `oil` fact no longer says "front-month", because The National doesn't name the contract.
  - AGENT.md §1 and §9 now document V17–V19 and the sweep log.
  - The regeneration claim is now precise (replayed scripts).

Fix for review 2026-10-27-002:
- **Blocker (L-010):** Anthropic's Oct 26 IPO filing is now on `aicapex` (replacing the duplicate bond-issuance fact, which stays on `issuance`) and on `overcap` as a counterpoint. `semis` now shows the Oct 26 rebound (SOX +2.82%).
  - Re-tested the `ai` chain: the demand doubt cuts both ways, and Anthropic's filing lifted chips.
  - Re-tested the `fund` chain: its funding mix now includes Meta's stock sale and the Anthropic IPO.
- Minors:
  - `semis` now has a period measure: eight straight SOX losses to Oct 16, the longest since 2008 (24/7 Wall St.). All its numbers use one index (SOX); the only percentage figures found were for SOXX or from tier-3 sites.
  - The changelog no longer says "regenerated" for an incremental commit: this run was regenerated from a1b264d in full.
  - `proactive_meta` stays tier 2 (named publisher), and the fact also rests on the SEC filing.
  - `cnbc_10y` and `bbg_ds` facts are unchanged and within their freshness limits.

Earlier on Oct 27 (fixes for reviews 2026-10-26-002 and 2026-10-27-001), kept in this version:
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
