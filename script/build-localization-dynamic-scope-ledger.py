#!/usr/bin/env python3
"""Build and check the dynamic localization scope ledger."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "documentation" / "localization-dynamic-scope-ledger.md"
AUDIT = ROOT / "script" / "audit-localization-dynamic-scope.py"
sys.dont_write_bytecode = True


def load_audit():
    spec = importlib.util.spec_from_file_location("audit_localization_dynamic_scope", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {AUDIT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def build() -> tuple[str, list[object]]:
    audit = load_audit()
    calls, issues = audit.collect()
    category_counts = Counter(call.category for call in calls)

    lines = [
        "# Dynamic Localization Scope Ledger",
        "",
        "Generated from shipped English localization. Rebuild with:",
        "",
        "```bash",
        "python3 script/build-localization-dynamic-scope-ledger.py",
        "python3 script/build-localization-dynamic-scope-ledger.py --check",
        "python3 script/audit-localization-dynamic-scope.py",
        "```",
        "",
        "This ledger prevents the ruler-audience regression where unsupported dynamic loc rendered as `ERROR:[c:EGY.GetRuler...]` in game. New dynamic localization expressions must either match a reviewed safe pattern here or be deliberately added to the audit allow-list with a note.",
        "",
        "## Contract",
        "",
        "- Do not use direct tag scopes such as `[c:EGY...]` in player-facing localization.",
        "- Do not use `GetRuler.GetTitle`; Victoria 3 1.13 uses `GetRuler.GetPrimaryRoleTitle`.",
        "- Ruler references must use `[ROOT.GetCountry.GetRuler.GetFullName]` and `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` in country events.",
        "- Legacy Layla journal variables use the proven `Country.MakeScope.Var(...)` form.",
        "- Legacy Layla journal labels and prose fragments use `ROOT.GetCountry.GetCustom('cp_layla_*')`.",
        "- Shared active journal slots use `ROOT.GetCountry.GetCustom('cp_common_people_active_body')` and `ROOT.GetCountry.GetCustom('cp_common_people_active_slot_<n>')`.",
        "- Shared active person stats may render only age, SoL, hope, and literacy through reviewed `Country.MakeScope.Var('cp_<person>_<stat>')` expressions.",
        "",
        "## Summary",
        "",
        f"- Dynamic expressions reviewed: {len(calls)}",
        f"- Allowed categories: {len(category_counts)}",
        f"- Issues: {len(issues)}",
        "",
        "## Category Counts",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in sorted(category_counts.items()):
        lines.append(f"| {md(category)} | {count} |")

    lines.extend([
        "",
        "## Dynamic Expressions",
        "",
        "| File | Key | Expression | Category |",
        "|---|---|---|---|",
    ])
    for call in sorted(calls, key=lambda item: (str(item.path), item.line, item.key, item.expression)):
        lines.append(
            f"| `{rel(call.path)}:{call.line}` | `{call.key}` | "
            f"`[{md(call.expression)}]` | {md(call.category)} |"
        )

    lines.extend([
        "",
        "## Checks",
        "",
        "```bash",
        "python3 script/audit-localization-dynamic-scope.py",
        "python3 script/build-localization-dynamic-scope-ledger.py --check",
        "script/audit-common-people.py",
        "script/audit-production-debug-leaks.py",
        "```",
    ])

    if issues:
        lines.extend(["", "## Issues", ""])
        for issue in issues:
            lines.append(
                f"- `{rel(issue.path)}:{issue.line}` `{issue.key}` "
                f"`[{md(issue.expression)}]`: {md(issue.message)}"
            )

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the ledger is stale or dynamic loc issues exist")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("dynamic localization scope ledger issues:", file=sys.stderr)
            for issue in issues:
                print(
                    f"- {rel(issue.path)}:{issue.line}: {issue.key} "
                    f"[{issue.expression}]: {issue.message}",
                    file=sys.stderr,
                )
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-localization-dynamic-scope-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
