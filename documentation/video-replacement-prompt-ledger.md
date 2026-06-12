# Video Replacement Prompt Ledger

Generated from visible non-debug events that still use vanilla `.bk2` video placeholders.
Rebuild with `python3 script/build-video-replacement-prompts.py`.

These prompts do not promote art into the mod. They create the review queue for replacing vanilla motion placeholders with custom GPT-image-2 stills or later custom motion exports.

## Summary

- Version: v0.1
- Vanilla video placeholder events: 0
- Persons affected: 0
- Prompt exports: 0
- Prompt directory: `image/generated/video-replacements/v0.1/prompts`
- Batch manifest: `image/generated/video-replacements/v0.1/gpt-image-2-batch.jsonl`

## Person Counts


## Previous Vanilla Video Reuse


## Replacement Targets

| Event | Person | Title | Old Video | Target DDS | Prompt | Source |
|---|---|---|---|---|---|---|

## Checks

```bash
python3 script/build-video-replacement-prompts.py --check
script/audit-generic-video-art.py --strict-no-vanilla-video
```

`--strict-no-vanilla-video` is expected to pass; there are no active vanilla `.bk2` event-video placeholders.
