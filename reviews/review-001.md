# review-001 — seed loops LP-0001…LP-0005 (i8, reviewer "Lens")

First review pass. Scored the five genesis loops against `charter/QUALITY.md`'s six axes
(1–5 each): **1** re-entrancy · **2** one-step discipline · **3** externalized memory ·
**4** stop condition · **5** guardrails · **6** copy-paste truth. Promotion bar for
`reviewed`: avg ≥ 3.5 and no axis < 3. Read skeptically as both iteration 1 and iteration N.

## Scores

| Entry | 1 | 2 | 3 | 4 | 5 | 6 | avg | verdict |
|-------|---|---|---|---|---|---|-----|---------|
| LP-0001 Spec-to-App Builder | 5 | 5 | 5 | 5 | 5 | 4 | 4.83 | draft → **reviewed** (canonical candidate) |
| LP-0002 Polish Pass         | 5 | 5 | 5 | 4 | 5 | 5 | 4.83 | draft → **reviewed** (canonical candidate) |
| LP-0003 Coverage Climber    | 5 | 5 | 5 | 5 | 5 | 5 | 5.00 | draft → **reviewed** (strong canonical candidate) |
| LP-0004 Docs Gardener       | 5 | 5 | 5 | 5 | 4 | 5 | 4.83 | draft → **reviewed** (canonical candidate) |
| LP-0005 Library Grower      | 5 | 5 | 5 | 4 | 5 | 3 | 4.50 | draft → **reviewed** (see caveat) |

All five clear the `reviewed` bar. None demoted. Quality ratio moves 0/8 → 5/8.

## Per-entry notes (what was strong, what would raise the score)

**LP-0001 Spec-to-App Builder.** Textbook shape: one requirement/pass, split-if-too-big,
"do not start another," never-weaken-a-test, blocked-after-2. Memory split across
SPEC/progress/decisions/journal is exactly right. Axis 6 loses a point only because it
inherently requires the operator to bring a spec and runtime/test tooling — well-flagged,
not a defect. To reach canonical: a second reviewer's smoke-read on a real spec.

**LP-0002 Polish Pass.** The Declined ledger is the standout — it makes "worth fixing" a
binding, remembered decision instead of per-pass bikeshedding. Axis 4 is a 4 (not 5)
because the stop bar ("nothing above the worth-fixing bar") is judgment-based; the Declined
list bounds it honestly, so no cap applies. Canonical candidate.

**LP-0003 Coverage Climber.** The only 5.00 in the set. Numeric, checkable stop
(`current >= target`); pinned command in state; "behavioral tests, not implementation" and
"never weaken the code under test unless it's a real bug — then say so loudly" are
excellent guardrails. Strongest canonical candidate; wants only the independent smoke-read.

**LP-0004 Docs Gardener.** Clean two-mode (AUDIT/MEND) state machine driven entirely off
`docs-audit.md`; "examples that can run must be run" and the explicit doc-vs-code call with
journaled reasoning are strong. Axis 5 is a 4: verification is inspection-based by domain
(no test suite), with an `unverifiable:` escape — appropriate, but softer than a green-gate.

**LP-0005 Library Grower.** Re-entrancy, memory, and guardrails (two-iteration rule, role-
cycle-as-law, per-pass backlog cap) are exemplary — it is this repo's own engine. Two
honest caveats hold it at the `reviewed` floor rather than canonical:
- **Axis 6 = 3 (copy-paste truth).** The `## The Loop Prompt` fence contains the prompt's
  *shape*, not the complete prompt — the real prompt is `LOOP.md`, fetched by reference. A
  deliberate anti-drift choice, but it means this entry cannot be pasted and run on its own,
  and it sits in tension with SCHEMA §4 ("ONE fenced block containing the **complete**
  prompt"). Not a defect to "fix" blindly — a question for the Librarian/Auditor (below).
- **Axis 4 = 4 (stop condition).** "Never by design" is an honest, explicit non-terminating
  garden with a clear manual halt (`STOP`) and milestone markers — so it is *not* the vague
  "until it's good" anti-pattern (no cap), but it also offers no automatic done-state.

## Seeds for other roles (not acted on here — reviewer stays in lane)
- **Librarian/Auditor:** should SCHEMA §4 carve an explicit exemption for meta/reference-
  implementation loops whose prompt legitimately lives elsewhere (LP-0005), or should such
  entries inline a runnable copy? The validator currently passes LP-0005 because a fence
  exists; the rubric penalizes it because the fence isn't the whole prompt. Reconcile.
- **Reviewer (next pass):** four canonical candidates (LP-0001/0002/0003/0004) await an
  independent skeptical smoke-read by an iteration other than their author to reach
  `canonical`; LP-0003 first.
