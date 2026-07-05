---
id: LP-0007
title: Data Janitor
category: data
tier: small
status: draft
version: 0.1.0
requires: [git, a dataset the loop can load, a profiling library or SQL access]
stop_when: every column in state/data-ledger.json is marked clean, accepted, or blocked
state_files: [state/data-ledger.json, JOURNAL.md]
tags: [data, cleaning, profiling, reproducible]
related: [LP-0002]
created: 2026-07-05
updated: 2026-07-05
---

# Data Janitor

Cleans a dataset one column (or field) at a time. Each pass profiles a single column,
proposes one cleaning rule, applies it as reproducible code — never as a manual edit to
the data — and logs the before/after. The rules file becomes an auditable, re-runnable
cleaning pipeline; the raw data is never mutated in place.

## When to reach for it
- A messy CSV / table / dataframe you need to trust before analysis or loading.
- Any place a reproducible, reviewable cleaning pipeline beats one-off manual fixes.
- Not a fit: one-off exploratory cleanup you will throw away; streaming/online data where
  a batch pass has no stable snapshot to profile.

## Setup
1. Put an immutable snapshot at `data/raw/` (read-only — the loop never writes here).
2. Create the transform entry point `clean.py` (or `clean.sql`) that reads `data/raw/`,
   applies every rule in order, and writes `data/clean/`. It starts as a no-op passthrough.
3. Seed `state/data-ledger.json`:
   ```json
   {
     "source": "data/raw/<file>",
     "output": "data/clean/<file>",
     "columns": [
       { "name": "<col>", "status": "pending" }
     ],
     "rules": []
   }
   ```
   Fill `columns` from the header; every column starts `pending`.

## The Loop Prompt

```
You are one pass of a data-cleaning loop. Files are your only memory; assume amnesia.
The raw snapshot in data/raw/ is READ-ONLY — you may never edit data by hand.

1. Read state/data-ledger.json and the last 30 lines of JOURNAL.md.
2. If no column has status "pending": append "DATA CLEAN — all columns resolved" to
   JOURNAL.md, create a STOP file, commit, and exit.
3. Pick exactly ONE "pending" column — prefer the one whose dirtiness is most likely to
   corrupt downstream use (keys, join fields, money, dates, categoricals with typos).
4. Profile only that column: row count, null/blank rate, distinct values, min/max/outliers
   for numerics, format variants for strings/dates, and 3–5 concrete offending examples.
   Write what you found to the journal — the profile IS part of the deliverable.
5. Decide ONE of:
   - a cleaning rule (trim, canonicalize case, parse to a type, map typo→canonical, clip
     an impossible range, flag-not-drop bad rows). Encode it as reproducible code in the
     transform (clean.py/clean.sql) and append it to "rules" with a plain-English note.
     Mark the column "clean".
   - "accept": the column is already fine or its quirks are meaningful. Add no rule; mark
     it "accepted" with a one-line reason.
   Never drop rows silently and never impute values without recording the assumption.
6. Re-run the transform end to end (raw → clean). It MUST run green and be deterministic:
   running it twice on the raw snapshot produces byte-identical output. If your rule makes
   the pipeline non-deterministic or errors, revert the rule and mark the column
   "blocked: <reason>".
7. Append a JOURNAL.md entry: column, what was wrong (with counts), rule applied or why
   accepted, rows affected. Commit: "data({column}): {rule summary}". Stop.

Hard rules: one column per pass; raw data is read-only; every change is code in the
transform, never a manual data edit; no silent row drops or imputations; a column that
resists twice becomes "blocked:" with a diagnosis.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Run unattended loops in a container or dedicated VM with only the project mounted; git is
the undo button. `--permission-mode acceptEdits` for supervised runs. Because the raw
snapshot is read-only and every fix is code, even a bad pass costs only a revert.

## Stop condition
Every column is `clean`, `accepted`, or `blocked` → the loop writes "DATA CLEAN", creates
STOP, and halts. The output is not just clean data but `clean.py`/`clean.sql` plus the
`rules` ledger: a reproducible, reviewable pipeline you can re-run on the next data drop.

## Failure modes
- **Manual data edits** (the cardinal sin) → raw/ is read-only and every fix must be code;
  a pass that can't express a fix as code marks the column `blocked` instead.
- **Silent row loss** → "flag, don't drop" rule; dropping requires an explicit, journaled
  decision and a preserved count of what was removed.
- **Non-deterministic cleaning** (random tie-breaks, unstable sorts) → the twice-identical-
  output check in step 6 fails the pass and forces a revert.
- **Over-cleaning meaningful quirks** → the `accept` path exists precisely so the loop can
  decide a column's oddity is signal, not noise, and record why.

## Variations
- SQL mode: the transform is a versioned `clean.sql` of idempotent `UPDATE`/`INSERT … 
  SELECT` steps into a staging table; the ledger tracks columns the same way.
- Great-Expectations mode: pair each rule with an assertion so the pipeline also grows a
  validation suite as it cleans.

## Review log
_(reviewers append here)_
