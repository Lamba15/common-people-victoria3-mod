#!/usr/bin/env python3
"""Export character seed prompts into a gpt-image-2 batch manifest."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "documentation" / "characters"
DEFAULT_VERSION = "v0.1"

SEED_RE = re.compile(r"seed-(v\d+(?:\.\d+)?)\.md$")
TOKEN_RE = re.compile(r"^- Token:\s*`([A-Za-z0-9_]+)`\s*$", re.M)
HEADING_RE = re.compile(r"^(##|###)\s+(.+)$")
FENCE_START = "```text"
FENCE_END = "```"


@dataclass(frozen=True)
class SeedPrompt:
    person: str
    source: Path
    version: str
    index: int
    heading: str
    body: str

    @property
    def slug(self) -> str:
        text = self.heading
        text = text.replace("`", "")
        text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
        text = text or f"prompt_{self.index:02d}"
        if text.startswith("cp_"):
            text = text.replace(".", "_")
        return text[:80].rstrip("_")

    @property
    def out_name(self) -> str:
        return f"{self.person}_{self.index:02d}_{self.slug}.png"

    @property
    def export_name(self) -> str:
        return f"{self.person}_{self.index:02d}_{self.slug}.prompt.txt"

    @property
    def export_text(self) -> str:
        return "\n".join(
            [
                f"Common People character seed prompt: {self.person}",
                f"Source ledger: {self.source.relative_to(ROOT)}",
                f"Prompt heading: {self.heading}",
                f"Target source PNG: image/generated/character-seeds/{self.version}/{self.out_name}",
                "",
                "Generation target:",
                "Use case: historical-scene",
                "Asset type: Victoria 3 event/portrait image, 3:2 landscape, final crop must read at 600x400",
                "Model: gpt-image-2",
                "Size: 1536x1024",
                "Quality: high",
                "",
                "Global Common People constraints:",
                "Painted historical realism, textured oil-paint surface, natural anatomy, grounded 19th-century Egyptian materials.",
                "No text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no heroic propaganda pose.",
                "The image must be human-scale and must include the required object or gesture named in the scene prompt.",
                "Victoria 3 event-window safety: place the essential face, action, and required object in the left half or center-left; the game's right-side text panel covers much of the right half, so reserve that area for atmosphere and background only.",
                "",
                "Specific prompt:",
                self.body.strip(),
                "",
            ]
        )

    def jsonl_job(self) -> dict[str, str]:
        return {
            "model": "gpt-image-2",
            "out": self.out_name,
            "output_format": "png",
            "prompt": self.export_text,
            "quality": "high",
            "size": "1536x1024",
        }


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def seed_files(version: str | None) -> list[Path]:
    files = sorted(CHARACTERS.glob("*/prompts/seed-v*.md"))
    if version is None:
        return files
    return [path for path in files if path.name == f"seed-{version}.md"]


def person_token(path: Path, text: str) -> str:
    match = TOKEN_RE.search(text)
    if match:
        return match.group(1)
    return path.parent.parent.name


def collect_prompts(path: Path) -> list[SeedPrompt]:
    version_match = SEED_RE.match(path.name)
    if not version_match:
        raise ValueError(f"{rel(path)} is not named seed-vNN.md")
    version = version_match.group(1)
    text = path.read_text(encoding="utf-8", errors="replace")
    person = person_token(path, text)
    lines = text.splitlines()
    prompts: list[SeedPrompt] = []
    current_heading = ""
    in_fence = False
    body: list[str] = []
    for line in lines:
        heading = HEADING_RE.match(line)
        if heading and not in_fence:
            current_heading = heading.group(2).strip()
            continue
        if line.strip() == FENCE_START and not in_fence:
            in_fence = True
            body = []
            continue
        if line.strip() == FENCE_END and in_fence:
            in_fence = False
            prompts.append(SeedPrompt(person, path, version, len(prompts) + 1, current_heading, "\n".join(body)))
            body = []
            continue
        if in_fence:
            body.append(line)
    if in_fence:
        raise ValueError(f"{rel(path)} has an unterminated text fence")
    if not prompts:
        raise ValueError(f"{rel(path)} has no text-fenced prompts")
    return prompts


def collect_all(version: str | None) -> list[SeedPrompt]:
    prompts: list[SeedPrompt] = []
    for path in seed_files(version):
        prompts.extend(collect_prompts(path))
    return sorted(prompts, key=lambda prompt: (prompt.person, prompt.source.name, prompt.index))


def output_paths(version: str) -> tuple[Path, Path]:
    root = ROOT / "image" / "generated" / "character-seeds" / version
    return root / "prompts", root / "gpt-image-2-seed-batch.jsonl"


def jsonl_text(prompts: list[SeedPrompt]) -> str:
    return "\n".join(json.dumps(prompt.jsonl_job(), ensure_ascii=False, sort_keys=True) for prompt in prompts) + "\n"


def export_prompts(prompts: list[SeedPrompt], check: bool) -> list[str]:
    stale: list[str] = []
    prompts_by_version: dict[str, list[SeedPrompt]] = {}
    for prompt in prompts:
        prompts_by_version.setdefault(prompt.version, []).append(prompt)

    for version, version_prompts in sorted(prompts_by_version.items()):
        prompt_dir, jsonl_path = output_paths(version)
        if not check:
            prompt_dir.mkdir(parents=True, exist_ok=True)
            jsonl_path.parent.mkdir(parents=True, exist_ok=True)

        for prompt in version_prompts:
            path = prompt_dir / prompt.export_name
            if check:
                if not path.exists():
                    stale.append(f"{rel(path)} is missing")
                elif path.read_text(encoding="utf-8") != prompt.export_text:
                    stale.append(f"{rel(path)} is stale")
            else:
                path.write_text(prompt.export_text, encoding="utf-8")
                print(f"wrote {rel(path)}")

        text = jsonl_text(version_prompts)
        if check:
            if not jsonl_path.exists():
                stale.append(f"{rel(jsonl_path)} is missing")
            elif jsonl_path.read_text(encoding="utf-8") != text:
                stale.append(f"{rel(jsonl_path)} is stale")
        else:
            jsonl_path.write_text(text, encoding="utf-8")
            print(f"wrote {rel(jsonl_path)}")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION, help="seed prompt version to export/check, or 'all'")
    parser.add_argument("--check", action="store_true", help="fail if exported prompts or JSONL are missing/stale")
    args = parser.parse_args()

    version = None if args.version == "all" else args.version
    prompts = collect_all(version)
    stale = export_prompts(prompts, args.check)
    if args.check and stale:
        print("FAIL: character seed prompt exports are stale:")
        for message in stale:
            print(f"- {message}")
        print(f"Run: python3 script/export-character-seed-prompts.py --version {args.version}")
        return 1
    if args.check:
        print(f"ok: {len(prompts)} character seed prompt export(s) and gpt-image-2 manifest(s) are current")
    else:
        print(f"wrote {len(prompts)} character seed prompt export(s) and gpt-image-2 manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
