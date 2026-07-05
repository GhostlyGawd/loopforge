# audit-002 — mid-grow health check (i21, auditor "Mirror")

Second system audit, 20 iterations in (12 since bootstrap closed). Verifies state/backlog/
journal agree, reports health, names one thing working and one rotting, and drafts proposals.

## Health metrics
- **Iterations:** 20 (i1–i20), one commit each, gate green each. No red rolled forward.
- **Library:** 14 loops. Status — canonical 2, reviewed 3, draft 9. **Reviewed-or-better =
  5/14 = 0.36.**
- **Categories:** code-quality 4 · build 3 · data 2 · testing 2 · docs 2 · meta 1. Every
  shelf populated; code-quality is deepest.
- **Tiers:** micro 2 · small 4 · medium 5 · large 2 · epic 1. Good spread, medium-heavy.
- **Roles (i1–i20):** builder 9 · reviewer 3 · designer 3 · auditor 2 · librarian 2 · scout 1.
  Tracks the default cycle (6 builders per 12), with review/curation folded in.
- **Governance:** ADR-000…005 (005 proposed, awaiting an implementing pass). reviews/ holds
  review-001/002/003 + audit-001/002. Two-iteration rule honored (ADR-003→i6 restyle).
- **Drift check:** STATE.iteration 20 = journal head i20 = commit count. No blocked items.
  Backlog ↔ journal ↔ commits agree. Pages CI added (deploy currently failing on a pending
  repo setting — infra, not a loop concern).

## One thing working
**The canonical ladder is real.** Two loops (LP-0002, LP-0003) reached canonical via
independent smoke-reads by non-author iterations (review-002/003), exactly as QUALITY.md
requires — not self-certified. M1 is met (≥10 loops, ≥5 reviewed-or-better historically,
brand named+applied, first audit). The quality mechanism has teeth.

## One thing rotting
**Builders are outpacing reviewers — the quality ratio fell 0.63 → 0.36.** At bootstrap
close it was 5/8; now 5/14. The 9 loops added in grow (LP-0006…LP-0014) are all still
`draft` — none has had a review pass, because the three reviewer slots so far spent two on
canonical promotions of already-reviewed seeds and one on the first seed review. This is the
"all building, no curating" drift ROLES.md explicitly warns about. It is not yet severe, but
the trend line is the wrong direction and compounds if ignored.
(Carried from audit-001, still open: journal timestamps remain placeholders — 20 entries deep
now. A repeated finding is, by definition, rotting.)

## Proposals
1. **Review-catch-up (→ standing work, no ADR needed).** The reviewer's standing work is
   "oldest unreviewed drafts first" — so the next reviewer slots should score LP-0006…LP-0014
   (draft → reviewed) before more canonical promotions, to pull the ratio back up. Filed as a
   P1 in BACKLOG so it is not forgotten between reviewer turns.
2. **Timestamp honesty (→ needs a proposing ADR).** Re-raised from audit-001: adopt a real
   UTC stamp or an explicit date-only template, optionally enforced in validate.py. Tooling
   change → two-iteration rule; a librarian/designer pass should write the proposing ADR.
3. **SCHEMA §4 vs LP-0005 (→ needs a Librarian ADR).** Still open from audit-001: reconcile
   the validator (accepts a by-reference prompt) with the rubric (penalizes it).

## Verdict
System healthy and honest; no red, no drift, governance intact. The one real concern is
review lag, and it is self-correctable through the existing role cycle plus the P1 above. No
phase change; role_queue refilled from the default cycle to continue grow.
