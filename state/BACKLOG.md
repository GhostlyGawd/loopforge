# BACKLOG

Priorities: **P0** = drop everything · P1 = important · P2 = normal · `blocked:` needs diagnosis.
Rules: check items off, don't delete them (strike-through history matters). Max 3 new
items added per iteration.

## Bootstrap (do in order; role in parentheses)
- [x] B1 (auditor) Run `python3 tools/validate.py && python3 tools/build.py`. Confirm
      green. Journal baseline stats: entry count by status/category, site built.
- [x] B2 (librarian) Interrogate taxonomy v0 in `library/categories.json`: are these the
      right categories for a loop library? Adjust (add/rename/merge), record as ADR-002.
      → Added `data` category (ADR-002, v1). `security` deferred until ≥2 ideas.
- [x] B3 (builder) Add loop LP-0006 — pick the strongest idea from § Loop ideas.
      → LP-0006 Dependency Upgrader (code-quality · small).
- [x] B4 (builder) Add loop LP-0007 — fill the emptiest category.
      → LP-0007 Data Janitor fills the new (empty) `data` shelf.
- [x] B5 (designer) **Naming Ceremony** per `charter/BRAND.md`. Name, ASCII wordmark,
      brand v1, ADR. Update STATE.json, README, site header copy.
      → Named **Weft** (ADR-003). Wordmark + brand v1 in BRAND.md; site header now "WEFT".
- [x] B6 (designer) Apply brand v1 to the site: propose template changes as ADR first
      (two-iteration rule), or restyle within existing structure if no tooling change.
      → Restyled tools/build.py template to the Weft palette + weft-line signature,
      implementing ADR-003 (proposed i5, applied i6 — two-iteration rule satisfied).
- [x] B7 (builder) Add loops LP-0008 and split follow-ups for 0009/0010 as P1 items.
      → LP-0008 Flake Hunter (testing · medium). Follow-ups filed as P1 below.
- [x] B8 (reviewer) First review pass: score LP-0001…LP-0005 against QUALITY.md, file
      `reviews/review-001.md`, promote/demote statuses.
      → All five cleared the bar; draft → reviewed (quality ratio 0/8 → 5/8).
- [x] B9 (auditor) Audit #1 → `reviews/audit-001.md`. If sound: set phase to "grow",
      refill role_queue, record transition as ADR.
      → Sound. Bootstrap closed; phase → grow, role_queue refilled (ADR-004).

## Grow (worked after bootstrap)
- [ ] **P0 (directed)** Make every loop copy-paste-runnable as a slash command — a `## Run it`
      block you save as `.claude/commands/<slug>.md`, self-initializing, run continuously with
      the built-in `/loop /<slug>`. Design in ADR-007. Split:
  - [x] P0a Propose the `## Run it` command-form + self-init + site copy-button (ADR-007). — i26
  - [x] P0b Add `## Run it` to library/SCHEMA.md; converted the canon (LP-0002, LP-0003). — i27
  - [x] P0c build.py renders a "Copy /command" button per converted card (ADR-007). — i28
  - [ ] P0d Builders: convert the remaining loops to include `## Run it`, canon-first.
- [ ] P1 Reviewer: clear the draft backlog (LP-0006…LP-0014) draft→reviewed before more
      canonical promotions — quality ratio fell to 0.36 (audit-002).
- [x] P1 LP-0009 changelog-scribe — reconstruct/maintain CHANGELOG from git history. (micro · docs)
      → shipped i10 as LP-0009 Changelog Scribe.
- [x] P1 LP-0010 a11y-sweeper — one WCAG issue class per pass across a web app. (small · code-quality)
      → shipped i11 as LP-0010 A11y Sweeper. Library hits 10 loops (M1 count).
- [ ] P1 Per-loop detail pages on the site (proposal ADR first; template change).
      → ADR-005 proposed i16; ready for an implementing pass (two-iteration rule satisfied next pass).
- [x] P1 Add `related:` cross-links across all seed loops.
      → i12: bidirectional clusters (maintenance/testing/docs); all links resolve.
- [ ] P2 CONTRIBUTING.md for humans who want to submit loops.
- [ ] P2 A "hall of deprecated loops" section — the graveyard should teach.

## Loop ideas (Scout feeds this; Builders consume top-down)
- ~~dependency-upgrader~~ — shipped i3 as LP-0006. (small · code-quality)
- ~~a11y-sweeper~~ — shipped i11 as LP-0010. (small · code-quality)
- ~~changelog-scribe~~ — shipped i10 as LP-0009. (micro · docs)
- ~~flake-hunter~~ — shipped i7 as LP-0008. (medium · testing)
- ~~api-client-generator~~ — shipped i13 as LP-0011. (medium · build)
- ~~benchmark-optimizer~~ — shipped i17 as LP-0013. (large · code-quality)
- ~~i18n-extractor~~ — shipped i15 as LP-0012. (medium · build)
- ~~security-walker~~ — shipped i25 as LP-0017. (large · code-quality)
- ~~data-janitor~~ — shipped i4 as LP-0007. (small · data)*
- readme-gardener — keep README truthful vs. actual CLI/API surface. (micro · docs)
- ~~migration-runner~~ — shipped i20 as LP-0014. (medium · data)
- ~~type-tightener~~ — shipped i22 as LP-0015. (small · code-quality)
- ~~contract-tester~~ — shipped i23 as LP-0016. (medium · testing)

*resolved i2: `data` category now exists (ADR-002). data-janitor is unblocked; B4 takes it.
