# Layla replacement image batch v0.12

Date: 2026-05-26

Purpose: queue the next single-window slice of Layla's remaining legacy/no-source DDS images after v0.11. This batch covers law, household, labor, religious, health, market, and industrial scenes where the image needs a concrete object: list, letter, loaf, scale, lamp, chimney, rug, paper, or stall tin.

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
| 1 | `cp_layla_insurance_man_v12.dds` | 1 | private insurance list |
| 2 | `cp_layla_law_new_v12.dds` | 1 | welfare law announced |
| 3 | `cp_layla_letter_folded_v12.dds` | 1 | closed border letter |
| 4 | `cp_layla_loaf_v12.dds` | 1 | price of the loaf |
| 5 | `cp_layla_mariam_letter_v12.dds` | 1 | Mariam writes from Cairo |
| 6 | `cp_layla_meeting_v12.dds` | 1 | meeting after shift |
| 7 | `cp_layla_merchants_scale_v12.dds` | 1 | merchant's scale |
| 8 | `cp_layla_midwife_lamp_v12.dds` | 1 | midwife's lamp |
| 9 | `cp_layla_mill_smoke_v12.dds` | 1 | first textile mill |
| 10 | `cp_layla_minaret_silence_v12.dds` | 1 | minaret's silence |
| 11 | `cp_layla_ministry_v12.dds` | 1 | ministry takes the stall |

## Prompt 1 - The Man with the Bag

```text
Event: cp_layla.109 - "The Man with the Bag"
Narrative function: private health insurance becomes a list that decides which doors matter.
Subject: older Layla at her doorstep while a town insurance man passes or pauses with a leather bag.
Scene/backdrop: narrow Egyptian village lane, modest doorways, dust, neighbors watching from thresholds.
Foreground action: the insurance man consults a folded list and leather bag while Layla watches from her step.
Required object/gesture: leather shoulder bag and official list with no readable writing; Layla's hand on the doorframe.
Background detail: Khaled or another older neighbor watching from the next house, better door farther down the lane.
Lighting/mood: dry daylight, politeness with quiet exclusion.
Avoid: modern insurance salesman, hospital setting, visible readable forms, villain caricature.
```

## Prompt 2 - The New Law

```text
Event: cp_layla.91 - "The New Law"
Narrative function: welfare reform reaches Layla as rumor, paper, and cautious hope before any envelope arrives.
Subject: older Layla seated on her threshold in late light.
Scene/backdrop: village lane or household doorway, bread basket, folded cloth, neighbor passing with news.
Foreground action: Layla holds still with the news while a plain paper or notice lies near her knee.
Required object/gesture: unofficial-looking law notice or paper held by a neighbor, no readable text; Layla's face uncertain.
Background detail: bread-woman or old woman in the lane, children barefoot nearby.
Lighting/mood: late afternoon, complicated gratitude, hope that is not yet trust.
Avoid: parliament room, cheering crowd, cash handout, readable law poster.
```

## Prompt 3 - The Gate Closes

```text
Event: cp_layla.122 - "The Gate Closes"
Narrative function: a closed border turns a cousin into a folded letter that can be kept but not used.
Subject: older Layla seated at a low table with a short letter from a cousin abroad.
Scene/backdrop: modest household room, drawer, child's photograph or small keepsake, low evening light.
Foreground action: Layla folds the letter into a small square after reading it twice.
Required object/gesture: folded letter on the table and an open drawer for kept things; no readable writing.
Background detail: Nur or another family member just outside the lamplight, travel bundle absent.
Lighting/mood: quiet dusk, distance, resignation without spectacle.
Avoid: border checkpoint, passport closeup, map, readable letter text.
```

## Prompt 4 - The Price of the Loaf

```text
Event: cp_layla.8 - "The Price of the Loaf"
Narrative function: tax is felt as missing bread before it is understood as policy.
Subject: Layla at the family table with Ahmed and children nearby.
Scene/backdrop: modest room, low table, clay wall, dim supper light.
Foreground action: Layla holds a loaf in both hands and senses that the weight is wrong.
Required object/gesture: smaller-than-expected loaf being torn into unequal pieces; Layla's hand measuring its weight.
Background detail: Ahmed watching quietly, children waiting, baker's paper or cloth without readable marks.
Lighting/mood: evening interior, hunger made ordinary, controlled anger.
Avoid: bakery display, famine tableau, comic oversized bread, modern currency.
```

## Prompt 5 - Mariam Writes from Cairo

```text
Event: cp_layla.128 - "Mariam Writes from Cairo"
Narrative function: a cousin's Cairo life enters the house through Nur reading a sentence aloud.
Subject: older Layla listening while Nur reads an unopened or newly opened letter on the mat.
Scene/backdrop: household room at lamplight, low mat, envelope, drawer, modest wall.
Foreground action: Nur reads slowly while Layla leans forward, asking for one sentence again.
Required object/gesture: letter and envelope between them, no readable text; Layla's hand lifted to pause Nur.
Background detail: faint Cairo keepsake or oud-shaped shadow suggested only through the letter, not as fantasy.
Lighting/mood: warm lamplight, curiosity, judgment withheld.
Avoid: Cairo salon scene, glamour portrait, readable handwriting, modern stationery.
```

## Prompt 6 - The Meeting After Shift

```text
Event: cp_layla.112 - "The Meeting After Shift"
Narrative function: a union list enters Layla's house and she notices the missing women.
Subject: Ahmed and Layla at the household step after a late mill meeting.
Scene/backdrop: night threshold, rough wall, low lamp, Ahmed's work clothes dusty from the mill.
Foreground action: Ahmed writes on the back of a folded list while Layla dictates calmly.
Required object/gesture: folded workers' list with no readable text; Ahmed's awkward writing hand; Layla's steady pointing hand.
Background detail: distant mill workers or lane shadows, kerosene lamp, bread piece set aside.
Lighting/mood: low kerosene light, practical courage, domestic politics.
Avoid: modern union hall, protest banner, readable slogans, triumphant rally.
```

## Prompt 7 - The Merchant's Scale

```text
Event: cp_layla.17 - "The Merchant's Scale"
Narrative function: betrayal is measured in the small difference between one onion and another weight.
Subject: Layla at a modest market stall watching a merchant's balance scale.
Scene/backdrop: village market by the well, baskets of onions, simple scale, dusty daylight.
Foreground action: Layla compares one onion on the merchant's scale with a small stone weight in her hand.
Required object/gesture: balance scale tilted slightly wrong; one onion; Layla's own small stone weight.
Background detail: Abu Hassan behind the stall, other merchant in the distance, well stones.
Lighting/mood: clear morning, suspicion kept quiet.
Avoid: modern shop scale, piles of luxury produce, accusation scene, readable prices.
```

## Prompt 8 - The Midwife's Lamp

```text
Event: cp_layla.28 - "The Midwife's Lamp"
Narrative function: the lane wakes at the moving lamp and understands that a woman has entered her hours.
Subject: Layla watching from behind slats or a doorway at night.
Scene/backdrop: narrow village lane after midnight, dark doors, mud-brick walls, one moving oil lamp.
Foreground action: the midwife's lamp pauses at another door while Layla remains inside, awake.
Required object/gesture: small oil lamp in Badr the midwife's hand; Layla's fingers near the window slats.
Background detail: door opening a crack, lane returning to darkness, no visible childbirth scene.
Lighting/mood: deep night, prayer, hush.
Avoid: birth-room interior, gore, supernatural glow, modern lantern.
```

## Prompt 9 - The Smoke Above the Palm

```text
Event: cp_layla.50 - "The Smoke Above the Palm"
Narrative function: the first textile mill makes the horizon larger and less certain.
Subject: Layla on a canal road, passing within sight of the new textile mill.
Scene/backdrop: Lower Egyptian canal path, palm tree in foreground, mill gate and chimney beyond fields.
Foreground action: Layla stops or slows while workers enter the mill gate at dawn or late afternoon.
Required object/gesture: straight column of chimney smoke above a palm; Layla's body turned toward the vibration.
Background detail: men in work clothes at the gate, cousin among them if visible, canal dust.
Lighting/mood: pale industrial morning, wonder mixed with worry.
Avoid: huge modern factory, steam-punk spectacle, Manchester skyline, empty scenic smoke.
```

## Prompt 10 - The Minaret's Silence

```text
Event: cp_layla.114 - "The Minaret's Silence"
Narrative function: state atheism is felt as the missing call and a prayer moved behind a door.
Subject: older Layla in a back room with a prayer rug while a silent minaret is glimpsed outside.
Scene/backdrop: modest house interior, half-closed door, small high window toward the minaret.
Foreground action: Layla lays out or folds a plain prayer rug in private.
Required object/gesture: prayer rug behind a closed or closing door; Layla's finger near her lips or the door latch.
Background detail: child watching from the doorway, minaret visible but distant through the window.
Lighting/mood: muted Friday light, secrecy, inherited memory.
Avoid: public mosque scene, confrontation with police, ornate religious pageantry, readable script.
```

## Prompt 11 - The Ministry Comes for the Stall

```text
Event: cp_layla.124 - "The Ministry Comes for the Stall"
Narrative function: command economy arrives as polite paperwork and the loss of the stall's tin.
Subject: older Layla at her food stall with a ministry man in a grey suit.
Scene/backdrop: modest market stall with cucumbers, tin cash box, clipboard, rough wooden counter.
Foreground action: Layla signs or refuses papers while the official gestures toward the cash tin.
Required object/gesture: tin cash box at the center; official papers with no readable text; Layla's pen or closed hand.
Background detail: cooperative clerk, familiar customer, market lane continuing around them.
Lighting/mood: daylight, arithmetic promise mixed with dispossession.
Avoid: Soviet poster style, modern bureaucracy, readable forms, villainous official.
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

When a generated candidate is accepted, wire it with a version suffix (`_v12`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.12-superseded/`.
