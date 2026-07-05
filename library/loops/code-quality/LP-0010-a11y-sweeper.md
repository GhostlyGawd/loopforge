---
id: LP-0010
title: A11y Sweeper
category: code-quality
tier: small
status: draft
version: 0.1.1
requires: [git, a running web app, an accessibility linter or axe-core]
stop_when: every WCAG issue class in state/a11y-ledger.json is cleared or accepted, none open
state_files: [state/a11y-ledger.json, JOURNAL.md]
tags: [accessibility, a11y, wcag, web, incremental]
related: [LP-0002]
created: 2026-07-05
updated: 2026-07-05
---

# A11y Sweeper

Fixes one class of accessibility issue per pass across a web app — all the missing alt
text, then all the unlabeled inputs, then the contrast failures — rather than one element
at a time. Working by issue *class* means each pass ships a coherent, reviewable fix and a
reusable pattern, and the ledger records both what was fixed and the rule the team should
follow going forward.

## When to reach for it
- A web UI that works but was built without accessibility in mind.
- You want steady, auditable WCAG progress instead of a single overwhelming a11y sprint.
- Not a fit: a design-system overhaul (structural — needs a design pass first); native apps
  without a DOM/axe-style tooling story (bring an equivalent auditor first).

## Setup
1. Get an automated auditor running once by hand (axe-core, `eslint-plugin-jsx-a11y`,
   Lighthouse a11y, or `pa11y`) and note the command and the URLs/routes it covers.
2. Seed `state/a11y-ledger.json`:
   ```json
   {
     "audit_command": "<command that lists violations by rule>",
     "routes": ["/", "/login", "..."],
     "classes": [
       { "rule": "image-alt", "status": "open" },
       { "rule": "label", "status": "open" },
       { "rule": "color-contrast", "status": "open" }
     ],
     "accepted": []
   }
   ```
   `status` is one of `open` | `fixed` | `accepted`.

## Run it

**One paste, then it loops itself.** Save the block below as `.claude/commands/a11y-sweeper.md`. Run one pass with `/a11y-sweeper`, or loop it with `/loop /a11y-sweeper` (default 10m). It self-initializes on first run.

```markdown
---
description: A11y Sweeper — fix one WCAG issue class per pass
---
You are one pass of an accessibility loop. Files are your only memory; assume amnesia.

0. If state/a11y-ledger.json does not exist: get an accessibility auditor running, then create state/a11y-ledger.json as { "audit_command": "", "routes": [], "classes": [], "accepted": [] }; STOP and ask me to set audit_command + routes and seed classes from the audit's rule list, and re-run.
1. Read state/a11y-ledger.json and the last 30 lines of JOURNAL.md.
2. Run "audit_command" across the routes. If it reports zero violations AND every class in
   the ledger is fixed/accepted: append "A11Y SWEEP CLEAN" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Pick ONE "open" issue CLASS (one WCAG rule) — prefer the one that most blocks assistive-
   tech users: keyboard traps and focus order, then names/labels, then text alternatives,
   then contrast. If the audit surfaces a class not yet in the ledger, add it as open and
   you may take it.
4. Fix EVERY instance of that one class across the routes — real semantic fixes, not
   suppressions: alt text that describes purpose (empty alt for decorative), a real
   <label>/aria-label, native semantics or correct ARIA, a visible focus style, a contrast
   ratio that actually meets 4.5:1 (3:1 for large text). Never silence a rule with an
   ignore comment to make the audit pass; if a finding is a genuine false positive, move it
   to "accepted" with a one-line reason instead.
5. Verify: re-run "audit_command"; that rule must now report zero across the routes. Do a
   quick manual sanity check for the class — tab to it for focus/keyboard, confirm the
   accessible name in the a11y tree. Run the app's test/build so you didn't break rendering.
6. Update the ledger (class → fixed, or false positives → accepted with reason). Append a
   JOURNAL.md entry: rule, instances fixed, the pattern to reuse, before/after counts.
   Commit: "a11y({rule}): fix {N} instances". Stop.

Hard rules: one issue class per pass; fix the cause with real semantics, never suppress or
ignore a rule to green the audit; contrast/keyboard fixes must be verified, not assumed; a
false positive is "accepted" with a reason, never hidden.
```

For fully unattended runs outside an interactive session, use the shell loop in `## Harness`.

## The Loop Prompt

```
You are one pass of an accessibility loop. Files are your only memory; assume amnesia.

1. Read state/a11y-ledger.json and the last 30 lines of JOURNAL.md.
2. Run "audit_command" across the routes. If it reports zero violations AND every class in
   the ledger is fixed/accepted: append "A11Y SWEEP CLEAN" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Pick ONE "open" issue CLASS (one WCAG rule) — prefer the one that most blocks assistive-
   tech users: keyboard traps and focus order, then names/labels, then text alternatives,
   then contrast. If the audit surfaces a class not yet in the ledger, add it as open and
   you may take it.
4. Fix EVERY instance of that one class across the routes — real semantic fixes, not
   suppressions: alt text that describes purpose (empty alt for decorative), a real
   <label>/aria-label, native semantics or correct ARIA, a visible focus style, a contrast
   ratio that actually meets 4.5:1 (3:1 for large text). Never silence a rule with an
   ignore comment to make the audit pass; if a finding is a genuine false positive, move it
   to "accepted" with a one-line reason instead.
5. Verify: re-run "audit_command"; that rule must now report zero across the routes. Do a
   quick manual sanity check for the class — tab to it for focus/keyboard, confirm the
   accessible name in the a11y tree. Run the app's test/build so you didn't break rendering.
6. Update the ledger (class → fixed, or false positives → accepted with reason). Append a
   JOURNAL.md entry: rule, instances fixed, the pattern to reuse, before/after counts.
   Commit: "a11y({rule}): fix {N} instances". Stop.

Hard rules: one issue class per pass; fix the cause with real semantics, never suppress or
ignore a rule to green the audit; contrast/keyboard fixes must be verified, not assumed; a
false positive is "accepted" with a reason, never hidden.
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
the undo button. `--permission-mode acceptEdits` when supervising — a11y fixes touch real
markup, so watching the first passes catches over-eager ARIA.

## Stop condition
Audit reports zero violations and every class is `fixed`/`accepted` → the loop writes
"A11Y SWEEP CLEAN", creates STOP, and halts. Automated audits catch ~30–50% of WCAG issues;
the ledger's cleared classes are a floor, not a certificate — schedule a human/AT audit for
the rest, and re-run this loop after new features land.

## Failure modes
- **Suppressing instead of fixing** (ignore comments, `role="presentation"` to dodge a rule)
  → explicitly banned; the only non-fix path is "accepted" with a written reason.
- **ARIA overuse** (redundant or wrong ARIA that harms AT) → prefer native semantics; ARIA
  only when native won't do, and verify the accessible name/role in the a11y tree.
- **Automated-audit blind spots** (meaningful alt text, logical focus order, real keyboard
  operability) → the manual sanity check in step 5 plus the "schedule a human audit" note.
- **Contrast "fixes" that fail** → verify the actual ratio against WCAG thresholds, don't
  eyeball it.

## Variations
- Single-route mode: constrain `routes` to one page for a tightly-scoped first sweep.
- Component-library mode: point it at a Storybook and fix each class at the component
  source so every consumer inherits the fix.

## Review log
_(reviewers append here)_
