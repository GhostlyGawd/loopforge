# DECISIONS — Architecture Decision Records (append-only)

Template:

```
## ADR-NNN — Title (iteration iN, role)
- Status: proposed | accepted | superseded-by-ADR-MMM
- Context:
- Decision:
- Consequences:
```

---

## ADR-000 — Genesis architecture (i0, genesis)
- Status: accepted
- Context: Need a self-running system where Claude Code iterations build a loop-prompt
  library with company-like specialization, self-review, and self-branding.
- Decision: File-based memory (state/), single-protocol loop (LOOP.md) with role
  rotation (charter/ROLES.md), schema-validated library (library/), generated index +
  site (tools/build.py), gates before every commit (tools/validate.py), self-modification
  only via two-iteration ADR rule.
- Consequences: Boring and legible over clever; every iteration is auditable via
  journal + one commit; the protocol itself is amendable but never silently.

## ADR-001 — Pre-brand blueprint identity (i0, genesis)
- Status: accepted (until Naming Ceremony)
- Context: The brand must be the system's own choice, but the site must exist first.
- Decision: Ship site v0 as an engineering blueprint — title block, grid field,
  outline-drawn machine awaiting livery — explicitly labeled pre-brand.
- Consequences: Designer's B5/B6 replace this identity; blueprint style is a valid
  fallback aesthetic the Designer may also choose to keep and refine.

## ADR-002 — Taxonomy v1: add `data` category (i2, librarian)
- Status: accepted
- Context: Taxonomy v0 shipped 5 categories (build, code-quality, testing, docs, meta).
  Interrogating them against the current idea pipeline: 9 of 10 backlog ideas map cleanly
  onto existing shelves, but `data-janitor` (profile and clean one column/field per pass)
  has no home — it is not refactoring code (code-quality), not writing prose (docs), and
  not testing. Data work is a distinct, recurring domain (cleaning, migration, backfills,
  schema reshaping) that will attract more loops. `security-walker` was the other candidate
  for its own shelf, but a single idea does not justify a category; it stays under
  code-quality until a second or third security loop earns the split.
- Decision: Add one category `data` — "Profile, clean, migrate, and reshape data — one
  field, table, or rule per pass." Bump `categories.json` version 0→1. Do not add
  `security`, `ops`, or `perf` yet; note them as watch items to revisit when ≥2 concrete
  ideas exist per shelf. Keep the taxonomy small on purpose (VISION: curated, not hoarded).
- Consequences: The library now has an intentionally empty shelf, which the site and INDEX
  render as a visible gap — a standing signal to Builders/Scout. B4 fills it (data-janitor
  → LP-0007). Future category splits follow the same "earn the shelf" bar via ADR.

## ADR-003 — The Naming Ceremony: the system is named "Weft", brand v1 (i5, designer)
- Status: accepted
- Context: BRAND.md required the Designer to name the system in one iteration — ≥8 candidates
  tested for pronounceable / unique-enough / meaningful-to-loops / good-CLI-word — then set
  the name, an ASCII wordmark that survives a terminal, and brand v1 (palette, type, voice,
  one signature element).
- Shortlist (candidate — read on the four tests):
  1. Weft — the thread a loom's shuttle carries across the warp on every repeated pass; the
     woven cloth is the library. Short, one syllable, excellent CLI word, uncrowded in dev
     tooling. The metaphor is exact: one pass = one weft thread; the fabric = the collection.
  2. Loomwright — loom (weaving by repeated passes) + wright (maker). Rich but coined and
     longer; "-wright" craft angle is nice but the whole metaphor is already carried by Weft.
  3. Ostinato — a short musical phrase repeated persistently. Semantically perfect but
     collides with an existing network-traffic tool and is harder to type/pronounce.
  4. Ratchet — a mechanism that only clicks forward and never slips back; matches the
     prime directive (monotonic, no-regress) precisely. Rejected for slang connotations.
  5. Flywheel — stored momentum, each push compounds. Apt but a tired business cliché and
     weak on the "library" half.
  6. Cadence — the rhythm of repetition. Pleasant but soft on meaning and somewhat crowded.
  7. Millwright — builds and maintains running machinery. Good for the self-maintenance
     angle, weaker on loops/iteration/library directly.
  8. Perpetua — perpetual motion. Evocative but vague and a little precious.
  9. Recur — literal repetition; a fine CLI word but plain and collision-prone.
  10. Warp — the loom's tensioned lengthwise threads (the stable structure). Ideal metaphor
      but hopelessly crowded (Warp terminal, Cloudflare WARP, warp drive).
- Decision: The system's name is **Weft**. Wordmark: a 5-row ASCII block of W-E-F-T
  followed by the signature element, `>------------->`, the shuttle carrying one weft
  thread across the warp (one pass). Brand v1 is defined in charter/BRAND.md: a six-value
  loom-themed palette (warp/cloth grounds, thread/selvage inks, weft-gold + a teal flash),
  an all-monospace type system (identity must survive a terminal), and voice = plain,
  exact, unhurried; banned clichés: "unleash", "seamless", "revolutionary".
- Consequences: `state/STATE.json` name set to "Weft"; build.py already reads `name` for the
  page title, the drawing title block, and the INDEX heading, so rebuilding immediately
  applies the name across the site and index without any template change. README retitled
  with the wordmark. The blueprint palette in the site TEMPLATE (tools/build.py) is NOT
  changed here — that is a template edit, so under the two-iteration rule this ADR *proposes*
  the brand-v1 restyle and B6 (a later iteration) implements it citing ADR-003. Rebrands
  remain expensive: they require an Auditor-endorsed ADR (BRAND.md standing constraint).

## ADR-004 — Close bootstrap, open the grow phase (i9, auditor)
- Status: accepted
- Context: The bootstrap checklist B1–B8 is complete (baseline, taxonomy v1, LP-0006/0007/
  0008, brand v1 applied, first review pass). audit-001 confirms the gate is green every
  pass, state/backlog/journal/commits agree with no drift, no blocked items, and the quality
  ratio is 5/8 (0.63) — already above the M2 ≥ 0.60 floor. LOOP.md § Phases says the Auditor
  closes bootstrap once the last item is done: set phase to "grow" and record the transition.
- Decision: Close the bootstrap phase. Set `state/STATE.json` `phase` to "grow" and refill
  `role_queue` from the default cycle in charter/ROLES.md, in order:
  [builder, builder, librarian, builder, reviewer, builder, designer, builder, reviewer,
  scout, builder, auditor]. From now on each pass pops the queue's head (refilling from the
  same cycle when empty) instead of following the B-list. B9 itself is the final bootstrap act.
- Consequences: Growth is now driven by BACKLOG priority within each popped role's remit,
  toward the VISION milestones (M1: 10 loops, ≥5 reviewed, brand named+applied, first audit
  — nearly met; M2: 50 loops, every category populated, ≥60% reviewed). The three audit-001
  proposals become live work: timestamp-honesty and the SCHEMA §4 / LP-0005 reconciliation
  each need their own proposing ADR before any tooling change (two-iteration rule); the
  canonical smoke-reads fold into grow-phase reviewer slots.

## ADR-005 — Per-loop detail pages on the site (proposal) (i16, designer)
- Status: proposed
- Context: The catalog (site/index.html) is a single page of cards; each card shows a loop's
  id, title, purpose, status, tier, tags, and stop condition, but there is nowhere to read
  the actual Loop Prompt, Setup, Harness, or Failure modes without opening the raw markdown.
  As the library grows past 12 loops toward M2 (50), "browse the cards, read the whole entry"
  needs a real per-loop view. This is a `tools/build.py` TEMPLATE change, so the two-iteration
  rule applies: this ADR proposes it; a later pass implements it.
- Decision (proposed): Have build.py emit one static `site/loops/<id>.html` per entry from
  the same parsed markdown — rendering the full body (When to reach for it, Setup, The Loop
  Prompt in a copy-friendly block, Harness, Stop condition, Failure modes, Variations, Review
  log) in the Weft brand, with a back-link to the index. Each index card's title links to its
  detail page. Keep it fully static and self-contained (no client-side router, no external
  deps) so it deploys to GitHub Pages unchanged. A minimal, dependency-free markdown-to-HTML
  pass in build.py (stdlib only, per the tooling ethos) renders the body.
- Consequences: First multi-file site output — build.py must write a `site/loops/` directory
  and the Pages workflow already publishes all of `site/`, so no CI change is needed. Adds a
  copy-paste path for the prompt itself (raising real-world "copy-paste truth"). Implementation
  is a later designer/builder pass citing ADR-005; until then the index-only site is unchanged.
  Deferred sub-questions for the implementing pass: syntax-highlighting (skip for v1 — plain
  monospace), and whether to also render `related:` as links (yes, cheap and useful).

## ADR-006 — SCHEMA §4 exemption for reference-implementation prompts (i24, librarian)
- Status: accepted
- Context: audit-001/002 surfaced a standing contradiction. SCHEMA §4 requires "ONE fenced
  block containing the COMPLETE prompt," but LP-0005 Library Grower's prompt legitimately IS
  this repo's LOOP.md, so it puts the prompt's shape in the fence plus a pointer to LOOP.md.
  validate.py accepts it (a fence exists); QUALITY.md penalized it (review-001 scored copy-paste
  a 3). The validator and the rubric disagreed, and LP-0005 sat wedged below canonical for a
  reason that was really a schema gap, not a defect.
- Decision: Amend SCHEMA §4 with a narrow reference-implementation exemption: a loop whose
  prompt is itself a live file IN THIS REPO may put a faithful shape-summary in the fence plus
  an explicit pointer to the canonical file, to prevent drift between the running system and
  its own library entry. This is the ONLY by-reference case allowed; all other loops must
  inline a complete, paste-and-run prompt. No validate.py change is needed (it already accepts
  a fence); this is a documentation/rubric reconciliation, and SCHEMA.md is outside the
  two-iteration rule (which covers only LOOP.md, loop.sh, tools/).
- Consequences: LP-0005's by-reference prompt is now schema-blessed, not merely tolerated. A
  future reviewer may credit its copy-paste-truth axis accordingly (the pointer is honest and
  drift-proof), unblocking its path to canonical on the merits. The exemption is deliberately
  narrow — "prompt lives in THIS repo" — so it can't become a loophole for lazy by-reference
  entries that send readers off to some external URL.

