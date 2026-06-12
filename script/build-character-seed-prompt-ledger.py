#!/usr/bin/env python3
"""Build and check a review ledger for character seed image prompts."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "documentation" / "character-seed-prompt-ledger.md"
EXPORT_SCRIPT = ROOT / "script" / "export-character-seed-prompts.py"
MOD = ROOT / "mod"
sys.dont_write_bytecode = True

REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)",
    re.S,
)


def load_exporter():
    spec = importlib.util.spec_from_file_location("export_character_seed_prompts", EXPORT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {EXPORT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def prompt_kind(heading: str) -> str:
    lower = heading.lower()
    if "portrait" in lower:
        return "portrait"
    if heading.startswith("`cp_") or "still" in lower or "event" in lower or "future" in lower:
        return "scene"
    return "seed"


def script_files() -> list[Path]:
    return sorted((MOD / "common").glob("**/*.txt")) + sorted((MOD / "events").glob("*.txt"))


def registered_persons() -> set[str]:
    text = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace") for path in script_files())
    return set(REGISTER_PERSON_RE.findall(text))


def build(version: str) -> tuple[str, list[str]]:
    exporter = load_exporter()
    version_filter = None if version == "all" else version
    prompts = exporter.collect_all(version_filter)
    persons = registered_persons()
    issues: list[str] = []

    if not prompts:
        issues.append(f"no character seed prompts found for version {version}")

    export_names: dict[tuple[str, str], str] = {}
    out_names: dict[tuple[str, str], str] = {}
    person_counts: Counter[str] = Counter()
    kind_counts: Counter[str] = Counter()
    version_counts: Counter[str] = Counter()
    source_files: dict[str, set[Path]] = defaultdict(set)

    for prompt in prompts:
        kind = prompt_kind(prompt.heading)
        key = (prompt.version, prompt.export_name)
        if key in export_names:
            issues.append(f"duplicate export name `{prompt.export_name}` in {rel(prompt.source)} and {export_names[key]}")
        export_names[key] = rel(prompt.source)

        out_key = (prompt.version, prompt.out_name)
        if out_key in out_names:
            issues.append(f"duplicate target PNG `{prompt.out_name}` in {rel(prompt.source)} and {out_names[out_key]}")
        out_names[out_key] = rel(prompt.source)

        person_counts[prompt.person] += 1
        kind_counts[kind] += 1
        version_counts[prompt.version] += 1
        source_files[prompt.person].add(prompt.source)

    if version != "all":
        missing_people = sorted(persons - set(person_counts))
        if missing_people:
            issues.append(
                f"registered person(s) missing seed prompts for {version}: "
                + ", ".join(f"`{person}`" for person in missing_people)
            )
        for person in sorted(persons & set(person_counts)):
            if not any(prompt.person == person and prompt_kind(prompt.heading) == "portrait" for prompt in prompts):
                issues.append(f"`{person}` has seed prompts for {version} but no canonical portrait prompt")

    versions = sorted(version_counts)
    manifest_lines = []
    for prompt_version in versions:
        _prompt_dir, manifest = exporter.output_paths(prompt_version)
        manifest_lines.append(f"- `{rel(manifest)}`")

    lines = [
        "# Character Seed Prompt Ledger",
        "",
        "Generated from character seed prompt docs. Rebuild with:",
        "",
        "```bash",
        f"python3 script/build-character-seed-prompt-ledger.py --version {version}",
        f"python3 script/build-character-seed-prompt-ledger.py --version {version} --check",
        "python3 script/export-character-seed-prompts.py --version v0.1 --check",
        "```",
        "",
        "This ledger is the review surface for the first non-Layla character art pass. The exported prompt files and JSONL manifests are generation-ready inputs for `gpt-image-2`; promoted event art still has to pass the event image and provenance audits.",
        "",
        "## Summary",
        "",
        f"- Requested version: `{version}`",
        f"- Versions found: {', '.join(f'`{item}`' for item in versions) if versions else '-'}",
        f"- Registered persons: {len(persons)}",
        f"- Persons with prompts: {len(person_counts)}",
        f"- Registered-person coverage: {len(persons & set(person_counts))}/{len(persons)}",
        f"- Prompt files: {sum(len(files) for files in source_files.values())}",
        f"- Prompt exports: {len(prompts)}",
        f"- Issues: {len(issues)}",
        "",
        "## Batch Manifests",
        "",
    ]
    lines.extend(manifest_lines or ["- -"])

    lines.extend([
        "",
        "## Prompt Types",
        "",
    ])
    for kind, count in sorted(kind_counts.items()):
        lines.append(f"- `{kind}`: {count}")

    lines.extend([
        "",
        "## Person Counts",
        "",
        "| Person | Prompt Files | Prompts |",
        "|---|---:|---:|",
    ])
    for person in sorted(person_counts):
        lines.append(f"| `{person}` | {len(source_files[person])} | {person_counts[person]} |")

    lines.extend([
        "",
        "## Seed Prompts",
        "",
        "| Person | Prompt | Kind | Source | Export | Target PNG |",
        "|---|---|---|---|---|---|",
    ])
    for prompt in prompts:
        prompt_dir, _manifest = exporter.output_paths(prompt.version)
        export_path = prompt_dir / prompt.export_name
        target_path = prompt_dir.parent / prompt.out_name
        lines.append(
            f"| `{prompt.person}` | {md(prompt.heading)} | {prompt_kind(prompt.heading)} | "
            f"`{rel(prompt.source)}` | `{rel(export_path)}` | `{rel(target_path)}` |"
        )

    lines.extend([
        "",
        "## Rules",
        "",
        "- Seed prompt docs live at `documentation/characters/<person>/prompts/seed-v*.md`.",
        "- Versioned seed batches must cover every registered person and include one canonical portrait prompt per person.",
        "- Each prompt must be exported through `script/export-character-seed-prompts.py` before image generation.",
        "- Generated source PNGs should stay under `image/generated/character-seeds/<version>/` until a reviewed DDS or BK2 promotion path exists.",
        "- New character art should preserve the person token, scene purpose, and 3:2 event-window crop contract.",
        "",
        "## Checks",
        "",
        "```bash",
        "python3 script/audit-character-art-contract.py",
        f"python3 script/build-character-seed-prompt-ledger.py --version {version} --check",
        f"python3 script/export-character-seed-prompts.py --version {version} --check",
        "```",
    ])

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="v0.1", help="seed prompt version to build/check, or 'all'")
    parser.add_argument("--check", action="store_true", help="fail if the ledger is stale or has prompt issues")
    args = parser.parse_args()

    text, issues = build(args.version)
    if args.check:
        if issues:
            print("character seed prompt ledger issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-character-seed-prompt-ledger.py --version {args.version}", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
