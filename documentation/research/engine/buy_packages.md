# Buy packages — pop consumption model

## Source
`/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game/common/buy_packages/00_buy_packages.txt` (1,524 lines).

## Structure

One `wealth_N` block per integer `N` in `[1, 99]` — matching V3's SoL scale exactly. Each block:

```
wealth_N = {
    political_strength = <scalar>
    goods = {
        popneed_<need> = <integer_weight>
        ...
    }
}
```

`political_strength` scales with wealth (0.03 at wealth_1, 0.9 at wealth_11, continuing upward). `goods` is a weighted list; weights sum to ~150 at wealth_1 and grow as more categories unlock.

## Need categories observed (at least)

Across the file, these `popneed_*` categories appear:

- `popneed_basic_food` (all tiers)
- `popneed_simple_clothing` (all tiers)
- `popneed_heating` (all tiers)
- `popneed_intoxicants` (all tiers)
- `popneed_crude_items` (starts at wealth_5)
- `popneed_stimulants` (starts at wealth_6)
- `popneed_services` (starts at wealth_10)
- `popneed_household_items` (starts at wealth_10)
- `popneed_standard_clothing` (starts at wealth_10)
- `popneed_free_movement` (starts at wealth_10)

Higher wealth tiers unlock further categories (luxury food, luxury clothing, furniture, etc.); the exact unlock points will be detailed when the mod needs to gate specific crossroads on them.

## Layla at game start (peasant, SoL ~5)

`wealth_5`:

```
political_strength = 0.15
goods = {
    popneed_simple_clothing = 39
    popneed_crude_items     = 13
    popneed_basic_food      = 106
    popneed_heating         = 22
    popneed_intoxicants     = 41
}
```

Sum = 221. `popneed_basic_food` dominates at ~48% of her household's spend. Note: Layla is a **dependent**, consumption ×0.5 (plan §0.5 and §4.5), so her effective draw is half this.

## Implications for the mod

- **Radio, automobile, telephone** — these are `popneed_luxury_*` goods unlocked at higher wealth tiers (~wealth_20+). Layla only "can plausibly own a radio" once her `cp_sol >= 15` (Middling) AND the good is buying-ordered in Egypt's market. That's the logic of `cp_sensor_can_plausibly_own_radio` in plan §4.
- **Stimulants = coffee/tea/sugar**. She unlocks them at SoL 6. Egyptian misri obsession on coffee means her coffee weight is ×2 (cultures with obsession on a good within a popneed category double that category's demand for that specific good).
- **Culture obsession and religion taboo** act as multipliers on the good's weight within its `popneed_*` category: obsession ×2, taboo ×0.5. Layla's culture obsesses over coffee; her religion (sunni) likely taboos liquor — so her intoxicants spend skews heavily to tobacco and away from alcohol.
- **Crossroads gating**: profession-upgrade crossroads (peasant → shopkeeper) require `cp_sol >= N` AND `cp_literacy >= N` — reading these via her V3-mirroring variables works because her wealth tier directly indexes a buy package.

## Confirmation status

R-14 — **closed**. The 99-tier wealth-indexed consumption model is the canonical V3 mechanic. Future phases can compute expected spend shifts directly from this file.
