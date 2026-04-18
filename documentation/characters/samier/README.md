# Samier the Factory Worker (Egypt)

## Profile

- **Pop type**: Laborer / Machinist
- **Culture**: Misri | **Religion**: Sunni | **Age**: 19 | **Traits**: Ambitious
- **Home state**: Cairo (or other industrial state)
- **IG**: unaligned at spawn, drifts toward Trade Unions
- **Personality**: Energetic, increasingly angry, politically awakening. Faith shaken by suffering.

## Personality Weights

| Interest | Weight | Why |
|----------|--------|-----|
| Labor laws | 10 | His survival depends on it |
| Revolution | 8 | Drawn to radical ideas |
| Economy | 8 | Feels exploitation directly |
| War | 4 | Not his primary concern |
| Land reform | 3 | Left farming behind |
| Education | 6 | Wishes he could read better |
| Religion | 3 | Lapsed -- faith shaken by suffering |
| Women's rights | 2 | Hasn't thought about it |
| France | 1 | Doesn't care about foreign affairs |
| Diplomacy | 1 | Too busy surviving |

## Anger Variable

Samier has a tracked anger variable `cp_samier_anger` (0-10). This is his branch selector.

**Increases:**
- Workers' rights law FAILS (+2)
- Factory accident event (+1)
- Economy booms but laborer SoL stays flat (+1)
- Factory owner (e.g. Tarek) gets richer while workers don't (+1)
- Player suppresses a protest (+2)

**Decreases:**
- Workers' rights law PASSES (-3)
- Laborer SoL rises (-1)
- Player negotiates with workers (-2)
- Education law passes (hope) (-1)

## Historical Context

Muhammad Ali's 1830s-40s industrialization created state-owned factories with conditions mirroring European industrialization. 14-16 hour days, no safety, wages barely covering subsistence, children working from age 4. Mills changed clocks to catch workers "late" and fine them. See `../research/egypt.md` (cigarette strike 1899) and `../research/europe.md` (Silesian weavers).

## Key V3 Hooks

```
# Spawn
AND = {
    country_has_primary_culture = cu:misri
    any_scope_building = { is_building_group = bg_manufacturing }
    has_law = law_type:law_no_workers_rights   # his suffering requires this
}

# Anger threshold branch gate
scope:samier = {
    var:cp_samier_anger >= 7
}
```

On-actions: `on_law_enacted` (workers' rights), yearly pulse (accidents, SoL), `on_revolution_start`, high turmoil in his state.

## Main Arc (7 chapters)

1. **"The City"** -- Arrives. Shock of scale. Assigned to textile factory. Pay barely better than farming.
2. **"The Machine"** -- Daily reality. Fourteen-hour shifts. Overseer's fines. A co-worker loses fingers. No compensation.
3. **"The Injury"** -- Serious accident. Owner offers nothing. Samier starts asking questions.
4. **"The Meeting"** -- Reform branch: new rules, cautious hope. Status quo branch: secret workers' meeting, talk of strikes.
5. **"The Spark"** -- Confrontation. Protest or work stoppage. Player: negotiate or suppress?
6. **"The Breaking Point"** -- Reform path: shop foreman, anger fades. Radical path: becomes Agitator. Tragic path: dies, nobody writes his name.
7. **"What Remains"** -- If alive: reflection. If Agitator: mechanically affecting politics. If dead: new workers replace him. The machines don't remember.

## Reaction Examples

- Workers' protection law enacted: Relief mixed with suspicion. "Words on paper. Let's see if the overseer listens."
- Workers' protection law FAILS: Fury. This is what can push him from annoyed to radical.
- Economy booms: Bitter. "The owner bought a new house. We got nothing."
- Revolution starts: Excited or frightened depending on his radicalization.
- New machinery tech: Worried. "They say the new machines need fewer hands."

## Story Tree

```
SAMIER SPAWNS (factories exist, weak labor laws)
  Pop type: Laborer | Home state: Cairo | IG: drifting toward Trade Unions
  |
  v
[FACTORY LIFE]
  Events: long hours, danger, low pay. Seeds of anger.
  |
  v
[THE ACCIDENT] -- yearly pulse, probability
  A coworker is injured. The foreman doesn't care.
  cp_samier_anger increments.
  |
  v
[ANGER THRESHOLD CHECK]
  cp_samier_anger >= 7?
  |
  +-- YES --> [RADICALIZATION PATH]
  +-- NO  --> [QUIET WORKER PATH]
```

### RADICALIZATION PATH

```
[SAMIER RADICALIZES]
  Attends secret meetings. Reads pamphlets.
  |
  v
[THE STRIKE] -- triggered by political movement or high turmoil
  |
  +-- "Negotiate" --> [SAMIER THE LEADER]
  |     Strike succeeds peacefully. Becomes Agitator.
  |     Trade Unions IG clout boost.
  |     Organizes, speaks, may run for office if democracy allows.
  |     Never returns to the factory floor.
  |
  +-- "Suppress" --> [SAMIER ARRESTED OR KILLED]
  |     +-- Survives (arrested): prison, comes out harder.
  |     |   Underground Agitator. Radical spike, turmoil up.
  |     |
  |     +-- Dies: "A worker died. Nobody wrote his name down."
  |           Massive radical spike among laborers.
  |           His death becomes a symbol. Other characters react:
  |           Layla hears. Tarek (if on factory floor) was there.
  |
  +-- "Ignore" --> [STRIKE FIZZLES]
        Nothing changes. Demoralized. Anger drops to 5. Broken, not calm.
        Returns to QUIET WORKER but bitter. May radicalize again.
```

### QUIET WORKER PATH

```
[SAMIER STAYS QUIET]
  Anger below threshold. Works. Survives.
  |
  v
[LIFE EVENTS] -- yearly pulse
  |
  +-- Labor laws pass --> [SAMIER FINDS PEACE]
  |     Conditions improve. Shorter hours. Safety rules.
  |     Becomes foreman. Teaches younger workers.
  |     Anger drops to 1-2. Loyalist boost.
  |     Not happy. Not angry. Tired.
  |
  +-- Education opens --> [SAMIER EDUCATES HIMSELF]
  |     Night school. Pop type: Laborer -> Shopkeeper/Clerk.
  |     Personality shifts completely. A different life.
  |     Still has the burn scar from the factory.
  |
  +-- Falls in love --> [SAMIER'S FAMILY]
        Meets someone. Has a child. Works to feed them, not to fight.
        If conditions worsen: protective anger, not revolutionary.
        "I don't care about the movement. I care about my son
         not losing his fingers."
```
