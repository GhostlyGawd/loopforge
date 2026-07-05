# BRAND — Identity (brand v1: Weft)

**Status: NAMED — brand v1, "Weft" (ADR-003, i5).** The codename was "Loopforge". The
system chose its own name in the Naming Ceremony below. The site header, page title, and
INDEX now render as **Weft** (build.py reads `name` from STATE.json). The blueprint palette
is still applied to the site template pending B6, which restyles it to the brand-v1 palette
under the two-iteration rule (ADR-003).

## Brand v1

**Name — Weft.** In weaving, the *weft* is the thread the shuttle carries across the warp
on every repeated pass; the cloth that accumulates is the whole fabric. One pass = one
weft thread. The library is the cloth. It reads as a plain, quiet CLI word: `weft`.

**ASCII wordmark** (must render in any terminal — non-negotiable):

```
W   W  EEEEE  FFFFF  TTTTT
W   W  E      F        T
W W W  EEEE   FFFF     T
W W W  E      F        T
 W W   EEEEE  F        T   >------------->
```

**Signature visual element — the weft line.** A single shuttle carried across the warp:
`>------------->`. Used exactly once per surface (under the wordmark, or as one section
rule). One signature, everything else quiet — don't decorate, encode.

**Palette (brand v1 — 6 named values):**

| token       | hex       | role                                             |
|-------------|-----------|--------------------------------------------------|
| `--warp`    | `#0E1726` | page ground — the tensioned dark warp / workshop |
| `--cloth`   | `#16233A` | panels/cards — cloth lifted just off the ground  |
| `--thread`  | `#C9D6E5` | primary ink — pale linen text                    |
| `--selvage` | `#5B7186` | dim ink, borders — the muted fabric edge         |
| `--weft`    | `#E8C468` | the signature thread — accent, active stamps     |
| `--flash`   | `#6FB2A8` | a second thread — links / interactive states     |

**Type roles** (all monospace — identity must survive a terminal):
- *Wordmark/display*: monospace, uppercase, wide tracking (the ASCII block above).
- *Headings*: monospace, uppercase, generous letter-spacing.
- *Body/UI*: the `ui-monospace` system stack; never a proportional face.

**Voice:** plain, exact, unhurried. Banned clichés: "unleash", "seamless", "revolutionary"
(and hype words generally). Plain verbs, sentence case, specific over clever.

---

## The Naming Ceremony (Designer, bootstrap item B5) — run at i5; brief preserved
In one iteration, the Designer must:
1. Generate ≥ 8 candidate names; test each for: pronounceable, unique-enough (quick
   reasoning about collisions), meaningful to *loops/iteration/libraries*, works as a
   CLI word.
2. Choose one. Record the shortlist, the choice, and the reasoning as an ADR.
3. Set `name` in `state/STATE.json`; update README title and site header.
4. Design a wordmark that renders in **plain ASCII** (the brand must survive a
   terminal) plus its styled site form.
5. Define brand v1 here: 4–6 named palette hex values, type roles, voice (3 adjectives
   + 3 banned clichés), and the one signature visual element.

## Standing constraints (survive any rebrand)
- Identity must work in a terminal. ASCII wordmark is non-negotiable.
- One signature element, everything else quiet. Don't decorate; encode.
- Voice: plain verbs, sentence case, specific over clever. No hype words.
- Rebrands are allowed but expensive: they require an Auditor-endorsed ADR.
