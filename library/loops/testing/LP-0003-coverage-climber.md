---
id: LP-0003
title: Coverage Climber
category: testing
tier: small
status: reviewed
version: 0.1.1
requires: [git, test runner with coverage reporting]
stop_when: coverage meets the target recorded in state/coverage.json
state_files: [state/coverage.json, JOURNAL.md]
tags: [testing, coverage, safety-net]
related: [LP-0001]
created: 2026-07-04
updated: 2026-07-05
---

# Coverage Climber

Raises real test coverage one meaningful test file at a time. Targets the riskiest
untested code first, and refuses to game the metric.

## When to reach for it
- A codebase you're afraid to change because nothing is tested.
- Before pointing a bigger build/refactor loop at the project.
- Not a fit: projects with no runnable test infrastructure yet (set that up first).

## Setup
1. Get coverage running once by hand; note the command.
2. Create `state/coverage.json`:
   `{ "target": 80, "current": <baseline>, "command": "<coverage command>", "worklist": [] }`

## The Loop Prompt

```
You are one pass of a coverage loop. Files are your only memory.

1. Read state/coverage.json and the last 30 lines of JOURNAL.md.
2. If current >= target: append "TARGET MET at {current}%" to JOURNAL.md, create STOP,
   commit, exit.
3. Run the coverage command. Update "current". Pick ONE untested-or-thin module — the
   one where a bug would hurt most (entry points, money paths, data mutation) — that is
   not marked blocked in the worklist.
4. Write real behavioral tests for it: happy path, one edge, one failure. Test observed
   behavior, not implementation details. If you must read deeply to understand the
   module, write what you learned as docstrings/comments — that's part of the value.
5. Run the full suite. Any red you caused: fix your tests (never the code under test,
   unless the test found a genuine bug — then fix the bug and say so loudly in the
   journal).
6. Re-run coverage; update state/coverage.json (current + append module to worklist as
   done). Append a JOURNAL.md entry: module, coverage before → after, anything learned.
7. Commit: "test({module}): {before}%→{after}%". Stop.

Hard rules: one module per pass; no asserting on private internals; no deleting or
skipping existing tests; a module that resists twice gets "blocked:" in the worklist
with a diagnosis.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Container or dedicated VM for unattended runs; git is the undo button.

## Stop condition
`current >= target` in state/coverage.json → announce, create STOP, halt. Raise the
target and delete STOP to keep climbing.

## Failure modes
- **Metric gaming** (trivial asserts) → "behavioral tests, not implementation" rule +
  reviewer spot checks between runs.
- **Legacy module too tangled** → blocked marker with diagnosis; a refactor loop
  (LP-0002 or larger) clears the path.
- **Coverage tool flakiness** → command is pinned in state; failures land in journal
  rather than silently skewing numbers.

## Variations
- Diff-coverage mode: only climb coverage on files changed since a given tag.
- Mutation-testing mode: swap the metric for mutation score.

## Review log
- review-001 (i8, Lens): re-entrancy 5 · one-step 5 · memory 5 · stop 5 · guardrails 5 · copy-paste 5 → avg 5.00. draft → reviewed. Strong canonical candidate; wants only the independent smoke-read. Full pass: reviews/review-001.md.
