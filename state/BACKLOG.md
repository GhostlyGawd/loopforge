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
- [ ] B5 (designer) **Naming Ceremony** per `charter/BRAND.md`. Name, ASCII wordmark,
      brand v1, ADR. Update STATE.json, README, site header copy.
- [ ] B6 (designer) Apply brand v1 to the site: propose template changes as ADR first
      (two-iteration rule), or restyle within existing structure if no tooling change.
- [ ] B7 (builder) Add loops LP-0008 and split follow-ups for 0009/0010 as P1 items.
- [ ] B8 (reviewer) First review pass: score LP-0001…LP-0005 against QUALITY.md, file
      `reviews/review-001.md`, promote/demote statuses.
- [ ] B9 (auditor) Audit #1 → `reviews/audit-001.md`. If sound: set phase to "grow",
      refill role_queue, record transition as ADR.

## Grow (worked after bootstrap)
- [ ] P1 Per-loop detail pages on the site (proposal ADR first; template change).
- [ ] P1 Add `related:` cross-links across all seed loops.
- [ ] P2 CONTRIBUTING.md for humans who want to submit loops.
- [ ] P2 A "hall of deprecated loops" section — the graveyard should teach.

## Loop ideas (Scout feeds this; Builders consume top-down)
- ~~dependency-upgrader~~ — shipped i3 as LP-0006. (small · code-quality)
- a11y-sweeper — one WCAG issue class per pass across a web app. (small · code-quality)
- changelog-scribe — reconstruct/maintain CHANGELOG from git history. (micro · docs)
- flake-hunter — find, reproduce, and fix one flaky test per pass. (medium · testing)
- api-client-generator — grow a typed client endpoint-by-endpoint from an OpenAPI spec. (medium · build)
- benchmark-optimizer — one profiled hotspot per pass, guarded by perf regression tests. (large · code-quality)
- i18n-extractor — externalize one component's strings per pass. (medium · build)
- security-walker — one OWASP category per pass with fixes + notes. (large · code-quality)
- ~~data-janitor~~ — shipped i4 as LP-0007. (small · data)*
- readme-gardener — keep README truthful vs. actual CLI/API surface. (micro · docs)

*resolved i2: `data` category now exists (ADR-002). data-janitor is unblocked; B4 takes it.
