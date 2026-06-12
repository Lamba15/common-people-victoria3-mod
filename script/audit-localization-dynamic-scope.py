#!/usr/bin/env python3
"""Audit dynamic localization calls that can show in player-facing text."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOC_DIR = ROOT / "mod" / "localization" / "english"

LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.-]+):\d+\s+"(.*)"\s*$')
DYNAMIC_RE = re.compile(r"\[([^\[\]]+)\]")

ALLOWED_EXACT = {
    "ROOT.GetCountry.GetRuler.GetFullName": "country ruler full name",
    "ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle": "country ruler role title",
    "Country.MakeScope.Var('cp_layla_age').GetValue|D": "Layla age variable",
    "Country.MakeScope.Var('cp_layla_hope').GetValue|D": "Layla hope variable",
    "Country.MakeScope.Var('cp_layla_sol').GetValue|1": "Layla SoL variable",
    "Country.MakeScope.Var('cp_layla_sol_delta').GetValue|1": "Layla SoL delta variable",
}

PERSON_TOKENS = (
    "layla",
    "nour",
    "mina",
    "zaynab",
    "bey",
    "nabil",
    "rashid",
    "salma",
    "samier",
    "tarek",
    "karim",
    "mansur",
    "soldier",
    "farid",
    "dawud",
    "huda",
)
PERSON_RE = "|".join(PERSON_TOKENS)

ALLOWED_CUSTOM_RE = re.compile(r"^ROOT\.GetCountry\.GetCustom\('cp_layla_[A-Za-z0-9_]+'\)$")
ALLOWED_SHARED_CUSTOM_RE = re.compile(
    rf"^ROOT\.GetCountry\.GetCustom\('(?:cp_common_people_active_(?:body|slot_[123])|cp_roster_(?:{PERSON_RE})_current)'\)$"
)
ALLOWED_ROSTER_INT_RE = re.compile(
    rf"^Country\.MakeScope\.Var\('cp_(?:{PERSON_RE})_(?:age|hope|literacy)'\)\.GetValue\|D$"
)
ALLOWED_ROSTER_SOL_RE = re.compile(
    rf"^Country\.MakeScope\.Var\('cp_(?:{PERSON_RE})_sol'\)\.GetValue\|1$"
)
ALLOWED_ROSTER_STATE_RE = re.compile(
    rf"^Country\.MakeScope\.Var\('cp_(?:{PERSON_RE})_state_pointer'\)\.GetState\.GetStateRegion\.GetName$"
)
FORBIDDEN_PATTERNS = [
    (re.compile(r"^[a-z]:[A-Z0-9_]+\."), "direct tag scopes such as c:EGY do not resolve reliably in V3 loc"),
    (re.compile(r"\bGetRuler\.GetTitle\b"), "use GetRuler.GetPrimaryRoleTitle on Victoria 3 1.13"),
    (re.compile(r"\bGetRuler\.GetFullName\b"), "ruler name must be reached through ROOT.GetCountry.GetRuler.GetFullName"),
    (re.compile(r"\bGetRuler\.GetPrimaryRoleTitle\b"), "ruler title must be reached through ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle"),
]


@dataclass(frozen=True)
class DynamicCall:
    path: Path
    line: int
    key: str
    expression: str
    category: str


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    key: str
    expression: str
    message: str


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def unescape_loc_value(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\n", "\n")


def classify(expression: str) -> tuple[str | None, str | None]:
    if expression in ALLOWED_EXACT:
        return ALLOWED_EXACT[expression], None
    if ALLOWED_CUSTOM_RE.match(expression):
        return "Layla custom localization", None
    if ALLOWED_SHARED_CUSTOM_RE.match(expression):
        return "shared active-roster custom localization", None
    if ALLOWED_ROSTER_INT_RE.match(expression):
        return "shared active-roster integer variable", None
    if ALLOWED_ROSTER_SOL_RE.match(expression):
        return "shared active-roster SoL variable", None
    if ALLOWED_ROSTER_STATE_RE.match(expression):
        return "shared active-roster home state pointer", None
    for pattern, message in FORBIDDEN_PATTERNS:
        if pattern.search(expression):
            return None, message
    return None, "dynamic localization expression is not in the reviewed allow-list"


def collect() -> tuple[list[DynamicCall], list[Issue]]:
    calls: list[DynamicCall] = []
    issues: list[Issue] = []

    for path in sorted(LOC_DIR.glob("*.yml")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            match = LOC_RE.match(line)
            if not match:
                continue
            key, raw_value = match.groups()
            value = unescape_loc_value(raw_value)
            for dynamic in DYNAMIC_RE.findall(value):
                category, issue = classify(dynamic)
                if issue:
                    issues.append(Issue(path, line_no, key, dynamic, issue))
                else:
                    calls.append(DynamicCall(path, line_no, key, dynamic, category or "allowed"))

    return calls, issues


def main() -> int:
    calls, issues = collect()
    category_counts = Counter(call.category for call in calls)

    print("Common People dynamic localization scope audit")
    print(f"Localization files: {len(list(LOC_DIR.glob('*.yml')))}")
    print(f"Reviewed dynamic expressions: {len(calls)}")
    print("Allowed categories:")
    for category, count in sorted(category_counts.items()):
        print(f"  {count:3}  {category}")
    print(f"Issues: {len(issues)}")
    for issue in issues:
        print(
            f"[FAIL] {rel(issue.path)}:{issue.line}: {issue.key} "
            f"uses [{issue.expression}]: {issue.message}"
        )
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
