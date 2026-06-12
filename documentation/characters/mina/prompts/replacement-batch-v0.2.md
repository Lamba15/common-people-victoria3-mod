# Mina replacement image batch v0.2

Date: 2026-05-30

Purpose: replace Mina's remaining vanilla/generic event videos with Common People generated art. This batch finishes the active Mina slice so all six visible Mina events use mod-owned still images with the important action kept in the left half of the event window.

Generated with: `gpt-image-2`

Shared visual contract for every prompt:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Subject: Mina, a young Coptic Egyptian printer's apprentice in late-19th-century Cairo; keep him grounded, unheroic, ink-stained, and visibly shaped by workshop labor.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials, 19th-century Egypt, quiet human scale.
Composition/framing: event-window readable at small size, close-medium or medium-wide, essential face/action/object in the left half or center-left, right half safe for atmosphere.
Constraints: no readable text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no palace grandeur, no invented flags, no decorative atmosphere without the required object.
```

## Batch targets

| Priority | Asset | Active windows | Main event families |
|---:|---|---:|---|
| 1 | `cp_mina_notice_sheet_v02.dds` | 1 | modern records, printed notice sheet |
| 2 | `cp_mina_night_proof_v02.dds` | 1 | night proofing, workshop fatigue |
| 3 | `cp_mina_catalogue_room_v02.dds` | 1 | universities, catalogues, government offices |
| 4 | `cp_mina_courtyard_sheet_v02.dds` | 1 | church courtyard notices |

## Prompt 1 - The Notice Sheet

```text
Event: cp_mina.30 - "The Notice Sheet"
Narrative function: modernization arrives as names and numbers that must survive the print shop without becoming wrong.
Subject: Mina as a young Coptic Egyptian printer's apprentice, sleeves rolled, ink on fingers; an older government clerk stands nearby.
Scene/backdrop: cramped Cairo letterpress workshop with a wooden press, type cases, paper stacks, and a doorway to a sunlit street.
Foreground action: Mina smooths a folded government list on the table while the clerk offers another paper.
Required object/gesture: folded notice sheet under Mina's hand, no readable text; type case and ink stone close enough to read as tools.
Background detail: modest shelves, worn stone floor, faint minaret or Cairo street beyond the doorway.
Lighting/mood: morning light, civic anxiety kept intimate and practical.
Avoid: telegraph office, readable forms, modern bureaucracy props, heroic official portrait.
```

## Prompt 2 - The Night Proof

```text
Event: cp_mina.40 - "The Night Proof"
Narrative function: the printer's invisible care appears as one corrected page after everyone else has gone home.
Subject: Mina alone at night in the workshop, tired but alert, holding a proof sheet close to an oil lamp.
Scene/backdrop: shuttered letterpress shop opening onto a narrow dark Cairo alley; press and type trays recede into shadow.
Foreground action: Mina reads the proof backward for errors, fingers stained with ink.
Required object/gesture: oil lamp, proof sheet with unreadable columns, Mina's hands gripping the paper.
Background detail: small cross or icon on a shelf, quiet alley, cooling press.
Lighting/mood: warm lamplight against blue-black night, mercy in careful labor, no melodrama.
Avoid: cafe scene, theatrical candlelit scholar pose, modern newspaper layout, readable type.
```

## Prompt 3 - The Catalogue Room

```text
Event: cp_mina.50 - "The Catalogue Room"
Narrative function: universities and offices become tactile through catalogues, margins, cords, and stacks.
Subject: Mina in a printer's apron, young and concentrated, sorting freshly printed catalogue sheets.
Scene/backdrop: Cairo print room with shelves of paper, type cases, bundled forms, and an open window with city architecture beyond.
Foreground action: Mina aligns a stack of catalogues and checks the margins with both hands.
Required object/gesture: catalogue sheets tied with blue cord or stacked in neat piles, no readable text.
Background detail: paper shelves, wooden cabinet, ink cup, distant school or mosque dome through the window.
Lighting/mood: clear daylight, order made by hand, modernization as modest craft.
Avoid: contract signing scene, office boardroom, female protagonist, modern filing cabinets, readable labels.
```

## Prompt 4 - The Courtyard Sheet

```text
Event: cp_mina.60 - "The Courtyard Sheet"
Narrative function: a printed sheet becomes public life as ordinary people pass it from hand to hand after church.
Subject: Mina in a simple dark robe or work clothes among Coptic courtyard neighbors; he remains a participant, not a preacher.
Scene/backdrop: small church courtyard in Cairo with sunlit plaster walls, archway, doorway, and a pinned notice on the right-side wall.
Foreground action: Mina offers or reads a sheet to an older woman while a boy watches and points.
Required object/gesture: sheet held between hands in the left half of frame, no readable text; pinned blank notice on the wall as secondary background.
Background detail: church cross, older men arguing quietly, dusty courtyard stones, warm afternoon light.
Lighting/mood: civic and communal, gentle tension, no sermon or spectacle.
Avoid: marketplace crowd, readable notice, modern church architecture, fantasy religious iconography.
```

## Built-in image generation output

- `cp_mina_notice_sheet_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_031624fcc273ddac016a1a7d80a58481918f4f7a6d7938a96f.png`
- `cp_mina_night_proof_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_031624fcc273ddac016a1a7e2116788191a747f57a6e4be765.png`
- `cp_mina_catalogue_room_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_031624fcc273ddac016a1a7f8b0f508191b815a507b8fa63e0.png`
- `cp_mina_courtyard_sheet_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_031624fcc273ddac016a1a7f3ef1a08191b0789382a3059ec6.png`

## Workspace archive

- `image/generated/mina/v0.2/cp_mina_notice_sheet_v02_1536.png`
- `image/generated/mina/v0.2/cp_mina_notice_sheet_v02.dds.png`
- `image/generated/mina/v0.2/cp_mina_night_proof_v02_1536.png`
- `image/generated/mina/v0.2/cp_mina_night_proof_v02.dds.png`
- `image/generated/mina/v0.2/cp_mina_catalogue_room_v02_1536.png`
- `image/generated/mina/v0.2/cp_mina_catalogue_room_v02.dds.png`
- `image/generated/mina/v0.2/cp_mina_courtyard_sheet_v02_1536.png`
- `image/generated/mina/v0.2/cp_mina_courtyard_sheet_v02.dds.png`

## Shipped DDS

- `mod/gfx/event_pictures/cp_mina_notice_sheet_v02.dds`
- `mod/gfx/event_pictures/cp_mina_night_proof_v02.dds`
- `mod/gfx/event_pictures/cp_mina_catalogue_room_v02.dds`
- `mod/gfx/event_pictures/cp_mina_courtyard_sheet_v02.dds`

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
