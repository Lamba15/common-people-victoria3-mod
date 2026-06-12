#!/usr/bin/env python3
"""Export versioned art-batch prompts from replacement-batch ledgers."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "documentation" / "characters" / "layla" / "prompts" / "replacement-batch-v0.7.md"

SHARED_RE = re.compile(r"Shared visual contract for every prompt:\s*\n\n```text\n(.*?)```", re.S)
TARGET_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+\.dds)`\s*\|", re.M)
PROMPT_HEADING_RE = re.compile(r"^## Prompt\s+(\d+)\s+-\s+(.+)$")
VERSION_RE = re.compile(r"replacement-batch-(v\d+(?:\.\d+)?)\.md$")


@dataclass(frozen=True)
class PromptExport:
    priority: int
    title: str
    asset: str
    text: str

    @property
    def filename(self) -> str:
        stem = self.asset.removesuffix(".dds")
        return f"{self.priority:02d}_{stem}.prompt.txt"

    @property
    def source_png_name(self) -> str:
        return f"{self.asset}.png"

    def jsonl_job(self) -> dict[str, str]:
        return {
            "prompt": self.text,
            "out": self.source_png_name,
            "model": "gpt-image-2",
            "size": "1536x1024",
            "quality": "high",
            "output_format": "png",
        }


@dataclass(frozen=True)
class BatchPaths:
    plan: Path
    person: str
    generated_person: str
    version: str
    output: Path
    jsonl: Path


def discover_plans() -> list[Path]:
    return sorted((ROOT / "documentation" / "characters").glob("*/prompts/replacement-batch-v*.md"))


def generated_person_slug(person: str) -> str:
    return {
        "the-soldier": "soldier",
    }.get(person, person)


def infer_batch_paths(plan: Path, output: Path | None, jsonl: Path | None) -> BatchPaths:
    version_match = VERSION_RE.match(plan.name)
    if not version_match:
        raise ValueError(f"{plan} must be named replacement-batch-vNN.md")
    version = version_match.group(1)

    try:
        prompt_dir = plan.parent
        person = prompt_dir.parent.name
        if prompt_dir.name != "prompts":
            raise ValueError
    except ValueError as exc:
        raise ValueError(f"{plan} must live under documentation/characters/<person>/prompts/") from exc

    generated_person = generated_person_slug(person)
    generated_root = ROOT / "image" / "generated" / generated_person / version
    inferred_output = generated_root / "prompts"
    inferred_jsonl = generated_root / "gpt-image-2-batch.jsonl"
    return BatchPaths(
        plan=plan,
        person=person,
        generated_person=generated_person,
        version=version,
        output=output if output is not None else inferred_output,
        jsonl=jsonl if jsonl is not None else inferred_jsonl,
    )


def display_person(person: str) -> str:
    return " ".join(part.capitalize() for part in person.replace("-", "_").split("_"))


def fenced_block(lines: list[str], start: int) -> str:
    in_block = False
    collected: list[str] = []
    for line in lines[start:]:
        if line.strip() == "```text" and not in_block:
            in_block = True
            continue
        if line.strip() == "```" and in_block:
            return "\n".join(collected).strip()
        if in_block:
            collected.append(line)
    raise ValueError("prompt section is missing a closing text fence")


def parse_exports(batch: BatchPaths) -> list[PromptExport]:
    text = batch.plan.read_text(encoding="utf-8")
    shared_match = SHARED_RE.search(text)
    if not shared_match:
        raise ValueError(f"{batch.plan} is missing the shared visual contract block")
    shared = shared_match.group(1).strip()

    targets = {int(match.group(1)): match.group(2) for match in TARGET_ROW_RE.finditer(text)}
    lines = text.splitlines()
    exports: list[PromptExport] = []
    for index, line in enumerate(lines):
        heading = PROMPT_HEADING_RE.match(line)
        if not heading:
            continue
        priority = int(heading.group(1))
        title = heading.group(2).strip()
        asset = targets.get(priority)
        if not asset:
            raise ValueError(f"prompt {priority} has no matching batch target")
        prompt = fenced_block(lines, index + 1)
        source_png = ROOT / "image" / "generated" / batch.generated_person / batch.version / f"{asset}.png"
        body = "\n".join(
            [
                f"Common People {display_person(batch.person)} {batch.version} replacement prompt",
                f"Source ledger: {batch.plan.relative_to(ROOT)}",
                f"Target DDS: mod/gfx/event_pictures/{asset}",
                f"Source PNG: {source_png.relative_to(ROOT)}",
                "",
                "Shared visual contract:",
                shared,
                "",
                "Victoria 3 event-window safety:",
                "Place the essential face, action, and required object in the left half or center-left. The game's right-side text panel covers much of the right half, so reserve that area for atmosphere and background only.",
                "",
                "Specific scene:",
                prompt,
                "",
            ]
        )
        exports.append(PromptExport(priority, title, asset, body))

    expected = set(range(1, len(targets) + 1))
    actual = {export.priority for export in exports}
    if actual != expected:
        raise ValueError(f"prompt priorities are {sorted(actual)}, expected {sorted(expected)}")
    return sorted(exports, key=lambda export: export.priority)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def jsonl_text(exports: list[PromptExport]) -> str:
    lines = [json.dumps(export.jsonl_job(), ensure_ascii=False, sort_keys=True) for export in exports]
    return "\n".join(lines) + "\n"


def export_batch(batch: BatchPaths, check: bool) -> tuple[int, list[str]]:
    exports = parse_exports(batch)
    stale: list[str] = []
    if not check:
        batch.output.mkdir(parents=True, exist_ok=True)
        batch.jsonl.parent.mkdir(parents=True, exist_ok=True)

    for export in exports:
        path = batch.output / export.filename
        if check:
            if not path.exists():
                stale.append(f"{rel(path)} is missing")
            elif path.read_text(encoding="utf-8") != export.text:
                stale.append(f"{rel(path)} is stale")
        else:
            path.write_text(export.text, encoding="utf-8")
            print(f"wrote {rel(path)}")

    batch_text = jsonl_text(exports)
    if check:
        if not batch.jsonl.exists():
            stale.append(f"{rel(batch.jsonl)} is missing")
        elif batch.jsonl.read_text(encoding="utf-8") != batch_text:
            stale.append(f"{rel(batch.jsonl)} is stale")
    else:
        batch.jsonl.write_text(batch_text, encoding="utf-8")
        print(f"wrote {rel(batch.jsonl)}")
    return len(exports), stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", nargs="?", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--all", action="store_true", help="export/check every replacement-batch-vNN.md ledger")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--check", action="store_true", help="fail if exported prompt files are missing or stale")
    args = parser.parse_args()

    if args.all:
        if args.output or args.jsonl:
            parser.error("--output/--jsonl cannot be combined with --all")
        plans = discover_plans()
    else:
        plans = [args.plan if args.plan.is_absolute() else ROOT / args.plan]

    total_exports = 0
    stale: list[str] = []
    for plan in plans:
        output = args.output if args.output is None or args.output.is_absolute() else ROOT / args.output
        jsonl = args.jsonl if args.jsonl is None or args.jsonl.is_absolute() else ROOT / args.jsonl
        batch = infer_batch_paths(plan, output, jsonl)
        count, batch_stale = export_batch(batch, args.check)
        total_exports += count
        stale.extend(batch_stale)

    if args.check and stale:
        print("FAIL: art prompt exports are stale:")
        for message in stale:
            print(f"- {message}")
        print("Run: python3 script/export-art-batch-prompts.py --all")
        return 1

    if args.check:
        print(f"ok: {total_exports} art prompt export(s) and gpt-image-2 batch manifest(s) are current")
    else:
        print(f"wrote {total_exports} art prompt export(s) and gpt-image-2 batch manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
