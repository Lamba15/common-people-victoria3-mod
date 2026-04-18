# Layla event image prompts

Every event image for Layla is generated via [Codex CLI](../../../image-generation-workflow.md) using a shared template. The template expects two reference images (canonical face, canonical style) and injects four per-event fields: **title**, **context**, **scene**, **mood**.

The runnable script is `script/gen-layla-event-images.sh` — that's the source of truth. This file documents the per-event fields in a human-readable form so they can be edited without diving into bash.

After generation: `script/convert-images-to-dds.sh` converts PNG → DDS and stages `mod/gfx/event_pictures/cp_layla_*.dds`.

---

## Shared references (all events)

- **Face reference**: `~/Pictures/common-people-mod-images/Layla/layla.png`
- **Style reference**: `~/Pictures/common-people-mod-images/Layla/cp_layla_homesteading.dds.png`
- **Mahfouz register**: quiet, specific, sensory, subtext. Not heroic. Not celebratory. Not tragic in a performed way. The image says what a witness would say, not what a narrator would.
- **Palette**: ochre, sienna, cream, the occasional deep red (wax seal, pomegranate sky). Warm. Painted-canvas texture. 19th-century genre painting register, not concept art.
- **Aspect**: 3:2 landscape, target 600×400.

---

## 1. cp_layla.1 — "The Farmer's Daughter" (intro)

- **Output**: `cp_layla_intro.dds.png`
- **Context**: Layla rises before dawn in her Lower Egyptian village; she stands on the threshold of her mud-brick house and waits for the light.
- **Scene**: Layla stands on the threshold of a low mud-brick house at the edge of a Lower Egyptian fellah village. She wears a faded headscarf and a long dark dress. Behind her the Nile is a thin silver line in the middle distance. The sky is the color of the inside of a pomegranate — pre-dawn, deep coral and indigo bands. A donkey is asleep in the lane. She is alone in frame, three-quarter view, looking out toward the river. No other people visible.
- **Mood**: Quiet anticipation. The stillness before a long day. The beginning of a long story.

## 2. cp_layla.2 — "The Deed" (homesteading)

- **Output**: `cp_layla_homesteading_v2.dds.png`
- **Context**: Egypt has just enacted homesteading; Layla receives a deed paper that says this patch of earth belongs to her.
- **Scene**: Layla stands in the middle of her own field, holding a folded deed paper sealed with a deep red wax seal. Her hands tremble visibly; she has never held a paper of her own before. Bright morning light. Behind her is a fellah field of green wheat or cotton, the village in the far distance. She looks at the paper, not at the camera. Three-quarter close-medium shot. Just her in frame.
- **Mood**: Quiet gravity, not celebration. The weight of a thing she did not believe could happen.

## 3. cp_layla.3 — "The Bey Returns" (serfdom restored)

- **Output**: `cp_layla_serfdom_restored.dds.png`
- **Context**: A regime change has restored serfdom; the bey rides through the village again and Layla and Ahmed back against the wall of their house.
- **Scene**: Layla and her husband Ahmed (a wiry Misri man in his late twenties, simple grey gallabiya) press their backs against the mud-brick wall of their house in the village lane. In the middle distance, a mounted Ottoman-Egyptian bey on a dark horse rides through the lane; dust rising from hooves; a bey servant on foot beside him. Doors of nearby houses are shut. Late afternoon light, harsh and angled. Layla holds Ahmed's wrist. Her face is composed but her eyes are wide. Wide cinematic composition; the bey is small in frame but central; Layla and Ahmed in the foreground left.
- **Mood**: Fear that has learned to be silent. The worst day, made of quiet.

## 4. cp_layla.4 — "He Marches" (Ahmed conscripted)

- **Output**: `cp_layla_ahmed_conscripted.dds.png`
- **Context**: War has started; Ahmed has been conscripted; he walks away in a column of village conscripts and Layla watches from the village edge.
- **Scene**: Layla stands at the edge of the village beside a low mud wall, watching a column of newly-conscripted Egyptian fellahin walking away down a dirt track raising dust. Ahmed is among them, recognizable by his grey gallabiya, looking back over his shoulder once. He carries a small bundle. The men are not in uniform yet — they are villagers, marched off to be made soldiers. Other women and children stand farther down the wall, also watching. Mid-morning light. The column is in the middle distance moving away from the camera. Layla in the foreground left, her hand at her throat, no tears.
- **Mood**: The worst kind of leaving — the kind that pretends, for the watcher's sake, that he will be back.

## 5. cp_layla.5 — "The First Cry" (childbirth)

- **Output**: `cp_layla_childbirth.dds.png`
- **Context**: Layla has survived childbirth; she holds her newborn for the first time in candlelight.
- **Scene**: Layla sits propped against pillows on a low bed in a small mud-brick room, holding a swaddled newborn in her arms. A single oil lamp on a wooden chest provides almost all the light. Her hair is undone and damp at the temples; she is exhausted, her face shining with sweat. The midwife (an older Misri woman) stands at the foot of the bed in shadow, drying her hands on a cloth. Ahmed kneels beside the bed, his hand on Layla's shoulder. Layla looks down at the baby, not at Ahmed. Warm amber lamplight, deep shadows in the corners of the room. Close-medium shot, Layla and the baby centered.
- **Mood**: Exhausted reverence. The small private miracle of having survived, and a child having survived.

---

## Slice-of-life dispatch pool (fired by "Check on Layla" button)

## 13. cp_layla.13 — "A Day With No Wind"

- **Output**: `cp_layla_no_wind.dds.png`
- **Trigger**: always available
- **Context**: A windless, heavy morning in the Delta; Layla grinds dhurra in her mud-brick courtyard, praying quietly while she works.
- **Scene**: Layla crouches beside a low stone grinding-bowl in the packed-earth courtyard of her mud-brick house. Her hands rest on the upper grinding stone; a small pile of dhurra grain is beside her on a shallow tray. The air is heavy and still — dust hangs motionless in the air, catching the light. A neighbour's lean cat walks along the top of the mud courtyard wall in the middle distance, stepping slowly. Two hens stand quietly, not scratching. The palm-frond roof of the house is visible at the top of frame, perfectly still. Her lips are slightly parted — she is silently praying while she works. Three-quarter view, looking down at the stone, not at the camera. Mid-morning light, diffuse and warm, no harsh shadows. No wind in the palms.
- **Mood**: The stillness of a windless Delta morning. Quiet prayer without expectation.

## 14. cp_layla.14 — "The Neighbour's Boy in the Lane"

- **Output**: `cp_layla_neighbours_boy.dds.png`
- **Trigger**: always available
- **Context**: A small boy cries alone in the dust of the village lane; Layla, hands still floured from dough, steps to the doorway so he can see a face.
- **Scene**: Layla stands just inside the doorway of her mud-brick house, one hand on the wooden doorframe. Her hands are dusted white with flour from dough she has left inside on the flat stone. In the middle distance of the narrow village lane, a small boy (about three years old, simple grey gallabiya, bare feet) sits in the dust of the lane crying, his face turned up toward Layla's doorway. His mother is not in frame. Other house doors along the lane are shut. Late morning light, harsh sun on the dust of the lane, but Layla's doorway is in deep cool shadow. Layla's face is not comforting or smiling — it is steady, present, witnessing. Her body is still; she does not step out into the lane. The viewer sees both figures in the same frame: Layla in shadow in the foreground left, the boy in sunlight in the middle distance.
- **Mood**: The restraint of being a good neighbour. Presence as a form of care. Being seen as enough.

## 15. cp_layla.15 — "Her Mother's Left Hand"

- **Output**: `cp_layla_mothers_hand.dds.png`
- **Trigger**: always available
- **Context**: Layla notices, mid-meal, that she has begun to reach for bread with her left hand — the way her dead mother always did.
- **Scene**: Close-medium interior shot of Layla sitting cross-legged on a worn woven mat inside her mud-brick house. A low wooden tray in front of her holds a small broken piece of aish baladi (flat Egyptian bread) and a shallow clay bowl of ful medames (brown stewed beans). Layla is in the middle of lifting a piece of the bread toward her mouth with her LEFT hand — this left-handedness is the single most important visual detail and must read clearly. Her right hand is busy in her lap, adjusting a seam of her headscarf. Her gaze is distant, not at the food, not at the camera — somewhere inward. The light is soft, single-source, from a wooden-lattice window off-frame right, casting a patterned shadow on the packed-earth floor. A single hen stands at the edge of the mat in the background, incurious. The interior is spare: a clay water-jar in one corner, a low wooden chest against the far wall. Palette is warm ochre, cream, the deep brown of the bread.
- **Mood**: The private grief of noticing you have become your mother. Inheritance as gesture, not story.

---

## After wiring new DDS into the mod

Three of the new slice-of-life events (.13, .14, .15) currently reuse `cp_layla_intro.dds` as a placeholder in `mod/events/cp_layla_events.txt`. Once the three new PNGs have been generated and DDS-converted, update the `event_image = { texture = ... }` line in each:

| Event | Current placeholder | Target DDS |
|---|---|---|
| cp_layla.13 | `cp_layla_intro.dds` | `cp_layla_no_wind.dds` |
| cp_layla.14 | `cp_layla_intro.dds` | `cp_layla_neighbours_boy.dds` |
| cp_layla.15 | `cp_layla_intro.dds` | `cp_layla_mothers_hand.dds` |
