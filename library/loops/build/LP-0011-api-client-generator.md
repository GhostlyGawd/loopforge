---
id: LP-0011
title: API Client Generator
category: build
tier: medium
status: draft
version: 0.1.0
requires: [git, an OpenAPI/schema spec, the target language toolchain with a test runner]
stop_when: every endpoint in state/api-client.json is implemented and tested — none pending
state_files: [state/api-client.json, JOURNAL.md]
tags: [api, client, openapi, typed, codegen]
related: [LP-0001]
created: 2026-07-05
updated: 2026-07-05
---

# API Client Generator

Grows a hand-quality, typed API client one endpoint per pass from an OpenAPI (or similar)
spec. Unlike a bulk generator, each pass adds a single method with real types, a focused
test against the spec's schema, and a note — so the client stays readable, reviewed, and
diff-able, and a spec change touches exactly the endpoints that moved.

## When to reach for it
- You consume an API that ships a machine-readable spec (OpenAPI/Swagger, GraphQL SDL, gRPC).
- You want a typed client you can actually read and trust, grown incrementally.
- Not a fit: a one-shot throwaway script (just call fetch); an API with no spec (write the
  spec first, or use a different loop to reverse-engineer one).

## Setup
1. Put the spec at `spec/openapi.yaml` (or point at its URL) and note the base URL.
2. Establish the client skeleton: a typed HTTP core (auth, base URL, error handling) and
   one place methods are added. Get one trivial call working by hand first.
3. Seed `state/api-client.json`:
   ```json
   {
     "spec": "spec/openapi.yaml",
     "test_command": "<runs the client's tests>",
     "endpoints": [
       { "op": "getWidget", "method": "GET", "path": "/widgets/{id}", "status": "pending" }
     ]
   }
   ```
   Populate `endpoints` from the spec's operations; each starts `pending`.

## The Loop Prompt

```
You are one pass of an API-client loop. Files are your only memory; assume amnesia.

1. Read state/api-client.json and the last 30 lines of JOURNAL.md.
2. If no endpoint is "pending": run the full test suite once more; if green, append
   "CLIENT COMPLETE — all endpoints implemented" to JOURNAL.md, create a STOP file,
   commit, and exit.
3. Pick ONE "pending" endpoint — prefer the ones others depend on (auth, then reads that
   later writes will need), and simple shapes before deeply-nested ones.
4. Read that operation in the spec: path, method, params (path/query/header/body), request
   and response schemas, error responses. Implement ONE typed client method for it:
   accurate parameter and return types generated from the schema (not `any`), the correct
   HTTP call through the shared core, and typed error handling for the documented failures.
   Follow the existing client's conventions exactly; do not restructure the core this pass.
5. Write a focused test: it asserts the method builds the right request (path, query, body)
   and decodes a spec-shaped response into the right type — mock the transport so the test
   is deterministic and needs no live server. One happy path + one documented error.
6. Run "test_command". Red because of your work → fix it; if the spec itself is ambiguous
   or contradictory, do NOT guess — mark the endpoint "blocked: <question>" and pick another.
7. Mark the endpoint "done" in state. Append a JOURNAL.md entry: op, types added, anything
   the spec left unclear. Commit: "client({op}): typed {method} {path}". Stop.

Hard rules: one endpoint per pass; types come from the schema, never `any` to move on;
every method ships with a test; never invent behavior the spec doesn't state — a spec gap
is "blocked:" with the question, not a guess; don't refactor the shared core mid-endpoint.
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
the undo button. `--permission-mode acceptEdits` when supervising. Tests mock the transport,
so passes need no network and stay deterministic.

## Stop condition
Every endpoint `done` and the suite green → the loop writes "CLIENT COMPLETE", creates
STOP, and halts. When the spec changes, diff it into the endpoint list (new = `pending`,
changed = `pending` again), clear STOP, and the loop re-touches only what moved.

## Failure modes
- **`any`-typed shortcuts** → banned; types are generated from the schema, so the client's
  value (compile-time safety) survives. A genuinely untyped `additionalProperties` is typed
  as such explicitly, not blanket-`any`.
- **Spec ambiguity or drift from reality** → "blocked:" with the exact question rather than
  a guess; a human or a spec-fix pass resolves it. The client never encodes a hallucinated shape.
- **Tests that need a live server** (flaky, slow) → the transport is mocked; assertions are
  on request-building and response-decoding, not on a real endpoint.
- **Core churn** → the shared HTTP core is frozen during endpoint passes; changing it is a
  separate, deliberate task so one pass never rewrites the foundation under the others.

## Variations
- GraphQL mode: `endpoints` become operations from the SDL; generate typed documents +
  result types per query/mutation.
- Contract-test mode: additionally assert the mocked responses validate against the live
  spec schema, so the client and spec can't silently diverge.

## Review log
_(reviewers append here)_
