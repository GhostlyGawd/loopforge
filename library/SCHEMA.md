# SCHEMA — anatomy of a library entry

Every loop lives at `library/loops/<category-id>/LP-NNNN-slug.md`. IDs are unique,
zero-padded, and never reused (even after deprecation).

## Front matter (YAML, all keys required unless marked optional)

```yaml
---
id: LP-0003
title: Coverage Climber
category: testing            # must exist in categories.json
tier: small                  # micro | small | medium | large | epic
status: draft                # draft | reviewed | canonical | deprecated
version: 0.1.0               # bump patch on edits, minor on behavior change
requires: [git, a test runner with coverage output]
stop_when: coverage in state/coverage.json meets the target set at kickoff
state_files: [state/coverage.json, JOURNAL.md]
tags: [testing, iterative, safety-net]
related: []                  # optional: other LP ids
created: 2026-07-04
updated: 2026-07-04
---
```

## Required body sections, in order

1. `# {title}` — one-paragraph purpose: what it builds/maintains and for whom.
2. `## When to reach for it` — 2–4 bullets of fit and non-fit.
3. `## Setup` — what to create before the first pass (state files, config, spec).
4. `## The Loop Prompt` — ONE fenced block containing the complete prompt, written to
   the QUALITY.md bar. This block is the product; everything else is packaging.
   **Reference-implementation exemption (ADR-006):** a loop whose prompt *is* a live file
   in this repository (e.g. a meta loop pointing at `LOOP.md`) may, instead of duplicating
   it, put a faithful summary of the prompt's shape in the fence plus an explicit pointer to
   the canonical file — so the running system and its library entry can never drift apart.
   This is the ONLY case where the fence may be a pointer rather than the full prompt; every
   other loop inlines a complete, paste-and-run prompt.
5. `## Harness` — the exact shell to run it (see house harness pattern below).
6. `## Stop condition` — how the loop knows it's done and what it does then.
7. `## Failure modes` — the 2–4 most likely ways it goes wrong, and the prompt's
   built-in response to each.
8. `## Variations` — optional; parameterizations worth knowing.
9. `## Review log` — reviewers append scores here; authors never edit it.

> **`## Run it` (rolling out — ADR-007).** A copy-paste slash-command form of the loop: one
> fenced ```` ```markdown ```` block the reader saves as `.claude/commands/<slug>.md`. It
> self-initializes (creates its state file from a template if missing, so `## Setup` becomes
> optional) and is run continuously by Claude Code's built-in `/loop /<slug>` — no shell
> harness needed interactively. Being added to every entry (canon first); becomes a
> gate-required section (validate.py) once all loops carry it, via a follow-up ADR. Until
> then it is optional and un-enforced. The shell `## Harness` remains the headless/CI path.

## House harness pattern

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Always accompanied by the safety note: run unattended loops in a container or dedicated
VM with only the project mounted; git is the undo button. Entries may substitute
`--permission-mode acceptEdits` for supervised runs.
