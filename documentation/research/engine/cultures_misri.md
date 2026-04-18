# cu:misri — Layla's culture

## Source
`/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game/common/cultures/00_cultures.txt:6521`.

## Verbatim definition (header)

```
misri = {
    color    = rgb{ 226 218 112 }
    religion = sunni
    obsessions = {
        coffee
    }
    heritage  = heritage_arab
    language  = language_arabic
    traditions = { }
    ...
}
```

## Key facts for the mod

- **Default religion**: `sunni`. Every misri pop starts sunni unless migration or events convert them.
- **Starting obsession**: `coffee`. This is hard-coded; `cu:misri = { has_cultural_obsession = coffee }` returns true from 1836.1.1 regardless of market conditions. Layla's pop group demands coffee at ×2 weight within `popneed_stimulants` as soon as her SoL lets her buy stimulants at all (SoL 6+, per the wealth_6 buy package).
- **Heritage**: Arab — affects acceptance with other Arab-heritage cultures in ways the mod reads via `is_heritage` triggers (not needed yet).
- **Language**: Arabic — affects discrimination/acceptance with non-Arabic-speaking cultures.
- **Traditions**: empty in the base definition. Any traditions would flow from the religion layer (sunni religion file) not the culture file.

## Implications for Layla's narrative

- She loves coffee from day one. Pulse prose can reference the coffee cup, the coffeehouse gossip Ahmed brings home, without gating on a "coffee arrives" tech event.
- The Muhammad Ali–era importation of coffee from Yemen/Brazil is already reflected: misri obsession is set in 1836.
- When Egypt's market `mg:coffee = { market_goods_cheaper >= 0.10 }` turns true, her household's demand spikes visibly in-game — her mood sensors can pick this up via `cp_sensor_coffee_is_abundant`.
- Religion-level taboos for sunni (checked by reading `common/religions/`) likely include pork and alcohol — those are taboos on the pop's **culture's default religion**, per plan §4.5 constraint #8. Her personal pop-type religion mechanic follows the culture's default, not her individual state.

## No-action items

Nothing to modify in vanilla. The mod reads these values; it does not override them.
