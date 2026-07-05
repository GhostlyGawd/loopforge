# review-004 — systemic finding: copy-paste truth is under-delivered (i26, reviewer "Lens")

Not a per-entry pass — a cross-library finding on QUALITY.md axis 6 (**copy-paste truth:
"runs as pasted; includes its harness, prerequisites, and setup; no hidden assumptions"**).

## Finding
All 17 entries score well on axes 1–5 but every one of them *fails the spirit of axis 6*.
To actually run any loop today, a reader must:
1. Read the `## Setup` prose and hand-create the state file it names.
2. Copy the `## The Loop Prompt` block into a separate `PROMPT.md`.
3. Wire up the `## Harness` shell `while` loop.

That is assembly, not copy-paste. The VISION promise — "copy it, run it, trust it" — is not
met by a single copy.

## What changed the calculus
Claude Code natively supports **slash commands** (`.claude/commands/<name>.md`) and a
**built-in `/loop [interval] /<name>`** that re-runs a command on an interval and continues
on its own (default 10m). So a loop packaged as a command needs **no shell harness** in an
interactive session — `/loop /<name>` *is* the loop. The shell `## Harness` is still correct,
but it is the *headless/CI* path (via `claude -p`), not the only one. The library was written
before this was leveraged.

## Proposal
Ship each loop as a self-contained, self-initializing slash command (a `## Run it` section).
Recorded as **ADR-007** (proposed; the `build.py` render is a two-iteration change).

## Score impact (deferred)
No re-scores this pass. Once entries carry a working `## Run it` command form, their axis-6
scores should rise, and several `reviewed` loops become genuine `canonical` candidates on the
strength of true one-paste runnability. Re-score after the rollout.
