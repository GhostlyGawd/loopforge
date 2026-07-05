# DECISIONS — Architecture Decision Records (append-only)

Template:

```
## ADR-NNN — Title (iteration iN, role)
- Status: proposed | accepted | superseded-by-ADR-MMM
- Context:
- Decision:
- Consequences:
```

---

## ADR-000 — Genesis architecture (i0, genesis)
- Status: accepted
- Context: Need a self-running system where Claude Code iterations build a loop-prompt
  library with company-like specialization, self-review, and self-branding.
- Decision: File-based memory (state/), single-protocol loop (LOOP.md) with role
  rotation (charter/ROLES.md), schema-validated library (library/), generated index +
  site (tools/build.py), gates before every commit (tools/validate.py), self-modification
  only via two-iteration ADR rule.
- Consequences: Boring and legible over clever; every iteration is auditable via
  journal + one commit; the protocol itself is amendable but never silently.

## ADR-001 — Pre-brand blueprint identity (i0, genesis)
- Status: accepted (until Naming Ceremony)
- Context: The brand must be the system's own choice, but the site must exist first.
- Decision: Ship site v0 as an engineering blueprint — title block, grid field,
  outline-drawn machine awaiting livery — explicitly labeled pre-brand.
- Consequences: Designer's B5/B6 replace this identity; blueprint style is a valid
  fallback aesthetic the Designer may also choose to keep and refine.
