#!/usr/bin/env python3
"""Audit shipped localization for debug UI leaks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOC_DIR = ROOT / "mod" / "localization" / "english"

LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.-]+):\d+\s+"(.*)"\s*$')
FORBIDDEN_VALUE_PATTERNS = [
    re.compile(r"Journal Entry ID", re.I),
    re.compile(r"\bDEBUG:", re.I),
    re.compile(r"Open Event in text editor", re.I),
    re.compile(r"Trigger description", re.I),
    re.compile(r"\bEvent ID:", re.I),
    re.compile(r"\bERROR:", re.I),
    re.compile(r"(?<!['\"])\bcp_[A-Za-z0-9_.-]+\b"),
]

ALLOWED_DEBUG_KEYS = (
    "cp_debug.",
    "cp_debug_",
)


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    key: str
    value: str
    pattern: str


def unescape_loc_value(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\n", "\n")


def is_debug_only_key(key: str) -> bool:
    return key.startswith(ALLOWED_DEBUG_KEYS)


def scan_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = LOC_RE.match(line)
        if not match:
            continue
        key, raw_value = match.groups()
        if is_debug_only_key(key):
            continue
        value = unescape_loc_value(raw_value)
        for pattern in FORBIDDEN_VALUE_PATTERNS:
            if pattern.search(value):
                issues.append(Issue(path, line_no, key, value, pattern.pattern))
    return issues


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    issues: list[Issue] = []
    for path in sorted(LOC_DIR.glob("*.yml")):
        issues.extend(scan_file(path))

    print("Common People production debug-leak audit")
    print(f"Localization files: {len(list(LOC_DIR.glob('*.yml')))}")
    print(f"Issues: {len(issues)}")
    for issue in issues:
        print(
            f"[FAIL] {rel(issue.path)}:{issue.line}: {issue.key} "
            f"contains forbidden debug pattern {issue.pattern!r}"
        )
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
