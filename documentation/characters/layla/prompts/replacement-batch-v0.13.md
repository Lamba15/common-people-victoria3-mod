# Layla replacement image batch v0.13

Date: 2026-05-29

Purpose: queue the next single-window slice of Layla's remaining legacy/no-source DDS images after v0.12. This batch covers social security absence, health systems, village humor, Nile rhythm, women's-rights papers, self-employment, propaganda, and religious coexistence.

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
| 1 | `cp_layla_month_without_v13.dds` | 1 | absent pension/envelope arithmetic |
| 2 | `cp_layla_mosque_doctor_v13.dds` | 1 | charitable mosque doctor |
| 3 | `cp_layla_mule_v13.dds` | 1 | stubborn village mule |
| 4 | `cp_layla_next_village_doctor_v13.dds` | 1 | public doctor in next village |
| 5 | `cp_layla_nile_rises_v13.dds` | 1 | flood year and silt |
| 6 | `cp_layla_old_woman_v13.dds` | 1 | Umm Saad sees through walls |
| 7 | `cp_layla_on_rolls_v13.dds` | 1 | women's suffrage rolls |
| 8 | `cp_layla_own_stall_v13.dds` | 1 | self-employment crossroads |
| 9 | `cp_layla_paper_my_name_v13.dds` | 1 | property deed in her name |
| 10 | `cp_layla_poster_v13.dds` | 1 | authoritarian poster in town |
| 11 | `cp_layla_procession_v13.dds` | 1 | Coptic procession passes |

## Prompt 1 - The Month Without

```text
Event: cp_layla.98 - "The Month Without"
Narrative function: the absence of social security is measured by four small coin stacks and the envelope that never comes.
Subject: older Layla alone at a kitchen table at night.
Scene/backdrop: modest room, worn table, cloth, kerosene lamp, grain sack, squeaking door hinge nearby.
Foreground action: Layla counts coins into four small stacks and folds the cloth back over them.
Required object/gesture: four small coin stacks; an empty place where an envelope might have been; Layla's hand pausing over the count.
Background detail: thin bread, repair string near the door, daughter just outside the light if visible.
Lighting/mood: low lamplight, arithmetic grief, anger beginning as clarity.
Avoid: official welfare office, visible cash windfall, readable envelope, melodramatic poverty tableau.
```

## Prompt 2 - The Doctor at the Mosque

```text
Event: cp_layla.108 - "The Doctor at the Mosque"
Narrative function: charitable health care arrives through an old doctor's bag, a mosque courtyard, and Khaled's cough quieting a little.
Subject: Layla bringing older Khaled to a young doctor with steady hands.
Scene/backdrop: plain mosque courtyard or side room after Friday prayer, worn mat, small table, shaded wall.
Foreground action: the doctor listens to Khaled's chest or prepares an infusion while Layla watches closely.
Required object/gesture: old medical bag and simple cup or bottle of infusion; Khaled seated, coughing but dignified.
Background detail: shoes near the threshold, a sheikh or committee man distant, no crowd spectacle.
Lighting/mood: afternoon shade, cautious gratitude, charity without romance.
Avoid: modern clinic, hospital bed, surgical theatre, ornate mosque interior, readable notices.
```

## Prompt 3 - The Mule That Will Not Move

```text
Event: cp_layla.23 - "The Mule That Will Not Move"
Narrative function: the village's pace is embodied by a stubborn mule blocking Layla's way to the well.
Subject: Layla in her doorway with a bucket, waiting for a mule and straw cart to move.
Scene/backdrop: village lane between mud-brick houses, well visible farther down, afternoon dust.
Foreground action: a small boy pleads with the mule while Layla leans with the bucket under her arm.
Required object/gesture: mule standing squarely in the lane; straw cart behind it; Layla's patient bucket.
Background detail: neighbors watching with dry amusement, well stones, no slapstick.
Lighting/mood: late afternoon, dry humor, village time.
Avoid: cute animal portrait, violent whipping, circus comedy, modern cart.
```

## Prompt 4 - The Doctor in the Next Village

```text
Event: cp_layla.110 - "The Doctor in the Next Village"
Narrative function: public health care becomes the four-mile road to a doctor who asks only who is ill.
Subject: Layla arriving with news of Khaled's illness at a simple village doctor's door.
Scene/backdrop: next village doorway, dusty road behind, modest room with doctor's bag and stool.
Foreground action: the doctor opens the door or steps out with his bag as Layla explains, hand pressed to her chest.
Required object/gesture: doctor's bag ready to travel; Layla's tired feet or dusty hem from the walk.
Background detail: Khaled's wife or a worried relative behind Layla, low evening light, no payment table.
Lighting/mood: dusk after a long walk, disbelief turning to relief.
Avoid: modern ambulance, hospital corridor, money exchange, bureaucratic papers.
```

## Prompt 5 - The Nile Rises

```text
Event: cp_layla.26 - "The Nile Rises"
Narrative function: the year's fate is read in dark silt and water height along the irrigation channel.
Subject: Layla walking beside Ahmed or Ahmed's memory along the irrigation channel.
Scene/backdrop: Lower Egyptian field edge, irrigation water, dark silt line, palms, low village fields.
Foreground action: Layla bends or pauses to read the color of the silt at the water's edge.
Required object/gesture: dark silt on the bank; Layla's hand near the water without touching it.
Background detail: quiet men in the lane or field edge, simple water wheel or channel wall.
Lighting/mood: early morning, reverence without sentimentality, ancient rhythm.
Avoid: grand Nile panorama, tourist felucca, flood disaster, desert fantasy.
```

## Prompt 6 - The Old Woman Who Sees Through Walls

```text
Event: cp_layla.19 - "The Old Woman Who Sees Through Walls"
Narrative function: Umm Saad's visit says nothing aloud and still sees the hidden pot behind the brick.
Subject: elderly Umm Saad in Layla's house while Layla offers a cup of water.
Scene/backdrop: modest interior, rough wall, loose brick, hidden storage place implied but not exposed.
Foreground action: Umm Saad drinks slowly and looks toward the brick while Layla holds the empty cup or pitcher.
Required object/gesture: cup of water; Umm Saad's gaze toward the loose brick; Layla standing still.
Background detail: doorway light, simple shelf, hens implied outside but not central.
Lighting/mood: quiet afternoon, unease, village knowledge.
Avoid: magical glow, fortune-teller costume, horror staging, revealed treasure.
```

## Prompt 7 - I Am on the Rolls

```text
Event: cp_layla.96 - "I Am on the Rolls"
Narrative function: women's suffrage reaches Layla as her name read aloud from a book.
Subject: Layla among village women while a town man reads names from a ledger.
Scene/backdrop: village square or well, modest municipal table, women listening without cheering.
Foreground action: the man points to a line in the ledger while Layla hears her name and touches the wall or doorjamb.
Required object/gesture: ledger book with unreadable lines; Layla's hand touching the wall or doorjamb.
Background detail: older women exchanging looks, one girl craning to hear, no ballot box focus.
Lighting/mood: public morning, recognition, uncertainty.
Avoid: election rally, modern polling booth, readable voter list, patriotic pageantry.
```

## Prompt 8 - Her Own Stall

```text
Event: cp_layla.97 - "Her Own Stall"
Narrative function: self-employment begins as goods laid out on the floor and the market corner imagined.
Subject: Layla sorting goods that could become a small stall.
Scene/backdrop: household floor or quiet market corner, baskets, cloth, bread, pickled jars, small coin purse.
Foreground action: Layla lays out what she can sell while Ahmed or a child watches from the side.
Required object/gesture: neat row of goods for a first stall; Layla's hand placing the final jar or cloth.
Background detail: empty market corner suggested through doorway or lane, no painted sign yet.
Lighting/mood: cautious courage, shame and victory together.
Avoid: prosperous shop, modern storefront, readable sign, triumph pose.
```

## Prompt 9 - A Paper with My Name

```text
Event: cp_layla.94 - "A Paper with My Name"
Narrative function: property rights become a deed in her own hand, not yet the village's belief.
Subject: Layla holding a deed with her name implied but not readable.
Scene/backdrop: village well or household doorway, older women nearby, rough wall and doorjamb.
Foreground action: Layla studies a folded deed while an official or neighbor has just handed it over.
Required object/gesture: deed paper with no readable text; Layla's thumb on the fold; house wall behind her.
Background detail: women half-scoffing and half-hoping, Ahmed's brothers absent but implied by space.
Lighting/mood: clear daylight, pride mixed with caution.
Avoid: courtroom, celebratory certificate pose, readable document, modern legal office.
```

## Prompt 10 - The Poster on the Wall

```text
Event: cp_layla.106 - "The Poster on the Wall"
Narrative function: authoritarian propaganda is noticed as a poster, a clipboard, and the faces of men who repeat it.
Subject: Layla walking past a new poster pasted to a post-office or coffeehouse wall.
Scene/backdrop: Tuesday market morning, village/town wall, coffeehouse doorway, market errand basket.
Foreground action: Layla passes without stopping while a town man with clipboard counts who reads the poster.
Required object/gesture: large cream-colored poster with unreadable blocks of text; clipboard; Layla's lowered head.
Background detail: coffeehouse men repeating the slogan too loudly, market traffic moving around them.
Lighting/mood: bright public daylight, suspicion, self-protection.
Avoid: readable slogans, modern propaganda poster, flags, crowd rally, police raid.
```

## Prompt 11 - The Procession Passes

```text
Event: cp_layla.115 - "The Procession Passes"
Narrative function: freedom of conscience is felt as a Coptic procession crossing the market lane in peace.
Subject: Layla at a vegetable cart as a small Coptic procession passes.
Scene/backdrop: market lane, vegetable cart, modest village street, people parting and reforming.
Foreground action: priest in black and two boys in white carry candles and a small icon board while Layla's fingers rest on a cucumber.
Required object/gesture: candle flames leaning in wind; small icon board with no readable text; Layla at the vegetable cart.
Background detail: a boy offering a date to the priest, cart-man weighing vegetables correctly, no hostile crowd.
Lighting/mood: ordinary daylight, grace held under the breath.
Avoid: church interior, sectarian confrontation, festival spectacle, readable religious text.
```

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-provenance.py --rank-missing --limit 140
script/audit-release-readiness.py --mode dev
```

When a generated candidate is accepted, wire it with a version suffix (`_v13`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.13-superseded/`.
