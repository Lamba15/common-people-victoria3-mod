# Image Generation Workflow

Current rebuild workflow, updated 2026-05-26 for the Layla v0.7-v0.12 replacement batches.

Current art direction lives in [art-bible-v0.5.md](art-bible-v0.5.md). Layla's active replacement queues live in [replacement-batch-v0.7.md](characters/layla/prompts/replacement-batch-v0.7.md), [replacement-batch-v0.8.md](characters/layla/prompts/replacement-batch-v0.8.md), [replacement-batch-v0.9.md](characters/layla/prompts/replacement-batch-v0.9.md), [replacement-batch-v0.10.md](characters/layla/prompts/replacement-batch-v0.10.md), [replacement-batch-v0.11.md](characters/layla/prompts/replacement-batch-v0.11.md), and [replacement-batch-v0.12.md](characters/layla/prompts/replacement-batch-v0.12.md). Use versioned batch ledgers, not old prompt catalogs, when generating replacement art.

---

## Rules

- Generate versioned replacements: `cp_<person>_<scene>_vNN.dds.png` as source, `cp_<person>_<scene>_vNN.dds` as shipped texture.
- Store generated source PNGs inside this repo under `image/generated/<person>/<version>/`.
- Do not use retired `cp_conversation_*` source names. The converter rejects them because they can recreate the old pre-r5 conversation art path.
- Keep high-resolution archives beside accepted sources when available: `cp_<person>_<scene>_vNN_1536.png`.
- Only wire an image into events after visual review. Move superseded DDS files to `image/archive/legacy-event-pictures/<version>-superseded/`.

---

## Directory Conventions

Generated sources:

```text
image/generated/
├── layla/
│   └── v0.7/
│       ├── gpt-image-2-batch.jsonl
│       ├── prompts/
│       │   └── 11_cp_layla_conversation_land_v07.prompt.txt
│       ├── cp_layla_conversation_land_v07.dds.png
│       └── cp_layla_conversation_land_v07_1536.png
│   └── v0.8/
│       ├── gpt-image-2-batch.jsonl
│       └── prompts/
│   └── v0.9/
│       ├── gpt-image-2-batch.jsonl
│       └── prompts/
│   └── v0.10/
│       ├── gpt-image-2-batch.jsonl
│       └── prompts/
│   └── v0.11/
│       ├── gpt-image-2-batch.jsonl
│       └── prompts/
│   └── v0.12/
│       ├── gpt-image-2-batch.jsonl
│       └── prompts/
└── <person>/
```

Shipped DDS textures:

```text
mod/gfx/event_pictures/
├── cp_layla_conversation_land_v07.dds
└── ...
```

The `.dds.png` suffix means "PNG source for this eventual DDS." For replacement batches, the version suffix is part of the asset name.

---

## Prompt Export

Export auditable prompt files from every active replacement ledger:

```bash
python3 script/export-art-batch-prompts.py --all
python3 script/export-art-batch-prompts.py --all --check
```

The exported files pair each target DDS with the shared visual contract and scene-specific prompt. Release readiness checks that these prompt files stay current.

The same exporter also writes a machine-ready gpt-image-2 JSONL manifest:

```text
image/generated/layla/<version>/gpt-image-2-batch.jsonl
```

Validate the manifest without spending API time:

```bash
python3 ~/.codex/skills/.system/imagegen/scripts/image_gen.py generate-batch \
  --input image/generated/layla/<version>/gpt-image-2-batch.jsonl \
  --out-dir image/generated/layla/<version> \
  --dry-run \
  --no-augment
```

Track the current generation/review/promotion state:

```bash
script/build-art-acceptance-ledger.py
script/build-art-acceptance-ledger.py --check
```

The generated ledger at `documentation/art-acceptance-ledger.md` records every planned target's legacy reference count, generated source state, shipped DDS state, promotion state, and next gate.

---

## Generation

Use the current Codex/OpenAI image tool to generate one candidate per prompt. Each manifest is already configured for `gpt-image-2`, `1536x1024`, high quality PNG outputs, and source filenames that match the converter/provenance audits.

When `OPENAI_API_KEY` is available:

```bash
python3 ~/.codex/skills/.system/imagegen/scripts/image_gen.py generate-batch \
  --input image/generated/layla/<version>/gpt-image-2-batch.jsonl \
  --out-dir image/generated/layla/<version> \
  --no-augment
```

Accepted 600x400 sources must live at:

```text
image/generated/layla/<version>/<asset>.dds.png
```

For example:

```text
image/generated/layla/v0.7/cp_layla_conversation_land_v07.dds.png
```

Keep a high-resolution archive when the tool provides one:

```text
image/generated/layla/v0.7/cp_layla_conversation_land_v07_1536.png
```

---

## Convert PNG To DDS

Victoria 3 event pictures must be DDS textures. Convert generated sources with:

```bash
script/convert-images-to-dds.sh
```

The script defaults to `image/generated/` and writes to `mod/gfx/event_pictures/`. It prefers `nvcompress` from `libnvtt-bin` and falls back to ImageMagick's `magick`.

Use `CP_IMAGES_SRC=/path/to/source` only for a deliberate external source library. The converter rejects `cp_conversation_*` source names in every source root.

---

## Motion Event Art

Victoria 3 event windows support moving event art through `event_image = { video = "..." }`. The installed 1.13.8 GUI renders this with `Event.HasVideo` and `Event.GetVideo`; static `texture = "...dds"` art does not pan by itself.

Vanilla examples use both forms:

```text
event_image = { video = "middleeast_middleclass_cafe" }
event_image = { video = "gfx/event_pictures/ip2_india_protest.bk2" }
```

The shipped moving-art format is `.bk2` under `gfx/event_pictures/`. Until a custom Bink/video export pipeline is proven, the safe options are:

1. keep generated GPT stills as reviewed DDS textures
2. use vanilla `.bk2` references only as temporary playtest placeholders
3. promote custom motion only after an in-game-tested `.bk2` pipeline exists

`documentation/motion-art-ledger.md` records every active motion event and
classifies it as custom motion or vanilla placeholder debt; regenerate it with
`python3 script/build-motion-art-ledger.py`.
`script/audit-event-images.py` inventories both referenced DDS textures and BK2
videos, while `script/audit-event-motion.py` and
`python3 script/build-motion-art-ledger.py --check` verify that any remaining
video references resolve and that the motion ledger does not drift. Release candidates must also pass
`script/audit-generic-video-art.py --strict-no-vanilla-video`. A video
reference must resolve against the mod or installed Victoria 3
`gfx/event_pictures` tree.

For vanilla video placeholder replacement, use the generated prompt queue:

```bash
python3 script/build-video-replacement-prompts.py
python3 script/build-video-replacement-prompts.py --check
```

The ledger at `documentation/video-replacement-prompt-ledger.md` maps each
vanilla-video event to a target DDS name, source event, prompt file, and
`gpt-image-2` batch manifest. These outputs are planning/review artifacts only;
event files should not be rewired until generated candidates have been reviewed,
converted, and checked in-game at event-window scale.

---

## Review And Promote

After generation, rebuild review sheets and inspect the batch before changing event references:

```bash
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/audit-art-provenance.py --rank-missing --limit 30
script/audit-release-readiness.py --mode dev
```

After the reviewed PNGs have been converted to DDS, inspect the promotion status:

```bash
script/promote-art-batch.py --all
```

When a full batch is accepted, promote it:

```bash
script/promote-art-batch.py documentation/characters/layla/prompts/replacement-batch-v0.7.md --apply
script/promote-art-batch.py documentation/characters/layla/prompts/replacement-batch-v0.8.md --apply
script/promote-art-batch.py documentation/characters/layla/prompts/replacement-batch-v0.9.md --apply
script/promote-art-batch.py documentation/characters/layla/prompts/replacement-batch-v0.10.md --apply
script/promote-art-batch.py documentation/characters/layla/prompts/replacement-batch-v0.11.md --apply
script/promote-art-batch.py documentation/characters/layla/prompts/replacement-batch-v0.12.md --apply
```

The promoter rewires event `event_image` references from legacy DDS names to the versioned `_vNN` DDS assets and moves superseded DDS files into `image/archive/legacy-event-pictures/<version>-superseded/`. It refuses to apply unless the generated source PNG and shipped DDS exist for every target in the batch.

When an image is accepted manually:

1. Rewire the event's `event_image = { texture = "gfx/event_pictures/<asset>.dds" }`.
2. Keep the new texture versioned (`_v07`, `_v08`, etc.).
3. Move the superseded DDS out of `mod/gfx/event_pictures/` and into the matching archive folder.
4. Update the batch ledger with any visual QA notes.

---

## Scaling Notes

Prompt ledgers are the scaling unit. Add new characters or Layla follow-up batches as new versioned ledgers, then add the corresponding prompt-export check when the batch becomes active. Avoid reintroducing one-off bulk generators: they drift silently, make prompts hard to audit, and can bring old art direction back into the shipped mod.
