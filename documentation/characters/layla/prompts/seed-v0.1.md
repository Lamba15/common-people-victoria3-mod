# Layla visual seed prompts v0.1

Purpose: canonical GPT-image-2 still/portrait direction for Layla. Her live art has many promoted event stills; this seed file makes the same shared portrait/scene pipeline cover her instead of leaving her as an exception.

## Identity

- Token: `layla`
- Age range: early twenties through elderhood
- Culture/religion: Misri Sunni
- Work: Delta fellaha, household worker, later landowner or laborer depending on play
- Visual anchors: patched headscarf, mud-brick threshold, folded land paper, grinding stone, canal dust
- Palette: Nile silt brown, faded indigo, pomegranate dawn, paper cream, brass lamp
- Avoid: palace fantasy, glamour portrait, tourist postcard, generic desert woman, readable text

## Canonical Portrait

```text
Use case: historical-scene
Asset type: Common People canonical character portrait, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism portrait-scene for Layla al-Sharif in the Common People Victoria 3 mod.
Subject: Layla al-Sharif, Misri Egyptian Sunni fellaha in her early twenties, olive-brown skin, dark tired eyes, plain earth-toned galabeya, patched muted headscarf wrapped for field work, work-worn hands, quiet posture.
Scene/backdrop: mud-brick house threshold in a Lower Egyptian Delta village, low roof patched with palm fronds, canal light and fields beyond the doorway.
Foreground action: Layla stands with one hand on the doorframe and the other holding the edge of her headscarf, looking toward the first work of the day rather than posing.
Required object/gesture: patched headscarf, doorframe hand, and mud-brick threshold must be legible at 600x400.
Composition/framing: close-medium portrait, Layla foreground slightly left, house threshold framing her, fields visible as context.
Lighting/mood: cool pre-dawn with a thin warm horizon, intimate and patient.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded 19th-century Egyptian materials.
Constraints: no text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no heroic pose.
Avoid: ornate palace room, smiling triumph, decorative atmosphere without the threshold and patched roof.
```

## First Custom Still Candidates

### `cp_layla.1` - The Farmer's Daughter

```text
Event: cp_layla.1 - "The Farmer's Daughter"
Narrative function: Introduce Layla as a person whose life begins before policy touches her directly.
Subject: Layla, young Delta fellaha in patched headscarf.
Scene/backdrop: packed dirt courtyard outside her family house before sunrise, grinding stone and water jar near the wall.
Foreground action: Layla pauses with both hands on a shallow basket of grain, not yet lifting it.
Required object/gesture: grain basket and grinding stone.
Lighting/mood: blue-grey morning, ordinary work held in stillness.
Avoid: royal court, market crowd, modern village, decorative empty landscape.
```

### `cp_layla.2` - The Deed

```text
Event: cp_layla.2 - "The Deed"
Narrative function: Land reform becomes visible as a paper that changes how Layla stands in her own field.
Subject: Layla, field worker, wary rather than triumphant.
Scene/backdrop: narrow Delta field edge beside a low irrigation canal and date palms.
Foreground action: Layla holds a folded paper at her waist while her bare feet remain in the field soil.
Required object/gesture: folded paper and feet in soil must both read clearly.
Lighting/mood: hard late morning, private disbelief under public law.
Avoid: courtroom, celebratory crowd, readable deed text, noble costume.
```
