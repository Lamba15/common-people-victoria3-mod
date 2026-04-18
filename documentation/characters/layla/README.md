# Layla the Farmer (Egypt)

> Reference novel for tone: Naguib Mahfouz's *Cairo Trilogy*. Register of Egyptian interiority, the petit-bourgeois life at a slight slant, the smallness of a day next to the weight of a century.
>
> **For MVP plan and event list:** see [MVP.md](MVP.md).

## Profile

- **Pop type binding (narrative)**: Farmer. Stored as `cp_social_class = "farmer"` on her character object. Reactions look up a real farmer pop in her home state for SoL/radicalism data.
- **Culture**: Misri | **Religion**: Sunni | **Age**: 22 at spawn
- **Traits**: `persistent` (endurance through hardship), `pious` (traditional faith), `reserved` (quiet temperament), `compliant` (yields to family/tradition). All verified vanilla personality traits; convention drops the `trait_` prefix in script.
- **Home state**: Lower Egypt. Stored as `cp_home_state` on her character object (1.12 workaround; migrates to 1.13 `set_home_state`).
- **IG affiliation**: Rural Folk (narrative; not a role assignment).
- **Personality**: Apolitical, family-oriented, wants stability and peace. Weights drift over the decades.
- **Family**: Married to Ahmed (narrative reference, not a separate character at MVP). Children spawn as narrative references; may be promoted to their own characters later.
- **Mortality**: Natural death after ~60 (V3 default). Event-driven death possible: cholera, famine, childbirth (era-dependent), war widowhood (Ahmed).

## Personality Weights

| Interest | Weight | Why |
|----------|--------|-----|
| Land reform | 10 | Her entire existence depends on it |
| War | 7 | Ahmed could be conscripted |
| Revolution | 8 | Terrified of instability |
| Religion | 6 | Traditional, attends mosque |
| Women's rights | 5 | Affects her but she doesn't organize |
| Economy | 5 | Feels it through harvests |
| France | 4 | Cousin Mariam works the port in Alexandria |
| Education | 3 | Wants children to read someday |
| Labor laws | 2 | Vaguely aware factories exist |
| Diplomacy | 1 | Doesn't know or care who rules where |

## Historical Context

Egypt in 1836 operated under corvee labor. Peasants (fellahin) worked land controlled by beys and the state. Muhammad Ali's agricultural reforms began consolidating land ownership. The shift from communal/feudal to private smallholdings mirrors V3's Serfdom -> Homesteading path. See `../research/egypt.md` for the full context (cotton boom/bust, Suez corvee, tooth-extraction conscription).

## Key V3 Hooks

- **Spawn**: Country is EGY (or culture=misri tag equivalent), law is `law_type:law_serfdom` or early transition.
- **Primary on_actions**: `on_law_enacted` (land reform transitions), yearly pulse (harvest/SoL check), `on_war_started` (Ahmed panic), `on_revolution_start`.
- **State checks**: `any_harvest_condition` on her home state, farmer pop SoL in her home state, `turmoil` in her home state.
- **Law triggers**:
  - `has_law = law_type:law_serfdom` -- baseline suffering
  - `has_law = law_type:law_tenant_farmers` -- half-free event
  - `has_law = law_type:law_homesteading` -- the deed event (loyalist boost)
  - `has_law = law_type:law_commercialized_agriculture` -- wage farmer event
  - `has_law = law_type:law_collectivized_agriculture` -- collective event
- **Backward trigger**: if current law < previous law (rollback), fire the backward-transition event.

## Main Arc (6 chapters)

1. **"The Farmer's Daughter"** -- Introduction to serfdom at the human level. Layla rises before dawn to work land she doesn't own. Wants a family, a roof, bread, peace. Establishes stakes.
2. **"Winds from Cairo"** -- Land reform law enacted. Rumors reach the village. The bey is angry. Tension. Player chooses: send administrators (smooth) or let people sort it out (chaotic).
3. **"New Earth"** -- The transition. Smooth path: Layla holds a deed for the first time. Chaotic path: disputes, violence, the bey's men harass villagers. Historical detail: the dissonance of owning land you always worked.
4. **"The First Harvest"** -- Bound to farmer SoL data in her state. SoL rising: good harvest, family eats better. SoL falling: market conditions consume her gains. Freedom on paper, not in the belly.
5. **"Crossroads"** -- Branching based on accumulated state. Path A (prosperity): family thrives, children educated. Path B (hardship): she considers leaving for the city. Path C (politicization): forced into local politics against her nature.
6. **"Layla's Legacy"** -- 10+ years later. Prosperity: grandchild plays in her field. Hardship: she's a domestic servant in Cairo, the land a memory. Political: she speaks at a Rural Folk meeting. She never wanted this. But here she is.

## Reaction Examples

Fire probabilistically based on her personality weights.

- Law failed (land reform): Devastated. "They promised."
- War declared: Terror. "Ahmed. They'll take Ahmed."
- France diplomatic event: Curious. Her cousin Mariam wrote about the French quarter in Alexandria.
- Revolution starts: Hides with her family. "I told you. I told you this would happen."
- New technology (agricultural): Cautious interest. "They say the new plows cut deeper."
- IG Landowners gain power: Fear. "The bey's people are back."

## Story Tree

```
LAYLA SPAWNS (Egypt, serfdom or early land reform)
  Pop type: Farmer | Home state: Lower Egypt | IG: Rural Folk
  |
  v
[LAYLA UNDER SERFDOM]
  Life events: daily toil, the bey's overseer, harvest conditions.
  She endures. She does not question.
  |
  v
[LAND REFORM ENACTED] -- on_law_enacted
  Which law?
  |
  +-- Tenant Farmers -----> [HALF FREE]
  |     She can leave but the bey still owns the land.
  |     She stays. Where would she go?
  |     Life events: paying rent, small freedoms, uncertainty.
  |
  +-- Homesteading -------> [THE DEED]
  |     She owns the land. The great moment.
  |     (Mechanical: loyalist boost among farmers)
  |     |
  |     v
  |   [FARMING LIFE] -- yearly pulse checks harvest conditions, SoL
  |     |
  |     +-- Good harvests, rising SoL ---------> [PROSPERITY PATH]
  |     |     Layla thrives. Children born. Family grows.
  |     |     |
  |     |     v
  |     |   [LAYLA'S CHILDREN] -- send children to school?
  |     |     Yes: literacy boost; child may become teacher/clerk.
  |     |     No: farm children, cycle continues.
  |     |
  |     +-- Drought/bad harvests, falling SoL --> [HARDSHIP PATH]
  |     |     Crops fail. Debt. Hunger.
  |     |     |
  |     |     v
  |     |   [THE CROSSROADS] -- life decision
  |     |     |
  |     |     +-- "Stay on the land" -----> [STUBBORN FARMER]
  |     |     |     Risks everything. Good harvest = back to prosperity.
  |     |     |     Bad = loses land to debt, falls to city anyway.
  |     |     |
  |     |     +-- "Move to the city" -----> [CITY MIGRATION]
  |     |     |     Pop type: Farmer -> Laborer
  |     |     |     Home state: Lower Egypt -> Cairo
  |     |     |     Interest shifts: land drops, labor/economy rise
  |     |     |     |
  |     |     |     v
  |     |     |   [LAYLA IN THE FACTORY]
  |     |     |     Farming hands wrong for machines. Foreman shouts.
  |     |     |     Shares a room with three other families.
  |     |     |     She misses the sky.
  |     |     |     |
  |     |     |     Crosses with Samier if active in same state.
  |     |     |
  |     |     +-- "Husband goes alone" ----> [SPLIT FAMILY]
  |     |           Ahmed to Cairo. She runs the farm alone.
  |     |           If war: Ahmed conscripted from Cairo.
  |     |           She becomes SOLDIER'S WIFE archetype.
  |     |
  |     +-- War declared -----------------------> [WAR PATH]
  |           Ahmed conscripted. Connects to Soldier tree.
  |           If Ahmed dies: widow farmer. New events: running farm alone.
  |
  +-- Commercialized -----> [CORPORATE FARM]
  |     A company bought the land. Layla works for wages.
  |     Same field, different master. Like serfdom with a paycheck.
  |
  +-- Collectivized ------> [THE COLLECTIVE]
        Everything shared. She doesn't understand it.
        Same field, committee now. Community or loss of ownership?
```

### Backward Transitions (at any point)

```
[ANY LAW -> SERFDOM RE-ENACTED]
  Overrides everything. If she owned land: taken. If in city: dragged back.
  Pop type forced to: Farmer (serf)
  (Mechanical: massive radical spike)
  The darkest event in the mod.

[HOMESTEADING -> TENANT FARMERS]
  Keeps land but now pays rent to a new landlord.
  Less devastating but still a loss. She tasted ownership.
```

## Narrative Tone

Quiet, intimate, grounded. The drama is extraordinary forces acting on ordinary existence. Written as a novel, not a game text -- specific details, sensory language, subtext. Reference: Naguib Mahfouz's Cairo Trilogy for the register of Egyptian interiority.

---

## Living Systems Applied to Layla

### Monthly Life Pulse

Monthly roll, 10% fire chance (~1.2 events per year on average). Most months silent. On fire: pick a small event weighted by her current phase of life, season, and state conditions. See `events/life-pulse.md` for the bucket catalog.

**Bucket categories** (expanded in events/):
- **Family**: Ahmed comes home tired, child has fever, her mother visits, pregnancy, loss of a child, a wedding in the family.
- **Faith**: fajr prayer in the dark, Ramadan nightfall, the imam's sermon, Eid preparations, a death and the washing of the body.
- **Harvest & seasons**: flooding Nile (positive), drought, locust sighting, the first cotton buds, the last day of threshing, a neighbor's field fails.
- **Community**: a village wedding, a neighbor's funeral, the tax collector's visit, a traveling storyteller passes through, a foreign traveler asks directions.
- **Home**: the mud-brick wall cracks, a snake in the grain store, Ahmed mends the roof, a new chicken, the cat has kittens.
- **Body**: exhaustion, hunger, a pain that won't go away, a fever, a wound, pregnancy.
- **Inner life**: a memory of her mother, a fear for her children, a moment of unexpected joy, doubt about God, gratitude.
- **World beyond**: a soldier passes through the village, a letter from Mariam in Alexandria, news of a far-off war, a foreign coin in the market.

Each bucket should end up with 5-20 events. That's hundreds of small moments. A campaign spanning 60+ years will see most of them, none exhaustively.

### Opinions on Other Nations

Layla's opinions live on her character as variables: `cp_opinion_fra`, `cp_opinion_gbr`, `cp_opinion_ott`. Default 0 for most nations (unaware).

**Starting opinions (1836):**
- `cp_opinion_fra = +5` -- cousin Mariam mentions "the French quarter" favorably.
- `cp_opinion_ott = +10` -- the sultan is a respected name the imam mentions.
- `cp_opinion_gbr = 0` -- hasn't heard of them meaningfully.
- Everyone else: 0.

**In-scope nations for Layla** (others stay 0 forever): OTT, FRA, GBR, GRE, ITA, any Levantine power, and Egypt itself (`cp_opinion_egy` -- how she feels about her own sovereign). Egyptian independence/Muhammad Ali dynamic: strong opinion if it happens.

**Shifts** (all gated by `cp_hears_foreign_news` or an equivalent personal connection):
- Mariam's letter describes French cruelty at the port -> `cp_opinion_fra -= 10`.
- A French ship shells Alexandria -> `cp_opinion_fra -= 25` (this hits regardless of info gate -- it's in her country).
- British famine-aid grain arrives during cotton bust -> `cp_opinion_gbr += 15`.
- Ottoman conscription of Ahmed -> `cp_opinion_ott -= 25`.
- Muhammad Ali wins independence -> `cp_opinion_egy += 30`, `cp_opinion_ott -= 10`.

**Info-flow gate**: Layla can only *form or change* an opinion about a foreign nation if `cp_hears_foreign_news` is true for her. If the country has censorship and she's illiterate in a rural state, foreign news doesn't reach her -- and her opinions on the world sit frozen at whatever they were last exposed to.

### Personality Drift

Weights shift over time. Reasons:

| Trigger | Effect |
|---------|--------|
| Bad harvest year | interest_revolution +1, hope -1 |
| Good harvest year | hope +1, interest_revolution -1 |
| Child dies | hope -2, interest_religion +1 |
| War drags into year 3 | interest_war +1 every year after |
| Literacy tech researched + children | interest_education +1 per year of schooling |
| Husband's conscription | interest_war +3, interest_revolution +1 |

All weights clamped 0-10. Auditable in her event source (grep for `change_variable`).

### Mortality

Per-year roll from age 40 onwards, accelerating past 60. Additional death rolls triggered by:

- Cholera outbreak in her state (`harvest_condition disease_outbreak`) -- meaningful probability
- Famine SoL crash -- meaningful probability
- Childbirth -- per pregnancy, higher in early campaign years
- Flood/drought catastrophe -- small

If she dies, one final event fires (funeral/"Ahmed sits at her grave" / her children scatter). A successor spawn may happen: her eldest daughter Fatima or a neighbor's wife Nefertari.
