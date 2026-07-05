---
id: LP-0009
title: Changelog Scribe
category: docs
tier: micro
status: draft
version: 0.1.1
requires: [git, a CHANGELOG.md following Keep a Changelog (or permission to create one)]
stop_when: the cursor in state/changelog-state.json has reached HEAD — no unwritten history remains
state_files: [state/changelog-state.json, JOURNAL.md]
tags: [changelog, docs, git-history, keep-a-changelog]
related: [LP-0004]
created: 2026-07-05
updated: 2026-07-05
---

# Changelog Scribe

Reconstructs and then maintains a `CHANGELOG.md` from git history, one release (or one
batch of unreleased commits) per pass. It walks history forward from a saved cursor,
translating raw commits into human-facing "what changed and why it matters" entries in the
Keep a Changelog format — never just pasting commit subjects. The cursor is the memory, so
the same range is never written twice.

## When to reach for it
- A project with real git history but a missing, stale, or commit-dump changelog.
- Ongoing upkeep: run it after each release to keep the log current.
- Not a fit: repos with no meaningful history or squashed single-commit imports (nothing
  to reconstruct); marketing release notes (this writes a technical changelog).

## Setup
1. Ensure a `CHANGELOG.md` exists with a `## [Unreleased]` section at the top (create the
   Keep a Changelog skeleton if absent).
2. Seed `state/changelog-state.json`:
   ```json
   {
     "cursor": "<oldest commit sha to start from, or the repo root>",
     "tag_pattern": "v*",
     "written_ranges": []
   }
   ```
   `cursor` advances toward HEAD as ranges are written; `tag_pattern` identifies releases.

## Run it

**One paste, then it loops itself.** Save the block below as `.claude/commands/changelog-scribe.md`. Run one pass with `/changelog-scribe`, or loop it with `/loop /changelog-scribe` (default 10m). It self-initializes on first run.

```markdown
---
description: Changelog Scribe — reconstruct the CHANGELOG one release range per pass
---
You are one pass of a changelog loop. Files are your only memory; assume amnesia.

0. If state/changelog-state.json does not exist: ensure CHANGELOG.md has a "## [Unreleased]" skeleton, then create state/changelog-state.json as { "cursor": "<oldest sha or repo root>", "tag_pattern": "v*", "written_ranges": [] }; STOP and confirm the cursor, and re-run.
1. Read state/changelog-state.json, the last 20 lines of JOURNAL.md, and the top of
   CHANGELOG.md.
2. Determine the next unwritten range. List tags matching tag_pattern in commit order.
   The next range is (cursor .. next-tag-after-cursor]; if no tag lies ahead of the
   cursor, the range is (cursor .. HEAD] and its entries go under "## [Unreleased]".
3. If cursor already equals HEAD and there are no new commits: append "CHANGELOG CURRENT"
   to JOURNAL.md, create a STOP file, commit, and exit.
4. Read the commits in that ONE range (git log with bodies). Group changes into Keep a
   Changelog buckets — Added / Changed / Deprecated / Removed / Fixed / Security — and
   write each as a human-facing line: what changed and why it matters to a user, not the
   raw commit subject. Collapse noise (merge commits, "fix typo", "wip") rather than
   transcribing it. Link issues/PRs if the messages reference them.
5. Insert the section in the right place: a tagged range becomes "## [x.y.z] - <date>"
   (use the tag's own commit date, never today's date for a past release) placed above
   older releases; an untagged range fills "## [Unreleased]". Never rewrite or reorder
   existing released sections — only add.
6. Advance cursor to the end of the range; append the range to written_ranges.
7. Append a JOURNAL.md entry: range covered, version/section, commit count summarized.
   Commit: "changelog: {version or 'unreleased'} ({N} commits)". Stop.

Hard rules: one range per pass; never fabricate a change you cannot trace to a commit;
never edit an already-published released section (append-only below Unreleased); past
releases are dated by their tag, not by the day you wrote them; commit noise is summarized,
not transcribed.
```

For fully unattended runs outside an interactive session, use the shell loop in `## Harness`.

## The Loop Prompt

```
You are one pass of a changelog loop. Files are your only memory; assume amnesia.

1. Read state/changelog-state.json, the last 20 lines of JOURNAL.md, and the top of
   CHANGELOG.md.
2. Determine the next unwritten range. List tags matching tag_pattern in commit order.
   The next range is (cursor .. next-tag-after-cursor]; if no tag lies ahead of the
   cursor, the range is (cursor .. HEAD] and its entries go under "## [Unreleased]".
3. If cursor already equals HEAD and there are no new commits: append "CHANGELOG CURRENT"
   to JOURNAL.md, create a STOP file, commit, and exit.
4. Read the commits in that ONE range (git log with bodies). Group changes into Keep a
   Changelog buckets — Added / Changed / Deprecated / Removed / Fixed / Security — and
   write each as a human-facing line: what changed and why it matters to a user, not the
   raw commit subject. Collapse noise (merge commits, "fix typo", "wip") rather than
   transcribing it. Link issues/PRs if the messages reference them.
5. Insert the section in the right place: a tagged range becomes "## [x.y.z] - <date>"
   (use the tag's own commit date, never today's date for a past release) placed above
   older releases; an untagged range fills "## [Unreleased]". Never rewrite or reorder
   existing released sections — only add.
6. Advance cursor to the end of the range; append the range to written_ranges.
7. Append a JOURNAL.md entry: range covered, version/section, commit count summarized.
   Commit: "changelog: {version or 'unreleased'} ({N} commits)". Stop.

Hard rules: one range per pass; never fabricate a change you cannot trace to a commit;
never edit an already-published released section (append-only below Unreleased); past
releases are dated by their tag, not by the day you wrote them; commit noise is summarized,
not transcribed.
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
the undo button. `--permission-mode acceptEdits` when supervising. A pure-docs loop with no
code changes — very low blast radius.

## Stop condition
`cursor == HEAD` with no new commits → the loop writes "CHANGELOG CURRENT", creates STOP,
and halts. After the next release, clear STOP and re-run: it resumes from the cursor and
writes only the new range.

## Failure modes
- **Commit-subject transcription** (a changelog nobody reads) → the "what changed and why
  it matters, not the raw subject" rule and the Added/Changed/Fixed grouping force
  translation into human terms.
- **Rewriting shipped history** → released sections are append-only; only "## [Unreleased]"
  and new sections above older ones may be touched.
- **Wrong dates on old releases** → past releases are stamped from their tag's commit date,
  never the day the entry was written.
- **Ambiguous or messy commits** → summarize and, where a change's user impact is unclear,
  say so plainly rather than inventing a benefit.

## Variations
- Unreleased-only mode: skip tag ranges; keep just "## [Unreleased]" current between releases.
- Conventional-Commits mode: map `feat:`/`fix:`/`BREAKING CHANGE` directly to buckets and
  derive the next semver bump from the range.

## Review log
_(reviewers append here)_
