# Common People -- Characters

This folder holds the character pool. Each anchor character has their own file: profile, personality weights, interests (game hooks), life events, and story tree. Lightweight "reaction-only" characters live in `sketches.md`.

The design philosophy (living characters, not arcs; personality-weighted reactions; pop/state binding) lives in `../the-holy-grail.md`. This folder is the content, not the theory.

## Anchor Characters (deep arcs)

Each anchor lives in its own folder: `README.md` holds the profile/weights/hooks/tree; `events/` holds the event text drafts; `prompts/` holds image-generation prompts; `images/` holds generated portraits and scene art.

| Folder | Character | Culture | Pop Type | One-line |
|--------|-----------|---------|----------|----------|
| [layla/](layla/) | Layla | Misri (Egypt) | Farmer | Apolitical serf riding the land-reform transitions |
| [al-sayyid/](al-sayyid/) | Hassan Bey al-Sayyid | Misri (Egypt) | Aristocrat | Bey watching his world collapse under modernization |
| [tarek/](tarek/) | Tarek al-Rashidi | Misri (Egypt) | Capitalist | Landowner's son who sold the estate and built a factory |
| [samier/](samier/) | Samier | Misri (Egypt) | Laborer | Factory worker whose anger either radicalizes or is bought off |
| [the-soldier/](the-soldier/) | The Soldier | Generic | Servicemen | Conscript archetype, reusable for every war |

## Lightweight Characters

- [sketches.md](sketches.md) -- 40+ short character sketches (farmers, workers, women, children, immigrants, slaves, clergy, artisans, sailors, miners, outcasts, elders). Reaction-only presence unless promoted later.

## Cross-Character Meetings

- [crossings.md](crossings.md) -- How characters' story trees can intersect (Tarek falling into Samier's factory, Layla migrating into Tarek's Cairo, etc.).

## How to add an anchor character

1. Create `<name>/` folder with subfolders `events/`, `prompts/`, `images/`.
2. Write `<name>/README.md` using the anchor template: Profile, Personality Weights, Historical Context, Key V3 Hooks, Life Events, Story Tree, Narrative Tone.
3. Add a row to the anchor table above.
4. Add event drafts to `events/` (one file per event, named by the chapter/beat).
5. Add image-generation prompts to `prompts/` and the rendered images to `images/`.
6. When it's time to wire them up, the character's triggers/effects become Paradox script in `mod/common/` and `mod/events/`.

## How to add a sketch character

Add an entry to `sketches.md`. If it later gets a deep arc, promote it to its own folder.
