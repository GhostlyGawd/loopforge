---
id: LP-0017
title: Security Walker
category: code-quality
tier: large
status: draft
version: 0.1.0
requires: [git, a test suite, a SAST/dependency scanner, an app you are authorized to test]
stop_when: every OWASP category in state/security-ledger.json is walked and its findings fixed or accepted
state_files: [state/security-ledger.json, JOURNAL.md]
tags: [security, owasp, hardening, defensive]
related: [LP-0010]
created: 2026-07-05
updated: 2026-07-05
---

# Security Walker

Hardens an application one OWASP category per pass — injection, then broken access control,
then authentication, and so on — finding real issues in that class, fixing them with a
regression test, and logging the rationale. It is defensive by construction: it works only
on code you own and are authorized to test, and it turns "we should do a security review
someday" into a tracked, category-by-category walk with an audit trail.

## When to reach for it
- A web/app codebase you own and are authorized to harden.
- You want steady, documented security progress instead of one overwhelming pentest dump.
- Not a fit: testing systems you don't own or lack written authorization for (out of scope,
  full stop); a formal pentest/red-team engagement (this complements, doesn't replace it).

## Setup
1. Confirm authorization (you own or are cleared to test this app). Get a SAST and a
   dependency/secret scanner running by hand; note the commands.
2. Seed `state/security-ledger.json`:
   ```json
   {
     "scan_command": "<SAST + deps + secret scan>",
     "test_command": "<the suite>",
     "categories": [
       { "owasp": "A01 Broken Access Control", "status": "open" },
       { "owasp": "A03 Injection", "status": "open" }
     ],
     "accepted": []
   }
   ```
   Seed `categories` from the OWASP Top 10 (or your threat model); each starts `open`.

## The Loop Prompt

```
You are one pass of a security-hardening loop. Files are your only memory; assume amnesia.
Scope rule: you operate ONLY on this codebase, which the operator owns/is authorized to test.
Defensive only — you find and FIX weaknesses; you never build or stage an actual attack.

1. Read state/security-ledger.json and the last 30 lines of JOURNAL.md.
2. If every category is fixed/accepted AND scan_command is clean: append "SECURITY WALK
   COMPLETE" to JOURNAL.md, create a STOP file, commit, and exit.
3. Pick ONE "open" OWASP category — prefer highest impact for this app (access control and
   injection usually first). Run scan_command and read the code for THAT class only.
4. Find the real issues in that class (e.g. for injection: unparameterized queries, shelling
   out with user input, unsafe deserialization). For EACH, apply the correct defensive fix —
   parameterized queries, output encoding, authz checks at the boundary, validated input,
   secrets moved to config, least privilege. Fix the root cause, not the symptom; do not
   weaken a check or add a bypass. If a finding is a false positive or an accepted risk,
   record it under "accepted" with a reason and (for accepted risk) a compensating control.
5. Add a regression test that FAILS if the vulnerability returns (an authz test that a
   non-owner is denied; a test that a payload is neutralized). Run test_command — stay green;
   any red you caused is fixed or reverted. Re-run scan_command for that class.
6. Mark the category fixed (or accepted). Append a JOURNAL.md entry: category, issues found,
   fixes, tests added, anything accepted with its reason. Commit: "sec({owasp}): {summary}".
   Stop.

Hard rules: one OWASP category per pass; defensive fixes only, never author an exploit or a
bypass; scope is this owned/authorized codebase only; every fix ships a regression test; an
accepted risk is logged with a reason and a compensating control, never silently ignored;
never commit a real secret — rotate and move it to config if found.
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
undo button. `--permission-mode acceptEdits` when supervising — security fixes change auth and
input handling, so watch early passes. Only ever point this at code you are authorized to test.

## Stop condition
Every category is `fixed`/`accepted` and the scanner is clean for those classes → the loop
writes "SECURITY WALK COMPLETE", creates STOP, halts. Automated scans miss logic flaws;
the walked categories are a documented floor, not a clean bill of health — pair with a human
review or pentest for what tools can't see, and re-walk after major features.

## Failure modes
- **Scope creep / unauthorized targets** → the scope rule pins the loop to the owned codebase;
  it never touches systems it isn't cleared to test.
- **Symptom patching** (input filters instead of parameterization) → root-cause fixes required;
  a blocklist that dodges the scanner without closing the hole doesn't count.
- **Scanner blind spots** (business-logic authz, IDOR) → category-by-category human reading,
  not just SAST output, plus the "pair with a human review" note.
- **Regressions** (a later change reopens a hole) → every fix ships a regression test, so a
  reintroduced vulnerability turns the suite red.

## Variations
- Dependency-CVE mode: swap the class list for `npm audit`/`pip-audit` findings and fix one
  advisory per pass (overlaps LP-0006's security mode — pick one owner).
- Threat-model mode: replace the OWASP list with categories from the app's own threat model.

## Review log
_(reviewers append here)_
