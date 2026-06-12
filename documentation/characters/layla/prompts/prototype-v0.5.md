# Layla v0.5 prototype image prompts

Use these six prompts before any bulk regeneration. They follow `documentation/art-bible-v0.5.md` and intentionally save as `_v05` candidates so existing shipped DDS files are not overwritten.

Shared references:

- Face reference: `/home/aboelsoud/Pictures/common-people-mod-images/Layla/layla.png`
- Current style reference, only for continuity: `/home/aboelsoud/Pictures/common-people-mod-images/Layla/cp_layla_homesteading.dds.png`
- Candidate output folder: `/home/aboelsoud/Pictures/common-people-mod-images/Layla/`

Generated candidate set, 2026-05-25:

- Workspace review sheet: `image/generated/layla/v0.5/contact-sheet.png`
- Workspace 600x400 PNG candidates: `image/generated/layla/v0.5/*_v05.dds.png`
- Workspace 1536x1024 archives: `image/generated/layla/v0.5/*_v05_1536.png`
- Asset-library 600x400 PNG candidates: `/home/aboelsoud/Pictures/common-people-mod-images/Layla/*_v05.dds.png`
- Asset-library 1536x1024 archives: `/home/aboelsoud/Pictures/common-people-mod-images/Layla/*_v05_1536.png`

Initial visual QA: all six candidates keep the requested 3:2 event frame, show a clear story object or gesture, avoid visible text/UI/watermarks, and remain readable after downscale to 600x400. The first promotion pass should wire them as `_v05` DDS files for in-game A/B review before replacing the shipped legacy names.

## cp_layla.1 - The Farmer's Daughter

Output candidate: `cp_layla_intro_v05.dds.png`

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: cp_layla.1 - "The Farmer's Daughter"
Narrative function: establish Layla, the Nile Delta village, and the private scale of the story before politics touches her.
Subject: Layla al-Sharif, Egyptian/Misri fellah woman, 22 years old, oval face, heavy brows, dark eyes, black hair under a faded indigo headscarf, sun-warmed olive-brown skin, work-worn hands.
Scene/backdrop: threshold of a mud-brick house in a Lower Egyptian village before dawn; irrigation channel and palms in the hazy distance; a donkey asleep in the lane.
Foreground action: Layla stands half inside and half outside the doorway, one hand on the rough wooden jamb, looking toward the first light rather than at the viewer.
Required object/gesture: her hand on the doorframe, fingers cracked and dusty, holding the threshold.
Composition/framing: medium-wide, Layla foreground left, village lane and Nile light opening to the right; quiet negative space for the morning.
Lighting/mood: pomegranate pre-dawn sky, low blue and coral light, stillness before labor.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials.
Constraints: no text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no heroic pose.
Avoid: generic desert scene, palace grandeur, decorative atmosphere without the doorway gesture.
```

## cp_layla.2 - The Deed

Output candidate: `cp_layla_homesteading_v05.dds.png`

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: cp_layla.2 - "The Deed"
Narrative function: Layla receives a paper deed that says the land she works is hers.
Subject: Layla al-Sharif, late twenties, same Egyptian/Misri face and practical village clothes, older than the intro by a few hard years.
Scene/backdrop: edge of a green field in Lower Egypt, village houses behind her, the bey's estate far away and visually small.
Foreground action: Layla holds a folded deed paper in both hands and stares at it because she cannot read it but understands its weight.
Required object/gesture: paper deed with red wax seal centered between her rough hands; the seal must be visible but not contain legible text.
Composition/framing: close-medium, hands and deed in the lower center, Layla's face above them, field behind.
Lighting/mood: early morning light breaking through dust, quiet gravity rather than celebration.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials.
Constraints: no readable text, no UI, no border, no watermark, no modern paper, no fantasy costume, no heroic pose.
Avoid: smiling triumph, crowd parade, palace office, generic certificate shot.
```

## cp_layla.4 - He Marches

Output candidate: `cp_layla_ahmed_conscripted_v05.dds.png`

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: cp_layla.4 - "He Marches"
Narrative function: Ahmed is taken with other village men before they are soldiers in their own minds.
Subject: Layla al-Sharif in her late twenties or early thirties; Ahmed is a wiry Egyptian fellah man in simple grey galabiya, carrying a small bundle.
Scene/backdrop: village edge, dirt road leaving through fields, low mud wall, dusty morning.
Foreground action: Layla stands at the wall with one hand at her throat while Ahmed walks away in a loose column of conscripted fellahin.
Required object/gesture: Ahmed's head turned back once from the middle distance; Layla's hand at her throat.
Composition/framing: medium-wide, Layla foreground left, departing men receding diagonally into dust on the right.
Lighting/mood: flat mid-morning light, dust in the air, restraint and dread without spectacle.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials.
Constraints: no text, no UI, no border, no watermark, no modern uniform, no battlefield, no heroic military pose.
Avoid: battle scene, flags, explosions, cavalry drama, clean parade uniforms.
```

## cp_layla.41 - The Clerk's Letter

Output candidate: `cp_layla_clerks_letter_v05.dds.png`

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: cp_layla.41 - "The Clerk's Letter"
Narrative function: the state tells Layla that Ahmed has died, and the news arrives as paperwork.
Subject: Layla al-Sharif, early thirties, Egyptian/Misri fellah woman, face still composed because grief has not yet reached the body.
Scene/backdrop: village lane outside her mud-brick doorway; a minor clerk on a donkey or small mule, ledger open; several women watching from a respectful distance.
Foreground action: Layla stands in the doorway while the clerk reads from the ledger, not yet weeping.
Required object/gesture: the open ledger angled toward the viewer, and Layla's hand gripping the doorframe.
Composition/framing: medium-wide, clerk middle right, Layla foreground left in doorway shadow, watchers behind.
Lighting/mood: hard late-morning sun in the lane, cool shade on Layla's face; news delivered like a parcel.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials.
Constraints: no readable text, no UI, no border, no watermark, no modern document, no theatrical grief.
Avoid: battlefield death, coffin, dramatic tears, palace official, military honor scene.
```

## cp_layla.80 - The Last Morning

Output candidate: `cp_layla_last_morning_v05.dds.png`

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: cp_layla.80 - "The Last Morning"
Narrative function: elderly Layla reaches the end of her life in a room that still contains the work of it.
Subject: Layla al-Sharif in her seventies or eighties, clearly the same woman aged: lined face, grey hair under a loose scarf, thin hands, calm exhaustion.
Scene/backdrop: small spare mud-brick room, low bed, clay water jug on a stool, folded cloth, open window to a quiet courtyard.
Foreground action: Layla lies on the low bed with one hand open on the blanket; she is still, not posed.
Required object/gesture: open resting hand on the blanket, with morning light crossing it.
Composition/framing: close-medium, bed low in frame, window light diagonally across Layla, room uncluttered.
Lighting/mood: warm pale morning light, absolute quiet, the day going on without asking for her.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials.
Constraints: no text, no UI, no border, no watermark, no modern bed, no angelic imagery, no melodrama.
Avoid: funeral scene, family crowd, glowing supernatural light, romantic deathbed cliche.
```

## cp_layla_vox.100 - A Word Between

Output candidate: `cp_layla_conversation_audience_v05.dds.png`

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: cp_layla_vox.100 - "A Word Between"
Narrative function: conversation mode becomes Layla's imagined audience with the country that governs her.
Subject: Layla al-Sharif in late middle age, same Egyptian/Misri identity, seated but alert; no ruler or grand official in frame.
Scene/backdrop: plain interior with a low table, oil lamp, folded papers, and an empty chair opposite her; the empty chair represents the absent state.
Foreground action: Layla sits with both hands on the table edge as if preparing to speak to someone who is not there.
Required object/gesture: the empty chair across from Layla, and her hands steadying themselves on the table.
Composition/framing: medium interior shot, Layla left of center, empty chair right of center, lamp between them.
Lighting/mood: lamplight, intimate and slightly unreal, not fantasy; the room is ordinary but the silence is formal.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials.
Constraints: no text, no UI, no border, no watermark, no palace, no throne, no literal personification of the country.
Avoid: courtroom, parliament, king, mystical apparition, decorative empty room with no table gesture.
```
