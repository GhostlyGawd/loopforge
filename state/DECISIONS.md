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
