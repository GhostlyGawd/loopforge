---
id: LP-0001
title: Spec-to-App Builder
category: build
tier: large
status: draft
version: 0.1.0
requires: [git, a written spec, the project's runtime and test tooling]
stop_when: every requirement in SPEC.md is checked off in state/progress.md and the full test suite passes
state_files: [SPEC.md, state/progress.md, state/decisions.md, JOURNAL.md]
tags: [greenfield, spec-driven, app]
related: [LP-0003]
created: 2026-07-04
updated: 2026-07-04
---

# Spec-to-App Builder

Turns a written specification into a working application, one requirement per pass.
The spec is the contract; the progress file is the memory; the test suite is the judge.

## When to reach for it
- You can write down what "done" looks like before starting.
- The work decomposes into independently shippable requirements.
- Not a fit: exploratory prototyping where the spec would change every pass — write the
  spec first, or use a smaller loop to draft the spec.

## Setup
1. Write `SPEC.md`: numbered requirements (R1, R2, …), each independently verifiable.
2. Create `state/progress.md` listing every requirement as `- [ ] R{n}: {summary}`.
3. Create empty `state/decisions.md` and `JOURNAL.md`.
4. `git init` if needed; commit the spec before the first pass.

## The Loop Prompt

```
You are one pass of a build loop. You have no memory of previous passes; the files are
your memory.

1. Read SPEC.md, state/progress.md, state/decisions.md, and the last 40 lines of
   JOURNAL.md.
2. If all requirements in state/progress.md are checked: run the full test suite once
   more; if green, append "DONE — all requirements met" to JOURNAL.md, create a file
   named STOP, commit, and exit.
3. Otherwise pick the SINGLE unchecked requirement with the fewest unmet dependencies.
   If it is too large for one pass, split it into sub-items in state/progress.md and
   take the first.
4. Implement it completely: code + tests proving it. Follow existing project
   conventions; record any architectural choice in state/decisions.md with one line of
   reasoning.
5. Run the test suite. If red because of your work, fix it; if you cannot within this
   pass, revert your changes and log the failure in JOURNAL.md with a diagnosis.
6. Check the requirement off in state/progress.md. Append to JOURNAL.md: pass summary,
   files touched, test result.
7. Commit: "build(R{n}): {summary}". Then stop. Do not start another requirement.

Hard rules: one requirement per pass; never weaken a test to pass it; never leave the
suite red at commit; if the same requirement failed the last 2 passes, mark it
"blocked:" in state/progress.md with a diagnosis and take a different one.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Run inside a container or dedicated VM with only the project mounted; git is the undo
button. For supervised runs, substitute `--permission-mode acceptEdits`.

## Stop condition
All requirements checked and suite green → the loop itself creates `STOP`, so the
harness halts. Resume later by deleting STOP and adding requirements to the spec.

## Failure modes
- **Spec ambiguity** → the prompt records interpretation in state/decisions.md rather
  than stalling; humans review decisions between runs.
- **Circular blocked requirements** → `blocked:` markers accumulate; the harness
  operator (or an audit pass) resolves the knot in the spec.
- **Test-suite rot** → rule "never weaken a test" forces fixes into code, not tests.

## Variations
- Prepend a design pass: first N passes may only write `state/architecture.md`.
- Swap "fewest unmet dependencies" for strict spec order when sequence matters.

## Review log
_(reviewers append here)_
