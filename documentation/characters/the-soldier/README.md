# The Soldier (Yusuf ibn Mahmud, Egypt)

## Implementation Status

First scaffold landed in the v0.5 rebuild:

- Name token: `soldier`
- Script files: `mod/events/cp_soldier_events.txt`, `mod/common/scripted_effects/cp_soldier_memory.txt`, `mod/localization/english/cp_soldier_l_english.yml`
- Shared wiring: `cp_shared_startup.1` registers him death-safely, `cp_roll_for_event` gives him a 7-weight ambient branch, `cp_on_yearly` ages and refreshes him, and `cp_on_war_started` / `cp_on_war_end` route his war spine. The internal war-start dispatcher is reached from vanilla `on_diplo_play_war_start`.
- Images: all six visible Soldier events now use mod-owned generated DDS art, with source/archive files under `image/generated/soldier/v0.1/`, `image/generated/soldier/v0.2/`, and `image/generated/soldier/v0.3/`. The v0.3 batch replaces the final generic machinery, garrison-city, and letter-writing motion plates.
- Current content: two ambient peacetime beats (`cp_soldier.10`, `cp_soldier.40`), a war-start notice (`cp_soldier.20`), a war-end return (`cp_soldier.21`), one modernization/world-response event (`cp_soldier.30`), and a wartime letter-home beat (`cp_soldier.50`). No battle branch, veteran branch, death event, JE, button, or conversation tree yet.

Note for Victoria 3 1.13: the local installed game names this pop type `soldiers` under `game/common/pop_types/soldiers.txt`, so the implemented cohort reader uses `poptype = soldiers` even though older design prose called the archetype "servicemen".

## Profile

- **Pop type**: Soldiers
- **Culture**: Misri | **Religion**: Sunni | **Age**: 20
- **Traits**: Not a V3 character entity in the first scaffold
- **Personality**: Resigned, observant, family-bound. Later branches can roll patriotic, fearful, or radicalized variants.

Initial implementation is Egypt-first: Yusuf ibn Mahmud is the first reusable soldier instance. The broader archetype can still become reusable for every country at war later. The soldier is often someone else's husband, brother, or son; other characters (Layla, etc.) can reference the soldier as a family member.

## Personality Weights (template)

Rolled at spawn. Ranges:

| Interest | Range | Notes |
|----------|-------|-------|
| War | 8-10 | Always high -- it's his life |
| Nationalism/patriotism | 2-10 | Rolled: defines his tone |
| Revolution | 1-8 | Rolled: deserter material if high |
| Family | 7-10 | Always high |
| Economy | 2-6 | Soldiers notice inflation and pay |
| Religion | 2-8 | Rolled |
| Diplomacy | 1-4 | Low -- he doesn't read the treaties |

## Key V3 Hooks

- **Spawn**: `on_diplo_play_war_start` (any country, via actor/target country scope). Can pre-exist in peacetime as a garrisoned soldier person.
- **On-actions**: `on_battle_won`, `on_battle_lost`, `on_war_end`, yearly pulse during war.
- **State checks**: state has `is_at_war`, infrastructure damage, devastation.
- **Integration**: if Layla's Ahmed is conscripted, the soldier archetype can BE Ahmed (link by character flag). Same for other characters' family members.

## Main Arc (6 chapters)

1. **"The Notice"** -- Conscription arrives. Family left behind.
2. **"The March"** -- Training. Reality vs. expectations. Period-accurate rations and conditions.
3. **"The Front"** -- Battle. Not heroic -- chaotic, terrifying, random. Friends die.
4. **"The Letter Home"** -- Writes to family. We see the dependent pop side.
5. **"The Aftermath"** -- War ends. Returns (or doesn't). Wounds, physical and psychological.
6. **"The Veteran"** -- Years later. Grateful, radicalized, or broken.

Implemented early side beats:

- `cp_soldier.30`, "The Arsenal Gate": fires through `cp_try_fire_world_response` when machine industry or military production makes war feel manufactured rather than merely ordered.
- `cp_soldier.40`, "Beans at Dusk": a peacetime ambient barracks beat that gives Yusuf ordinary breath between war hooks.
- `cp_soldier.50`, "The Letter Folded Twice": a wartime ambient/world-response beat that lets the monthly life pulse continue while Yusuf is away.

## Branches

Rolled by battle outcomes, traits, and player military choices (professional army vs. conscription laws, use of mass mobilization, etc.).

```
[CONSCRIPTED]
  |
  +-- Survives the war
  |     +-- Patriotic trait -> [GRATEFUL VETERAN]
  |     |     Proud of service. Conservative. Loyalist.
  |     +-- Resigned trait -> [BROKEN VETERAN]
  |     |     PTSD before the word existed. Drinks if culture allows.
  |     |     Can't hold work. Wife carries the household.
  |     +-- Radicalized by war -> [THE AGITATOR VETERAN]
  |           Saw the officers eat while privates starved.
  |           Joins Trade Unions or a radical IG.
  |           Strong candidate for Agitator role.
  |
  +-- Deserts -> [THE DESERTER]
  |     Lives in hiding. Guilty and free. Reaction-only from here.
  |
  +-- Dies
        His wife/mother receives the news.
        If linked to Layla or another character: they get the death event.
        Small loyalist boost if war was popular; radical spike if not.
```

## Reaction Examples

- War declared: The arc begins. First event fires.
- Peace signed: Relief or rage depending on terms. "For THIS we died?"
- Conscription law changed (Mass Conscription <-> Professional Army): Massive impact -- changes whether this archetype can even exist.
- Revolution at home while he's at the front: Existential. Fights for a government that may not exist when he returns.

## Narrative Tone

Unglamorous. War is not heroic here -- it is random, muddy, and full of small indignities. The soldier's fear is specific: cold feet, a bad officer, the smell of a field hospital. Period-accurate: what rations looked like, what a musket misfire means, what a wound infection does.
