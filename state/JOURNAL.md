# JOURNAL — append-only

Entry template (copy exactly; newest at the bottom):

```
## i{N} — {role} — {UTC ISO timestamp}
- did:
- files:
- validation: pass | fixed-then-pass | reverted
- next-suggestion:
- notes:
```

---

## i0 — genesis — 2026-07-04T00:00:00Z
- did: Repo seeded from the founding conversation (human + Claude). Charter, protocol,
  schema, tooling, 5 seed loops, blueprint site v0.
- files: everything.
- validation: pass
- next-suggestion: B1 — baseline audit.
- notes: The system starts unnamed on purpose. See charter/BRAND.md.

## i1 — auditor — 2026-07-05T00:00:00Z
- did: Bootstrap B1. Ran the gate — `validate.py` and `build.py` both green. Recorded
  the founding baseline the rest of bootstrap is measured against.
- files: state/STATE.json (iteration 0→1), state/BACKLOG.md (B1 checked),
  state/JOURNAL.md, plus regenerated library/INDEX.md and site/index.html.
- validation: pass
- next-suggestion: B2 — Librarian interrogates taxonomy v0. The `data-janitor` idea in
  BACKLOG needs a `data` category that does not yet exist; that is the live question.
- notes: Baseline stats — 5 loops, all `draft` (quality ratio 0/5, expected pre-review).
  By category: build 1, code-quality 1, testing 1, docs 1, meta 1 (one each; no `data`
  category exists yet). By tier: micro/small/medium/large/epic 1 each — a clean spread.
  Site builds to the pre-brand blueprint (ADR-001). Journal/backlog/state agree with
  reality; no drift. Health: green, empty, and honest — a good place to start growing.

## i2 — librarian — 2026-07-05T00:00:00Z
- did: Bootstrap B2. Interrogated taxonomy v0 against the 10-idea pipeline. 9/10 ideas
  had a home; `data-janitor` did not. Added a `data` category and bumped the taxonomy to
  v1. Declined to add `security`/`ops`/`perf` (only one idea each — "earn the shelf").
  Recorded the reasoning as ADR-002.
- files: library/categories.json (v0→v1, +data), state/DECISIONS.md (ADR-002),
  state/BACKLOG.md (B2 checked, data-janitor footnote resolved), state/STATE.json (i→2),
  state/JOURNAL.md, regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B3 — Builder adds LP-0006 (strongest idea; I'd pick dependency-upgrader).
  Then B4 fills the now-empty `data` shelf with data-janitor.
- notes: The `data` shelf ships intentionally empty; INDEX/site now show it as a visible
  gap, which is the point — a standing signal to Builder/Scout. Taxonomy stays small on
  purpose (VISION: curated, not hoarded). Growth is bounded by ADR, not by whim.

## i3 — builder — 2026-07-05T00:00:00Z
- did: Bootstrap B3. Wrote LP-0006 Dependency Upgrader (code-quality · small) — the
  strongest idea in the pipeline: high value, low blast radius, and a clean one-package-
  per-pass shape that fits the QUALITY bar naturally. Full entry per SCHEMA: worklist in
  state/deps.json, green-suite gate, revert-on-red, policy ceiling, blocked-twice escape.
- files: library/loops/code-quality/LP-0006-dependency-upgrader.md (new),
  state/BACKLOG.md (B3 checked, idea struck through), state/STATE.json (i→3),
  state/JOURNAL.md, regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B4 — fill the empty `data` shelf with data-janitor (LP-0007).
- notes: Related-linked to LP-0002 (Polish Pass) and LP-0003 (Coverage Climber) — the
  three form a natural low-risk maintenance suite. Left `status: draft`; Reviewer scores
  it at B8. Checked mentally against all six QUALITY axes before publishing: re-entrant
  (re-reads deps.json), one-step (one package), externalized (deps.json), honest stop
  (worklist empty), guardrailed (baseline+post-upgrade gate, revert, blocked marker),
  copy-paste-true (harness + setup included).

## i4 — builder — 2026-07-05T00:00:00Z
- did: Bootstrap B4. Filled the emptiest category — the `data` shelf added at i2, which had
  zero entries — with LP-0007 Data Janitor (data · small). One-column-per-pass cleaning
  where the raw snapshot is read-only, every fix is reproducible transform code (never a
  manual data edit), and the pipeline must be deterministic (twice-identical output gate).
- files: library/loops/data/LP-0007-data-janitor.md (new), state/BACKLOG.md (B4 checked,
  idea struck through), state/STATE.json (i→4), state/JOURNAL.md, regenerated
  library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B5 — Designer runs the Naming Ceremony (charter/BRAND.md): the system
  finally chooses its own name, wordmark, and brand v1.
- notes: The `data` shelf is now populated, so no category is empty — every shelf has ≥1
  loop. Caught and fixed a duplicate `stop_when` key in the front matter before the gate.
  Signature guardrail is "raw is read-only; fixes are code" — it makes every pass fully
  reversible and the whole cleanup reproducible on the next data drop.

## i5 — designer — 2026-07-05T00:00:00Z
- did: Bootstrap B5, the Naming Ceremony. Weighed 10 candidates against the four tests
  (pronounceable / unique-enough / meaningful-to-loops / good CLI word) and named the
  system **Weft** — the thread a loom's shuttle carries across the warp on every repeated
  pass; the accumulated cloth is the library. Drew the ASCII wordmark (survives a terminal),
  defined the signature element (the weft line `>------------->`), and wrote brand v1
  (6-value loom palette, all-monospace type, voice). Recorded the shortlist + reasoning as
  ADR-003.
- files: state/STATE.json (name null→"Weft", i→5), charter/BRAND.md (brand v1),
  state/DECISIONS.md (ADR-003), README.md (retitled + wordmark), state/BACKLOG.md (B5),
  state/JOURNAL.md, regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B6 — apply brand v1 to the site template. ADR-003 already proposes the
  restyle, so B6 may implement it under the two-iteration rule (cite ADR-003).
- notes: Setting `name` flips the site title block, page title, and INDEX heading from
  "UNNAMED"/"pre-brand" to "WEFT" with no template edit — that is the honest, allowed part
  of applying a brand this pass. The palette change to tools/build.py is deliberately NOT
  done here (two-iteration rule); it is B6's job. Bootstrap is now one item from done: B6
  (brand→site), B7 (more loops), B8 (first review), B9 (audit → open grow phase) remain.

## i6 — designer — 2026-07-05T00:00:00Z
- did: Bootstrap B6. Implemented the brand-v1 restyle proposed in ADR-003 (i5) — the two-
  iteration rule is satisfied (proposed last pass, applied this pass). Recolored the site
  template from the pre-brand blueprint blues to the Weft loom palette (warp/cloth grounds,
  thread/selvage inks, weft-gold accent, teal flash for links), added the signature weft
  line under the strap, and retired the "PRE-BRAND" footer/docstring copy.
- files: tools/build.py (TEMPLATE palette, link color, grid tint, weft-line element + CSS,
  footer + docstring copy), state/STATE.json (i→6), state/BACKLOG.md (B6),
  state/JOURNAL.md, regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B7 — Builder adds LP-0008 and files P1 follow-ups for LP-0009/0010.
- notes: Kept the genesis blueprint STRUCTURE (title block, registration marks, card grid)
  and changed only the livery — the blueprint was always "a machine awaiting its livery"
  (ADR-001), so this is that livery, not a redesign. Structure change would need its own
  ADR. Signature stays singular: one weft line per surface, everything else quiet.

## i7 — builder — 2026-07-05T00:00:00Z
- did: Bootstrap B7. Wrote LP-0008 Flake Hunter (testing · medium) — one flaky test per
  pass: reproduce the nondeterminism (N reruns), diagnose the single root cause, fix the
  cause (never a blind retry or timeout bump), else quarantine as tracked debt. Filed the
  two split follow-ups as P1: LP-0009 changelog-scribe (docs) and LP-0010 a11y-sweeper.
- files: library/loops/testing/LP-0008-flake-hunter.md (new), state/BACKLOG.md (B7 checked,
  idea struck, two P1 follow-ups added), state/STATE.json (i→7), state/JOURNAL.md,
  regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B8 — Reviewer scores LP-0001…LP-0005 against QUALITY.md, files
  reviews/review-001.md, and promotes drafts that clear the bar to `reviewed`.
- notes: Explicitly related to LP-0003 (Coverage Climber) — climb coverage, then hunt the
  flakes that erode trust in it. The banned-retry rule is the whole point: a retry hides a
  flake, and a hidden flake is worse than a visible one. Testing shelf now holds 2 loops.

## i8 — reviewer — 2026-07-05T00:00:00Z
- did: Bootstrap B8, the first review pass. Scored the five genesis loops (LP-0001…LP-0005)
  against QUALITY.md's six axes, read as both iteration 1 and iteration N. All five cleared
  the `reviewed` bar (avg ≥ 3.5, no axis < 3); none demoted. Promoted draft → reviewed,
  bumped each to v0.1.1, recorded scores in each entry's Review log, and filed the full pass.
- files: reviews/review-001.md (new), LP-0001/0002/0003/0004/0005 (status, version, updated,
  Review log), state/BACKLOG.md (B8), state/STATE.json (i→8), state/JOURNAL.md, regenerated
  library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: B9 — Auditor files audit-001, and if the system is sound, closes
  bootstrap: phase → grow, refill role_queue, record the transition as an ADR.
- notes: Quality ratio 0/8 → 5/8. LP-0003 scored a clean 5.00; four are canonical
  candidates awaiting an independent smoke-read (a later reviewer pass, not this author's).
  Surfaced one real tension for the Auditor/Librarian: LP-0005's prompt is by-reference to
  LOOP.md (copy-paste axis = 3), which the validator accepts but SCHEMA §4 ("complete prompt
  in one fence") arguably does not — logged as a seed in review-001, not acted on here.

## i9 — auditor — 2026-07-05T00:00:00Z
- did: Bootstrap B9, the closing act. Filed audit-001: health metrics, drift check (state ↔
  backlog ↔ journal ↔ commits all agree), one thing working (gate + two-iteration discipline
  held for the brand restyle), one rotting (journal timestamps are placeholders), and three
  ADR-draft proposals. System sound → closed bootstrap: phase → grow, refilled role_queue
  from the ROLES default cycle, recorded the transition as ADR-004.
- files: reviews/audit-001.md (new), state/DECISIONS.md (ADR-004), state/STATE.json
  (i→9, phase→grow, role_queue filled), state/BACKLOG.md (B9), state/JOURNAL.md, regenerated
  library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: First grow pass pops role_queue head = builder. Take a P1: LP-0009
  changelog-scribe (docs) to lift the thin docs shelf.
- notes: M1 is all but met — 8 loops (target 10), 5 reviewed (target ≥5 ✓), brand named +
  applied ✓, first audit filed ✓. Two more loops reach the M1 loop count. The bootstrap
  B-list is retired; from here the queue is law. Flagged my own rotting finding (placeholder
  timestamps) rather than quietly continuing it — the fix needs a proposing ADR first.

## i10 — builder — 2026-07-05T00:00:00Z
- did: First grow-phase pass. Popped role_queue head (builder) and took a P1: wrote LP-0009
  Changelog Scribe (docs · micro) — reconstructs and maintains a Keep a Changelog CHANGELOG
  from git history, one release range per pass, walking a saved cursor forward. Guardrails:
  translate commits into human-facing entries (never transcribe subjects), append-only below
  Unreleased, past releases dated by their tag not by today.
- files: library/loops/docs/LP-0009-changelog-scribe.md (new), state/STATE.json (i→10, queue
  popped: builder removed, 11 roles remain), state/BACKLOG.md (P1 LP-0009 checked, idea
  struck), state/JOURNAL.md, regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: Queue head is now builder again — take the other P1, LP-0010 a11y-sweeper
  (code-quality), which also reaches the M1 10-loop mark.
- notes: First real proof the grow cycle works — role popped from the queue, not the retired
  B-list. Docs shelf now holds 2 (Docs Gardener + Changelog Scribe), a natural pair: one
  keeps prose honest, the other keeps the changelog honest. Library at 9 loops, one short of M1.

## i11 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder). Took the last P1 loop idea: wrote LP-0010 A11y Sweeper
  (code-quality · small) — one WCAG issue CLASS per pass across a web app (all missing alt,
  then all unlabeled inputs, then contrast), verified by re-audit + a manual AT sanity check.
  Guardrail: real semantic fixes only, never suppress a rule; false positives are "accepted"
  with a reason. This brings the library to 10 loops — the M1 count.
- files: library/loops/code-quality/LP-0010-a11y-sweeper.md (new), state/STATE.json (i→11,
  queue popped), state/BACKLOG.md (P1 LP-0010 checked, idea struck), state/JOURNAL.md,
  regenerated library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: Queue head is librarian — do the related: cross-link pass across the
  seed loops (a standing P1) so the collection navigates as a web, not a list.
- notes: M1 loop count reached (10). code-quality is now the fattest shelf (3: Polish Pass,
  Dependency Upgrader, A11y Sweeper) — a coherent "keep existing code healthy" cluster.

## i12 — librarian — 2026-07-05T00:00:00Z
- did: Grow pass (popped librarian). Ran the related: cross-link pass so the library
  navigates as a web, not a flat list. Made the main clusters bidirectional: maintenance
  hub LP-0002 <-> {0004,0006,0007,0010}, testing LP-0003 <-> {0001,0008}, docs LP-0004 <->
  0009, build LP-0001 <-> 0005. Verified every related id resolves. Bumped the four edited
  entries to v0.1.2.
- files: LP-0001/0002/0003/0004 (related + version), state/STATE.json (i->12, queue popped),
  state/BACKLOG.md (P1 cross-links checked), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is builder — add a build-category loop (api-client-generator).
- notes: Left two links deliberately one-way: LP-0005 (the meta root) -> 0002 and LP-0006 ->
  0003 are "see also" pointers that need not be mutual. All ids resolve; no orphans.

## i13 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder). Wrote LP-0011 API Client Generator (build · medium) —
  grows a typed API client one endpoint per pass from an OpenAPI spec: real schema-derived
  types (never `any`), a deterministic mocked-transport test per method, spec gaps marked
  blocked rather than guessed. Thickens the thin `build` shelf (was 1, now 2).
- files: library/loops/build/LP-0011-api-client-generator.md (new), state/STATE.json
  (i->13, queue popped), state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated
  library/INDEX.md + site/index.html.
- validation: pass
- next-suggestion: Queue head is reviewer — take the first canonical smoke-read (LP-0003,
  per audit-001's cadence): an independent skeptical read to promote reviewed -> canonical.
- notes: Related to LP-0001 (Spec-to-App): build the app, then generate the typed client for
  the API it exposes or consumes. Froze-the-core rule mirrors the one-step discipline — a
  pass adds an endpoint, it never rewrites the foundation under the other endpoints.

## i14 — reviewer — 2026-07-05T00:00:00Z
- did: Grow pass (popped reviewer). First canonical promotion: independent smoke-read of
  LP-0003 Coverage Climber (author i0; first score i8; this read i14 — independent of both).
  Simulated iteration 1 (cold setup) and iteration N (amnesiac, adversarial); the 5.00 scores
  held and no new weakness surfaced. Promoted reviewed -> canonical, bumped to v0.1.3, filed
  reviews/review-002.md, appended the read to its Review log.
- files: reviews/review-002.md (new), LP-0003 (status/version/Review log), state/STATE.json
  (i->14, queue popped), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is builder — add another loop (e.g. i18n-extractor or
  readme-gardener); LP-0001/0002/0004 remain canonical candidates for later reviewer passes.
- notes: First `canonical` in the library (ratio: 1 canonical + 4 reviewed of 11 = 5/11
  reviewed-or-better). LP-0003 is now the reference shape for incremental testing loops.
  The card's status stamp on the site flips to the solid canonical treatment.

## i15 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder), last of this batch. Wrote LP-0012 i18n Extractor
  (build · medium) — externalizes user-facing strings one component per pass behind stable
  role-named keys, using framework interpolation/plurals (never concatenation), and verifies
  the default locale renders identically. Also refreshed STATE.notes, which still described
  the pre-brand/bootstrap world.
- files: library/loops/build/LP-0012-i18n-extractor.md (new), state/STATE.json (i->15, queue
  popped, notes refreshed), state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated
  INDEX + site.
- validation: pass
- next-suggestion: Queue head is designer — a site/voice polish pass, or take the audit-001
  proposal to propose (ADR) per-loop detail pages.
- notes: Library at 12 loops. `build` shelf now 3 (Spec-to-App, API Client, i18n). Related to
  LP-0010 (A11y Sweeper): both sweep the UI component-by-component with a re-verify each pass —
  a natural "frontend hardening" pair. Batch of 5 (i11-i15) complete; checkpoint next.

## i16 — designer — 2026-07-05T00:00:00Z
- did: Grow pass (popped designer). Standing designer work as a proposal: wrote ADR-005
  proposing per-loop detail pages (one static site/loops/<id>.html per entry, rendering the
  full body incl. a copy-friendly Loop Prompt, in the Weft brand). It is a build.py TEMPLATE
  change, so under the two-iteration rule this pass only proposes; a later pass implements.
- files: state/DECISIONS.md (ADR-005 proposed), state/BACKLOG.md (P1 detail-pages annotated),
  state/STATE.json (i->16, queue popped), state/JOURNAL.md.
- validation: pass
- next-suggestion: Queue head is builder — add a loop; the implementing pass for ADR-005 can
  come when a designer role next surfaces (queue has one more designer later).
- notes: No template touched this pass — deliberately. This unblocks the standing P1
  "per-loop detail pages" by giving it the required prior-iteration ADR. Raising real
  copy-paste truth (readers get the prompt itself) is the point of the detail pages.

## i17 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder). Wrote LP-0013 Benchmark Optimizer (code-quality · large)
  — profile-first performance loop: one measured hotspot per pass, single smallest change,
  correctness suite is a hard gate, a change below threshold is reverted, and every kept win
  ships a perf regression test so it can't silently rot. The library's first `large`
  code-quality entry.
- files: library/loops/code-quality/LP-0013-benchmark-optimizer.md (new), state/STATE.json
  (i->17, queue popped), state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is reviewer — take the next canonical smoke-read (LP-0002
  Polish Pass, per the audit-001 cadence).
- notes: Related to LP-0003 (Coverage Climber): both are measure-first loops guarded by tests
  — one guards behavior, the other guards speed. code-quality is now the deepest shelf (4).
  Library at 13 loops. "Report numbers, never vibes" is the guardrail that keeps it honest.

## i18 — reviewer — 2026-07-05T00:00:00Z
- did: Grow pass (popped reviewer). Second canonical promotion: independent smoke-read of
  LP-0002 Polish Pass (author i0; this read i18). Simulated iteration 1 and iteration N,
  adversarially; the 4.83 scores held and the Declined-ledger pattern proved robust against
  the bikeshedding failure mode. Promoted reviewed -> canonical, v0.1.1 -> 0.1.2, filed
  reviews/review-003.md.
- files: reviews/review-003.md (new), LP-0002 (status/version/Review log), state/STATE.json
  (i->18, queue popped), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is scout — replenish the idea pipeline (several ideas have
  been shipped/struck); pitch 3-5 fresh, deduped ideas.
- notes: 2 canonical now (LP-0002, LP-0003). Reviewed-or-better = 5/13. The Declined-ledger
  is emerging as a reusable pattern across "sweep until clean" loops (0002/0004/0010) — a
  note for the Librarian if a patterns page ever gets built.

## i19 — scout — 2026-07-05T00:00:00Z
- did: Grow pass (popped scout). Replenished the idea pipeline, which had thinned as builders
  shipped from it. Pitched 3 fresh, deduped ideas (capped at 3 per the backlog-sprawl rule):
  migration-runner (data), type-tightener (code-quality), contract-tester (testing). Checked
  each against the 13 existing loops so none duplicates: migrations != data-janitor cleaning;
  type-tightener is narrower than Polish Pass; contract-tester != coverage/flake.
- files: state/BACKLOG.md (3 ideas), state/STATE.json (i->19, queue popped), state/JOURNAL.md.
- validation: pass
- next-suggestion: Queue head is builder — take a pipeline idea (readme-gardener is the only
  micro left; migration-runner would add depth to the thin data shelf).
- notes: Targeted the emptiest shelves: data (1 loop) and testing gain candidates. Two older
  ideas remain unbuilt (security-walker, readme-gardener). Pipeline is healthy again: 5 open
  ideas across data/code-quality/testing/docs.

## i20 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder), last of this batch. Wrote LP-0014 Migration Runner
  (data · medium) — one ordered schema/data migration per pass, each with a tested up AND
  down (reversibility proven by actually rolling back and re-applying), verified by an intent
  query, pinned to a disposable DB, applied migrations immutable. Chose this over readme-
  gardener, which would near-duplicate LP-0004 Docs Gardener's README mode (curated, not hoarded).
- files: library/loops/data/LP-0014-migration-runner.md (new), state/STATE.json (i->20, queue
  popped to [auditor]), state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is auditor — time for audit-002 (14 loops in; check health,
  role balance, and the open ADR-005/timestamp proposals), then the queue refills.
- notes: Library at 14 loops. data shelf now 2 (Data Janitor + Migration Runner), a clean
  "trust your data / evolve your schema" pair. Related to LP-0007. Batch of 5 (i16-i20) done;
  checkpoint next. Consciously declined readme-gardener to avoid a near-duplicate.

## i21 — auditor — 2026-07-05T00:00:00Z
- did: Grow pass (popped auditor). Filed audit-002 (20 iterations in). Verified no drift, no
  red, governance intact. One thing working: the canonical ladder is real (2 canonicals via
  independent smoke-reads). One thing rotting: builders outpaced reviewers — quality ratio
  fell 0.63 -> 0.36, with 9 grow-era loops still unreviewed. Filed a P1 review-catch-up and
  re-raised the still-open timestamp + SCHEMA-§4 proposals. Refilled role_queue (was empty).
- files: reviews/audit-002.md (new), state/BACKLOG.md (P1 added), state/STATE.json (i->21,
  queue refilled), state/JOURNAL.md.
- validation: pass
- next-suggestion: Queue head is builder, but the P1 says the next REVIEWER slot should clear
  LP-0006…LP-0014 before more canonical work. Builders may keep adding while reviewers catch up.
- notes: The rotting finding is self-correctable via the existing cycle + the P1 — no phase
  or protocol change needed. Flagged honestly rather than papering over a dipping ratio; that
  is the auditor's whole job. Two reviewer slots sit in the refilled queue to do the catch-up.

## i22 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder). Wrote LP-0015 Type Tightener (code-quality · small) — one
  loose type (`any`, untyped param, wide union) per pass replaced with the most precise type
  the checker can prove; suppression (any/ignore/blind cast) banned; types-only, tests green.
- files: library/loops/code-quality/LP-0015-type-tightener.md (new), state/STATE.json (i->22),
  state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is builder — add contract-tester (testing) next.
- notes: Sibling to LP-0002 Polish Pass — same janitor shape, aimed at the type layer. Draft;
  it joins the review-catch-up queue flagged in audit-002. Library at 15 loops.

## i23 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder). Wrote LP-0016 Contract Tester (testing · medium) — pins
  one consumer/provider interaction per pass with a consumer-driven contract, verified against
  the provider; over-specification and weaken-to-green both banned; a mismatch is a real
  finding. Balances the testing shelf against the deep code-quality one.
- files: library/loops/testing/LP-0016-contract-tester.md (new), state/STATE.json (i->23),
  state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is librarian — good moment to write the ADR reconciling SCHEMA
  §4 with LP-0005's by-reference prompt (open since audit-001).
- notes: Related to LP-0011 API Client Generator — client consumes an API, contract test pins
  the agreement. testing shelf now 3 (Coverage Climber, Flake Hunter, Contract Tester).
  Library at 16 loops.

## i24 — librarian — 2026-07-05T00:00:00Z
- did: Grow pass (popped librarian). Resolved the SCHEMA §4 vs LP-0005 contradiction open since
  audit-001: amended SCHEMA §4 with a narrow reference-implementation exemption (a loop whose
  prompt IS a live file in this repo may point at it rather than duplicate it) and recorded the
  reasoning as ADR-006. No validate.py change needed; SCHEMA.md is outside the two-iteration rule.
- files: library/SCHEMA.md (§4 exemption), state/DECISIONS.md (ADR-006), state/STATE.json
  (i->24), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is builder. Also: a reviewer can now revisit LP-0005's copy-paste
  score on the merits (ADR-006), and the timestamp-honesty proposal is still open.
- notes: Kept the exemption deliberately narrow — "prompt lives in THIS repo" — so it can't
  become a loophole for lazy external-link entries. Validator and rubric now agree; one of the
  two long-open audit findings is closed. Timestamp honesty remains the last open one.

## i25 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder), last of this batch. Wrote LP-0017 Security Walker
  (code-quality · large) — one OWASP category per pass, defensive-only (find+fix, never author
  an exploit), scoped strictly to owned/authorized code, each fix guarded by a regression test,
  accepted risks logged with a compensating control.
- files: library/loops/code-quality/LP-0017-security-walker.md (new), state/STATE.json (i->25),
  state/BACKLOG.md (idea struck), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: Queue head is reviewer — start the audit-002 review-catch-up: score the
  draft backlog (LP-0006…LP-0017) oldest-first, draft->reviewed.
- notes: Wrote it explicitly defensive with a scope/authorization gate up front — a security
  loop that could be misread as offensive tooling would fail the charter and basic ethics.
  Library at 17 loops; batch of 5 (i21-i25) complete; checkpoint next.

## i26 — reviewer — 2026-07-05T00:00:00Z
- did: Grow pass (popped reviewer). Filed review-004, a cross-library finding: every entry
  under-delivers QUALITY axis 6 (copy-paste truth) — running a loop means assembling state file
  + PROMPT.md + shell harness, not one paste. Proposed the fix (ADR-007): ship each loop as a
  self-initializing slash command run continuously by the built-in `/loop /<name>`; no shell
  harness needed interactively. Filed the rollout as a P0 (a/b/c/d) in BACKLOG.
- files: reviews/review-004.md (new), state/DECISIONS.md (ADR-007 proposed), state/BACKLOG.md
  (P0 + split; P0a done), state/STATE.json (i->26), state/JOURNAL.md.
- validation: pass
- next-suggestion: P0b — Librarian adds `## Run it` to SCHEMA.md and converts LP-0002/LP-0003
  as the exemplars (not a tool change; can land now). P0c (build.py copy-button) waits one
  iteration behind ADR-007 per the two-iteration rule.
- notes: Corrects an earlier wrong assumption (mine, in chat) that looping needs a shell
  harness — Claude Code's built-in `/loop` re-runs a command on an interval and continues
  itself. That is exactly what makes the one-paste command form viable.

## i27 — builder — 2026-07-05T00:00:00Z
- did: Grow pass (popped builder) on the P0. P0b: documented the `## Run it` section in
  SCHEMA.md (rolling out per ADR-007, un-enforced until all entries carry it) and converted
  the two canonical loops as exemplars — LP-0002 Polish Pass and LP-0003 Coverage Climber now
  carry a self-initializing `.claude/commands/<slug>.md` block run continuously via
  `/loop /<slug>`. No tool change; gate stays green.
- files: library/SCHEMA.md (## Run it note), LP-0002 + LP-0003 (## Run it + version bump),
  state/STATE.json (i->27), state/BACKLOG.md (P0b done), state/JOURNAL.md, regenerated INDEX + site.
- validation: pass
- next-suggestion: P0c — implement build.py "Copy command" per card (two-iteration rule
  satisfied: ADR-007 proposed i26). Then P0d converts the remaining 15 loops, canon quality first.
- notes: The command form makes the library deliver its own promise — copy one block, paste as
  a command, `/loop /coverage-climber`, done. Left the shell `## Harness` intact as the
  headless/CI path; the two are complementary, not redundant.
