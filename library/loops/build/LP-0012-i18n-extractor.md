---
id: LP-0012
title: i18n Extractor
category: build
tier: medium
status: draft
version: 0.1.1
requires: [git, an i18n framework wired up, a test/build that catches broken renders]
stop_when: no in-scope component in state/i18n-ledger.json still holds a hardcoded user-facing string
state_files: [state/i18n-ledger.json, JOURNAL.md]
tags: [i18n, localization, strings, incremental, build]
related: [LP-0010]
created: 2026-07-05
updated: 2026-07-05
---

# i18n Extractor

Externalizes hardcoded user-facing strings into a translation catalog, one component (or
screen) per pass. Each pass moves a coherent set of strings behind stable keys, swaps in
the framework's translation call, and verifies the UI still renders identically in the
default locale — turning "internationalize the whole app" into a tracked, low-risk sweep.

## When to reach for it
- An app with an i18n library installed but strings still hardcoded in the markup.
- You want translation-readiness grown safely without a big-bang refactor.
- Not a fit: choosing/wiring an i18n framework from scratch (do that first, by hand); apps
  with no test or visual check to confirm the default locale is unchanged.

## Setup
1. Confirm the i18n framework works: one string already renders through `t("key")` in the
   default locale. Note the catalog path (e.g. `locales/en.json`) and the key convention.
2. Seed `state/i18n-ledger.json`:
   ```json
   {
     "catalog": "locales/en.json",
     "verify_command": "<test/build/visual check for the default locale>",
     "components": [
       { "path": "src/components/Header.tsx", "status": "pending" }
     ],
     "accepted": []
   }
   ```
   List in-scope components; each starts `pending`. `accepted` holds intentional non-strings.

## Run it

**One paste, then it loops itself.** Save the block below as `.claude/commands/i18n-extractor.md`. Run one pass with `/i18n-extractor`, or loop it with `/loop /i18n-extractor` (default 10m). It self-initializes on first run.

```markdown
---
description: i18n Extractor — externalize one component's strings per pass
---
You are one pass of an i18n-extraction loop. Files are your only memory; assume amnesia.

0. If state/i18n-ledger.json does not exist: confirm the i18n framework renders one t("key"), then create state/i18n-ledger.json as { "catalog": "locales/en.json", "verify_command": "", "components": [], "accepted": [] }; STOP and ask me to set verify_command and list in-scope components, and re-run.
1. Read state/i18n-ledger.json and the last 30 lines of JOURNAL.md.
2. If no component is "pending": append "I18N SWEEP CLEAN" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Pick ONE "pending" component. Find every user-facing hardcoded string in it: visible
   text, labels, placeholders, aria-labels, titles, alt text, error/toast messages.
   IGNORE non-user strings: keys, enum values, test ids, class names, log lines, URLs.
4. For each, add a stable, namespaced key to the catalog (e.g. "header.signIn") with the
   current English text as the value, and replace the literal with the framework's
   translation call. Handle interpolation and pluralization with the framework's features,
   never string concatenation. Keep keys meaningful (by role, not by English words, so a
   copy tweak doesn't churn the key). If a "string" is genuinely not translatable (a brand
   name, a code sample), leave it and record it under "accepted" with a reason.
5. Verify: run "verify_command". The default locale must render EXACTLY as before — same
   text, same layout. Any diff you caused is a bug: fix it (usually a missed interpolation
   or a wrong key). Do not change wording while extracting; extraction is not copy-editing.
6. Mark the component "done". Append a JOURNAL.md entry: component, strings extracted, keys
   added, anything left "accepted". Commit: "i18n({component}): extract {N} strings". Stop.

Hard rules: one component per pass; never change the visible default-locale text while
extracting; no string concatenation for sentences (use interpolation/plurals); non-user
strings stay hardcoded; an untranslatable literal is "accepted" with a reason, not forced.
```

For fully unattended runs outside an interactive session, use the shell loop in `## Harness`.

## The Loop Prompt

```
You are one pass of an i18n-extraction loop. Files are your only memory; assume amnesia.

1. Read state/i18n-ledger.json and the last 30 lines of JOURNAL.md.
2. If no component is "pending": append "I18N SWEEP CLEAN" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Pick ONE "pending" component. Find every user-facing hardcoded string in it: visible
   text, labels, placeholders, aria-labels, titles, alt text, error/toast messages.
   IGNORE non-user strings: keys, enum values, test ids, class names, log lines, URLs.
4. For each, add a stable, namespaced key to the catalog (e.g. "header.signIn") with the
   current English text as the value, and replace the literal with the framework's
   translation call. Handle interpolation and pluralization with the framework's features,
   never string concatenation. Keep keys meaningful (by role, not by English words, so a
   copy tweak doesn't churn the key). If a "string" is genuinely not translatable (a brand
   name, a code sample), leave it and record it under "accepted" with a reason.
5. Verify: run "verify_command". The default locale must render EXACTLY as before — same
   text, same layout. Any diff you caused is a bug: fix it (usually a missed interpolation
   or a wrong key). Do not change wording while extracting; extraction is not copy-editing.
6. Mark the component "done". Append a JOURNAL.md entry: component, strings extracted, keys
   added, anything left "accepted". Commit: "i18n({component}): extract {N} strings". Stop.

Hard rules: one component per pass; never change the visible default-locale text while
extracting; no string concatenation for sentences (use interpolation/plurals); non-user
strings stay hardcoded; an untranslatable literal is "accepted" with a reason, not forced.
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
the undo button. `--permission-mode acceptEdits` when supervising — extraction touches real
markup, so watching early passes catches over-eager replacement of non-user strings.

## Stop condition
Every in-scope component is `done` (or its strings `accepted`) → the loop writes "I18N SWEEP
CLEAN", creates STOP, and halts. The catalog is now translation-ready: hand `locales/en.json`
to translators for other locales. Re-seed `components` after new UI lands and clear STOP.

## Failure modes
- **Wording drift during extraction** (silently "improving" copy) → banned; the default
  locale must render identically. Copy changes are a separate, deliberate task.
- **Over-extraction** (keys, enums, log lines) → the "user-facing only" rule + the `accepted`
  list keep non-user strings hardcoded and the catalog clean.
- **Concatenated sentences** (untranslatable in many languages) → interpolation/plural rules
  required; grammatical order and plurals differ across locales.
- **Key churn** (keys named after English text) → keys are named by role, so re-wording a
  string doesn't rename its key and break every locale.

## Variations
- Extract-and-pseudolocalize: add a pseudo-locale that accents/pads every value, so a later
  visual pass surfaces untranslated leftovers and layouts that break on longer strings.
- Framework-native mode: for message-extraction toolchains (e.g. FormatJS/gettext), run the
  extractor after each pass so the catalog is generated, not hand-maintained.

## Review log
_(reviewers append here)_
