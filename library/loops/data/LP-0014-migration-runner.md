---
id: LP-0014
title: Migration Runner
category: data
tier: medium
status: draft
version: 0.1.1
requires: [git, a migration tool, a disposable dev/staging database to apply against]
stop_when: every migration in state/migrations.json is applied and verified — none pending
state_files: [state/migrations.json, JOURNAL.md]
tags: [database, migration, schema, reversible]
related: [LP-0007]
created: 2026-07-05
updated: 2026-07-05
---

# Migration Runner

Works through a queue of schema/data migrations one per pass, each written with a forward
(`up`) and reverse (`down`) step, applied against a disposable database, and confirmed by a
verification query before it is accepted. Reversibility is proven by actually rolling back
and re-applying — not assumed. Applied migrations are immutable history; new intent always
becomes a new migration.

## When to reach for it
- Evolving a database schema (or backfilling data) in ordered, reviewable steps.
- You have a migration tool and a throwaway database you can freely apply/roll back against.
- Not a fit: ad-hoc one-off SQL in production (that's not a loop); a database with no
  migration tooling or no safe environment to test against (set those up first).

## Setup
1. Confirm the migration tool runs against a disposable dev/staging DB (never prod). Note
   the up/down/status commands.
2. Seed `state/migrations.json` from your planned changes:
   ```json
   {
     "db_url_env": "DEV_DATABASE_URL",
     "up_command": "<apply next migration>",
     "down_command": "<roll back one migration>",
     "status_command": "<show applied/pending>",
     "planned": [
       { "name": "add_users_email_index", "intent": "index users.email", "status": "pending" }
     ],
     "done": []
   }
   ```

## Run it

**One paste, then it loops itself.** Save the block below as `.claude/commands/migration-runner.md`. Run one pass with `/migration-runner`, or loop it with `/loop /migration-runner` (default 10m). It self-initializes on first run.

```markdown
---
description: Migration Runner — apply one reversible migration per pass
---
You are one pass of a migration loop. Files are your only memory; assume amnesia.
You operate ONLY against the disposable database in {db_url_env} — never a production DB.

0. If state/migrations.json does not exist: confirm a migration tool runs against a DISPOSABLE dev database, then create state/migrations.json as { "db_url_env": "DEV_DATABASE_URL", "up_command": "", "down_command": "", "status_command": "", "planned": [], "done": [] }; STOP and ask me to set the commands + planned migrations, and re-run. Never target production.
1. Read state/migrations.json and the last 30 lines of JOURNAL.md. Run "status_command" to
   see what is actually applied (reconcile drift between the ledger and the DB before acting).
2. If no migration is "pending": append "MIGRATIONS CURRENT" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Take the FIRST "pending" migration (order matters — never skip ahead). Write it as a new
   migration file with BOTH an `up` and a `down`. Never edit a migration that is already in
   "done" or already applied — if a past migration was wrong, add a new corrective migration.
4. Apply it: run "up_command". Then PROVE reversibility: run "down_command" (it must cleanly
   reverse), then "up_command" again. If down fails or leaves residue, the migration is not
   safe — fix the down step or mark the migration "blocked: irreversible — <reason>" and stop.
5. Verify the intent with a concrete check: a query/assertion that the schema or data is now
   as intended (index exists, column nullable, rows backfilled). A migration that "ran" but
   didn't achieve its intent is not done. Run the app's test/build if migrations affect it.
6. Move the migration to "done" (record the file name and the verification used). Append a
   JOURNAL.md entry: name, intent, up/down summary, verification result. Commit:
   "migrate({name}): {intent}". Stop.

Hard rules: one migration per pass, in order; every migration has a tested up AND down;
applied/done migrations are immutable — corrections are new migrations; verify the intent,
not just that it ran; operate only on the disposable DB; an irreversible migration is
"blocked:" with a reason, never forced.
```

For fully unattended runs outside an interactive session, use the shell loop in `## Harness`.

## The Loop Prompt

```
You are one pass of a migration loop. Files are your only memory; assume amnesia.
You operate ONLY against the disposable database in {db_url_env} — never a production DB.

1. Read state/migrations.json and the last 30 lines of JOURNAL.md. Run "status_command" to
   see what is actually applied (reconcile drift between the ledger and the DB before acting).
2. If no migration is "pending": append "MIGRATIONS CURRENT" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Take the FIRST "pending" migration (order matters — never skip ahead). Write it as a new
   migration file with BOTH an `up` and a `down`. Never edit a migration that is already in
   "done" or already applied — if a past migration was wrong, add a new corrective migration.
4. Apply it: run "up_command". Then PROVE reversibility: run "down_command" (it must cleanly
   reverse), then "up_command" again. If down fails or leaves residue, the migration is not
   safe — fix the down step or mark the migration "blocked: irreversible — <reason>" and stop.
5. Verify the intent with a concrete check: a query/assertion that the schema or data is now
   as intended (index exists, column nullable, rows backfilled). A migration that "ran" but
   didn't achieve its intent is not done. Run the app's test/build if migrations affect it.
6. Move the migration to "done" (record the file name and the verification used). Append a
   JOURNAL.md entry: name, intent, up/down summary, verification result. Commit:
   "migrate({name}): {intent}". Stop.

Hard rules: one migration per pass, in order; every migration has a tested up AND down;
applied/done migrations are immutable — corrections are new migrations; verify the intent,
not just that it ran; operate only on the disposable DB; an irreversible migration is
"blocked:" with a reason, never forced.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Run unattended loops in a container or dedicated VM with only the project and a DISPOSABLE
database mounted; git is the undo button for the files, and the down-migration is the undo
button for the schema. Never point `db_url_env` at production. `--permission-mode acceptEdits`
when supervising — schema changes deserve watching.

## Stop condition
Every planned migration is `done` or `blocked` → the loop writes "MIGRATIONS CURRENT",
creates STOP, and halts. The output is an ordered, each-reversible migration set proven
against a real database. Add new planned migrations and clear STOP to keep evolving the schema.

## Failure modes
- **Editing an applied migration** (history rewrite that desyncs environments) → banned;
  applied migrations are immutable, corrections are new migrations.
- **Untested `down`** (a rollback that doesn't roll back) → step 4 actually runs down then
  up; a down that fails blocks the migration instead of shipping a lie.
- **"Ran" but wrong** (migration applied but intent unmet) → the verification query in step 5
  checks the intent, not just exit code.
- **Touching production** → the loop is pinned to a disposable DB via `db_url_env`; the prompt
  refuses any other target.

## Variations
- Data-backfill mode: the `up` backfills/repairs rows in batches and `down` is a documented
  no-op or inverse; verification asserts row-level correctness and counts.
- Expand/contract mode: split a breaking change into an additive migration now and a
  destructive one later, each its own pass, so deploys stay zero-downtime.

## Review log
_(reviewers append here)_
