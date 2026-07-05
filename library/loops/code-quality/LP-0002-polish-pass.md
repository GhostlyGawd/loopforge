---
id: LP-0002
title: Polish Pass
category: code-quality
tier: micro
status: canonical
version: 0.1.2
requires: [git, project linter/formatter, test suite]
stop_when: a full sweep of the codebase finds nothing above the "worth fixing" bar
state_files: [state/polish-ledger.md, JOURNAL.md]
tags: [refactor, lint, tidy, low-risk]
related: [LP-0004, LP-0006, LP-0007, LP-0010]
created: 2026-07-04
updated: 2026-07-05
---

# Polish Pass

The janitor loop. Each pass fixes exactly one small blemish — a lint warning, a dead
import, a confusing name, a missing docstring — verified by tests, logged in a ledger.
Cheap, safe, and endlessly repeatable.

## When to reach for it
- A codebase that works but accumulated grime.
- Overnight runs where you want strictly low-risk improvement.
- Not a fit: structural refactors (use a medium/large loop with a design file).

## Setup
Create `state/polish-ledger.md` with two sections: `## Fixed` and `## Declined (and
why)`. Ensure the linter and test suite run clean-ish; note the baseline in the ledger.

## The Loop Prompt

```
You are one pass of a polish loop. Files are your only memory.

1. Read state/polish-ledger.md and the last 20 lines of JOURNAL.md.
2. Find ONE small blemish not already in the ledger: linter warning, dead code, unclear
   name, missing docstring on a public function, magic number, inconsistent formatting.
   Prefer the highest-confidence, lowest-blast-radius fix available.
3. If a full skim of linter output and the codebase surfaces nothing above the
   "worth fixing" bar, append "SWEEP CLEAN" to the ledger, create STOP, commit, exit.
4. Fix it. Behavior must not change: run the test suite; any red means revert.
5. Log it under ## Fixed (file, what, why). If you considered and rejected a fix,
   log that under ## Declined so future passes skip it.
6. Append a one-line JOURNAL.md entry. Commit: "polish: {what}". Stop.

Hard rules: one blemish per pass; no behavior changes; no new dependencies; anything
requiring judgment about product behavior goes to ## Declined, not into code.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Container or dedicated VM for unattended runs; `--permission-mode acceptEdits` when
supervising. This loop is the classic first unattended run — blast radius is tiny.

## Stop condition
A pass that finds nothing worth fixing declares SWEEP CLEAN and creates STOP.

## Failure modes
- **Endless bikeshedding** → the ledger's Declined section is binding; once declined,
  skip forever unless a human deletes the line.
- **Sneaky behavior change** → test gate + revert rule.
- **Ledger bloat** → acceptable; it is the loop's memory and audit trail.

## Variations
- Scope to a directory: add "only under src/legacy/" to step 2.
- Docstring-only mode, rename-only mode: constrain the blemish menu.

## Review log
- review-001 (i8, Lens): re-entrancy 5 · one-step 5 · memory 5 · stop 4 · guardrails 5 · copy-paste 5 → avg 4.83. draft → reviewed. Canonical candidate; stop bar is judgment-based but bounded by the Declined ledger. Full pass: reviews/review-001.md.
- review-003 (i18, Lens): independent canonical smoke-read; scores held, Declined-ledger pattern validated. reviewed -> canonical. See reviews/review-003.md.
