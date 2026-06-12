# Layla event image prompts

The active replacement queues are [`replacement-batch-v0.7.md`](./replacement-batch-v0.7.md) and [`replacement-batch-v0.8.md`](./replacement-batch-v0.8.md). They are the source of truth for the current rebuild pass: versioned `_vNN` assets, no palace-grandiosity fallback, no retired `cp_conversation_*` source names, and no bulk generator that can silently recreate old art direction.

[`catalog.md`](./catalog.md) is retained as a historical inventory of earlier scene ideas, not as the runnable generation source. Before promoting any old catalog idea, rewrite it into the current batch format and add it to a versioned replacement batch.

## Pipeline

1. **Edit** a versioned batch ledger, currently `replacement-batch-v0.7.md` or `replacement-batch-v0.8.md`.
2. **Export** prompt files and gpt-image-2 batch manifests with `python3 script/export-art-batch-prompts.py --all`. Generated prompt files live under `image/generated/layla/<version>/prompts/`, and each machine-ready manifest lives at `image/generated/layla/<version>/gpt-image-2-batch.jsonl`.
3. **Validate** each manifest before spending API time:
   ```bash
   python3 ~/.codex/skills/.system/imagegen/scripts/image_gen.py generate-batch \
     --input image/generated/layla/<version>/gpt-image-2-batch.jsonl \
     --out-dir image/generated/layla/<version> \
     --dry-run \
     --no-augment
   ```
4. **Generate** candidates into `image/generated/layla/<version>/<asset>.dds.png`, keeping high-resolution archives beside them when available.
   ```bash
   python3 ~/.codex/skills/.system/imagegen/scripts/image_gen.py generate-batch \
     --input image/generated/layla/<version>/gpt-image-2-batch.jsonl \
     --out-dir image/generated/layla/<version> \
     --no-augment
   ```
5. **Convert** PNG -> DDS with `script/convert-images-to-dds.sh`. The converter defaults to `image/generated/` and rejects retired `cp_conversation_*` source names.
6. **Audit** the batch with `script/audit-art-batch-plan.py --all`, `script/audit-event-images.py`, and `script/audit-art-provenance.py --rank-missing --limit 30`.
7. **Promote** accepted batches with `script/promote-art-batch.py <replacement-batch.md> --apply`. The promoter rewires accepted events to versioned `_vNN` DDS files and moves superseded DDS into `image/archive/legacy-event-pictures/<version>-superseded/`.

## Generation tiers

Start with the v0.7 replacement batch, then v0.8. The v0.5 and v0.6 prototype packs remain useful for provenance, but the active art queue now prioritizes the worst in-game blockers and high-use legacy/no-source images.

Because the catalog covers 70+ events, generate in tiers (see `catalog.md §"Priority tiers"`):

- **Tier 1** — biggest narrative moments and observed blockers. Add them to a versioned replacement batch and export prompts.
- **Tier 2** — 20 more law-reaction beats. Bash entries to be added.
- **Tier 3** — tech + market goods. 6 images.
- **Tier 4** — remaining pulses. ~15 images.
- **Tier 5** — conversation root / topic openers. ~15 images.

## After a tier generates

For each new DDS file, replace the existing placeholder reference in `cp_layla_events.txt`:

| Event | Current placeholder | Target DDS |
|---|---|---|
| cp_layla.50 | cp_layla_intro.dds | cp_layla_mill_smoke.dds |
| cp_layla.70 | cp_layla_intro.dds | cp_layla_cairo_calling.dds |
| cp_layla.72 | cp_layla_mothers_hand.dds | cp_layla_suitor.dds |
| cp_layla.73 | cp_layla_serfdom_restored.dds | cp_layla_mill_closed.dds |
| cp_layla.80 | cp_layla_mothers_hand.dds | cp_layla_last_morning.dds |
| cp_layla.82 | cp_layla_childbirth.dds | cp_layla_child_fever.dds |
| cp_layla.94 | cp_layla_neighbours_boy.dds | cp_layla_paper_my_name.dds |
| cp_layla.103 | cp_layla_homesteading.dds | cp_layla_chains.dds |
| cp_layla.116 | cp_layla_mothers_hand.dds | cp_layla_square_fills.dds |
| cp_layla.120 | cp_layla_serfdom_restored.dds | cp_layla_rifles.dds |
| cp_layla.123 | cp_layla_homesteading.dds | cp_layla_factory_field.dds |
| cp_layla.124 | cp_layla_no_wind.dds | cp_layla_ministry.dds |

Do the rewire as a separate commit from the DDS add so the diff is clean.

## Shared references (all events)

- Face: `~/Pictures/common-people-mod-images/Layla/layla.png`
- Style: `~/Pictures/common-people-mod-images/Layla/cp_layla_homesteading.dds.png`
- Register: Mahfouz — quiet, specific, sensory, subtext.
- Palette: warm ochre, sienna, cream; painted-canvas texture.
- Aspect: 3:2 landscape, target 600×400.

## Historical per-event specs (already-generated images)

Kept here for reference; live source is `catalog.md`.

### cp_layla.1 — "The Farmer's Daughter"
Threshold at pre-dawn, pomegranate sky. Quiet anticipation.

### cp_layla.2 — "The Deed"
Field, folded deed, red wax seal, hands trembling. Quiet gravity.

### cp_layla.3 — "The Bey Returns"
Layla and Ahmed backs against the wall, bey on horseback in the lane. Fear that has learned to be silent.

### cp_layla.4 — "He Marches"
Column of conscripts in the middle distance; Layla at the edge of the village. The worst kind of leaving.

### cp_layla.5 — "The First Cry"
Oil lamp, midwife in shadow, Ahmed kneeling. Exhausted reverence.

### cp_layla.13 — "A Day With No Wind"
Grinding stone in the yard, dust hanging still. Windless Delta stillness.

### cp_layla.14 — "The Neighbour's Boy in the Lane"
Floured hands at the doorframe; crying boy in the lane. Restraint as care.

### cp_layla.15 — "Her Mother's Left Hand"
Close-medium interior; left hand lifting bread; gaze distant. Private grief of becoming one's mother.
