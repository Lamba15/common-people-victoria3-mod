#!/usr/bin/env python3
"""Audit generated art prompts for Victoria 3 event-window safety."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "image" / "generated"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def has_any(text: str, needles: tuple[str, ...]) -> bool:
    folded = text.lower()
    return any(needle in folded for needle in needles)


def prompt_safety_issues(label: str, prompt: str) -> list[str]:
    folded = prompt.lower()
    issues: list[str] = []
    if "600x400" not in folded:
        issues.append(f"{label}: prompt does not state final 600x400 readability")
    if not has_any(folded, ("left half or center-left", "left side")):
        issues.append(f"{label}: prompt does not keep essential subject/action/object on the left-safe side")
    if not has_any(folded, ("right-side text panel", "right side text panel", "right half")):
        issues.append(f"{label}: prompt does not reserve the right side for the event text panel")
    if not has_any(folded, ("no text", "no readable text")):
        issues.append(f"{label}: prompt does not forbid generated text")
    if "no ui" not in folded:
        issues.append(f"{label}: prompt does not forbid generated UI")
    return issues


def audit_prompt_files() -> tuple[int, list[str]]:
    issues: list[str] = []
    prompt_files = sorted(GENERATED.glob("**/*.prompt.txt"))
    for path in prompt_files:
        prompt = path.read_text(encoding="utf-8", errors="replace")
        issues.extend(prompt_safety_issues(rel(path), prompt))
    return len(prompt_files), issues


def audit_jsonl_manifests() -> tuple[int, int, list[str]]:
    issues: list[str] = []
    manifests = sorted(GENERATED.glob("**/gpt-image-2*.jsonl"))
    jobs = 0
    for manifest in manifests:
        for line_no, line in enumerate(manifest.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not line.strip():
                continue
            label = f"{rel(manifest)}:{line_no}"
            try:
                job = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append(f"{label}: invalid JSONL row: {exc}")
                continue
            jobs += 1
            if job.get("model") != "gpt-image-2":
                issues.append(f"{label}: model is {job.get('model')!r}, expected 'gpt-image-2'")
            if job.get("size") != "1536x1024":
                issues.append(f"{label}: size is {job.get('size')!r}, expected '1536x1024'")
            if job.get("quality") != "high":
                issues.append(f"{label}: quality is {job.get('quality')!r}, expected 'high'")
            if job.get("output_format") != "png":
                issues.append(f"{label}: output_format is {job.get('output_format')!r}, expected 'png'")
            prompt = job.get("prompt")
            if not isinstance(prompt, str):
                issues.append(f"{label}: prompt is missing or not a string")
                continue
            issues.extend(prompt_safety_issues(label, prompt))
    return len(manifests), jobs, issues


def main() -> int:
    prompt_count, prompt_issues = audit_prompt_files()
    manifest_count, job_count, manifest_issues = audit_jsonl_manifests()
    issues = prompt_issues + manifest_issues

    print("Common People art prompt safety audit")
    print(f"Prompt exports: {prompt_count}")
    print(f"gpt-image-2 manifests: {manifest_count}")
    print(f"gpt-image-2 jobs: {job_count}")
    print("Required prompt contract: 600x400 readability, left-safe subject/action/object, right-side text-panel reserve, no generated text/UI")
    print(f"Issues: {len(issues)}")
    for issue in issues:
        print(f"- {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
