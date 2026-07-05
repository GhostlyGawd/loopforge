# CLAUDE.md — standing instructions for any Claude Code session in this repo

This repository is a self-running system. Its full protocol is `LOOP.md`; its laws are
in `charter/`. Whether you arrived via `loop.sh`, the `/loop` command, or an interactive
session, these rules bind you:

## Map
- `LOOP.md` — the iteration protocol (the product's engine)
- `charter/` — vision, roles, quality rubric, brand rules
- `state/` — STATE.json, BACKLOG.md, JOURNAL.md (append-only), DECISIONS.md (ADRs)
- `library/` — SCHEMA.md, categories.json, loops/<category>/LP-NNNN-*.md, generated INDEX.md
- `tools/` — validate.py and build.py: both must pass before ANY commit
- `site/` — generated catalog page (never edit by hand; template lives in tools/build.py)
- `reviews/` — review passes and audits (append-only)

## Non-negotiables (digest of LOOP.md hard rules)
1. One task, one commit, one journal entry per iteration.
2. `python3 tools/validate.py && python3 tools/build.py` green before every commit.
3. JOURNAL, DECISIONS, and reviews are append-only history.
4. Changes to LOOP.md, loop.sh, or tools/ require a prior-iteration ADR (two-iteration rule).
5. Library entries follow `library/SCHEMA.md` exactly — no placeholders, everything runnable.
6. Stay inside this repo; write nothing outside it.
7. A file named `STOP` at root means: journal one line, exit.

When in doubt, do less, write it down, and let the next iteration continue.
