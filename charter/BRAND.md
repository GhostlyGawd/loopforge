# BRAND — Identity (pre-brand)

**Status: PRE-BRAND.** "Loopforge" is a codename. The site ships in a deliberately
unbranded engineering-blueprint style: a machine drawn in outline, awaiting its livery.
The system chooses its own identity — that's the point.

## The Naming Ceremony (Designer, bootstrap item B5)
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
