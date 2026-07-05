#!/usr/bin/env python3
"""validate.py — the gate. Exits nonzero with readable errors if anything is off.

Checks: state files parse; taxonomy is sane; every library entry satisfies SCHEMA.md
(front matter, required sections, loop-prompt fence, id uniqueness, category/dir match).
Stdlib only, on purpose: future iterations must understand this at cat speed.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOOPS = ROOT / "library" / "loops"

REQUIRED_KEYS = [
    "id", "title", "category", "tier", "status", "version",
    "requires", "stop_when", "state_files", "tags", "created", "updated",
]
REQUIRED_SECTIONS = [
    "## When to reach for it",
    "## Setup",
    "## The Loop Prompt",
    "## Harness",
    "## Stop condition",
    "## Failure modes",
    "## Review log",
]
ID_RE = re.compile(r"^LP-\d{4}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def parse_front_matter(text, errors, label):
    """Minimal YAML-ish front matter parser: `key: value`, inline [a, b] lists."""
    if not text.startswith("---"):
        errors.append(f"{label}: missing front matter (must start with ---)")
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{label}: unterminated front matter")
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{label}: bad front matter line: {line!r}")
            continue
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.split(" #")[0].strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            meta[key] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key] = raw
    return meta, parts[2]


def load_taxonomy(errors):
    path = ROOT / "library" / "categories.json"
    try:
        tax = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - report and bail
        errors.append(f"categories.json: unreadable ({exc})")
        return None
    for key in ("categories", "tiers", "statuses"):
        if key not in tax:
            errors.append(f"categories.json: missing key {key!r}")
    return tax


def check_state(errors):
    path = ROOT / "state" / "STATE.json"
    try:
        state = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        errors.append(f"STATE.json: unreadable ({exc})")
        return
    for key in ("iteration", "phase", "role_queue", "codename"):
        if key not in state:
            errors.append(f"STATE.json: missing key {key!r}")
    if state.get("phase") not in ("bootstrap", "grow"):
        errors.append(f"STATE.json: phase must be bootstrap|grow, got {state.get('phase')!r}")


def check_entry(path, tax, seen_ids, errors):
    label = str(path.relative_to(ROOT))
    text = path.read_text()
    meta, body = parse_front_matter(text, errors, label)

    for key in REQUIRED_KEYS:
        if key not in meta:
            errors.append(f"{label}: front matter missing {key!r}")
    entry_id = meta.get("id", "")
    if entry_id:
        if not ID_RE.match(entry_id):
            errors.append(f"{label}: id {entry_id!r} must match LP-NNNN")
        if entry_id in seen_ids:
            errors.append(f"{label}: duplicate id {entry_id} (also in {seen_ids[entry_id]})")
        seen_ids[entry_id] = label

    cat_ids = {c["id"] for c in tax.get("categories", [])} if tax else set()
    if meta.get("category") and meta["category"] not in cat_ids:
        errors.append(f"{label}: category {meta['category']!r} not in categories.json")
    if meta.get("category") and path.parent.name != meta["category"]:
        errors.append(f"{label}: filed under {path.parent.name}/ but category is {meta['category']!r}")
    if tax:
        if meta.get("tier") and meta["tier"] not in tax.get("tiers", []):
            errors.append(f"{label}: tier {meta['tier']!r} not in taxonomy")
        if meta.get("status") and meta["status"] not in tax.get("statuses", []):
            errors.append(f"{label}: status {meta['status']!r} not in taxonomy")
    for key in ("created", "updated"):
        if meta.get(key) and not DATE_RE.match(meta[key]):
            errors.append(f"{label}: {key} must be YYYY-MM-DD")
    if meta.get("version") and not VERSION_RE.match(meta["version"]):
        errors.append(f"{label}: version must be semver (N.N.N)")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{label}: missing required section {section!r}")
    prompt_part = body.split("## The Loop Prompt", 1)
    if len(prompt_part) == 2:
        before_next = prompt_part[1].split("\n## ", 1)[0]
        if "```" not in before_next:
            errors.append(f"{label}: '## The Loop Prompt' has no fenced block")
    if text.count("```") % 2 != 0:
        errors.append(f"{label}: unbalanced code fences")
    return meta


def main():
    errors = []
    check_state(errors)
    tax = load_taxonomy(errors)
    entries = sorted(LOOPS.rglob("LP-*.md"))
    if not entries:
        errors.append("library/loops: no entries found")
    seen_ids = {}
    for path in entries:
        check_entry(path, tax, seen_ids, errors)

    if errors:
        print(f"VALIDATE: FAIL — {len(errors)} problem(s)")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    print(f"VALIDATE: OK — {len(entries)} entries, ids unique, schema satisfied")


if __name__ == "__main__":
    main()
