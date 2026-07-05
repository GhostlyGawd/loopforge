---
id: LP-0015
title: Type Tightener
category: code-quality
tier: small
status: draft
version: 0.1.0
requires: [git, a static type checker, a test suite]
stop_when: no loose/any type remains in state/types-ledger.json scope, or all remaining are justified
state_files: [state/types-ledger.json, JOURNAL.md]
tags: [types, static-analysis, refactor, safety]
related: [LP-0002]
created: 2026-07-05
updated: 2026-07-05
---

# Type Tightener

Replaces one loose type per pass — an `any`, an untyped param, a too-wide union, a missing
return type — with the most precise type the checker can prove, verified by a clean type
check and a green test suite. Each pass shrinks the "unsafe surface" a little and records
why any remaining looseness is intentional. Boring, safe, and endlessly repeatable, like a
type-focused Polish Pass.

## When to reach for it
- A typed codebase (TS, Python+mypy, etc.) that leaks `any`/`Any` or untyped edges.
- You want steady, low-risk type coverage without a big-bang annotation sprint.
- Not a fit: an untyped codebase with no checker configured (set that up first); designing a
  complex generic API (that's deliberate design work, not a sweep).

## Setup
1. Get the type checker running clean-ish by hand; note the command and current error/`any` count.
2. Seed `state/types-ledger.json`:
   ```json
   {
     "check_command": "<runs the type checker, reports any/errors>",
     "test_command": "<runs the suite>",
     "sites": [ { "where": "src/api.ts:42 param `data`", "kind": "any", "status": "open" } ],
     "justified": []
   }
   ```
   Seed `sites` from the checker's `any`/implicit-any/missing-annotation report; each `open`.

## The Loop Prompt

```
You are one pass of a type-tightening loop. Files are your only memory; assume amnesia.

1. Read state/types-ledger.json and the last 30 lines of JOURNAL.md.
2. Run "check_command". If it is clean and no site is "open": append "TYPES TIGHT" to
   JOURNAL.md, create a STOP file, commit, and exit.
3. Pick ONE "open" site — prefer the widest blast radius (exported/public signatures, then
   shared utilities, then leaves). If the report shows a site not in the ledger, add it.
4. Replace the loose type with the MOST PRECISE type the checker can prove — infer from
   usage, follow the value's real shape, introduce a named type/interface if it clarifies.
   Do NOT use `any`, `unknown`-and-cast, or `@ts-ignore`/`# type: ignore` to "win"; if the
   value is genuinely dynamic, type it honestly (`unknown` with a real narrowing guard) or
   mark the site "justified" with a reason. Change types only — no behavior changes.
5. Verify BOTH: run "check_command" (must have zero NEW errors and one fewer loose site) and
   "test_command" (must stay green — a type change that breaks a test revealed a real bug or
   a wrong annotation; fix the annotation, or the bug if it's real and say so). Revert on red.
6. Move the site to done (or "justified"). Append a JOURNAL.md entry: site, old→new type,
   anything learned about the code. Commit: "types({where}): {any→precise}". Stop.

Hard rules: one site per pass; never suppress the checker (`any`/ignore/blind cast) to pass;
no behavior changes; a genuinely dynamic value is typed honestly or "justified" with a
reason; the test suite stays green.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Run unattended loops in a container or dedicated VM with only the project mounted; git is the
undo button. `--permission-mode acceptEdits` when supervising. Tiny blast radius — a good
early unattended loop, like Polish Pass for types.

## Stop condition
Checker clean and every site `done`/`justified` → the loop writes "TYPES TIGHT", creates
STOP, halts. Tighten the checker config (enable `strict`, ban implicit any) and re-seed to
climb further.

## Failure modes
- **Suppression masquerading as a fix** (`any`, `@ts-ignore`, blind casts) → explicitly
  banned; the only non-fix path is "justified" with a written reason.
- **A "type fix" that changes behavior** → types-only rule + the test gate; any red reverts.
- **Over-narrowing** (a type too tight for real inputs) → verify against real call sites; if
  callers legitimately pass more shapes, the honest type is the wider one, not a lie.
- **Endless justified list** → acceptable and intended; it is the audit trail of deliberate
  dynamic edges, and the stop condition counts them as resolved.

## Variations
- Strictness-ratchet mode: each "clean" milestone enables one stricter compiler flag and
  re-seeds, so the type floor only ever rises.
- Public-API-only mode: constrain `sites` to exported signatures for a high-value first pass.

## Review log
_(reviewers append here)_
