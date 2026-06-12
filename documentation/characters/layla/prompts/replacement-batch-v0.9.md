# Layla replacement image batch v0.9

Date: 2026-05-26

Purpose: queue the next ranked Layla legacy/no-source DDS images after v0.7 and v0.8. This batch begins the lower-reuse but story-critical backlog from `script/audit-art-provenance.py --rank-missing --limit 80`, emphasizing domestic pressure, family shocks, and early modernization beats that need clearer narrative objects.

Shared visual contract for every prompt:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Subject: Layla al-Sharif, an Egyptian/Misri fellah woman; keep her grounded, unheroic, with work-worn hands, dark eyes, heavy brows, and practical 19th-century clothing. Age her to the event.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials, 19th-century Egypt, quiet human scale.
Composition/framing: close-medium or medium-wide, no epic hero camera.
Constraints: no text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no palace grandeur, no invented flags, no decorative atmosphere without the required object.
```

## Batch targets

| Priority | Asset | Active windows | Main event families |
|---:|---|---:|---|
| 1 | `cp_layla_moment_v09.dds` | 3 | private conversation |
| 2 | `cp_layla_neighbours_boy_v09.dds` | 2 | neighbor's boy, Cairo errand |
| 3 | `cp_layla_no_wind_v09.dds` | 2 | stagnant air, welfare-down pressure |
| 4 | `cp_layla_bread_not_rise_v09.dds` | 1 | failed bread and household scarcity |
| 5 | `cp_layla_brothers_letter_v09.dds` | 1 | letter from her brother |
| 6 | `cp_layla_burning_letters_v09.dds` | 1 | papers destroyed, memory refusing archive |
| 7 | `cp_layla_cairo_calling_v09.dds` | 1 | Cairo offer |
| 8 | `cp_layla_chains_v09.dds` | 1 | law, bondage, and remembered constraint |
| 9 | `cp_layla_child_fever_v09.dds` | 1 | sick child |
| 10 | `cp_layla_childbirth_v09.dds` | 1 | first child |
| 11 | `cp_layla_children_school_v09.dds` | 1 | children and school |

## Prompt 1 - A Moment at the Door

```text
Event: cp_layla_vox.92, .93, .96 - "A Moment"
Narrative function: Layla's private conversation lane receives a human-scale glimpse rather than a plot turn.
Subject: Layla in middle age, practical village clothes and dark headscarf, tired but steady.
Scene/backdrop: mud-brick threshold between a small household room and a Delta courtyard.
Foreground action: Layla pauses in the doorway with one hand on the lintel, listening to something inside before returning to work.
Required object/gesture: her work-worn hand on the doorframe and a small clay cup or folded cloth in the other hand.
Background detail: grinding stone, reed mat, low shelf, thin strip of field light beyond the courtyard.
Lighting/mood: late-afternoon quiet, intimate and observational, no melodrama.
Avoid: portrait pose, empty atmospheric doorway, palace or city street, modern housewares.
```

## Prompt 2 - The Neighbor's Boy

```text
Event: cp_layla.14 and cp_layla_vox.85 - "The Neighbor's Boy"
Narrative function: a boy carrying news makes the village feel connected to roads, offices, and consequences beyond Layla's door.
Subject: Layla in her thirties or forties at a village threshold; a neighbor's boy stands before her, dusty and anxious.
Scene/backdrop: Delta lane with mud-plaster walls, donkey track, low doorways, and a distant canal line.
Foreground action: the boy offers a folded message or small wrapped parcel while Layla studies his face.
Required object/gesture: boy's outstretched hand with a folded paper; Layla's hand half-raised but not yet taking it.
Background detail: a woman watching from another doorway, sandals in the dust, water jar near the wall.
Lighting/mood: bright morning dust, urgency kept small.
Avoid: readable text, modern school uniform, messenger on horseback, comic child expression.
```

## Prompt 3 - No Wind

```text
Event: cp_layla.13 and cp_layla.92 - "No Wind"
Narrative function: economic pressure is felt as heat, still air, and a room where nothing moves.
Subject: Layla in middle age, seated low beside a household ledger or food basket, face composed.
Scene/backdrop: cramped village or Cairo room with reed mat, shuttered opening, and hanging cloth that does not stir.
Foreground action: Layla looks toward a still curtain while her hand rests near a few coins or a small ration of grain.
Required object/gesture: motionless hanging cloth; Layla's fingers touching coins or grain without counting them.
Background detail: sleeping mat rolled against the wall, clay jar, weak light under the door.
Lighting/mood: heavy summer heat, financial dread, no storm or spectacle.
Avoid: desert landscape, dramatic weather, modern fan, obvious poverty tableau.
```

## Prompt 4 - Bread That Will Not Rise

```text
Event: cp_layla.20 - "The Bread Will Not Rise"
Narrative function: scarcity enters through failed dough, not a speech about prices.
Subject: young or middle-aged Layla kneeling beside a low bread tray.
Scene/backdrop: household courtyard with flat stone, clay oven, mud wall, and a little shade.
Foreground action: Layla presses her fingers into dough that has stayed flat.
Required object/gesture: shallow bread tray with flat dough; flour on Layla's fingertips.
Background detail: empty grain sack folded near the wall, chicken or water jar at the edge of frame.
Lighting/mood: hard morning light, practical worry, no theatrical despair.
Avoid: bakery shop, abundant food, modern kitchen tools, readable packaging.
```

## Prompt 5 - Her Brother's Letter

```text
Event: cp_layla.22 - "Her Brother's Letter"
Narrative function: family news arrives as a paper that changes the air in the room.
Subject: Layla in her thirties, seated near Ahmed or an older relative who remains secondary.
Scene/backdrop: village interior at lamplight, low table, reed roof, folded bedding.
Foreground action: Layla holds a letter close while another hand points to a line she cannot fully read.
Required object/gesture: folded letter with no readable text; Layla's thumb smoothing a crease.
Background detail: lamp flame, clay cup, doorway into night.
Lighting/mood: warm lamplight, family tension under quiet voices.
Avoid: modern envelope, readable Arabic calligraphy, dramatic reunion, military dispatch scene.
```

## Prompt 6 - Burning Letters

```text
Event: cp_layla.117 - "Burning Letters"
Narrative function: records and memories are destroyed because keeping them has become unsafe or unbearable.
Subject: older Layla crouched near a small brazier or clay hearth, face lit from below.
Scene/backdrop: modest household courtyard or room corner at night, clay wall and reed shadows.
Foreground action: Layla lowers a folded paper into a small flame.
Required object/gesture: burning paper edge, Layla's hand held steady despite age.
Background detail: a small stack of saved papers or cloth bundle just behind her, untouched.
Lighting/mood: dark amber firelight, secrecy, grief under control.
Avoid: bonfire spectacle, readable documents, political poster burning, fantasy ritual.
```

## Prompt 7 - Cairo Is Calling

```text
Event: cp_layla.70 - "Cairo Is Calling"
Narrative function: the city offer appears as a road and a bundle, not as romance about escape.
Subject: Layla in middle age at the edge of her village, holding a tied cloth bundle.
Scene/backdrop: road from a Delta village toward Cairo, canal edge, low fields, distant telegraph poles or city haze.
Foreground action: Layla stands with one foot on the path while looking back toward the household door.
Required object/gesture: tied cloth bundle in her hand; door or family threshold behind her.
Background detail: donkey cart on the road, irrigation ditch, dust in low light.
Lighting/mood: early morning decision, possibility mixed with fear.
Avoid: panoramic city skyline, train-station glamour, modern suitcase, heroic departure pose.
```

## Prompt 8 - Chains Remembered

```text
Event: cp_layla.103 - "Chains"
Narrative function: legal freedom is measured against remembered constraint and the marks it leaves on bodies.
Subject: elderly Layla, hands in foreground, looking at an old iron chain or tether on a table.
Scene/backdrop: storage corner of a village house or estate outbuilding, not a prison.
Foreground action: Layla touches the cold chain with one finger while keeping her body slightly back.
Required object/gesture: old iron chain beside a wooden yoke or field tool; Layla's hand near but not gripping it.
Background detail: dusty shelf, folded sack, shaft of light through a small opening.
Lighting/mood: quiet historical weight, no violence shown.
Avoid: dungeon, slave-market spectacle, heroic emancipation poster, modern metal handcuffs.
```

## Prompt 9 - Child Fever

```text
Event: cp_layla.82 - "Fever"
Narrative function: child mortality is intimate and practical, carried by a wet cloth and a mother's silence.
Subject: Layla in her twenties or thirties beside a feverish child, posture tight and controlled.
Scene/backdrop: dim household room, low mat, clay wall, oil lamp, water basin.
Foreground action: Layla wrings or folds a damp cloth over the child.
Required object/gesture: damp cloth in Layla's hands; small brass or clay water basin nearby.
Background detail: Ahmed's shadow or another relative at the threshold, unable to help.
Lighting/mood: low lamplight, fear held very still.
Avoid: visible death, hospital ward, modern medicine, sentimental angelic child pose.
```

## Prompt 10 - The First Child

```text
Event: cp_layla.5 - "The First Cry"
Narrative function: childbirth is both joy and danger, a room of women and breath rather than a symbolic cradle.
Subject: young Layla after childbirth, exhausted, with a midwife and one older woman near her.
Scene/backdrop: village room with reed roof, woven mat, clay lamp, clean cloths, and water basin.
Foreground action: the midwife wraps the newborn while Layla reaches one tired hand toward the bundle.
Required object/gesture: newborn mostly hidden in plain cloth; Layla's hand reaching, not posing.
Background detail: folded towels, brass or clay basin, doorway curtain.
Lighting/mood: dawn or lamplight, fragile relief, bodily reality without gore.
Avoid: modern hospital, angelic glow, explicit birth scene, smiling family portrait.
```

## Prompt 11 - Children and School

```text
Event: cp_layla.101 - "The School"
Narrative function: school arrives as a slate, a threshold, and a child leaving household labor for letters.
Subject: Layla in middle age watching one of her children at a school doorway.
Scene/backdrop: modest village school or courtyard room in 19th-century Egypt, mud wall, bench, teacher's low table.
Foreground action: a child holds a slate and steps away from Layla; Layla remains near the threshold.
Required object/gesture: slate in the child's hand; Layla's hand still holding a small food cloth.
Background detail: other children seated on mats, teacher partly visible, no modern desks.
Lighting/mood: morning light, pride mixed with household worry.
Avoid: modern classroom, cheerful campaign poster, readable letters, idealized schoolyard.
```

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-provenance.py --rank-missing --limit 80
script/audit-release-readiness.py --mode dev
```

When a generated candidate is accepted, wire it with a version suffix (`_v09`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.9-superseded/`.
