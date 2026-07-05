---
id: LP-0008
title: Flake Hunter
category: testing
tier: medium
status: draft
version: 0.1.0
requires: [git, a test runner that can run a single test repeatedly, CI history or a flake list]
stop_when: no test in state/flakes.json is still "open" — each is fixed, quarantined, or accepted
state_files: [state/flakes.json, JOURNAL.md]
tags: [testing, flaky, reliability, ci]
related: [LP-0003]
created: 2026-07-05
updated: 2026-07-05
---

# Flake Hunter

Finds, reproduces, and kills one flaky test per pass. A flake is a test that passes and
fails on the same code — the most corrosive thing in a suite, because it teaches everyone
to ignore red. This loop makes flakiness a tracked, closeable queue instead of ambient
noise: reproduce the nondeterminism, fix the real cause, and only quarantine when a fix is
genuinely out of reach — never silently.

## When to reach for it
- A suite where reds are routinely re-run until green ("just hit retry").
- CI that is slow or distrusted because failures are often noise.
- Not a fit: a genuinely broken feature (that is a real failure, not a flake — fix the
  code); a suite with no way to run a single test in a loop (add that first).

## Setup
1. Note the command to run ONE test repeatedly (e.g. `pytest -k <id> --count 50`,
   `go test -run <T> -count=50`, `jest <file> -t "<name>"` in a loop).
2. Seed `state/flakes.json` from CI history or a known-bad list:
   ```json
   {
     "reruns": 50,
     "suspects": [
       { "test": "<fully-qualified test id>", "status": "open", "seen": "<where/when>" }
     ],
     "fixed": [],
     "quarantined": []
   }
   ```
   `status` is one of `open` | `fixed` | `quarantined` | `accepted`.

## The Loop Prompt

```
You are one pass of a flake-hunting loop. Files are your only memory; assume amnesia.

1. Read state/flakes.json and the last 30 lines of JOURNAL.md.
2. If no suspect has status "open": append "NO OPEN FLAKES" to JOURNAL.md, create a STOP
   file, commit, and exit.
3. Pick ONE "open" suspect. If the suspects list is empty but you have CI access, mine the
   last N failed runs for one test that also has green runs on the same commit, add it as
   a suspect, and take it.
4. Reproduce the flake: run that single test "reruns" times (from state). Record the
   observed failure rate (e.g. 7/50). If it passes 100%, it is not reproducibly flaky from
   here — mark it "accepted: not reproduced locally (Nx)" with the date and move on; do not
   guess at fixes for something you cannot see fail.
5. Diagnose the ONE root cause from the failure output. The usual suspects: test-order or
   shared-state coupling, real time / timezone, unseeded randomness, unawaited async or
   fixed sleeps, network/filesystem/DB assumptions, floating-point equality. Write the
   cause in the journal in one sentence.
6. Fix the CAUSE, not the symptom: seed the RNG, inject a clock, await the condition
   instead of sleeping, isolate the shared fixture, stub the boundary. Do NOT add blind
   retries or bump timeouts to paper over it. Re-run the single test "reruns" times: it
   must now pass 100%. Then run the surrounding file to confirm no collateral damage.
   - If you genuinely cannot fix it this pass: quarantine it with the runner's skip/exclude
     mechanism, tagged with a link to the diagnosis, and set status "quarantined". A
     quarantine is a tracked debt, never a silent skip.
7. Update state/flakes.json (move the suspect to fixed/quarantined, or mark accepted).
   Append a JOURNAL.md entry: test, failure rate before, root cause, fix or quarantine,
   rate after. Commit: "flake({test}): {cause} — {N/50}→0/50" or "flake({test}): quarantined".
   Stop.

Hard rules: one flake per pass; fix the cause, never add retries or inflate timeouts to
hide it; never delete a test to make red go away; a quarantine must carry a diagnosis and
a status, so the debt stays visible.
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
the undo button. `--permission-mode acceptEdits` when supervising. Reproduction can be slow
(50× a test); tune `reruns` down for fast suites, up for rare flakes.

## Stop condition
Every suspect is `fixed`, `quarantined`, or `accepted` → the loop writes "NO OPEN FLAKES",
creates STOP, and halts. Feed it new suspects from CI and clear STOP to keep hunting. The
`quarantined` list is a standing to-do: the debt that a future pass or human must still pay.

## Failure modes
- **Can't reproduce locally** → the `accepted: not reproduced` path; never fabricate a fix
  for a failure you never observed. Note the environment gap for CI-side investigation.
- **"Fix" is a hidden retry** → explicitly banned; retries and timeout bumps mask flakes
  and let them rot. Quarantine honestly instead if the real cause resists.
- **Fixing one flake reveals another** (shared-state dominoes) → one per pass keeps commits
  bisectable; add the newly-exposed test as a new suspect rather than chasing both at once.
- **Quarantine becomes a graveyard** → status + diagnosis keep it visible; the stop
  condition does not count `quarantined` as done work, only as tracked debt.

## Variations
- CI-mining mode: step 3 pulls suspects straight from the last N CI runs by
  green-and-red-on-same-sha detection, so the loop feeds itself.
- Stress mode: raise `reruns` and run under load / parallelism to surface concurrency
  flakes that a quiet single-threaded rerun hides.

## Review log
_(reviewers append here)_
