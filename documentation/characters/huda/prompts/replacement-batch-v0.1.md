# Huda replacement image batch v0.1

Date: 2026-05-30

Purpose: replace Huda's generic vanilla motion plates with authored GPT-image-2 stills that read correctly in Victoria 3's event window. The event text panel covers the right half of the image, so every prompt keeps the important face, action, and object in the left or center-left safe area.

Shared visual contract for every prompt:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Subject: Huda al-Matariya, a Misri Egyptian city lodger and day laborer; practical tired face, olive-brown skin, dark eyes, faded indigo scarf, plain work dress, grounded 19th-century Cairo materials.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, quiet human scale.
Composition/framing: event-window safe composition; place the essential face, action, and required object in the left half or center-left because the game's text panel covers the right half. The right half may carry atmosphere, architecture, or background only.
Constraints: no text, no UI, no border, no watermark, no modern clothing, no modern machinery, no fantasy costume, no palace grandeur, no heroic propaganda pose.
```

## Batch targets

| Priority | Asset | Active windows | Main event families |
|---:|---|---:|---|
| 1 | `cp_huda_room_alley_v01.dds` | 1 | Huda intro, rented room |
| 2 | `cp_huda_street_planks_v01.dds` | 1 | construction street, planks |
| 3 | `cp_huda_water_under_stone_v01.dds` | 1 | clean water, courtyard tap |
| 4 | `cp_huda_rent_book_v01.dds` | 1 | rent collector, ledger |
| 5 | `cp_huda_roof_patch_v01.dds` | 1 | roof leak, rented shelter |
| 6 | `cp_huda_white_road_v01.dds` | 1 | paved road, dust, washing |

## Prompt 1 - The Room Above the Alley

```text
Event: cp_huda.10 - "The Room Above the Alley"
Narrative function: urban growth becomes personal when Huda counts what fits in one rented room.
Scene/backdrop: cramped rented upstairs room above a Cairo alley shop, low ceiling, cracked plaster wall, narrow wooden window, rolled bedding, small wooden chest.
Foreground action: Huda sets a heavy clay water jar down beside folded bedding and looks toward the narrow window, measuring the room with her eyes.
Required object/gesture: Huda, clay water jar, folded bedding, cramped rented room, and narrow window.
Lighting/mood: dusty late-afternoon window light, quiet pressure, tired calculation.
Avoid: wealthy interior, empty slum panorama, picturesque tourist alley, palace room.
```

## Prompt 2 - The Street Under Planks

```text
Event: cp_huda.20 - "The Street Under Planks"
Narrative function: city improvement arrives as broken stone, open trenches, and Huda's body carrying the cost.
Scene/backdrop: 19th-century Cairo street under construction, road stones lifted, narrow ditch, rough wooden planks over exposed pipe trench, plaster shopfronts and rented rooms overhead.
Foreground action: Huda carries a basket of lime chips or broken stone, pausing at the plank with one foot testing it before crossing.
Required object/gesture: Huda, wooden plank bridge, open trench, basket of lime chips, and city construction.
Lighting/mood: harsh dusty morning light, dignity under pressure, labor and disruption.
Avoid: generic factory floor, South American architecture, picturesque tourist alley, empty cityscape.
```

## Prompt 3 - The Water Under Stone

```text
Event: cp_huda.30 - "The Water Under Stone"
Narrative function: clean water is relief in the hand before it becomes rent in the landlord's mouth.
Scene/backdrop: cramped 19th-century Cairo courtyard below rented rooms, cracked plaster walls, a new simple courtyard tap or pipe, clay jars nearby.
Foreground action: Huda kneels or bends at the tap, putting one hand under the cold clear stream before filling a clay jar.
Required object/gesture: Huda, clear water stream, courtyard tap or pipe, clay jar, and rented courtyard.
Lighting/mood: cool morning shade, relief mixed with worry about rent.
Avoid: public fountain spectacle, wealthy bathhouse, empty architecture, modern sink.
```

## Prompt 4 - The Rent Book

```text
Event: cp_huda.40 - "The Rent Book"
Narrative function: city growth raises the rent before it raises anyone's dignity.
Scene/backdrop: 19th-century Cairo alley doorway below her rented room, rough stair rising behind her, landlord's small table near the wall.
Foreground action: Huda watches a landlord mark a rent book while her hand tightens around a coin.
Required object/gesture: Huda's tense hand with coin, landlord's rent book with unreadable marks, pencil or reed pen, rough stair behind her.
Lighting/mood: hard noon shade, anger kept inside the body.
Avoid: readable text or numbers, modern office, courtroom, eviction spectacle, comic miser.
```

## Prompt 5 - The Roof Patch

```text
Event: cp_huda.50 - "The Roof Patch"
Narrative function: rented shelter fails in places the owner never sleeps under.
Scene/backdrop: small rented upstairs room in 19th-century Cairo, low patched tin-and-wood roof, cracked plaster, folded bedding, basin on the floor, flour sack moved away from a drip.
Foreground action: Huda moves a basin under a leak while a young repair boy presses tar or cloth onto a roof patch.
Required object/gesture: Huda, dripping roof, basin, folded bedding, and makeshift roof patch.
Lighting/mood: rainy dim interior, weary patience, rented fragility.
Avoid: collapsed roof disaster, wealthy house, comic repair scene, theatrical crying.
```

## Prompt 6 - The White Road

```text
Event: cp_huda.60 - "The White Road"
Narrative function: a paved road improves the city while sending white dust back into Huda's washing.
Scene/backdrop: newly paved pale road in a 19th-century Cairo district, white dust, plaster walls, shopfronts, narrow shade, children pushed to the side by passing carts.
Foreground action: Huda sweeps or shakes white road dust from a sheet at her threshold while holding folded washing.
Required object/gesture: Huda, pale new road, dust on cloth, threshold, and nearby carts or children.
Lighting/mood: bright hard afternoon, improvement with no shade, domestic labor against civic polish.
Avoid: grand boulevard triumph, European city, empty road, celebratory parade, readable signs.
```

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-provenance.py --strict-generated
script/audit-release-readiness.py --mode dev
```
