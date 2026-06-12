# Layla replacement image batch v0.8

Date: 2026-05-26

Purpose: queue the next high-impact Layla legacy/no-source DDS images after v0.7. This batch continues the ranked backlog from `script/audit-art-provenance.py --rank-missing --limit 30`, skipping assets already planned in v0.7 and prioritizing images reused across five or four active event windows.

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
| 1 | `cp_layla_children_leave_v08.dds` | 5 | child-labor law, children conversation |
| 2 | `cp_layla_election_day_v08.dds` | 5 | first vote, vote conversation |
| 3 | `cp_layla_foreman_runner_v08.dds` | 5 | Ahmed mill death, worker conversation |
| 4 | `cp_layla_rifles_v08.dds` | 5 | militarized police, war/ruler conversation |
| 5 | `cp_layla_strangers_v08.dds` | 5 | migration and strangers in the lane |
| 6 | `cp_layla_conversation_country_v08.dds` | 4 | old ruler / country memory |
| 7 | `cp_layla_conversation_lost_child_v08.dds` | 4 | lost-child memory |
| 8 | `cp_layla_conversation_paper_v08.dds` | 4 | homesteading paper and water petition |
| 9 | `cp_layla_conversation_rolls_v08.dds` | 4 | mill rolls and worker names |
| 10 | `cp_layla_conversation_room_v08.dds` | 4 | marriage room at night |
| 11 | `cp_layla_daughter_reads_v08.dds` | 4 | daughter literacy |

## Prompt 1 - The Children Leave the Floor

```text
Event: cp_layla.118 and cp_layla_vox.24 follow-ups - "The Children Leave the Floor"
Narrative function: a humane law creates a household crisis because one small wage disappears.
Subject: Layla in later middle age, practical city clothes, standing at a textile mill doorway with a bread bundle.
Scene/backdrop: 19th-century Egyptian textile mill interior near the exit, low light, looms and cotton dust behind.
Foreground action: children are being led or told to leave the shop floor; one small boy passes Layla.
Required object/gesture: Layla breaking bread from her bundle for the boy; the boy's hands reaching without ceremony.
Background detail: foreman with open hand, not cruel, workers at looms pausing without becoming a crowd.
Lighting/mood: dusty morning light through high windows, mercy mixed with dread.
Avoid: schoolroom, smiling reform poster, modern factory safety signs, readable notices.
```

## Prompt 2 - Election Day

```text
Event: cp_layla.24 and cp_layla_vox.105 follow-ups - "Election Day"
Narrative function: voting is made ordinary, awkward, and permanent in a woman's life.
Subject: elderly Layla, careful and composed, with a plain shawl and weathered hands.
Scene/backdrop: small district polling room or municipal office in late 19th-century Egypt, not a grand parliament.
Foreground action: Layla folds a ballot or marked paper at a simple table.
Required object/gesture: folded ballot in Layla's hand; pencil or stamp on the table, with no readable names.
Background detail: male clerk waiting politely, another voter outside the doorway, sunlit lane beyond.
Lighting/mood: warm cramped room, formal politeness, private significance.
Avoid: campaign posters, modern ballot boxes, triumphant suffrage iconography, readable text.
```

## Prompt 3 - The Foreman's Runner

```text
Event: cp_layla.81 and cp_layla_vox.72 follow-ups - "The Foreman's Runner"
Narrative function: Ahmed's workplace death arrives through a boy who cannot say the first word.
Subject: Layla in middle age at a city tenement doorway, still before grief.
Scene/backdrop: narrow stair landing or doorway above a mill district, 19th-century Egypt.
Foreground action: a young mill runner stands in the doorway holding his cap, unable to speak.
Required object/gesture: the boy's cap twisted in his hands; Layla's hand on the doorframe.
Background detail: dim stairwell, neighbor's half-open door, faint mill smoke outside a small window.
Lighting/mood: morning light that feels wrong, news delivered like a parcel.
Avoid: body on screen, melodramatic collapse, modern industrial accident scene.
```

## Prompt 4 - Rifles in the Square

```text
Event: cp_layla.120 and cp_layla_vox.104 follow-ups - "Rifles in the Square"
Narrative function: state power becomes visible in an ordinary market square.
Subject: elderly Layla passing through the square with a basket of onions, shoulders drawn small.
Scene/backdrop: Egyptian market square, late 19th century; low shops, weighing stall, dusty ground.
Foreground action: Layla walks past two policemen or soldiers whose rifles remain on their shoulders.
Required object/gesture: rifle on shoulder in the middle distance; Layla's basket held close at her hip.
Background detail: onion scale or kunafa stall, a few villagers watching with lowered eyes.
Lighting/mood: hard afternoon light, quiet intimidation, no battle.
Avoid: battlefield, heroic soldiers, modern uniforms, revolutionary poster composition.
```

## Prompt 5 - Strangers in the Lane

```text
Event: cp_layla.121 and cp_layla_vox.81, .83, .84, .89 - "Strangers in the Lane"
Narrative function: migration reaches Layla as a smell, an accent, and a plate crossing a lane.
Subject: older Layla holding a plate or bowl at her doorway, cautious but curious.
Scene/backdrop: mixed Cairo or Delta lane with modest doors, plaster walls, coffee pot, carpenter's wood, and laundry.
Foreground action: Layla offers or receives a dish from a newly arrived neighbor family.
Required object/gesture: plate changing hands; Layla's fingers not quite relaxed.
Background detail: brass coffee pot, pine boards near a carpenter, children watching from different doorways.
Lighting/mood: Ramadan or late-afternoon warmth, lane becoming larger than it was.
Avoid: cosmopolitan postcard, national flags, exotic costume display, modern street.
```

## Prompt 6 - The Old Ruler, Remembered

```text
Event: cp_layla_vox.106 and follow-ups - "The Old Ruler, Remembered"
Narrative function: Layla measures rulers by what their years did to bodies, fields, and knees.
Subject: elderly Layla at the edge of an imagined administrative room, not intimidated but tired.
Scene/backdrop: modest Egyptian government room with a desk, ledger shelves, and a wall map suggested without readable labels.
Foreground action: Layla stands before a distant seated official silhouette, one hand resting on a cane or folded shawl.
Required object/gesture: Layla's fingers counting rulers on one hand; a clerk's closed ledger nearby.
Background detail: a younger clerk, faded map, worn carpet, no throne.
Lighting/mood: late dusty light, memory and fatigue rather than spectacle.
Avoid: palace grandeur, coronation scene, readable ruler portraits, fantasy court.
```

## Prompt 7 - The Lost Child

```text
Event: cp_layla_vox.35 and follow-ups - "The Lost Child"
Narrative function: grief is held by an object and by what Layla does not say aloud.
Subject: Layla in middle age, seated low beside a small wrapped bundle or child's garment.
Scene/backdrop: dim household interior with reed roof, clay wall, woven mat, and doorway light.
Foreground action: Layla folds a small garment or cloth slowly, alone.
Required object/gesture: child's small garment in Layla's hands; her mouth closed as if holding a name back.
Background detail: unused sleeping mat, clay cup, narrow strip of field beyond the door.
Lighting/mood: lamplight and doorway light, intimate restraint.
Avoid: graveyard melodrama, visible dead child, saintly grief pose, sentimental family tableau.
```

## Prompt 8 - She Has Come With the Paper

```text
Event: cp_layla_vox.103 and follow-ups - "She Has Come with the Paper"
Narrative function: the deed gives Layla courage to ask a second, practical question about water.
Subject: Layla in middle age, holding a folded deed or land paper with cautious pride.
Scene/backdrop: modest provincial office or audience room, 19th-century Egypt, not a palace.
Foreground action: Layla holds the paper outward while glancing toward a clerk's ledger.
Required object/gesture: folded deed with seal, no readable text; one finger pointing toward a canal sketch or blank ledger page.
Background detail: official or secretary at a wooden table, clay-colored wall, open shutter light.
Lighting/mood: dry bureaucratic daylight, gratitude turning into a question.
Avoid: readable document text, courtroom drama, triumphant landowner pose.
```

## Prompt 9 - The Mill Rolls

```text
Event: cp_layla_vox.74 and follow-ups - "The Rolls"
Narrative function: factory names and absences become a ledger before they become grief.
Subject: Layla at a mill office threshold, older but alert, watching a clerk write names.
Scene/backdrop: small textile mill office beside the shop floor; shelves, stool, cotton dust, ledger table.
Foreground action: a clerk turns a large roll book while workers wait outside the door.
Required object/gesture: large ledger/roll book with unreadable marks; Layla's hand gripping the threshold.
Background detail: mill gate, oil-stained sleeve, a worker looking away.
Lighting/mood: smoky dusk, anxiety before bad news.
Avoid: modern payroll office, readable names, faceless crowd, heroic labor poster.
```

## Prompt 10 - The Room, Dark

```text
Event: cp_layla_vox.15 and follow-ups - "The Room, Dark"
Narrative function: marriage is shown as breath, a wall, a door ajar, and a hand reaching back.
Subject: young or middle-aged Layla and Ahmed in a modest room at night.
Scene/backdrop: village room with reed roof, woven mat, clay lamp now out, door ajar to the lane.
Foreground action: Layla lies or sits with her face half-turned from Ahmed, reaching one hand back toward his shoulder.
Required object/gesture: hand reaching back without turning; ajar door letting in a thin line of night.
Background detail: low mat, clay jar, faint dog or lane shadow beyond the door.
Lighting/mood: very low blue night and residual lamp warmth, private tenderness without glamour.
Avoid: romantic glamour, modern bed, exposed bodies, theatrical embrace.
```

## Prompt 11 - The Daughter Reads

```text
Event: cp_layla.102 and cp_layla_vox.2301-.2303 - "The Daughter Reads"
Narrative function: literacy arrives through Layla's daughter, small to the child and enormous to the mother.
Subject: Layla in middle age with her young daughter Nur, both plainly dressed.
Scene/backdrop: household interior in afternoon or lamplight, low table, woven mat, clay wall.
Foreground action: Nur reads a folded letter aloud while Layla listens with her face partly turned away.
Required object/gesture: letter in the child's hands; Layla's hands still in her lap, not touching the paper.
Background detail: small oil lamp, low shelf, doorway to a lane or courtyard.
Lighting/mood: quiet revelation, pride hidden under restraint.
Avoid: modern classroom, smiling literacy campaign poster, readable letter text.
```

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-provenance.py --rank-missing --limit 30
script/audit-release-readiness.py --mode dev
```

When a generated candidate is accepted, wire it with a version suffix (`_v08`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.8-superseded/`.
