# QUALITY — What Makes a Loop Prompt Great

A loop prompt is a program whose interpreter is an agent. Judge it like a program.

## The six axes (score 1–5 each)

1. **Re-entrancy.** Safe to run 1,000 times. It re-reads state fresh every pass, assumes
   amnesia, and never depends on the previous run's context window.
2. **One-step discipline.** Each pass does exactly one smallest-valuable unit, then
   exits. No "and then also…".
3. **Externalized memory.** Names its state files explicitly. Progress, decisions, and
   failures all land on disk.
4. **Stop condition.** A checkable, honest definition of done — and instructions for
   what to do when reached (announce, tag, halt).
5. **Guardrails.** A validation gate before commit; failure handling (fix or revert);
   no destructive operations without a check; a blocked-task escape hatch.
6. **Copy-paste truth.** Runs as pasted: includes its harness snippet, prerequisites,
   and setup. No hidden assumptions.

## Scoring & the ladder
- **draft** — published, unscored.
- **reviewed** — avg ≥ 3.5, no axis below 3. Reviewer's scores recorded in the entry.
- **canonical** — avg ≥ 4.5 AND smoke-read (a full skeptical read-through simulating
  iteration 1 and iteration N) by an iteration other than the author's.
- **deprecated** — superseded or unsound. Keep the file; mark it; link its replacement.

## House anti-patterns (automatic score caps)
- Vague stop conditions ("until it's good") — caps axis 4 at 2.
- Multi-task passes ("do A, B and C each loop") — caps axis 2 at 2.
- Memory in prose ("remember that…") instead of files — caps axis 3 at 2.
- Prompts that only work on the happy path — caps axis 5 at 2.
