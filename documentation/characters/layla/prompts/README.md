# Layla event image prompts

The authoritative prompt catalog lives in [`catalog.md`](./catalog.md). It lists, for every Layla event, the scene spec that feeds the image-generation pipeline.

## Pipeline

1. **Edit** `catalog.md` when adding or revising an event's scene.
2. **Mirror** the `run_one ...` call in `script/gen-layla-event-images.sh` (that's the bash script Codex CLI actually runs).
3. **Generate** PNGs: `script/gen-layla-event-images.sh [names...]` — no args runs all, positional args run only that subset.
4. **Convert** PNG → DDS: `script/convert-images-to-dds.sh` — stages the DDS files under `mod/gfx/event_pictures/`.
5. **Rewire** the event's `event_image = { texture = ... }` line in `mod/events/cp_layla_events.txt` to point at the new DDS.

## Generation tiers

Because the catalog covers 70+ events, generate in tiers (see `catalog.md §"Priority tiers"`):

- **Tier 1** — biggest narrative moments (12 images). The bash script has these entries now; run `script/gen-layla-event-images.sh cp_layla_mill_smoke cp_layla_cairo_calling cp_layla_suitor cp_layla_mill_closed cp_layla_last_morning cp_layla_child_fever cp_layla_paper_my_name cp_layla_chains cp_layla_square_fills cp_layla_rifles cp_layla_factory_field cp_layla_ministry`.
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
