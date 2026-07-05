---
id: LP-0006
title: Dependency Upgrader
category: code-quality
tier: small
status: draft
version: 0.1.1
requires: [git, a package manager, a green test suite]
stop_when: state/deps.json worklist is empty or every remaining item is marked blocked
state_files: [state/deps.json, JOURNAL.md]
tags: [dependencies, upgrade, maintenance, low-risk]
related: [LP-0002, LP-0003]
created: 2026-07-05
updated: 2026-07-05
---

# Dependency Upgrader

Walks a project's outdated dependencies one at a time, upgrading a single package per
pass and running the full test suite between each. The green suite is the gate; a bisected
worklist is the memory. It turns the dreaded "upgrade everything and pray" into a boring,
reversible chore that a loop can grind through overnight.

## When to reach for it
- A project whose dependencies have drifted months or years behind.
- You have a test suite you trust enough to catch a breaking upgrade.
- Not a fit: bumping a single pinned dep by hand (just do it), or a repo with no tests
  (point LP-0003 Coverage Climber at it first — a blind upgrade loop is dangerous).

## Setup
1. Confirm the suite is green by hand and note the exact command.
2. Generate the outdated list once (`npm outdated`, `pip list --outdated`,
   `cargo outdated`, `bundle outdated`, …) and seed `state/deps.json`:
   ```json
   {
     "test_command": "<the command that must pass>",
     "policy": "minor",
     "worklist": [
       { "name": "<pkg>", "from": "<cur>", "to": "<target>", "status": "todo" }
     ],
     "done": []
   }
   ```
   `policy` is one of `patch` | `minor` | `major` — the ceiling a single pass may cross.

## Run it

**One paste, then it loops itself.** Save the block below as `.claude/commands/dependency-upgrader.md`. Run one pass with `/dependency-upgrader`, or loop it with `/loop /dependency-upgrader` (default 10m). It self-initializes on first run.

```markdown
---
description: Dependency Upgrader — upgrade one dependency per pass
---
You are one pass of a dependency-upgrade loop. Files are your only memory; assume you
remember nothing.

0. If state/deps.json does not exist: create it as { "test_command": "", "policy": "minor", "worklist": [], "done": [] }, then STOP and ask me to set test_command and seed the worklist from the outdated list, and re-run.
1. Read state/deps.json and the last 30 lines of JOURNAL.md.
2. If the worklist has no item with status "todo": append "DEPS CLEAN — worklist empty"
   to JOURNAL.md, create a STOP file, commit, and exit.
3. Confirm the baseline is green: run the exact "test_command". If it is already RED
   before you touch anything, do not upgrade — append a note to JOURNAL.md ("baseline
   red, human needed"), create STOP, and exit. Never build on a red baseline.
4. Pick exactly ONE "todo" item — prefer the lowest-risk hop first (patch, then minor,
   then major), and within that the leaf dependencies before the widely-depended-on ones.
   Do not exceed the "policy" ceiling in a single pass; if the only hop available is a
   major and policy forbids it, mark that item "blocked: exceeds policy" and pick another.
5. Upgrade only that one package (edit the manifest / run the manager's targeted upgrade),
   then reinstall the lockfile. Change nothing else.
6. Run "test_command".
   - GREEN: move the item to "done" with its new version; if the changelog notes a
     required code change you made, say what and why in the journal.
   - RED: revert the manifest and lockfile (git checkout -- <files>), mark the item
     "blocked: <one-line reason from the failure>". Do NOT try to fix product code to
     accommodate the upgrade in this pass — that is a separate, deliberate task.
7. Append a JOURNAL.md entry: package, from→to, GREEN/BLOCKED, anything learned.
8. Commit: "deps({name}): {from}→{to}" (green) or "deps({name}): blocked — {reason}".
   One package, one commit. Stop.

Hard rules: one package per pass; never upgrade past the policy ceiling; a red suite —
baseline or post-upgrade — always means revert, never force; a package that blocks twice
stays blocked until a human or a dedicated pass clears it.
```

For fully unattended runs outside an interactive session, use the shell loop in `## Harness`.

## The Loop Prompt

```
You are one pass of a dependency-upgrade loop. Files are your only memory; assume you
remember nothing.

1. Read state/deps.json and the last 30 lines of JOURNAL.md.
2. If the worklist has no item with status "todo": append "DEPS CLEAN — worklist empty"
   to JOURNAL.md, create a STOP file, commit, and exit.
3. Confirm the baseline is green: run the exact "test_command". If it is already RED
   before you touch anything, do not upgrade — append a note to JOURNAL.md ("baseline
   red, human needed"), create STOP, and exit. Never build on a red baseline.
4. Pick exactly ONE "todo" item — prefer the lowest-risk hop first (patch, then minor,
   then major), and within that the leaf dependencies before the widely-depended-on ones.
   Do not exceed the "policy" ceiling in a single pass; if the only hop available is a
   major and policy forbids it, mark that item "blocked: exceeds policy" and pick another.
5. Upgrade only that one package (edit the manifest / run the manager's targeted upgrade),
   then reinstall the lockfile. Change nothing else.
6. Run "test_command".
   - GREEN: move the item to "done" with its new version; if the changelog notes a
     required code change you made, say what and why in the journal.
   - RED: revert the manifest and lockfile (git checkout -- <files>), mark the item
     "blocked: <one-line reason from the failure>". Do NOT try to fix product code to
     accommodate the upgrade in this pass — that is a separate, deliberate task.
7. Append a JOURNAL.md entry: package, from→to, GREEN/BLOCKED, anything learned.
8. Commit: "deps({name}): {from}→{to}" (green) or "deps({name}): blocked — {reason}".
   One package, one commit. Stop.

Hard rules: one package per pass; never upgrade past the policy ceiling; a red suite —
baseline or post-upgrade — always means revert, never force; a package that blocks twice
stays blocked until a human or a dedicated pass clears it.
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
the undo button. Use `--permission-mode acceptEdits` when supervising — upgrades are a good
loop to watch the first few passes of, because ecosystems break in surprising ways.

## Stop condition
Every worklist item is either `done` or `blocked` → the loop writes "DEPS CLEAN", creates
STOP, and halts. To continue later, regenerate the outdated list into the worklist, clear
STOP, and re-run. Blocked items are a deliberate to-do list for a human or a major-upgrade pass.

## Failure modes
- **Green suite, broken runtime** (tests miss a real regression) → keep hops small (patch/
  minor first) and one-per-commit so `git bisect` and revert are trivial; widen coverage
  with LP-0003 before raising `policy` to `major`.
- **Transitive/lockfile churn** → upgrade one direct dependency at a time and commit the
  lockfile with it; never hand-edit transitive pins.
- **A major that needs code changes** → not this loop's job; mark `blocked` with the
  reason and let a human or a scoped migration pass own the code change.
- **Flaky tests masquerading as breakage** → a package that blocks twice with different
  failures is a flake signal; note it and send LP (flake-hunter) after it.

## Variations
- Security-only mode: seed the worklist from `npm audit` / `pip-audit` and set
  `policy: "major"` — patching a CVE outranks the risk ceiling.
- Grouped mode: for tightly-coupled families (e.g. a framework and its plugins), treat the
  group as one worklist item upgraded and tested together.

## Review log
_(reviewers append here)_
