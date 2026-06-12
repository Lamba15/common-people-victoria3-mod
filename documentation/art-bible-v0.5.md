# Common People art bible - v0.5 rebuild

Date: 2026-05-26

This replaces the loose image direction from the proof-of-concept phase. The mod should look human, historical, and intimate, not like generic fantasy concept art.

## North star

Common People event art is a witness's memory of one ordinary life inside a grand strategy game. The image should feel like a painted historical scene that happened before anyone thought it was important.

The frame must answer three questions at 600x400:

- Who is this about?
- What changed?
- What object or gesture carries the change?

If the image is only atmospheric, it fails. If it is heroic, it fails. If it cannot be read at event-window size, it fails.

## Visual language

- 3:2 landscape composition, generated at high resolution and shipped as 600x400 DDS.
- Painted historical realism with visible brush texture, natural anatomy, and physical weight.
- Lower Egypt first: Nile Delta mud brick, irrigation channels, cotton and grain fields, palms, market dust, village doors, Cairo mill interiors only when the event calls for the city.
- Human-scale framing: close-medium or medium-wide. No epic camera angles unless the scene is explicitly about a public crowd.
- Light carries meaning: dawn for beginnings, flat noon for coercion, lamplight for household interior, dusty afternoon for bureaucratic pressure, grey dawn for grief.
- Palettes are warm but not monochrome: ochre earth, Nile green, faded indigo cloth, dark wood, red wax, brass, paper cream, smoke grey.

## Must avoid

- Generic medieval, fantasy, or Orientalist costumes.
- Modern clothing, modern paper, modern interiors, modern factory equipment.
- Glossy digital smoothness, airbrushed skin, plastic faces, extreme depth-of-field blur.
- Text, UI, borders, signatures, watermarks, fake labels, legible slogans, or invented flags.
- Hero poses, cinematic battle spectacle, royal court grandeur, crowds that dwarf the personal scene.
- Pure atmosphere with no specific object: every event image needs a deed, letter, loaf, rifle, shutter, school slate, mill gate, ledger, child, cup, or other story anchor.

## Layla identity

Layla al-Sharif begins as a Lower Egyptian fellah woman in her early twenties.

Stable traits:

- Egyptian/Misri, sun-warmed olive-brown skin.
- Oval face, heavy brows, dark eyes, black hair usually covered or braided.
- Work-worn hands are as important as her face.
- Practical village clothes: faded blue, brown, cream, and indigo cloth; headscarf; no jewelry except when a scene specifically earns it.
- She ages across the story. Do not render every event with the same twenty-two-year-old face.

Age discipline:

- 1830s-1840s rural events: early twenties to early thirties.
- War, land, early family beats: twenties to thirties.
- Mill/Cairo/welfare/property arcs: middle age.
- death, late bureaucracy, and late conversation beats: old age.

## Event image contract

Every replacement prompt must include:

- event id and title
- one-sentence narrative function
- exact age range for Layla or the relevant person
- setting
- foreground action
- required story object
- background detail, if any
- lighting
- rejection line

Prompt template:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Event: <event_id> - "<title>"
Narrative function: <what changed in this beat>
Subject: <Layla/person identity and age here>
Scene/backdrop: <specific place and period>
Foreground action: <what the person is doing>
Required object/gesture: <single visual anchor>
Composition/framing: <close-medium, medium-wide, etc>
Lighting/mood: <specific light and emotional register>
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials
Constraints: no text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no heroic pose
Avoid: generic desert scene, palace grandeur, decorative atmosphere without the required object
```

## Prototype set

The prototype set established the visual standard for the later bulk pass:

| Event | Why |
|---|---|
| `cp_layla.1` / `cp_layla_intro_v06.dds` | establishes Layla's face, village, and tone |
| `cp_layla.2` / `cp_layla_homesteading_v05.dds` | proves paper/deed readability and quiet emotional weight |
| `cp_layla.4` / `cp_layla_ahmed_conscripted_v06.dds` | proves multi-figure war departure without spectacle |
| `cp_layla.41` / `cp_layla_clerks_letter_v06.dds` | proves grief without melodrama |
| `cp_layla.80` / `cp_layla_last_morning_v05.dds` | proves old-age continuity and restraint |
| `cp_layla_vox.100` / `cp_layla_conversation_audience_v06.dds` | proves the new conversation visual language |

Two of these remain wired as non-destructive `_v05` DDS assets. The intro, Ahmed-conscripted, clerk-letter, and conversation-audience proofs have stronger `_v06` replacements wired; the superseded `_v05` DDS files are archived outside the shipped mod tree. The full Layla replacement queue has since been generated, converted, and promoted through v0.15, but the in-game visual QA pass still needs to confirm these images at event-window scale.

## Person expansion sets

First-pass sources and promoted stills for new persons now live beside the Layla prototype set. Earlier vanilla motion placeholders have been replaced; active release art is custom still DDS with generated-source coverage.

| Person | Files | Archive |
|---|---|---|
| Hassan Bey al-Sayyid (`bey`) | 6 stills: intro, homesteading, serfdom, commercialized agriculture, factory boundary, visitors' card | `image/generated/al-sayyid/` |
| Yusuf ibn Mahmud (`soldier`) | 6 stills: intro, notice, return, arsenal gate, letter folded, beans at dusk | `image/generated/soldier/` |
| Samier (`samier`) | 6 stills: gate of smoke, labor law, red thread, bread at the gate, false quarter hour, letters after the bell | `image/generated/samier/v0.1/` |
| Tarek al-Rashidi (`tarek`) | 6 stills: mill ledger, labor law, new boiler, account book, second chimney, locked gate | `image/generated/tarek/v0.1/` |
| Nour (`nour`) | 6 stills: intro, property paper, rent receipt, key under pillow, register shelf, morning account | `image/generated/nour/` |
| Mina (`mina`) | 6 stills: intro, public schools, notice sheet, night proof, catalogue room, courtyard sheet | `image/generated/mina/` |
| Zaynab (`zaynab`) | 6 stills: intro, doctor outside, fever bowl, long night, lime bucket, thread around the wrist | `image/generated/zaynab/v0.1/` |
| Farid al-Haddad (`farid`) | 6 stills: platform boy, blue wire, embankment stones, night lamp, new carriage, parcel bag | `documentation/characters/farid/prompts/seed-v0.1.md` |
| Dawud Hanna (`dawud`) | 6 stills: rope burn, iron hook, smoke at the quay, salt floor, tariff chalk, manifest room | `documentation/characters/dawud/prompts/seed-v0.1.md` |
| Rashid al-Katib (`rashid`) | 6 stills: counter window, archive lamp, paper name, dust in ink, new seal, numbered drawer | `documentation/characters/rashid/prompts/seed-v0.1.md` |
| Salma Farag (`salma`) | 6 stills: switchboard, first light, voices in the wall, night bell, burned fuse, crossed line | `documentation/characters/salma/prompts/seed-v0.1.md` |
| Karim al-Nahhas (`karim`) | 6 stills: iron teeth, tool bench, broken finger, new engine, steel color, night gauge | `documentation/characters/karim/prompts/seed-v0.1.md` |
| Huda al-Matariya (`huda`) | `cp_huda_room_alley_v01.dds`, `cp_huda_street_planks_v01.dds`, `cp_huda_water_under_stone_v01.dds`, `cp_huda_rent_book_v01.dds`, `cp_huda_roof_patch_v01.dds`, `cp_huda_white_road_v01.dds` | `image/generated/huda/v0.1/` |
| Mansur al-Mahalla (`mansur`) | 6 stills: mat beside looms, first wage token, belt does not stop, money sent home, bed rent, meal tin | `documentation/characters/mansur/prompts/seed-v0.1.md` |
| Nabil al-Haras (`nabil`) | 6 stills: lamp at the corner, new station, rifles by bakery, square afterwards, lost boy, complaint bench | `documentation/characters/nabil/prompts/seed-v0.1.md` |

## Production target

- Source/archive: high-resolution PNG is fine and should be kept outside the mod repo.
- Shipped asset: 600x400 DDS, DXT5/BC3, no mipmaps.
- Build review sheets after each generated batch:
  ```bash
  script/build-image-contact-sheets.py
  script/build-image-contact-sheets.py --check
  ```
- Run `script/audit-event-images.py` after conversion.
- Run `script/audit-art-provenance.py` to track how much active event art has generated source coverage.
- Export roster-wide character seed prompts before generating custom stills or portraits:
  ```bash
  python3 script/build-character-seed-prompt-ledger.py --version v0.1
  python3 script/build-character-seed-prompt-ledger.py --version v0.1 --check
  python3 script/export-character-seed-prompts.py --version v0.1
  python3 script/export-character-seed-prompts.py --version v0.1 --check
  ```
- Run `script/audit-event-images.py --strict-size --strict-unused` before a release candidate.

Current inventory:

```text
Referenced DDS: 191
Referenced BK2: 0
Known BK2:      244
Shipped DDS:    191
Missing:        0
Missing videos: 0
Unused shipped: 0
Dimensions:     191 at 600x400
Non-standard referenced images: 0
```

Current provenance:

```text
Active event DDS references: 191
Generated source coverage:  191
Legacy/no generated source: 0
```

All active event DDS references are now generated-source-covered. The remaining art rebuild work is qualitative and character-expansion work: in-game QA for promoted stills, event-window readability review, and generation/conversion of future roster-wide per-person seed prompts when new intimate scenes or portraits are added. The current motion ledger reports 0 custom/mod motion events and 0 vanilla video placeholders.

The shipped event-art pool is now dimension-clean and unused-clean. The legacy comparison DDS files live outside the shipped mod tree under `image/archive/legacy-event-pictures/v0.5/`; do not copy them back into `mod/gfx/event_pictures/` unless an event is explicitly rewired to use them.

First-pass visual findings live in `documentation/art-review-v0.5.md`. The promoted Layla replacement ledgers run from `documentation/characters/layla/prompts/replacement-batch-v0.7.md` through `replacement-batch-v0.15.md`; `documentation/art-acceptance-ledger.md` is the current proof of source PNG, DDS, reference, and promotion state.

Character seed prompt exports live under `image/generated/character-seeds/v0.1/`, with `documentation/character-seed-prompt-ledger.md` as the review ledger. The current `gpt-image-2-seed-batch.jsonl` manifest covers all 16 registered persons with 16 canonical portrait prompts and 32 first-scene prompts, but it is not automatically promoted; generated candidates still need contact sheets, visual review, DDS conversion, and event rewiring before they become shipped art.
