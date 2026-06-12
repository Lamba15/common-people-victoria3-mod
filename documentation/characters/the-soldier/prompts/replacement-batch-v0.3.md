# Soldier replacement image batch v0.3

Date: 2026-05-30

Purpose: replace Yusuf ibn Mahmud's remaining vanilla/generic event videos with Common People generated art. This finishes the active Soldier slice so all visible Soldier events use mod-owned still images with the required military object and Yusuf's human reaction left-safe for the Victoria 3 event panel.

Generated with: `gpt-image-2`

Shared visual contract for every prompt:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Subject: Yusuf ibn Mahmud, a young Misri Egyptian soldier around 20; worn uniform, observant and uneasy, family-bound, never heroic propaganda.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials, 19th-century Egypt, quiet human scale.
Composition/framing: close-medium or medium-wide. Put Yusuf, the key action, and required object in the left half or center-left; right half can carry barracks, rifles, smoke, bedding, and atmosphere.
Constraints: no readable text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no heroic parade, no battlefield poster, no decorative atmosphere without the required object.
```

## Batch targets

| Priority | Asset | Active windows | Main event families |
|---:|---|---:|---|
| 1 | `cp_soldier_arsenal_gate_v03.dds` | 1 | arsenal gate, military industry |
| 2 | `cp_soldier_beans_dusk_v03.dds` | 1 | peacetime barracks meal |
| 3 | `cp_soldier_letter_folded_v03.dds` | 1 | wartime letter home |

## Prompt 1 - The Arsenal Gate

```text
Event: cp_soldier.30 - "The Arsenal Gate"
Narrative function: military modernization becomes oil, smoke, benches, and hands making the order possible.
Subject: Yusuf in worn barracks uniform, watching rather than commanding.
Scene/backdrop: late-19th-century Egyptian arsenal workshop just inside a heavy gate before dawn; benches, rifles, oil, coal smoke, hot iron, men in aprons passing rifle parts.
Foreground action: Yusuf stands just inside the gate while a boy files a screw head until it shines.
Required object/gesture: Yusuf's face, open arsenal gate, filed rifle part or screw, oil-dark workbench.
Background detail: rifle racks, smoke, lamps, quiet workers, dawn beyond the gate.
Lighting/mood: pre-dawn industrial lamplight, war as manufactured labor, restrained unease.
Avoid: modern factory machinery, giant steampunk gears, heroic inspection, parade ground, clean museum weapons.
```

## Prompt 2 - Beans at Dusk

```text
Event: cp_soldier.40 - "Beans at Dusk"
Narrative function: ordinary warmth survives inside military hardship for a moment.
Subject: Yusuf sitting with other soldiers, tired and tender.
Scene/backdrop: modest Egyptian barracks courtyard or room at dusk with low wall, oil lamp, rolled bedding, rifles stacked nearby, city lamps beginning outside the gate.
Foreground action: Yusuf sits with his back to a wall, holding a warm bowl of thin beans and carefully tearing bread.
Required object/gesture: bowl of beans, torn bread, rifles stacked nearby, evening lamp light.
Background detail: two or three soldiers eating or humming quietly, rolled bedding, dusk gate.
Lighting/mood: dusk and lamplight, homesickness, small shared humanity, no spectacle.
Avoid: cafe scene, grand city plaza, banquet table, heroic military poster, modern mess hall.
```

## Prompt 3 - The Letter Folded Twice

```text
Event: cp_soldier.50 - "The Letter Folded Twice"
Narrative function: a letter home carries fear because the soldier cannot.
Subject: Yusuf in worn campaign uniform, exhausted and homesick.
Scene/backdrop: rough military camp or barracks table during wartime, oil lamp, borrowed ink, thin paper, other soldiers writing or waiting, bedrolls and rifles in shadow.
Foreground action: Yusuf folds a thin letter twice and presses the crease with his thumb after scratching out a line.
Required object/gesture: thin letter paper, ink pot, Yusuf's thumb pressing the folded crease, no readable text.
Background detail: men borrowing ink, dim rifles, bedrolls, tent or barracks shadow.
Lighting/mood: low lamplight, fear kept private, fragile letter as burden.
Avoid: office desk, readable letter, battlefield action, modern uniforms, heroic farewell scene.
```

## Built-in image generation output

- `cp_soldier_arsenal_gate_v03`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a93ee27d88191a2937c99350b58da.png`
- `cp_soldier_beans_dusk_v03`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a945d85688191a5602b00efedc8a3.png`
- `cp_soldier_letter_folded_v03`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a94c152a481918ce643f8e9228a24.png`

## Workspace archive

- `image/generated/soldier/v0.3/cp_soldier_arsenal_gate_v03_1536.png`
- `image/generated/soldier/v0.3/cp_soldier_arsenal_gate_v03.dds.png`
- `image/generated/soldier/v0.3/cp_soldier_beans_dusk_v03_1536.png`
- `image/generated/soldier/v0.3/cp_soldier_beans_dusk_v03.dds.png`
- `image/generated/soldier/v0.3/cp_soldier_letter_folded_v03_1536.png`
- `image/generated/soldier/v0.3/cp_soldier_letter_folded_v03.dds.png`

## Shipped DDS

- `mod/gfx/event_pictures/cp_soldier_arsenal_gate_v03.dds`
- `mod/gfx/event_pictures/cp_soldier_beans_dusk_v03.dds`
- `mod/gfx/event_pictures/cp_soldier_letter_folded_v03.dds`

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
