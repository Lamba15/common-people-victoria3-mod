# The Soldier (Generic)

## Profile

- **Pop type**: Servicemen
- **Culture**: Generated from spawning country
- **Age**: 18-25 at conscription
- **Traits**: Random
- **Personality**: Varies -- could be patriotic, fearful, or resigned. Rolled at spawn.

Generic archetype -- reusable for every country at war. The soldier is often someone else's husband, brother, or son; other characters (Layla, etc.) can reference the soldier as a family member.

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

- **Spawn**: `on_war_started` (any country). Can pre-exist in peacetime as a garrisoned servicemen character.
- **On-actions**: `on_battle_won`, `on_battle_lost`, `on_war_ended`, yearly pulse during war.
- **State checks**: state has `is_at_war`, infrastructure damage, devastation.
- **Integration**: if Layla's Ahmed is conscripted, the soldier archetype can BE Ahmed (link by character flag). Same for other characters' family members.

## Main Arc (6 chapters)

1. **"The Notice"** -- Conscription arrives. Family left behind.
2. **"The March"** -- Training. Reality vs. expectations. Period-accurate rations and conditions.
3. **"The Front"** -- Battle. Not heroic -- chaotic, terrifying, random. Friends die.
4. **"The Letter Home"** -- Writes to family. We see the dependent pop side.
5. **"The Aftermath"** -- War ends. Returns (or doesn't). Wounds, physical and psychological.
6. **"The Veteran"** -- Years later. Grateful, radicalized, or broken.

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
