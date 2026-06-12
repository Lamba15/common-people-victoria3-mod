# Layla replacement image batch v0.10

Date: 2026-05-26

Purpose: queue another story-critical slice of Layla's remaining legacy/no-source DDS images after v0.9. This batch covers single-window assets that still carry major emotional or thematic beats: household goods, Ahmed's return, slavery at the village edge, and several conversation-specific images that need concrete objects instead of generic mood.

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
| 1 | `cp_layla_cloth_v10.dds` | 1 | cloth from the port |
| 2 | `cp_layla_coffee_v10.dds` | 1 | first cup of coffee |
| 3 | `cp_layla_column_returns_v10.dds` | 1 | Ahmed homecoming |
| 4 | `cp_layla_compound_v10.dds` | 1 | compound on the village edge |
| 5 | `cp_layla_conversation_distance_v10.dds` | 1 | age in the water jar |
| 6 | `cp_layla_conversation_envelope_v10.dds` | 1 | man with official papers |
| 7 | `cp_layla_conversation_kitchen_v10.dds` | 1 | Qur'an on the shelf |
| 8 | `cp_layla_conversation_nile_v10.dds` | 1 | walking home alone |
| 9 | `cp_layla_conversation_school_v10.dds` | 1 | daughter reads aloud |
| 10 | `cp_layla_conversation_small_v10.dds` | 1 | nothing tonight |
| 11 | `cp_layla_conversation_stall_v10.dds` | 1 | traveler with news |

## Prompt 1 - The Cloth from the Port

```text
Event: cp_layla.35 - "The Cloth from the Port"
Narrative function: a new market good becomes a small permission Layla's mother never had.
Subject: Layla in middle age at a village merchant's stall, practical clothes and dark headscarf.
Scene/backdrop: modest Lower Egyptian market stall with folded bolts of cloth, baskets, and dust.
Foreground action: Layla touches a blue bolt of imported cloth with one careful finger.
Required object/gesture: vivid blue cloth bolt half-unrolled; Layla's work-worn hand testing the weave.
Background detail: merchant behind the stall, river-port bundle or crate suggested without readable labels.
Lighting/mood: clear market daylight, restrained desire and calculation.
Avoid: luxury boutique, fashion pose, readable shipping marks, modern textiles.
```

## Prompt 2 - The Cup of Coffee

```text
Event: cp_layla.33 - "The Cup of Coffee"
Narrative function: coffee becomes a private act of choice, not a luxury spectacle.
Subject: Layla in middle age seated alone near a small brazier after supper.
Scene/backdrop: modest village or Cairo room, clay wall, woven mat, low shelf, night at the doorway.
Foreground action: Layla pours or lifts a tiny cup of dark coffee, uncertain whether she likes it yet.
Required object/gesture: small coffee cup and a paper twist of grounds; Layla's hand paused before tasting.
Background detail: brazier, brass or clay pot, folded apron, quiet doorway.
Lighting/mood: warm lamplight, private curiosity, dry humor under fatigue.
Avoid: coffeehouse crowd, ornate tray, modern porcelain, glamorous leisure scene.
```

## Prompt 3 - The Column Returns

```text
Event: cp_layla.40 - "The Column Returns"
Narrative function: Ahmed comes home from war changed, and Layla recognizes him by small domestic habits.
Subject: Layla and Ahmed in middle age at the household threshold; Ahmed is dusty, thinner, not heroic.
Scene/backdrop: village doorway by the canal road, low wall, clay threshold, dust hanging in afternoon light.
Foreground action: Ahmed stands just outside the door before crossing; Layla sets down bread or a plate inside.
Required object/gesture: extra plate or bread placed on a low table; Ahmed's hand touching the doorframe.
Background detail: receding column of men on the road, donkey track, canal dust.
Lighting/mood: late afternoon, relief complicated by distance.
Avoid: battlefield return, parade, military glory, theatrical embrace.
```

## Prompt 4 - The Compound on the Edge

```text
Event: cp_layla.104 - "The Compound on the Edge of the Village"
Narrative function: Layla notices the nearby wall and understands that her own hardship is not the bottom of the world.
Subject: Layla carrying water past a high mud-plaster wall, older but still working.
Scene/backdrop: village edge in 19th-century Egypt, irrigation path, compound wall, water jar.
Foreground action: Layla walks without slowing, but her eyes turn briefly toward the wall.
Required object/gesture: water jar balanced or gripped; high plastered wall with a narrow shadowed opening.
Background detail: a faint human silhouette behind the wall, not staged as spectacle.
Lighting/mood: hard daylight, moral discomfort, ordinary horror kept at the edge.
Avoid: prison scene, exposed violence, plantation imagery, heroic rescue composition.
```

## Prompt 5 - Her Face in the Water

```text
Event: cp_layla_vox.94 - "Her Face in the Surface of the Water"
Narrative function: Layla sees age in a water jar and accepts the face without turning it into a sermon.
Subject: older Layla leaning over a large clay water jar.
Scene/backdrop: quiet household room or courtyard corner, low evening light, clay wall.
Foreground action: Layla scoops water while her reflected face breaks on the surface.
Required object/gesture: water reflection in a clay jar; cup in Layla's hand.
Background detail: flour dust on a shelf, hanging cloth, small stool.
Lighting/mood: cool dusk, self-recognition, calm without sentimentality.
Avoid: mirror vanity scene, magical reflection, modern basin, glamour portrait.
```

## Prompt 6 - A Man with Papers

```text
Event: cp_layla_vox.86 - "A Man with a Clipboard"
Narrative function: the state arrives at Layla's door as a polite man, a stamp, and a pencil.
Subject: Layla at her doorway facing a district-office man with papers.
Scene/backdrop: modest threshold in a Cairo or Delta lane, plaster wall, household shadows behind her.
Foreground action: the man holds a clipboard or board toward Layla while she keeps one hand on the door.
Required object/gesture: official paper with stamp but no readable text; pencil poised above the page.
Background detail: children or neighbor partly visible behind Layla, water jar by the wall.
Lighting/mood: formal daylight, caution, bureaucratic pressure.
Avoid: modern clipboard hardware, readable forms, police raid, comic official.
```

## Prompt 7 - The Book on the Shelf

```text
Event: cp_layla_vox.91 - "The Book on the Shelf"
Narrative function: Layla's prayer is not recitation but touching the wrapped Qur'an she cannot read.
Subject: Layla in middle age standing on a low stool or reaching toward a high shelf.
Scene/backdrop: dim household room, high shelf, clay wall, wrapped book, lamplight.
Foreground action: Layla holds the wrapped Qur'an against her forehead for one breath.
Required object/gesture: cloth-wrapped book; Layla's forehead and hands touching the cloth reverently.
Background detail: small stool, oil lamp, quiet household objects below.
Lighting/mood: warm low light, private devotion, no pageantry.
Avoid: mosque interior, readable scripture, saintly halo, ornate religious tableau.
```

## Prompt 8 - Walking Home Alone

```text
Event: cp_layla_vox.95 - "Walking Home Alone"
Narrative function: Layla has a minute in which she is not wife, mother, or worker, only herself walking home.
Subject: Layla in later middle age walking alone from the field at dusk.
Scene/backdrop: Delta path between fields and canal, village low in the distance, apricot sky.
Foreground action: Layla walks with empty hands swinging naturally, head slightly lifted.
Required object/gesture: her solitary walking posture; field path worn by repeated use.
Background detail: Ahmed and donkey far ahead as small silhouettes, bird crossing the sky.
Lighting/mood: dusk, earned solitude, quiet joy.
Avoid: romantic landscape, pilgrimage scene, empty scenic panorama without Layla.
```

## Prompt 9 - She Reads to Me

```text
Event: cp_layla_vox.23 - "She Reads to Me"
Narrative function: the daughter's reading changes the house before Layla fully understands the words.
Subject: Layla in middle age listening to her daughter Nur read aloud.
Scene/backdrop: household room at lamplight, low table, woven mat, clay wall.
Foreground action: Nur holds a thin school book while Layla watches her hands, half pretending to follow.
Required object/gesture: small book in the daughter's hands; Layla's hands still and folded in her lap.
Background detail: lamp, low shelf, doorway curtain, no modern school objects.
Lighting/mood: bright lamp in a dark room, pride hidden under humility.
Avoid: classroom, readable book text, smiling campaign poster, modern printed colors.
```

## Prompt 10 - Nothing Tonight

```text
Event: cp_layla_vox.99 - "Nothing Tonight"
Narrative function: an empty night is allowed to be enough.
Subject: older Layla sitting with her hands on her knees near a low lamp.
Scene/backdrop: very modest room at night, woven mat, clay wall, lamp almost spent.
Foreground action: Layla sits quietly, neither praying nor working, looking at a small moth by the lamp.
Required object/gesture: low lamp with a small brown moth nearby; Layla's hands resting still.
Background detail: folded work cloth, dark doorway, tomorrow's tools left in place.
Lighting/mood: low amber light, rest, silence.
Avoid: dramatic loneliness, ghostly atmosphere, decorative still life without Layla.
```

## Prompt 11 - A Traveler with News

```text
Event: cp_layla_vox.82 - "A Traveler with News"
Narrative function: distant violence enters the market through gossip while ordinary buying continues.
Subject: Layla at a market stall with a cloth-seller and a traveler speaking too loudly.
Scene/backdrop: Egyptian market lane, cloth stall, baskets, dust, a few listeners.
Foreground action: the traveler gestures with one hand while the cloth-seller tries to keep measuring fabric.
Required object/gesture: measuring cord or folded cloth in the seller's hands; Layla's basket held close.
Background detail: port bundle or cotton sack suggesting news from Alexandria, no readable labels.
Lighting/mood: busy daylight with unease threading through it.
Avoid: newspaper scene, modern port, brawl on screen, crowd panic.
```

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-provenance.py --rank-missing --limit 120
script/audit-release-readiness.py --mode dev
```

When a generated candidate is accepted, wire it with a version suffix (`_v10`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.10-superseded/`.
