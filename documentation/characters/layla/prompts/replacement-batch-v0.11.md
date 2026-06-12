# Layla replacement image batch v0.11

Date: 2026-05-26

Purpose: queue the next single-window slice of Layla's remaining legacy/no-source DDS images after v0.10. This batch focuses on grounded domestic, bureaucratic, religious, labor, and market scenes where the old art still reads as placeholder or generic mood instead of the exact event beat.

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
| 1 | `cp_layla_dates_v11.dds` | 1 | date harvest |
| 2 | `cp_layla_district_office_v11.dds` | 1 | real audience / district office |
| 3 | `cp_layla_dust_on_water_v11.dds` | 1 | khamaseen and cistern |
| 4 | `cp_layla_every_man_v11.dds` | 1 | universal male suffrage decree |
| 5 | `cp_layla_factory_field_v11.dds` | 1 | market eats village / factory field |
| 6 | `cp_layla_first_envelope_v11.dds` | 1 | first welfare envelope |
| 7 | `cp_layla_forty_days_v11.dds` | 1 | forty-day mourning coda |
| 8 | `cp_layla_guard_v11.dds` | 1 | machine guard installed |
| 9 | `cp_layla_hajj_v11.dds` | 1 | Hajj returnees |
| 10 | `cp_layla_hen_v11.dds` | 1 | hen that will not lay |
| 11 | `cp_layla_imam_visit_v11.dds` | 1 | imam's visit |

## Prompt 1 - The Date Harvest

```text
Event: cp_layla.29 - "The Date Harvest"
Narrative function: an ordinary village harvest becomes a measure of work, sharing, and seasonal order.
Subject: Layla in young or middle adulthood among village women sorting dates.
Scene/backdrop: Delta courtyard with palm fronds, low mud-brick walls, woven trays, and date palms above.
Foreground action: women sort dates by hand while boys are visible high in the palms or climbing down.
Required object/gesture: Layla's hands separating dates on a wide tray; a small pile of bruised dates set aside.
Background detail: palm climber with rope, baskets, sunlit courtyard dust.
Lighting/mood: late afternoon gold, busy concentration, no festival spectacle.
Avoid: exotic market fantasy, palace garden, glossy fruit still life, readable signs.
```

## Prompt 2 - The District Office

```text
Event: cp_layla.125 - "The District Office"
Narrative function: the real audience with power shrinks into waiting, paper, and a tired clerk.
Subject: older Layla seated on a hard wooden bench in a provincial district office.
Scene/backdrop: plain government room in Lower Egypt, cracked plaster, wooden desk, inkstand, shuttered window.
Foreground action: Layla holds a folded paper in both hands while a clerk writes without looking up.
Required object/gesture: folded petition paper creased from being carried; Layla's feet planted under the bench.
Background detail: other petitioners waiting, stack of ledgers, dust in window light.
Lighting/mood: flat bureaucratic daylight, endurance, humiliation kept quiet.
Avoid: grand ministry, courtroom, modern office furniture, readable documents.
```

## Prompt 3 - Dust on the Water

```text
Event: cp_layla.21 - "Dust on the Water"
Narrative function: khamaseen weather turns household water into labor and foreboding.
Subject: Layla in early or middle adulthood at the courtyard cistern.
Scene/backdrop: modest courtyard under a yellow dust sky, clay cistern, broom, covered jars.
Foreground action: Layla bends to lift or secure the cistern lid while dust gathers on the water surface.
Required object/gesture: cistern lid, visible dusty water edge, Layla's hand wiping grit from the rim.
Background detail: laundry pulled down from a line, palm fronds blurred by wind, hen sheltering near a wall.
Lighting/mood: hot ocher haze, dryness, practical urgency.
Avoid: sandstorm disaster scene, desert dunes, magical atmosphere, modern water pump.
```

## Prompt 4 - Every Man, They Say

```text
Event: cp_layla.105 - "Every Man, They Say"
Narrative function: universal male suffrage reaches the square while Layla notices who is still outside the sentence.
Subject: Layla at the edge of a village square while men listen to a decree.
Scene/backdrop: village square or market corner, mosque wall or municipal doorway, small crowd of men.
Foreground action: an official or literate man reads from a paper; Layla stands half in shadow at the side.
Required object/gesture: decree paper held high but unreadable; Layla's basket held tight against her hip.
Background detail: men exchanging looks, one boy craning to hear, dusty ground.
Lighting/mood: bright public daylight, political gravity, exclusion without melodrama.
Avoid: ballot box focus, campaign poster, crowd celebration, readable decree text.
```

## Prompt 5 - The Market Eats the Village

```text
Event: cp_layla.123 - "The Market Eats the Village"
Narrative function: foreign capital and factory expansion turn familiar fields into a new economic edge.
Subject: older Layla near her stall or field boundary watching workmen mark land.
Scene/backdrop: village edge with field rows, a new fence line, factory chimney or railway siding in distance.
Foreground action: Layla stands beside a small stall or basket while laborers drive stakes into the field.
Required object/gesture: wooden survey stakes and string crossing cultivated soil; Layla's hand resting on a basket.
Background detail: distant factory wall, cart, rail sleepers, smoke kept small but unmistakable.
Lighting/mood: hard afternoon, opportunity mixed with loss.
Avoid: modern industrial skyline, heroic factory progress, colonial flag, empty landscape.
```

## Prompt 6 - The First Envelope

```text
Event: cp_layla.90 - "The First Envelope"
Narrative function: welfare arrives as a plain envelope that changes the way the state feels in the hand.
Subject: older Layla at home receiving or opening a small official envelope.
Scene/backdrop: modest room or doorway, low table, bread, folded cloth, worn wall.
Foreground action: Layla holds the envelope carefully while a clerk, neighbor, or Ahmed watches from nearby.
Required object/gesture: small sealed envelope with no readable writing; Layla's thumb under the flap.
Background detail: bread woman at threshold or ledger man receding, clay cup, household shadows.
Lighting/mood: soft morning light, disbelief, cautious relief.
Avoid: cash display, modern welfare office, celebratory pose, readable stamps.
```

## Prompt 7 - The Forty Days

```text
Event: cp_layla.83 - "The Forty Days"
Narrative function: mourning becomes household continuity through bread, paper, and objects left in place.
Subject: Nur and an older neighbor in Layla's house after Layla's death; Layla is absent.
Scene/backdrop: quiet room with low shelf, mat, doorway light, mourning bread on a tray.
Foreground action: Nur writes or folds a letter while Um Yusuf sets mourning bread nearby.
Required object/gesture: Ahmed's tobacco tin and the deed visible on a shelf or low table.
Background detail: covered bowl, plain cushion, muted doorway where visitors have come and gone.
Lighting/mood: dim afternoon, grief held by routine.
Avoid: corpse or funeral scene, melodramatic weeping, mosque interior, ghost image of Layla.
```

## Prompt 8 - The Guard Has Been Installed

```text
Event: cp_layla.111 - "The Guard Has Been Installed"
Narrative function: worker protection is understood through Ahmed's hands coming home intact.
Subject: Ahmed near a mill machine with Layla or another worker nearby; keep Layla present but not central if needed.
Scene/backdrop: small 19th-century mill or workshop, belts and gears, dusty light, rough floor.
Foreground action: Ahmed shows or rests his hands near a newly fitted iron machine guard.
Required object/gesture: simple iron guard over moving parts; Ahmed's hands visible and uninjured.
Background detail: foreman or worker in shadow, grain sacks, shaft of mill light.
Lighting/mood: industrial interior, relief without triumph.
Avoid: modern factory safety rail, sparks and spectacle, clean steel plant, injured gore.
```

## Prompt 9 - The Hajj Returnees

```text
Event: cp_layla.27 - "The Hajj Returnees"
Narrative function: distant holiness enters the lane as dates shared at a threshold.
Subject: Layla at her doorway receiving a date from a returned pilgrim cousin.
Scene/backdrop: village lane, low houses, neighbors gathered with restraint, travel dust on clothing.
Foreground action: a returned pilgrim extends a single date while Layla receives it with both hands.
Required object/gesture: one date in the palm between them; Layla's threshold clearly visible.
Background detail: small bundle, water skin, neighbor women watching, no grand caravan.
Lighting/mood: warm daylight, reverence made domestic.
Avoid: Mecca scene, religious pageantry, crowd spectacle, readable amulets or banners.
```

## Prompt 10 - The Hen That Will Not Lay

```text
Event: cp_layla.16 - "The Hen That Will Not Lay"
Narrative function: scarcity is measured through an old hen and the mercy of one more day.
Subject: Layla in the courtyard crouching near an old red hen.
Scene/backdrop: modest household courtyard with clay wall, grinding stone, small feed dish, straw.
Foreground action: Layla watches the hen and keeps her hand still instead of reaching for it.
Required object/gesture: old red hen near an empty nesting place; Layla's hand holding a little grain.
Background detail: flour stone, low door, two other hens farther back.
Lighting/mood: quiet morning, dry humor, tenderness under hunger.
Avoid: cute animal portrait, farm abundance, dramatic slaughter implication, modern coop.
```

## Prompt 11 - The Imam's Visit

```text
Event: cp_layla.126 - "The Imam's Visit"
Narrative function: Sheikh Abdallah's visit brings dignity without preaching or spectacle.
Subject: older Layla receiving the village imam in her modest room.
Scene/backdrop: household interior, second-best cushion, tea tray, low shelf, clean swept floor.
Foreground action: the imam sits respectfully while Layla pours tea or sets a cup between them.
Required object/gesture: second-best cushion under the guest; small tea glass or clay cup offered by Layla.
Background detail: doorway curtain, plain prayer beads at the imam's hand, household objects kept neat.
Lighting/mood: warm indoor afternoon, quiet honor, the visit feels like a kindness.
Avoid: mosque sermon, ornate clerical costume, saintly glow, crowd around them.
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

When a generated candidate is accepted, wire it with a version suffix (`_v11`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.11-superseded/`.
