# Hassan Bey replacement image batch v0.3

Date: 2026-05-30

Purpose: replace Hassan Bey al-Sayyid's remaining vanilla/generic event videos with Common People generated art. This finishes his active slice: every visible Bey event now uses mod-owned still art, with the important person/action/object kept left-safe for the Victoria 3 event text panel.

Generated with: `gpt-image-2`

Shared visual contract for every prompt:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Subject: Hassan Bey al-Sayyid, an older Misri Egyptian aristocrat in late-19th-century estate clothes, proud but unsettled; never a villain caricature.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials, 19th-century Egypt, quiet human scale.
Composition/framing: close-medium or medium-wide, no epic hero camera. Put the essential face, action, and required object in the left half or center-left; right half can carry atmosphere and background.
Constraints: no readable text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no invented flags, no palace grandeur, no decorative atmosphere without the required object.
```

## Batch targets

| Priority | Asset | Active windows | Main event families |
|---:|---|---:|---|
| 1 | `cp_bey_factory_boundary_v03.dds` | 1 | factory smoke at the estate boundary |
| 2 | `cp_bey_visitors_card_v03.dds` | 1 | new officialdom and visitor's card |

## Prompt 1 - Smoke at the Boundary

```text
Event: cp_bey.30 - "Smoke at the Boundary"
Narrative function: industrialization makes the estate boundary look suddenly obsolete.
Subject: Hassan Bey al-Sayyid, about 52, proud but unsettled, in a dark coat and fez.
Scene/backdrop: edge of an Egyptian Delta estate where a new brick factory wall rises at the old field boundary; unfinished beams and a thin smoke column behind the wall.
Foreground action: Al-Sayyid stands beside the old boundary stone, one hand hovering near it but not fully touching.
Required object/gesture: old boundary stone, Al-Sayyid's hovering hand, brick factory wall, and factory smoke.
Background detail: boys from tenant houses carrying timber through the gate without deference, fields and palms behind.
Lighting/mood: dusty afternoon, grief under control, modernization felt as brick, smoke, and labor.
Avoid: South American architecture, giant modern factory, celebratory opening, heroic industrial poster.
```

## Prompt 2 - The Visitor's Card

```text
Event: cp_bey.40 - "The Visitor's Card"
Narrative function: bureaucracy enters the estate as printed paper and polite absence.
Subject: Hassan Bey al-Sayyid, about 52, proud and isolated, in estate clothes with a fez and dark coat.
Scene/backdrop: upper room of an Egyptian estate house with shuttered light, aging polished furniture, high ceiling, and a servant near the doorway.
Foreground action: Al-Sayyid studies a small cream visitor's card left by a new government official who did not wait.
Required object/gesture: blank visitor's card in Al-Sayyid's hand or on the tray, no readable text; his expression restrained and unsettled.
Background detail: tray, empty chairs, doorway, polite distance around the room.
Lighting/mood: daylight through shutters, bureaucracy arriving as paper, restrained dread.
Avoid: cafe scene, social party, modern business card design, readable letters, obvious luxury-palace staging.
```

## Built-in image generation output

- `cp_bey_factory_boundary_v03`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a8aa52d408191942c5e26bf0a4818.png`
- `cp_bey_visitors_card_v03`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a8b05961c81918e46cab12f4a0e3c.png`

## Workspace archive

- `image/generated/al-sayyid/v0.3/cp_bey_factory_boundary_v03_1536.png`
- `image/generated/al-sayyid/v0.3/cp_bey_factory_boundary_v03.dds.png`
- `image/generated/al-sayyid/v0.3/cp_bey_visitors_card_v03_1536.png`
- `image/generated/al-sayyid/v0.3/cp_bey_visitors_card_v03.dds.png`

## Shipped DDS

- `mod/gfx/event_pictures/cp_bey_factory_boundary_v03.dds`
- `mod/gfx/event_pictures/cp_bey_visitors_card_v03.dds`

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-generic-video-art.py
script/audit-release-readiness.py --mode dev
```
