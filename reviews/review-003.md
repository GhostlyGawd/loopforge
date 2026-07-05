# review-003 — canonical smoke-read: LP-0002 Polish Pass (i18, reviewer "Lens")

Second canonical promotion (audit-001 cadence). LP-0002 scored 4.83 in review-001; this is
its independent skeptical smoke-read by an iteration (i18) other than its author (i0),
simulating iteration 1 and iteration N.

## Iteration-1 read (cold start)
- Setup is concrete and runnable: create `state/polish-ledger.md` with `## Fixed` and
  `## Declined (and why)`, get linter/tests running, note the baseline. No hidden step. ✓
- First pass reads the ledger + journal, finds one small blemish, fixes it, gates on tests,
  logs it. A newcomer can paste the harness and go. ✓

## Iteration-N read (amnesiac, adversarial)
- **Re-entrancy:** re-reads `polish-ledger.md` each pass; no context-window dependence. ✓
- **One-step:** exactly one blemish per pass, explicitly "no behavior changes." ✓
- **The Declined ledger** is the entry's best idea and holds up under attack: once a fix is
  declined it is skipped "forever unless a human deletes the line," which kills the obvious
  failure mode of a polish loop — endless bikeshedding over the same subjective nit. ✓
- **Stop honesty:** "a full skim finds nothing above the worth-fixing bar → SWEEP CLEAN +
  STOP." The bar is judgment-based (why axis 4 was a 4, not 5), but the Declined ledger
  bounds it so it is not the vague "until it's good" anti-pattern — no cap applies. ✓
- **Guardrails:** test gate + revert on red; "no new dependencies"; anything needing product
  judgment goes to Declined, not into code. Tried to find a path to a silent behavior change
  — the test gate plus the no-behavior-change rule close it. ✓

## Verdict
Scores hold on the second independent read; no new weakness. **LP-0002 Polish Pass:
reviewed → canonical.** It is the reference shape for a low-risk janitor loop, and its
Declined-ledger pattern is worth reusing in other "sweep until clean" loops (LP-0010 A11y
Sweeper, LP-0004 Docs Gardener already echo it).

Canonical candidates remaining (audit-001 cadence): LP-0001, LP-0004 — each needs its own
independent smoke-read.
