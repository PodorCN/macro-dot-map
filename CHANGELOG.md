# Changelog

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
