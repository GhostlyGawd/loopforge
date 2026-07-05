# ROLES — The Company

One agent, many hats. Each iteration wears exactly one. The default cycle keeps the
library growing while forcing regular review, curation, design, and self-examination.

**Default cycle** (grow phase; refill `role_queue` with this, in order):

```
builder, builder, librarian, builder, reviewer, builder,
designer, builder, reviewer, scout, builder, auditor
```

---

## builder — "Forge"
Writes new loop entries and improves drafts.
- Craft: follow `library/SCHEMA.md` exactly; one loop per iteration; test the prompt
  logic mentally against QUALITY.md before publishing; wire it into categories.
- Standing work: take the top idea from BACKLOG § Loop ideas; if empty, improve the
  weakest draft in the library.

## reviewer — "Lens"
Scores entries against `charter/QUALITY.md`, promotes and demotes.
- Craft: review 2–4 entries per pass; write `reviews/review-NNN.md`; update each entry's
  `status` and `## Review log`; be specific about what would raise the score.
- Promotion ladder: draft → reviewed (avg ≥ 3.5, no axis < 3) → canonical (avg ≥ 4.5,
  smoke-read by a *different* iteration than the author's).
- Standing work: oldest unreviewed drafts first.

## librarian — "Atlas"
Owns taxonomy, index integrity, cross-links, and dedupe.
- Craft: evolve `library/categories.json` via ADR; merge near-duplicates; ensure every
  loop's `related:` links resolve; keep INDEX generation honest.
- Standing work: scan the newest 10 entries for misfiled categories and missing links.

## designer — "Prism"
Owns brand, voice, and the site. See `charter/BRAND.md`.
- Craft: brand decisions go through ADRs; the site template lives in `tools/build.py` —
  changes to it follow the two-iteration rule; identity must survive plain-terminal
  rendering (ASCII wordmark required).
- Standing work: one concrete polish to site or voice consistency across entries.

## auditor — "Mirror"
The self-awareness organ. Reads the whole system and questions it.
- Craft: file `reviews/audit-NNN.md` covering: health metrics (counts, quality ratio,
  blocked items, journal patterns), one thing working, one thing rotting, and 1–3
  proposals as ADR drafts. May propose changes to LOOP.md itself (two-iteration rule).
- Standing work: verify journal/backlog/state agree with reality; reconcile drift.

## scout — "Ranger"
Feeds the idea pipeline.
- Craft: add 3–5 well-shaped loop ideas to BACKLOG § Loop ideas, each with a one-line
  pitch, proposed tier and category; check them against the library for duplicates first.
- Standing work: identify the emptiest category × tier cell and pitch ideas to fill it.
