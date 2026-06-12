# Layla replacement image batch v0.7

Date: 2026-05-26

Purpose: replace the highest-impact active Layla legacy/no-source DDS images first. This batch is ranked by `script/audit-art-provenance.py --rank-missing`, prioritizing assets reused across many visible event windows and conversation branches. It also includes in-game observed blockers even when they sit just below the usage cutoff.

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
| 1 | `cp_layla_bey_eye_v07.dds` | 22 | Bey pressure, class conversation |
| 2 | `cp_layla_coptic_neighbour_v07.dds` | 18 | Um Yusuf / Coptic neighbor conversation |
| 3 | `cp_layla_mothers_hand_v07.dds` | 18 | Mother memory conversation |
| 4 | `cp_layla_not_on_deed_v07.dds` | 18 | Property-rights absence + paper conversation |
| 5 | `cp_layla_conversation_ahmed_v07.dds` | 13 | Ahmed at home / marriage conversation |
| 6 | `cp_layla_conversation_children_v07.dds` | 13 | Daughter / children conversation |
| 7 | `cp_layla_conversation_mill_v07.dds` | 9 | Factory/Ahmed mill conversation |
| 8 | `cp_layla_letter_not_come_v07.dds` | 5 | Ahmed-at-war letter absence |
| 9 | `cp_layla_mill_closed_v07.dds` | 5 | Mill closure crossroads |
| 10 | `cp_layla_strike_v07.dds` | 5 | Labor strike |
| 11 | `cp_layla_conversation_land_v07.dds` | 4 | Ruler audience / land petition |

## Prompt 1 - Bey's Eye

```text
Event: shared asset for cp_layla.12 and cp_layla_vox.61-65 - "Under the Bey's Eye"
Narrative function: class power sits in the room before anyone names it; Layla knows the landlord's attention has narrowed on her household.
Subject: Layla in her late twenties or thirties, village clothes faded indigo and brown, tense but not theatrical.
Scene/backdrop: Lower Egyptian village edge near a mud-brick storehouse and field gate, 1840s-1850s.
Foreground action: Layla stands half in shadow near a doorframe with her hand on a rough wooden latch.
Required object/gesture: the landlord's seal or folded notice on a small table, and Layla's hand gripping the latch.
Background detail: Hassan Bey al-Sayyid is visible at middle distance with a clerk, not dominant, watching from the field path.
Lighting/mood: hard late-afternoon light, quiet surveillance, pressure without spectacle.
Avoid: villain pose, courtly grandeur, empty desert, palace interior, modern legal paper.
```

## Prompt 2 - The Coptic Neighbor

```text
Event: shared asset for cp_layla.107 and cp_layla_vox.41-44 - "The Neighbor's Door"
Narrative function: ordinary coexistence becomes legible through borrowed care, bread, and a threshold conversation.
Subject: Layla in middle age beside Um Yusuf, a Coptic Egyptian neighbor woman, both practical and tired.
Scene/backdrop: narrow Cairo or Delta neighborhood lane with mud-plaster walls, modest wooden doors, and household vessels.
Foreground action: Layla receives a covered bowl or folded cloth from Um Yusuf at the threshold.
Required object/gesture: two women's hands meeting over the bowl, one hand marked by work, the other holding a small cross pendant mostly hidden by cloth.
Background detail: a child half-visible behind the door, laundry line, worn stone step.
Lighting/mood: soft morning side light, intimacy and caution, no sermon.
Avoid: church interior, religious pageantry, staged tolerance poster, modern street.
```

## Prompt 3 - Mother's Hand

```text
Event: shared asset for cp_layla.15 and cp_layla_vox.31-35 - "Her Mother's Hand"
Narrative function: Layla's choices are haunted by an older woman's remembered labor and silence.
Subject: young Layla in her early twenties seated beside her mother, who is older, weathered, and practical.
Scene/backdrop: dim village interior with reed roof, clay wall, low stool, and woven mat.
Foreground action: the mother's hand covers Layla's hand while a small household object waits between them.
Required object/gesture: interlocked hands beside a clay cup or folded scrap of cloth.
Background detail: open doorway showing a strip of field and irrigation water.
Lighting/mood: lamplight and doorway light mixed, tender but unsentimental.
Avoid: saintly mother pose, sickbed melodrama, decorative nostalgia.
```

## Prompt 4 - Not on the Deed

```text
Event: cp_layla.99 and cp_layla_vox.51-54 - "Her Name Is Not on the Deed"
Narrative function: the household's property is real in Layla's hands but absent from the official paper.
Subject: Layla in middle age, composed, with restrained anger in her posture.
Scene/backdrop: modest office or market-side scribe table in 19th-century Egypt; not a grand ministry.
Foreground action: a clerk holds or points to a deed while Layla looks at the blank space where her name should be.
Required object/gesture: deed with wax seal turned toward Layla; her fingers press the table edge.
Background detail: Ahmed or another male relative is partly visible, uncomfortable and secondary.
Lighting/mood: flat bureaucratic daylight, paper-cream and dusty wood, quiet exclusion.
Avoid: readable text, modern pen, courtroom drama, heroic protest.
```

## Prompt 5 - Conversation With Ahmed

```text
Event: shared asset for cp_layla_vox.12, .13, .16 and follow-ups - "Ahmed at Home"
Narrative function: marriage as ordinary negotiation: affection, fatigue, and money spoken under a low roof.
Subject: Layla and Ahmed in their late twenties or thirties; Ahmed is a Misri peasant husband with tired hands and a modest galabiyya.
Scene/backdrop: village room at night, reed roof, low table, clay lamp, folded work clothes.
Foreground action: Layla sits opposite Ahmed, both turned slightly toward a small lamp rather than toward the viewer.
Required object/gesture: Ahmed's hand with field dirt or mill oil near Layla's folded hand.
Background detail: sleeping mat, clay jar, open doorway into darkness.
Lighting/mood: warm lamplight, private conversation, tension softened by familiarity.
Avoid: romantic glamour, wedding scene, modern bed, theatrical embrace.
```

## Prompt 6 - Conversation With Children

```text
Event: shared asset for cp_layla_vox.21, .22, .25 and follow-ups - "Children at the Mat"
Narrative function: Layla measures the future through a child's question, hunger, or school lesson.
Subject: Layla in her thirties or forties with one child or young daughter; both Egyptian, plainly dressed.
Scene/backdrop: household interior opening onto a lane or field, 19th-century Egypt.
Foreground action: a child sits near Layla with a slate, scrap of paper, or small loaf.
Required object/gesture: child's hand holding a slate/loaf while Layla's hand hovers, unsure whether to correct or comfort.
Background detail: woven basket, low shelf, worn sandals near the door.
Lighting/mood: afternoon household light, protective worry, no sentimentality.
Avoid: classroom crowd, modern school supplies, smiling family portrait.
```

## Prompt 7 - Conversation at the Mill

```text
Event: shared asset for cp_layla_vox.14 and .71 - "Oil on the Shirt"
Narrative function: industrial work enters Layla's marriage as smell, risk, and wage, not as abstract progress.
Subject: Layla and Ahmed in middle age; Ahmed is a mill worker with oil-stained sleeves.
Scene/backdrop: outside a Cairo or Delta textile mill gate, 19th-century Egyptian industrial edge.
Foreground action: Ahmed shows Layla a stained cuff or small injury while workers pass behind them.
Required object/gesture: dark oil stain on cloth, Layla's fingers touching the edge of the sleeve.
Background detail: mill gate, smoke, cotton bundles, not a European factory fantasy.
Lighting/mood: smoky dusk, fatigue and calculation.
Avoid: modern machinery, heroic labor poster, huge anonymous crowd.
```

## Prompt 8 - The Letter That Has Not Come

```text
Event: cp_layla.10 and cp_layla_vox.11 - "The Letter That Has Not Come"
Narrative function: Ahmed's absence at war is felt through the empty place where a letter should be.
Subject: Layla in her twenties or thirties, waiting without theatrical grief.
Scene/backdrop: village threshold at evening, road visible beyond the door.
Foreground action: Layla sits with an unopened old letter or blank folded paper beside a clay lamp.
Required object/gesture: empty hand over folded paper; a shadowed road outside.
Background detail: Ahmed's unused sandals or work cloth near the wall.
Lighting/mood: blue evening and lamp warmth, restrained dread.
Avoid: battlefield, soldier spectacle, visible modern envelope text.
```

## Prompt 9 - The Mill Closes

```text
Event: cp_layla.73 and cp_layla_vox.73 - "The Mill Closes"
Narrative function: household strategy changes because a wage disappears.
Subject: Layla in middle age at the mill gate with Ahmed or another worker partly in frame.
Scene/backdrop: closed textile mill gate in Egypt, cotton dust, shuttered entrance, workers dispersing.
Foreground action: Layla studies a tied cloth bundle or wage token while the gate behind her is being shut.
Required object/gesture: locked gate or lowered bar; small bundle in Layla's hands.
Background detail: a foreman or guard in distance, smoke fading, workers not as a mob.
Lighting/mood: grey late afternoon, practical fear, no riot.
Avoid: modern factory signage, readable notices, dramatic fire, European city street.
```

## Prompt 10 - The Strike

```text
Event: cp_layla.113 and cp_layla_vox.75 - "The Strike"
Narrative function: labor politics becomes personal when the household recognizes its own risk in the crowd.
Subject: Layla in middle age near workers, not leading them as a hero.
Scene/backdrop: textile mill yard or street outside a mill in 19th-century Egypt.
Foreground action: Layla stands at the edge of gathered workers, holding a folded cloth or food bundle, watching Ahmed or a worker speak.
Required object/gesture: a worker's raised open hand, not a fist; Layla's bundle held tight.
Background detail: cotton bales, mill wall, soldiers or police only distant and ambiguous.
Lighting/mood: hot dusty daylight, tension before decision.
Avoid: banners with text, modern protest signs, revolutionary poster composition, battle scene.
```

## Prompt 11 - The Land Petition

```text
Event: cp_layla_vox.102 and follow-ups - "The Land"
Narrative function: Layla asks the ruler's imagined room to recognize land her family has worked for generations; the scene must feel like a private petition, not a triumph.
Subject: Layla in middle age, Egyptian/Misri fellah woman, practical dark headscarf and worn blue-grey dress, holding herself upright through fear.
Scene/backdrop: modest 19th-century Egyptian administrative room or provincial audience chamber, not a palace; woven carpet, plaster wall, wooden desk, clerk's table.
Foreground action: Layla stands at the end of a carpet holding a folded petition close to her chest.
Required object/gesture: folded paper in Layla's work-worn hands; a clerk's ledger or seal on a table farther away.
Background detail: a ruler or official is only suggested at distance by seated silhouette or shoulder, with a secretary nearby; Layla remains the emotional focus.
Lighting/mood: dusty side light, formal distance, quiet courage under class pressure.
Avoid: readable text, palace grandeur, fantasy harem costume, heroic victory pose, modern office, dramatic throne.
```

## Verification commands after generation

```bash
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-art-provenance.py --rank-missing --limit 20
script/audit-release-readiness.py --mode dev
```

When a generated candidate is accepted, wire it with a version suffix (`_v07`) and keep the superseded DDS under `image/archive/legacy-event-pictures/v0.7-superseded/`.
