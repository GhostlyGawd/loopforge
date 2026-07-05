---
id: LP-0005
title: Library Grower
category: meta
tier: epic
status: reviewed
version: 0.1.1
requires: [git, a charter defining quality, a schema for entries, validate/build tooling]
stop_when: never by design — milestones advance, the loop continues (halt with STOP)
state_files: [state/STATE.json, state/BACKLOG.md, state/JOURNAL.md, state/DECISIONS.md]
tags: [meta, self-organizing, curation, multi-role]
related: [LP-0001, LP-0002]
created: 2026-07-04
updated: 2026-07-05
---

# Library Grower

The loop that grows a curated library — of prompts, patterns, recipes, components,
anything entry-shaped — by rotating one agent through company roles: builder, reviewer,
librarian, designer, auditor, scout. **This repository is the reference implementation:
the loop you are reading about is the loop that maintains the file you are reading.**

## When to reach for it
- You want a collection that stays organized, reviewed, and on-brand without a human
  curating it daily.
- The entries can be schema-validated mechanically.
- Not a fit: one-shot content generation (that's a builder loop, not a company).

## Setup
Stand up the four pillars before the first pass:
1. **Charter** — vision, roles with standing work, a scoring rubric, brand rules.
2. **Schema** — front matter + required sections every entry must satisfy.
3. **State** — STATE.json (iteration, phase, role_queue), BACKLOG, JOURNAL, DECISIONS.
4. **Gates** — a validator and an index/site builder that must pass before any commit.

(Cloning this repository and gutting `library/loops/` is a legitimate setup.)

## The Loop Prompt

The complete prompt is `LOOP.md` at this repository's root — kept there, not inlined
here, so the running system and its library entry can never drift apart. Its shape:

```
0. Orient: read STATE, journal tail, backlog. Honor STOP.
1. Claim: bump iteration; take the next role (bootstrap checklist, or pop role_queue).
2. Choose ONE task: red build > P0 > role-fit backlog > role's standing work.
3. Execute to the rubric's bar; half-done work gets reverted, not committed.
4. Gate: validator + builder must pass. Never leave the repo red.
5. Record: backlog, journal entry, ADR if a structural decision was made.
6. Commit once: "loop(i{n}/{role}): {what}".
7. Exit. The harness restarts you.

Self-modification only via the two-iteration rule: one pass proposes (ADR), a later
pass implements.
```

## Harness

```bash
./loop.sh 25        # this repo's harness: max iterations, STOP file, run logs,
                    # consecutive-failure cutoff, sandbox acknowledgment
```

Or the house pattern with `claude -p "$(cat LOOP.md)"`. Unattended runs belong in a
container or dedicated VM.

## Stop condition
Intentionally none. A library is a garden, not a building. Milestones (see the
charter's VISION) mark maturity; `touch STOP` halts; deleting STOP resumes.

## Failure modes
- **Backlog sprawl** → per-iteration cap on new items; scout role gatekeeps ideas.
- **Quality drift** → reviewer cadence baked into the role cycle; promotion ladder
  requires a non-author smoke-read.
- **Runaway self-modification** → two-iteration ADR rule; journal + one-commit-per-pass
  keep every change auditable.
- **Role starvation** (all building, no curating) → the default cycle is law; the
  auditor checks journal role distribution and flags drift.

## Variations
- Recipe box, design-pattern catalog, component gallery: swap the schema and rubric,
  keep the machine.
- Multi-agent: run N harnesses on branches; a merge-role iteration reconciles.

## Review log
- review-001 (i8, Lens): re-entrancy 5 · one-step 5 · memory 5 · stop 4 · guardrails 5 · copy-paste 3 → avg 4.50. draft → reviewed. Held at the floor: prompt is by-reference to LOOP.md (copy-paste 3) and stop is 'never by design' (4). See review-001 seeds. Full pass: reviews/review-001.md.
