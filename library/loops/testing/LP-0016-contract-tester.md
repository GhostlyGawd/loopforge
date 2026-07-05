---
id: LP-0016
title: Contract Tester
category: testing
tier: medium
status: draft
version: 0.1.0
requires: [git, a test runner, a service boundary with a consumer and a provider]
stop_when: every interaction in state/contracts.json has a passing consumer+provider contract test
state_files: [state/contracts.json, JOURNAL.md]
tags: [testing, contract, integration, boundary]
related: [LP-0011]
created: 2026-07-05
updated: 2026-07-05
---

# Contract Tester

Pins the agreement between a consumer and a provider across a service boundary, one
interaction per pass. Each pass writes a consumer-driven contract (the exact request the
consumer sends and the response shape it depends on), then verifies the provider honors it —
so a breaking change on either side turns a fast test red instead of surfacing in production.
It closes the gap that unit tests (each side mocks the other) and full e2e (slow, flaky)
both leave open.

## When to reach for it
- Two independently-deployed services (or a frontend and an API) that must agree on a wire format.
- You keep getting burned by "the provider changed a field and the consumer broke."
- Not a fit: a single in-process module boundary (a unit/integration test is enough); a
  third-party API you don't control the provider side of (use recorded-response tests instead).

## Setup
1. Pick a contract tool (Pact-style, or a hand-rolled shared-schema check) and note how to run
   the consumer side (generate/verify the contract) and the provider side (verify against it).
2. Seed `state/contracts.json`:
   ```json
   {
     "consumer_command": "<runs consumer contract tests / generates the pact>",
     "provider_command": "<verifies the provider against the contract>",
     "interactions": [
       { "name": "GET /widgets/{id} -> 200 widget", "status": "pending" }
     ]
   }
   ```
   List each request/response interaction the consumer relies on; each starts `pending`.

## The Loop Prompt

```
You are one pass of a contract-testing loop. Files are your only memory; assume amnesia.

1. Read state/contracts.json and the last 30 lines of JOURNAL.md.
2. If no interaction is "pending": run consumer_command and provider_command once more; if
   both green, append "CONTRACTS COVERED" to JOURNAL.md, create a STOP file, commit, and exit.
3. Pick ONE "pending" interaction — prefer the ones whose breakage would hurt most (auth,
   money, the highest-traffic reads).
4. Write the CONSUMER side of the contract: the exact request the consumer makes and ONLY the
   parts of the response it actually depends on (fields, types, status). Do not over-specify —
   pinning fields the consumer ignores makes the contract brittle and blocks safe provider
   evolution. Assert on shape/type, not on incidental example values, unless the value is
   semantically required.
5. Verify the PROVIDER honors it: run provider_command against the real provider (or its
   test double built from real handlers). If the provider does NOT satisfy the contract, that
   is a genuine finding — do not weaken the contract to make it pass. Either the provider has a
   bug (record it loudly in the journal and mark the interaction "blocked: provider mismatch —
   <detail>") or the consumer's expectation was wrong (fix the consumer expectation and say so).
6. Run both sides green. Mark the interaction done. Append a JOURNAL.md entry: interaction,
   what the consumer depends on, provider result. Commit: "contract({name}): pin + verify". Stop.

Hard rules: one interaction per pass; the contract encodes only what the consumer truly needs
(no over-specification); never weaken a contract just to make a red provider pass — a mismatch
is a real bug or a wrong expectation, recorded either way; assert shapes, not incidental values.
```

## Harness

```bash
while :; do
  [ -f STOP ] && break
  claude -p "$(cat PROMPT.md)" --dangerously-skip-permissions
  sleep 2
done
```

Run unattended loops in a container or dedicated VM with only the project mounted; git is the
undo button. `--permission-mode acceptEdits` when supervising. Contract tests are fast and
deterministic (no live cross-service calls needed if the provider verifies against its handlers).

## Stop condition
Every interaction has a passing consumer + provider contract test → the loop writes
"CONTRACTS COVERED", creates STOP, halts. Add interactions as the boundary grows and clear
STOP; run both sides in each service's CI so either team's breaking change fails fast.

## Failure modes
- **Over-specification** (pinning fields the consumer ignores) → the "only what the consumer
  needs" rule keeps contracts loose enough to let the provider evolve safely.
- **Weakening a contract to go green** → banned; a provider mismatch is a real finding, fixed
  or blocked with a diagnosis, never hidden.
- **Contracts that drift from real deploys** → both sides must run in CI; a contract not
  verified against the actual provider is decoration, not a guarantee.
- **Asserting incidental values** → assert types/shapes; pin a concrete value only when it is
  semantically required (an enum, a status code).

## Variations
- Bi-directional mode: also generate a provider-driven contract for events the provider emits,
  so async/message boundaries are covered too.
- Schema-registry mode: back contracts with a shared schema (OpenAPI/Avro) and assert
  compatibility on every change instead of per-interaction pacts.

## Review log
_(reviewers append here)_
