---
id: LP-0004
title: Docs Gardener
category: docs
tier: medium
status: draft
version: 0.1.0
requires: [git, a docs directory, the codebase the docs describe]
stop_when: a full audit pass finds zero broken claims in state/docs-audit.md
state_files: [state/docs-audit.md, JOURNAL.md]
tags: [documentation, drift, maintenance]
related: [LP-0002]
created: 2026-07-04
updated: 2026-07-04
---

# Docs Gardener

Keeps documentation truthful against a moving codebase. Alternates between auditing
(finding claims that drifted from reality) and mending (fixing one drifted claim per
pass, verified against the code).

## When to reach for it
- Docs exist but nobody trusts them.
- After a big refactor or API change.
- Not a fit: writing docs from zero (use a builder loop with a docs spec instead).

## Setup
Create `state/docs-audit.md` with sections `## Unverified`, `## Broken`, `## Fixed`.
List every doc file under `## Unverified`.

## The Loop Prompt

```
You are one pass of a docs-gardening loop. Files are your only memory.

1. Read state/docs-audit.md and the last 30 lines of JOURNAL.md.
2. Mode select:
   - If ## Broken has entries → MEND mode.
   - Else if ## Unverified has entries → AUDIT mode.
   - Else → run one final skim of the newest 5 commits for doc-relevant changes; if
     none, append "GARDEN CLEAN" to the audit file, create STOP, commit, exit.
3. AUDIT mode: take ONE file from ## Unverified. Check every testable claim in it
   against the actual code (commands run? flags exist? examples execute? names match?).
   Move the file to ## Fixed if clean, or list each broken claim under ## Broken with
   file, claim, and evidence. Do not fix anything in this mode.
4. MEND mode: take ONE claim from ## Broken. Determine the truth from the code, fix the
   doc (or the code, if the doc describes intended behavior the code lost — say which
   and why in the journal). Verify examples by running them where possible. Move the
   claim to ## Fixed.
5. Append a JOURNAL.md entry. Commit: "docs(audit|mend): {what}". Stop.

Hard rules: one file audited or one claim mended per pass; never delete a doc to
"fix" it without recording the deletion rationale under ## Fixed; examples that can run
must be run.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Container or dedicated VM for unattended runs.

## Stop condition
Both queues empty and a final commit-skim clean → GARDEN CLEAN, STOP created. Re-seed
`## Unverified` any time to garden again.

## Failure modes
- **Doc vs code: which is right?** → prompt forces an explicit call with reasoning in
  the journal; a human can veto between runs.
- **Unrunnable examples** (need creds, external services) → verified by inspection and
  flagged `unverifiable:` rather than silently trusted.
- **Audit finds hundreds of breaks** → fine; MEND mode metabolizes them one per pass.

## Variations
- Point it at README-only for a quick truthfulness pass.
- Inverse mode: audit code comments against behavior instead of docs.

## Review log
_(reviewers append here)_
