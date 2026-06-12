#!/usr/bin/env python3
"""Generate safe popup-QA selectors for every visible person event."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
AUDIT_PATH = ROOT / "script" / "audit-person-roster.py"
OUTPUT = EVENTS / "cp_debug_person_events.txt"
EFFECT_OUTPUT = MOD / "common" / "scripted_effects" / "cp_debug_person_fire_selected.txt"
LEGACY_EFFECT = MOD / "common" / "scripted_effects" / "cp_debug.txt"
SCRIPT_ENCODING = "utf-8-sig"

SELECTOR_RE = re.compile(
    r"limit\s*=\s*\{\s*var:cp_debug_selected_event\s*=\s*([0-9]+)\s*\}"
    r".*?"
    r"cp_button_fire\s*=\s*\{\s*event\s*=\s*([A-Za-z0-9_]+\.[0-9]+)\s+person\s*=\s*([A-Za-z0-9_]+)\s*\}",
    re.S,
)


@dataclass(frozen=True)
class Target:
    person: str
    event_id: str
    wrapper: int
    selector: int


def load_roster_audit():
    spec = importlib.util.spec_from_file_location("audit_person_roster", AUDIT_PATH)
    if not spec or not spec.loader:
        raise RuntimeError(f"could not load {AUDIT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def event_number(event_id: str) -> int:
    return int(event_id.split(".", 1)[1])


def generated_targets(audit) -> list[tuple[str, str]]:
    persons = audit.registered_persons()
    targets: list[tuple[str, str]] = []
    for block in audit.iter_event_blocks():
        event_id = str(block["id"])
        if not audit.visible_event(block):
            continue
        owners = [person for person in persons if audit.person_owns_event(person, event_id)]
        if len(owners) > 1:
            raise ValueError(f"{event_id} is owned by multiple persons: {owners}")
        if owners:
            targets.append((owners[0], event_id))
    return sorted(
        targets,
        key=lambda item: (
            0 if item[0] == "layla" else 1,
            item[0],
            item[1].split(".", 1)[0],
            event_number(item[1]),
        ),
    )


def person_numbers(raw_targets: list[tuple[str, str]]) -> dict[str, int]:
    """Read the documented Person N headers for stable selector numbering."""
    numbers: dict[str, int] = {}
    for person in sorted({person for person, _event_id in raw_targets}):
        path = EVENTS / f"cp_{person}_events.txt"
        if not path.exists():
            continue
        text = path.read_text(encoding=SCRIPT_ENCODING, errors="replace")
        match = re.search(r"\bPerson\s+([0-9]+)\b", text)
        if match:
            numbers[person] = int(match.group(1))
    return numbers


def person_number_bases(numbers: dict[str, int]) -> dict[str, int]:
    """Use Person N headers as stable, memorable selected-event bases."""
    return {person: (number + 1) * 10000 for person, number in numbers.items()}


def wrapper_number(person: str, event_id: str, numbers: dict[str, int]) -> int:
    if person == "layla":
        namespace, number_text = event_id.split(".", 1)
        number = int(number_text)
        if namespace == "cp_layla":
            wrapper = 1000 + number
        elif namespace == "cp_layla_vox":
            wrapper = 2000 + number
        else:
            raise ValueError(f"unsupported Layla debug target: {event_id}")
        if wrapper > 9999:
            raise ValueError(f"wrapper id cp_debug_person.{wrapper} exceeds the 4-digit event range")
        return wrapper

    if person not in numbers:
        raise ValueError(f"{person} is missing a 'Person N' header in mod/events/cp_{person}_events.txt")
    person_number = numbers[person]
    number = event_number(event_id)
    if person_number > 99:
        raise ValueError(f"{person} Person {person_number} exceeds cp_debug_person wrapper range")
    if number > 99:
        raise ValueError(f"{event_id} exceeds cp_debug_person wrapper range; use a new debug namespace")
    return person_number * 100 + number


def existing_selectors() -> dict[str, tuple[int, str]]:
    selectors: dict[str, tuple[int, str]] = {}
    for path in (EFFECT_OUTPUT, LEGACY_EFFECT):
        if not path.exists():
            continue
        text = path.read_text(encoding=SCRIPT_ENCODING, errors="replace")
        for match in SELECTOR_RE.finditer(text):
            selector = int(match.group(1))
            event_id = match.group(2)
            person = match.group(3)
            selectors.setdefault(event_id, (selector, person))
    return selectors


def assign_selectors(raw_targets: list[tuple[str, str]]) -> list[Target]:
    preserved = existing_selectors()
    numbers = person_numbers(raw_targets)
    seeded_bases = person_number_bases(numbers)
    used: set[int] = set()
    used_wrappers: set[int] = set()
    person_bases: dict[str, int] = {}
    targets: list[Target] = []
    pending: list[tuple[str, str, int]] = []

    for person, event_id in raw_targets:
        wrapper = wrapper_number(person, event_id, numbers)
        wrapper = next_available_wrapper(wrapper, used_wrappers, event_id)
        used_wrappers.add(wrapper)
        if person == "layla":
            selector = wrapper
            if selector in used:
                raise ValueError(f"selector {selector} is reused")
            used.add(selector)
            targets.append(Target(person=person, event_id=event_id, wrapper=wrapper, selector=selector))
            continue
        if person in seeded_bases:
            selector = seeded_bases[person] + event_number(event_id)
            while selector in used or selector <= 0:
                selector += 1
            used.add(selector)
            person_bases.setdefault(person, seeded_bases[person])
            targets.append(Target(person=person, event_id=event_id, wrapper=wrapper, selector=selector))
            continue
        if event_id not in preserved:
            pending.append((person, event_id, wrapper))
            continue
        selector, mapped_person = preserved[event_id]
        if mapped_person != person:
            raise ValueError(f"{event_id} selector says person={mapped_person}, expected {person}")
        if selector in used:
            raise ValueError(f"selector {selector} is reused")
        used.add(selector)
        person_bases.setdefault(person, selector - event_number(event_id))
        targets.append(Target(person=person, event_id=event_id, wrapper=wrapper, selector=selector))

    next_base = next_person_base(person_bases.values())
    for person, event_id, wrapper in pending:
        if person not in person_bases:
            person_bases[person] = next_base
            next_base += 10000
        selector = person_bases[person] + event_number(event_id)
        while selector in used or selector <= 0:
            selector += 1
        used.add(selector)
        targets.append(Target(person=person, event_id=event_id, wrapper=wrapper, selector=selector))

    targets.sort(key=lambda target: target.wrapper)
    return targets


def next_person_base(bases: object) -> int:
    existing = [base for base in bases if isinstance(base, int) and base >= 10000]
    if not existing:
        return 30000
    return ((max(existing) // 10000) + 1) * 10000


def next_available_wrapper(wrapper: int, used_wrappers: set[int], event_id: str) -> int:
    while wrapper in used_wrappers:
        wrapper += 100
    if wrapper > 9999:
        raise ValueError(f"{event_id} could not find an unused cp_debug_person wrapper under 9999")
    return wrapper


def render_events(targets: list[Target]) -> str:
    lines = [
        "###############################################################################",
        "# Common People -- generated person debug queue",
        "#",
        "# Generated by script/generate-person-debug-wrappers.py. Do not hand-edit.",
        "# These hidden wrappers give console QA a stable selector for every visible",
        "# registered-person event.",
        "#",
        "# The wrapper only stores cp_debug_selected_event. To review the popup,",
        '# click the shared JE button "Open queued QA event" afterward.',
        "# This keeps visible popups in game-thread button context instead of the",
        "# console-thread path that has crashed V3 in prior testing.",
        "#",
        "# Fire with: event cp_debug_person.<wrapper>",
        "###############################################################################",
        "",
        "namespace = cp_debug_person",
        "",
    ]
    for target in targets:
        lines.extend(
            [
                f"# cp_debug_person.{target.wrapper} -- queue {target.event_id} for JE-button popup QA",
                f"cp_debug_person.{target.wrapper} = {{",
                "\ttype = country_event",
                "\thidden = yes",
                "\torphan = yes",
                "",
                "\timmediate = {",
                "\t\tc:EGY ?= {",
                f"\t\t\tset_variable = {{ name = cp_debug_selected_event value = {target.selector} }}",
                "\t\t}",
                "\t}",
                "}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def render_effect(targets: list[Target]) -> str:
    lines = [
        "###############################################################################",
        "# Common People -- generated person debug popup dispatcher",
        "#",
        "# Generated by script/generate-person-debug-wrappers.py. Do not hand-edit.",
        "# Called by cp_debug_fire_selected after a cp_debug_person.N console selector",
        "# or legacy cp_debug.N shortcut stores cp_debug_selected_event on EGY.",
        "###############################################################################",
        "",
        "cp_debug_person_fire_selected = {",
    ]

    for index, target in enumerate(targets):
        branch = "if" if index == 0 else "else_if"
        lines.extend(
            [
                f"\t{branch} = {{",
                f"\t\tlimit = {{ var:cp_debug_selected_event = {target.selector} }}",
                f"\t\tcp_button_fire = {{ event = {target.event_id} person = {target.person} }}",
                "\t}",
            ]
        )

    lines.extend(["}", ""])
    return "\n".join(lines)


def expected_files(targets: list[Target]) -> dict[Path, str]:
    return {
        OUTPUT: render_events(targets),
        EFFECT_OUTPUT: render_effect(targets),
    }


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the generated person debug queue/dispatcher files are stale",
    )
    args = parser.parse_args()

    audit = load_roster_audit()
    targets = assign_selectors(generated_targets(audit))
    files = expected_files(targets)

    if args.check:
        stale: list[str] = []
        for path, expected in files.items():
            actual = path.read_text(encoding=SCRIPT_ENCODING, errors="replace") if path.exists() else ""
            if actual != expected:
                stale.append(relpath(path))
        if stale:
            print("FAIL: generated person debug QA files are stale:")
            for path in stale:
                print(f"- {path}")
            print("Run: python3 script/generate-person-debug-wrappers.py")
            return 1
        print(f"ok: {len(targets)} generated person debug QA target(s) are current")
        return 0

    for path, text in files.items():
        path.write_text(text, encoding=SCRIPT_ENCODING)
    print(
        f"wrote {len(targets)} person debug QA target(s): "
        f"{relpath(OUTPUT)}, {relpath(EFFECT_OUTPUT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
