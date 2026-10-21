# REVIEWER.md — Reviewing a Macro Dot Map update

You are the **reviewer**. Nothing is released unless you write a review record with `verdict: PASS` for the exact content you checked. Your standard is the current map: small, clean, every number traceable, every link explainable. If an update makes the map harder to read or less rigorous, it fails, even if every fact is true.

You did not write this update. Do not ask the updater for its reasoning. Judge only what is in the repository.

---

## 1. Setup

1. Read `AGENT.md` so you know the rules the updater had to follow.
2. Read `reviews/LESSONS.md` in full. You will check every lesson.
3. Read the previous review record in `reviews/records/` and the newest `CHANGELOG.md` entry.
4. See what changed: `git diff <last release tag> -- data/map.json src/ scripts/`.

---

## 2. Review procedure, in order

### Step A — Mechanical gate

Run:
```
python3 scripts/build.py
python3 scripts/validate.py
```
- Any ERROR is a **blocker**.
- Every WARN must be justified in the changelog. An unjustified WARN is a **major** finding.
- Every FLAG names a lesson. Open the flagged text and confirm it obeys that lesson's rule. List the lesson ID under `lessons_acknowledged` only after you checked it.
- If `scripts/` or `src/` changed, read the diff line by line. Any change that loosens a check, raises a cap or hides content is a **blocker** unless the changelog gives a design reason you agree with.

### Step B — Fact check

- **Every changed or added number, date and name**: open its source URL and confirm the source says it, for the date claimed. Quote the supporting words (under 15 words) in your record.
- **Spot check**: also verify at least 3 unchanged facts chosen at random, including at least one from a chain script.
- Check the tier assigned to each new source against the tier list in `AGENT.md` section 3.
- Check `basis`: `sourced` only if a tier-1/2 source says it; `weak` if only tier 3; `unsourced` for our reasoning. A wrong basis is a **blocker**.
- Check `asOf` values are honest: the fact must have been re-verified on that date.

### Step C — Logic check (the dots)

For each new or changed edge:
- Does it pass the four tests in `AGENT.md` 4.1 (mechanism, sentence, sign, evidence)?
- Is the sign right for the direction the chain describes?
- Does a sourced edge's source actually state the causal link, not just the two facts?

For each chain:
- Read the script aloud. Is it about 60 seconds, does it open with the conclusion, follow the edges in order, and end with an implication?
- Does every claim in it appear in the chain's nodes or edges?
- Does the story still hold given today's data? A chain that describes last week's market is a **blocker**.

### Step D — Additions and retirements

- For each added node: check the four gates and the score in the changelog (`AGENT.md` section 6). Is it really better than the weakest existing node? If the map would read just as well without it, it is a **major** finding.
- For each retired item: was the reason valid, and was everything that depended on it removed or rewritten?
- For what was **not** retired: is any node past its real relevance even if within TTL? Is every `keepReason` still true today?
- Did today's research miss a major driver that a PM would expect? (Example from the past: a Fed hike left out of the story.) Missing a top-3 driver of the week is a **major** finding.

### Step E — Readability

Run `python3 scripts/render_check.py --shots <scratch dir>`. Any failure is a **blocker**. Then open the screenshots (desktop about 1300px and phone about 400px, light and dark) and check by eye. If Playwright is not available, render the page by hand and set `render_check: manual` in your record. Check:
- No overlapping boxes, lines through boxes, overlapping +/− markers, or clipped text.
- The map is no denser than the previous release unless the additions earned it.
- Each panel reads cleanly: headline value, facts, driven by, drives, script, sources.
- Plain English, short sentences, units and periods stated.

### Step F — Lessons

Go through **every** lesson in `LESSONS.md`. For each one, check the update does not repeat it, and list its ID under `lessons_checked`. A repeat of any lesson is a **blocker**.

---

## 3. Severity and verdict

| Severity | Examples | Effect |
|---|---|---|
| **Blocker** | Validator error. Wrong number, date or attribution. Wrong basis or tier. Stale fact presented as current. Chain that no longer matches the market. Lines or markers overlapping. A repeated lesson. A weakened check. | **FAIL** |
| **Major** | Unjustified warning. Addition that does not earn its place. Missing a top-3 driver. Unclear or misleading wording. Script that runs long or buries the conclusion. | **FAIL** if 2 or more, or if any major from the previous review is still unfixed |
| **Minor** | Small wording or style polish. | Record it; does not block |

**PASS** only if there are no blockers and the major rule is met. Being "mostly right" is not a pass: the update must be regenerated (see `AGENT.md` section 10).

---

## 4. Write the review record

Create `reviews/records/YYYY-MM-DD-NNN.md` from `reviews/TEMPLATE.md`. NNN counts reviews that day (001, 002). The front matter is machine-read by `release_check.py`:

```
---
review_id: YYYY-MM-DD-NNN
content_hash: <from validate.py output>
verdict: PASS or FAIL
reviewer: <who you are>
lessons_checked: [L-001, L-002, ...every lesson ID...]
lessons_acknowledged: [<lesson IDs flagged by validate.py that you checked>]
new_lessons: [<IDs you added, or empty>]
render_check: auto or manual
---
```

The `content_hash` must be the hash printed by `validate.py` for the exact files you reviewed. If anything changes after your review, the hash changes and the gate blocks release until a new review is written.

Never edit or delete an old record. A FAIL record stays in history even after a later PASS.

---

## 5. Keeping mistakes from coming back

Every blocker or major finding goes through this loop:

1. **Match it** to an existing lesson in `LESSONS.md`.
2. **New mistake:** add a lesson `L-NNN` with: what happened, the rule, the guard, the date first seen, occurrences = 1. The guard is one of:
   - a validator check (best: add it to `scripts/validate.py` with a new or existing V-code),
   - a pattern in `reviews/lesson_patterns.json` (for risky phrasings that need a human look),
   - a manual checklist line in Step B–E above (only when it cannot be automated).
3. **Repeated mistake:** increase the occurrence count, and **upgrade the guard one level** (manual → pattern → validator check). A lesson that has recurred twice must have an automated validator check. Upgrading the guard is part of the review, not optional.
4. If you add or change a validator check, run it against the **last released** data too. If the released map fails your new check, record that as a finding for the next update.
5. Commit `LESSONS.md`, `lesson_patterns.json` and any validator change together with your review record.

This loop is why `release_check.py` requires `lessons_checked` to list every lesson: each review re-checks the whole history of mistakes, not just today's diff.
