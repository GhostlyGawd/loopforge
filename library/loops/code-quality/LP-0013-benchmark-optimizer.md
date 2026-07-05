---
id: LP-0013
title: Benchmark Optimizer
category: code-quality
tier: large
status: draft
version: 0.1.1
requires: [git, a profiler, a benchmark harness with stable measurement, a test suite]
stop_when: no hotspot in state/perf-ledger.json is above the improvement threshold, or all remaining are accepted
state_files: [state/perf-ledger.json, JOURNAL.md]
tags: [performance, profiling, benchmarks, regression-guard]
related: [LP-0003]
created: 2026-07-05
updated: 2026-07-05
---

# Benchmark Optimizer

Optimizes performance one profiled hotspot per pass, and locks each win behind a perf
regression test so it can never silently rot. The discipline is profile-first: no change
is made without a measurement that justifies it, and none is kept without a before/after
that proves it and a test that guards it. Correctness is never traded for speed — the
functional suite must stay green.

## When to reach for it
- A program with a real, measured performance problem and a representative workload.
- You can measure reliably (warm caches, enough iterations, low variance).
- Not a fit: "make it faster" with no benchmark or target (build the benchmark first);
  micro-optimizing code that isn't hot (profile first — you'll be surprised).

## Setup
1. Build a repeatable benchmark with a representative workload; run it until variance is
   low (note iterations/warmup). Record the command and the metric (time, allocs, p99).
2. Capture a baseline profile and the baseline numbers.
3. Seed `state/perf-ledger.json`:
   ```json
   {
     "bench_command": "<runs the benchmark, prints the metric>",
     "profile_command": "<produces a profile>",
     "test_command": "<full functional suite>",
     "threshold_pct": 5,
     "baseline": { "metric": "wall_ms", "value": 0 },
     "hotspots": [],
     "accepted": []
   }
   ```
   `threshold_pct` is the smallest improvement worth keeping a change for.

## Run it

**One paste, then it loops itself.** Save the block below as `.claude/commands/benchmark-optimizer.md`. Run one pass with `/benchmark-optimizer`, or loop it with `/loop /benchmark-optimizer` (default 10m). It self-initializes on first run.

```markdown
---
description: Benchmark Optimizer — optimize one profiled hotspot per pass
---
You are one pass of a performance loop. Files are your only memory; assume amnesia.
Profile first: never optimize what you have not measured.

0. If state/perf-ledger.json does not exist: build a repeatable benchmark and capture a baseline, then create state/perf-ledger.json as { "bench_command": "", "profile_command": "", "test_command": "", "threshold_pct": 5, "baseline": { "metric": "wall_ms", "value": 0 }, "hotspots": [], "accepted": [] }; STOP and ask me to fill the commands + baseline, and re-run.
1. Read state/perf-ledger.json and the last 30 lines of JOURNAL.md.
2. Run "bench_command" to get the current number. If every known hotspot is fixed or
   accepted AND the current number is at/below target (or no hotspot beats threshold_pct):
   append "PERF TARGET MET at {value}" to JOURNAL.md, create a STOP file, commit, and exit.
3. Run "profile_command". Identify the ONE biggest hotspot not already fixed/accepted —
   the function or allocation site with the largest share of the metric. Record its share.
4. Form ONE hypothesis for why it is slow (algorithmic complexity, needless allocation,
   repeated work, cache misses, I/O in a loop, wrong data structure) and make the SINGLE
   smallest change that tests it. Prefer algorithmic wins over micro-tuning. Do not rewrite
   unrelated code; do not trade correctness for speed.
5. Verify BOTH:
   a. Correctness: run "test_command". Any red you caused → revert; the change is rejected.
   b. Speed: re-run "bench_command". If the improvement is < threshold_pct, revert and mark
      the hotspot "accepted: <hypothesis> gave <x%>, below threshold" so it is not retried.
6. If kept: write a perf regression test that fails if this hotspot regresses past a set
   bound (assert the benchmark metric stays under a ceiling, or the big-O via input scaling).
   Update baseline.value to the new number; move the hotspot to fixed with before→after.
7. Append a JOURNAL.md entry: hotspot, hypothesis, before→after (with %), test added.
   Commit: "perf({hotspot}): {before}→{after} ({pct}%)". Stop.

Hard rules: one hotspot per pass; profile before you touch anything; correctness suite must
stay green (revert on red); a kept win ships with a regression test; a change below threshold
is reverted and "accepted", never kept "just because"; report numbers, never vibes.
```

For fully unattended runs outside an interactive session, use the shell loop in `## Harness`.

## The Loop Prompt

```
You are one pass of a performance loop. Files are your only memory; assume amnesia.
Profile first: never optimize what you have not measured.

1. Read state/perf-ledger.json and the last 30 lines of JOURNAL.md.
2. Run "bench_command" to get the current number. If every known hotspot is fixed or
   accepted AND the current number is at/below target (or no hotspot beats threshold_pct):
   append "PERF TARGET MET at {value}" to JOURNAL.md, create a STOP file, commit, and exit.
3. Run "profile_command". Identify the ONE biggest hotspot not already fixed/accepted —
   the function or allocation site with the largest share of the metric. Record its share.
4. Form ONE hypothesis for why it is slow (algorithmic complexity, needless allocation,
   repeated work, cache misses, I/O in a loop, wrong data structure) and make the SINGLE
   smallest change that tests it. Prefer algorithmic wins over micro-tuning. Do not rewrite
   unrelated code; do not trade correctness for speed.
5. Verify BOTH:
   a. Correctness: run "test_command". Any red you caused → revert; the change is rejected.
   b. Speed: re-run "bench_command". If the improvement is < threshold_pct, revert and mark
      the hotspot "accepted: <hypothesis> gave <x%>, below threshold" so it is not retried.
6. If kept: write a perf regression test that fails if this hotspot regresses past a set
   bound (assert the benchmark metric stays under a ceiling, or the big-O via input scaling).
   Update baseline.value to the new number; move the hotspot to fixed with before→after.
7. Append a JOURNAL.md entry: hotspot, hypothesis, before→after (with %), test added.
   Commit: "perf({hotspot}): {before}→{after} ({pct}%)". Stop.

Hard rules: one hotspot per pass; profile before you touch anything; correctness suite must
stay green (revert on red); a kept win ships with a regression test; a change below threshold
is reverted and "accepted", never kept "just because"; report numbers, never vibes.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Run unattended loops in a container or dedicated VM with only the project mounted; git is
the undo button. `--permission-mode acceptEdits` when supervising. Pin the benchmark
environment (CPU governor, no noisy neighbors) or variance will drown the signal — run on a
quiet, consistent machine.

## Stop condition
No remaining hotspot beats `threshold_pct` (or the target metric is met) → the loop writes
"PERF TARGET MET", creates STOP, and halts. The lasting output is not just a faster program
but a suite of perf regression tests that keep it fast. Lower the target or add a workload
and clear STOP to keep optimizing.

## Failure modes
- **Optimizing cold code** → profile-first rule; the hotspot is chosen from the profile,
  not from intuition about what "feels" slow.
- **Speed at the cost of correctness** → the functional suite is a hard gate; any red
  reverts the change, no exceptions.
- **Measurement noise read as a win** → threshold_pct plus low-variance benchmarking; a
  change under threshold is reverted, so noise can't masquerade as improvement.
- **Wins that silently regress later** → every kept win ships a regression test, so a future
  change that undoes it turns the suite red.

## Variations
- Allocation mode: swap the metric to allocations/GC pressure for memory-bound hotspots.
- Big-O mode: the regression test asserts scaling (time roughly linear in N) rather than an
  absolute ceiling, so it survives faster hardware.

## Review log
_(reviewers append here)_
