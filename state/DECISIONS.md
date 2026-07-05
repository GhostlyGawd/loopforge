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
