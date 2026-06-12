#!/usr/bin/env python3
"""Audit per-person narrative docs for the scalable person contract."""

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
REQUIRED_SECTIONS = {
    "token": re.compile(r"\b(?:Name token|Token)\b|\bcp_[A-Za-z0-9_]+_alive\b", re.I),
    "home": re.compile(r"\b(?:Home|residence|lives?|STATE_|state marker|home state)\b", re.I),
    "work": re.compile(r"\b(?:Work|workplace|Pop cohort|Pop type|Occupation|laborer|worker|clerk|shopkeeper|porter|soldier|peasant)\b", re.I),
    "entry": re.compile(r"\b(?:Entry|Enters|appears?|registers?|startup|conditional|try_spawn|first appearance|shared wiring)\b", re.I),
    "events": re.compile(r"\b(?:Event Surface|Current Events|content|cp_[A-Za-z0-9_]+\.[0-9]+)\b", re.I),
}
STALE_DOC_PATTERNS = {
    "moving video art claim": re.compile(r"All visible events use moving event-window video art", re.I),
}


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


def main() -> int:
    issues: list[tuple[str, str]] = []
    persons = registered_persons()
    dirs = character_dirs_by_person(persons)

    for person in sorted(persons):
        character_dir = dirs.get(person)
        if character_dir is None:
            issues.append(("CHARACTER_DOC_MISSING", f"{person} has no matching documentation/characters README"))
            continue

        readme = character_dir / "README.md"
        text = readme.read_text(encoding="utf-8", errors="replace")
        for section, pattern in REQUIRED_SECTIONS.items():
            if not pattern.search(text):
                issues.append(("CHARACTER_DOC_CONTRACT", f"{rel(readme)} lacks {section} contract text"))
        for label, pattern in STALE_DOC_PATTERNS.items():
            if pattern.search(text):
                issues.append(("CHARACTER_DOC_STALE", f"{rel(readme)} contains stale {label}"))

    print("Common People character doc contract audit")
    print(f"Registered persons: {len(persons)}")
    print(f"Character docs matched: {len(dirs)}")
    print("Required README contract: token, home/residence, work/pop cohort, entry/routing, event surface")
    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"- [{code}] {message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
