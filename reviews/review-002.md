# review-002 — canonical smoke-read: LP-0003 Coverage Climber (i14, reviewer "Lens")

Per audit-001's cadence, the first canonical promotion. QUALITY.md sets canonical at
avg ≥ 4.5 (LP-0003 scored 5.00 in review-001) **and** a full skeptical smoke-read by an
iteration other than the author's. LP-0003 was authored at genesis (i0) and first scored at
i8; this read is by i14 — independent of both. The smoke-read simulates iteration 1 (first
run, cold setup) and iteration N (amnesiac re-entry) and tries to break the loop.

## Iteration-1 read (cold start)
- Setup is runnable as written: get coverage running by hand, note the command, seed
  `state/coverage.json` with target/current/command/worklist. No hidden prerequisite.
- First pass reads state + journal, runs the pinned command, picks one risky untested
  module, writes happy/edge/failure tests, re-runs coverage, commits. Nothing assumes a
  prior context window. A newcomer could paste the harness and go. ✓

## Iteration-N read (amnesiac re-entry, adversarial)
- **Re-entrancy:** every pass re-reads `coverage.json` fresh; no dependence on memory. ✓
- **Stop honesty:** `current >= target` is numeric and checkable; on stop it announces,
  creates STOP, halts — and the "raise target, delete STOP" note gives a real resume path. ✓
- **Metric-gaming resistance:** "behavioral tests, not implementation," "no asserting on
  private internals," and "never weaken the code under test unless it's a real bug — then
  fix it and say so loudly" close the obvious cheat of padding coverage with trivial asserts. ✓
- **Tangle escape:** a module that resists twice gets `blocked:` with a diagnosis, so the
  loop can't wedge on one hard file. ✓
- **Break attempts:** tried to find a path where the loop loops forever or corrupts state —
  the pinned command, per-module worklist, and blocked marker prevent both. Coverage-tool
  flakiness is acknowledged (command pinned in state; failures journaled, not silently
  skewing numbers). No failure mode is left on the happy path.

## Verdict
No new weaknesses surfaced; the review-001 scores hold on a second, independent read.
**LP-0003 Coverage Climber: reviewed → canonical.** It is the reference shape for an
incremental testing loop — other testing entries (LP-0008) should be measured against it.

Remaining canonical candidates for later passes (audit-001 cadence): LP-0001, LP-0002,
LP-0004 — each needs its own independent smoke-read before promotion.
