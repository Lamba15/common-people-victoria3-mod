#!/usr/bin/env python3
"""Audit per-person visual prompt contracts for Common People."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
CHARACTERS = ROOT / "documentation" / "characters"

REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)",
    re.S,
)
TOKEN_PATTERNS = (
    re.compile(r"\b(?:Name token|Token)\b\**:?\s*`([A-Za-z0-9_]+)`", re.I),
    re.compile(r"\|\s*(?:Name token|Token)\s*\|\s*`([A-Za-z0-9_]+)`\s*\|", re.I),
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def script_files() -> list[Path]:
    return sorted((MOD / "common").glob("**/*.txt")) + sorted((MOD / "events").glob("*.txt"))


def registered_persons() -> set[str]:
    text = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace") for path in script_files())
    return set(REGISTER_PERSON_RE.findall(text))


def token_for_readme(path: Path, persons: set[str]) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    for pattern in TOKEN_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1)
    if path.parent.name in persons:
        return path.parent.name
    return None


def character_dirs_by_person(persons: set[str]) -> dict[str, Path]:
    dirs: dict[str, Path] = {}
    for readme in sorted(CHARACTERS.glob("*/README.md")):
        if readme.parent.name.startswith("_"):
            continue
        token = token_for_readme(readme, persons)
        if token in persons:
            dirs[token] = readme.parent
    return dirs


def prompt_files(character_dir: Path) -> list[Path]:
    prompts = character_dir / "prompts"
    if not prompts.exists():
        return []
    return sorted(path for path in prompts.glob("*.md") if path.name != ".gitkeep")


def prompt_has_contract(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return "Use case: historical-scene" in text and "Asset type:" in text and (
        "Subject:" in text or "Scene:" in text or "Scene/backdrop:" in text
    )


def main() -> int:
    issues: list[tuple[str, str]] = []
    persons = registered_persons()
    dirs = character_dirs_by_person(persons)
    prompt_counts: dict[str, int] = {}
    contract_counts: dict[str, int] = {}

    for person in sorted(persons):
        character_dir = dirs.get(person)
        if character_dir is None:
            issues.append(("CHARACTER_DOC_MISSING", f"registered person {person} has no documentation/characters README with a matching token"))
            continue
        prompts = prompt_files(character_dir)
        prompt_counts[person] = len(prompts)
        if not prompts:
            issues.append(("PROMPT_DOC_MISSING", f"{person} has no markdown prompt contract under {rel(character_dir / 'prompts')}"))
            continue
        valid = [path for path in prompts if prompt_has_contract(path)]
        contract_counts[person] = len(valid)
        if not valid:
            issues.append(("PROMPT_CONTRACT_MISSING", f"{person} prompt docs lack a historical-scene prompt contract: {', '.join(rel(path) for path in prompts)}"))

    print("Common People character art contract audit")
    print(f"Registered persons: {len(persons)}")
    print(f"Character docs matched: {len(dirs)}")
    print(f"Persons with prompt docs: {sum(1 for count in prompt_counts.values() if count > 0)}")
    print(f"Persons with prompt contracts: {sum(1 for count in contract_counts.values() if count > 0)}")
    print("Prompt files by person:")
    for person in sorted(persons):
        count = prompt_counts.get(person, 0)
        valid = contract_counts.get(person, 0)
        print(f"  {person}: {count} prompt file(s), {valid} contract file(s)")
    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"- [{code}] {message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
