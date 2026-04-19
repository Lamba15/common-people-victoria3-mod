# The Life of Layla al-Sharif — Story Map

The master index of every event, every conversation, every ambient pulse, grouped by the **act of her life** they fall in and the **thematic arc** they advance.

The mod now has **77 Layla events** (`cp_layla.1` .. `cp_layla.124`, with gaps where IDs were reserved) and **~60 conversation events** (`cp_conversation.*`). This document is how we see them together.

---

## 1. The shape of the story

Layla is 22 in 1836, a Misri-sunni peasant in Lower Egypt, newly married to Ahmed (subsistence farmer, not a real V3 character — narrative only). The mod plays her full life, roughly:

- **~1836–1850 (her 20s–30s)** — she is a young wife, bearing children, losing one or two, learning the seasons; everything is very small and very close to the ground.
- **~1850–1875 (her 30s–50s)** — the world starts arriving: the first law that changes her household's relation to the land, the first tax that changes the loaf, the first technology that reaches the village, the first crossroads (Cairo, the stall, the factory).
- **~1875–1900 (her 50s–70s)** — she is a matriarch. Welfare reaches her; the vote reaches her; she may be a widow; she is literate or not; her daughter is married or delayed. She has fantasy audiences with the Pasha about her life.
- **~1900–end (her 70s+)** — the evening. Mortality climbs. Some version of her dies in childbirth at 25, some version dies of pollution-poisoned lungs at 78 in a tenement above a cotton mill, some version dies in her village bed at 82 with her daughter reading to her.

She is never the same woman twice. The mod is the system that makes each playthrough's Layla feel like *a* Layla, not *the* Layla.

---

## 2. The five acts

### Act I — The Young Wife (events that fire in her first ~15 years)

The world is small: the house, the field, the lane, the river. Ahmed is alive; the children are being born.

| ID | Title | Kind | Trigger |
|----|-------|------|---------|
| cp_layla.1 | The Farmer's Daughter | intro | cp_startup.1 → on game start |
| cp_layla.5 | The First Cry | life-beat | console / story gate |
| cp_layla.6 | A Moment | pulse | JE monthly pool |
| cp_layla.11 | Walking the Field She Owns | pulse | has_variable = cp_owns_land |
| cp_layla.12 | Under the Bey's Eye | pulse | has_variable = cp_under_serfdom |
| cp_layla.13 | A Day With No Wind | pulse | always |
| cp_layla.14 | The Neighbour's Boy in the Lane | pulse | always |
| cp_layla.15 | Her Mother's Left Hand | pulse | always |
| cp_layla.16 | The Hen That Will Not Lay | pulse | rural |
| cp_layla.17 | The Merchant's Scale | pulse | rural / market |
| cp_layla.18 | Friday, the River Low | pulse | rural |
| cp_layla.19 | The Old Woman Who Sees Through Walls | pulse | rural, neighbours |
| cp_layla.20 | The Bread That Did Not Rise | pulse | always (household) |
| cp_layla.21 | Dust on the Water | pulse | rural, Nile |
| cp_layla.22 | The Younger Brother's Letter | pulse | needs literacy OR letter-reader |
| cp_layla.23 | The Mule That Will Not Move | pulse | rural |
| cp_layla.25 | The First Day of Ramadan | seasonal pulse | Ramadan window |
| cp_layla.26 | The Nile Rises | seasonal pulse | Aug-Sep window |
| cp_layla.27 | The Hajj Returnees | seasonal pulse | Dhu al-Hijjah |
| cp_layla.28 | The Midwife's Lamp | pulse | rural, children present |
| cp_layla.29 | The Date Harvest | seasonal pulse | autumn, rural |

**Dominant feeling**: slow earth-time. The story is only just starting.

### Act II — The Claim on Land (the big law-reactions of mid-life)

Laws change. The state arrives. Each first-enactment is a one-shot memory.

| ID | Title | Kind | Trigger |
|----|-------|------|---------|
| cp_layla.2 | The Deed | reaction | law_homesteading |
| cp_layla.3 | The Bey Returns | reaction | law_serfdom (regression) |
| cp_layla.7 | The Tax Collector | reaction | cp_tax_burden spike |
| cp_layla.8 | The Price of the Loaf | reaction | has_consumption_tax g:grain |
| cp_layla.93 | The Law Catches Up to Us | reaction | law_women_in_the_fields |
| cp_layla.94 | A Paper with My Name | reaction | law_women_own_property |
| cp_layla.100 | A School in the Next Village | reaction | law_public_schools |
| cp_layla.101 | They Will Be Taken to the School | reaction | law_compulsory_primary_school |
| cp_layla.107 | The Coptic Neighbour Exhales | reaction | law_multicultural |
| cp_layla.115 | The Procession Passes | reaction | law_freedom_of_conscience |
| cp_layla.118 | The Children Leave the Floor | reaction | law_restricted_child_labor |

**Dominant feeling**: the state has a hand now; the hand can be kind or cruel; it is always a hand.

### Act III — The World Arrives (technology + industry + migration)

The village is no longer a sealed unit. The world enters.

| ID | Title | Kind | Trigger |
|----|-------|------|---------|
| cp_layla.4 | He Marches | reaction | on_war_started + Ahmed eligible |
| cp_layla.10 | The Letter That Has Not Come | pulse | cp_ahmed_at_war |
| cp_layla.30 | The Iron Horse | reaction | has_technology_researched = railways |
| cp_layla.31 | A Word From Beyond | reaction | has_technology_researched = electric_telegraph |
| cp_layla.32 | Voices in the Air | reaction | has_technology_researched = radio |
| cp_layla.33 | The Cup of Coffee | market pulse | mg:coffee market_goods_import_share |
| cp_layla.34 | The White Sugar | market pulse | mg:sugar market_goods_cheaper |
| cp_layla.35 | The Cloth from the Port | market pulse | mg:luxury_clothes market_goods_buy_orders |
| cp_layla.40 | The Column Returns | reaction | on_war_end (homecoming) |
| cp_layla.41 | The Clerk's Letter | reaction | on_war_end (killed) |
| cp_layla.50 | The Smoke Above the Palm | reaction | first building_textile_mill in her state |
| cp_layla.70 | Cairo Is Calling | crossroads | mill exists + peasant + not serfdom + SoL ≤12 |
| cp_layla.121 | Strangers in the Lane | reaction | law_no_migration_controls |
| cp_layla.122 | The Gate Closes | reaction | law_closed_borders |
| cp_layla.123 | The Market Eats the Village | reaction | law_laissez_faire |
| cp_layla.124 | The Ministry Comes for the Stall | reaction | law_command_economy |

**Dominant feeling**: the outside has breached the walls. Some breaches feed her; some cost her.

### Act IV — The Household at its Peak (matriarch events)

She is older, her children are older, the state now reaches her directly.

| ID | Title | Kind | Trigger |
|----|-------|------|---------|
| cp_layla.24 | Election Day | reaction / pulse | on election (fixed period) |
| cp_layla.60 | The Shutters Close | reaction | on_revolution_start |
| cp_layla.71 | The Small Concern | crossroads | urban + literate + permissive economy |
| cp_layla.72 | The Suitor | crossroads | cp_age≥38 + cp_children≥1 |
| cp_layla.73 | The Mill Closes | crossroads | in_city + laborer + SoL ≤9 |
| cp_layla.90 | The First Envelope | life-beat | first welfare eligibility |
| cp_layla.91 | The New Law | reaction | welfare tier up |
| cp_layla.92 | They Have Taken It Back | reaction | welfare tier down |
| cp_layla.95 | They Are Hiring Women Now | reaction | law_women_in_the_workplace |
| cp_layla.96 | I Am on the Rolls | reaction | law_womens_suffrage |
| cp_layla.97 | Her Own Stall | crossroads | cp_may_work (forced/chosen) |
| cp_layla.98 | The Month Without | absence-bite | long-term shock echo |
| cp_layla.99 | Her Name Is Not on the Deed | absence-bite | rural + male-heir-only |
| cp_layla.102 | The Daughter Reads | life-beat | cp_daughter_at_school |
| cp_layla.103 | The Chains Are Cut | reaction | law_slavery_banned |
| cp_layla.104 | The Compound on the Edge of the Village | ambient pulse | slavery is active |
| cp_layla.105 | Every Man, They Say | reaction | law_universal_suffrage |
| cp_layla.106 | The Poster on the Wall | reaction | law_single_party_state |
| cp_layla.108 | The Doctor at the Mosque | reaction | law_charitable_health_system |
| cp_layla.109 | The Man with the Bag | reaction | law_private_health_insurance |
| cp_layla.110 | The Doctor in the Next Village | reaction | law_public_health_insurance |
| cp_layla.111 | The Guard Has Been Installed | reaction | law_worker_protections |
| cp_layla.112 | The Meeting After Shift | reaction | law_right_to_associate |
| cp_layla.113 | The Strike | pulse | laborer + assoc-law + low-wage |
| cp_layla.114 | The Minaret's Silence | reaction | law_state_atheism |
| cp_layla.116 | The Square Fills and Does Not Empty | reaction | law_right_of_assembly |
| cp_layla.117 | The Letter That Should Not Have Been Written | reaction | law_outlawed_dissent |
| cp_layla.119 | The Station in the Lane | reaction | law_dedicated_police |
| cp_layla.120 | Rifles in the Square | reaction | law_militarized_police |

**Dominant feeling**: she is surrounded by the state at every hour. She has opinions now. She is counted.

### Act V — The Long Evening (mortality + legacy)

She is old. Her body reports back. The last events.

| ID | Title | Kind | Trigger |
|----|-------|------|---------|
| cp_layla.80 | The Last Morning | death | mortality roll |
| cp_layla.81 | The Foreman's Runner | death | Ahmed worker-accident roll |
| cp_layla.82 | The Child | death | child-mortality roll |

Plus the **conversation** cluster, which is Layla's inner life in Act V:

- **cp_conversation.1** — the fantasy audience with the Pasha (opens ~90-day-cooldown)
- **Topic clusters** (each: one opener + three Pasha voices + one closer via .90):
  - **.10-19 The Land** (rural)
  - **.20-23 Ahmed** (married)
  - **.30-33 The Children** (children ≥ 1)
  - **.40-43 The Room** (urban)
  - **.50-53 The Paper** (owns land)
  - **.60-63 What I Think of the Country** (radical OR loyalist)
  - **.70-73 The Mill** (urban laborer)
  - **.80-82 A Small Thing** (always — fallback)
  - **.100-103 The Distance** (SoL ≥ 25)
  - **.110-113 The Envelope** (has welfare)
  - **.120-123 The Rolls** (has voted)
  - **.130-133 The Stall** (self-employed)
  - **.140-143 The River** (rural)
  - **.150-153 The One We Lost** (lost a child)
  - **.160-163 The School** (daughter at school)

**Dominant feeling**: the life is ending; she is the one who names what was felt; the closer walks her back into the kitchen.

---

## 3. The cross-cutting arcs (the threads you pull through)

Acts are vertical. Arcs are horizontal. Every event belongs to at least one arc.

### Arc A — Ahmed (the husband)
- Act I: baseline presence — every rural pulse assumes him next to her
- cp_layla.4 — conscripted
- cp_layla.10 — the letter that has not come
- cp_layla.40 — homecoming
- cp_layla.41 — killed
- cp_layla.81 — worker accident (if he survived war, ended up in a factory)
- All later events branch on `cp_ahmed_alive` value (1 alive, 0 dead)
- `cp_conversation.20-23` is the Ahmed topic

### Arc B — The Land (ownership + tenure)
- cp_layla.12 — under the bey's eye (default serfdom)
- cp_layla.2 — the deed (homesteading granted — `cp_owns_land` set)
- cp_layla.11 — walking the field she owns (pulse, post-.2)
- cp_layla.3 — the bey returns (regression)
- cp_layla.99 — her name is not on the deed (absence-bite — ownership is formal, not hers)
- cp_layla.123 — the market eats the village (the field becomes a company's)
- `cp_conversation.10-19` (Land) and `.50-53` (The Paper) belong here

### Arc C — Literacy (the girl's mouth, then hers)
- Baseline: `cp_literacy = 0` at start
- cp_layla.22 — the younger brother's letter (she cannot read it)
- cp_layla.100 — public schools enacted
- cp_layla.101 — compulsory school (daughter gate)
- cp_layla.102 — the daughter reads
- `cp_conversation.160-163` — The School
- Pop-tick literacy drift can push `cp_literacy` up across years
- Needed by: cp_layla.73 option B (Ahmed apprentices), cp_layla.71 (small concern ownership), cp_layla.96 interpretation

### Arc D — Welfare (the envelope)
- cp_layla.90 — first envelope
- cp_layla.91 — new law (tier up)
- cp_layla.92 — they have taken it back (tier down)
- `cp_conversation.110-113` — The Envelope
- Set by: `cp_receives_welfare`, `cp_welfare_tier`

### Arc E — Women's Rights ladder
- cp_layla.93 — the law catches up to us (law_women_in_the_fields)
- cp_layla.94 — a paper with my name (law_women_own_property)
- cp_layla.95 — they are hiring women now (law_women_in_the_workplace → sets `cp_may_work`)
- cp_layla.96 — I am on the rolls (law_womens_suffrage → sets `cp_has_voted` if she votes)
- cp_layla.24 — election day pulse
- cp_layla.97 — her own stall (crossroads, requires `cp_may_work`)

### Arc F — Slavery
- cp_layla.104 — the compound on the edge of the village (ambient while law is active)
- cp_layla.103 — the chains are cut (law_slavery_banned → one-shot)

### Arc G — Market / Goods (the daily felt economy)
- cp_layla.7 — tax collector (structural)
- cp_layla.8 — price of the loaf (grain consumption tax)
- cp_layla.33 — cup of coffee (imported)
- cp_layla.34 — white sugar (cheap imported)
- cp_layla.35 — cloth from the port (luxury cloth)
- cp_layla.17 — merchant's scale (pulse, distrust of the market)
- cp_layla.98 — the month without (absence-bite, structural hunger)

### Arc H — Church & State
- baseline: state_religion / people_of_the_book / millet (no event)
- cp_layla.115 — procession passes (freedom_of_conscience)
- cp_layla.114 — minaret's silence (state_atheism)
- cp_layla.25 — first day of Ramadan (seasonal; tone varies with church/state)
- cp_layla.27 — Hajj returnees (seasonal)
- cp_layla.107 — Coptic neighbour exhales (multicultural — adjacent)

### Arc I — Free Speech & Dissent
- cp_layla.116 — the square fills and does not empty (right_of_assembly)
- cp_layla.117 — the letter that should not have been written (outlawed_dissent)
- cp_layla.60 — the shutters close (revolution_start)
- `cp_conversation.60-63` — What I Think of the Country

### Arc J — Policing
- cp_layla.119 — the station in the lane (dedicated_police)
- cp_layla.120 — rifles in the square (militarized_police)

### Arc K — Migration
- cp_layla.70 — Cairo is calling (personal crossroads)
- cp_layla.121 — strangers in the lane (no_migration_controls)
- cp_layla.122 — the gate closes (closed_borders)
- `cp_in_city` gates many downstream pulses (.40-43 room topic, .70-73 mill, .119 station)

### Arc L — Industry & Economy
- cp_layla.50 — smoke above the palm (first mill)
- cp_layla.30 — iron horse (railways)
- cp_layla.31 — a word from beyond (telegraph)
- cp_layla.32 — voices in the air (radio)
- cp_layla.123 — market eats the village (laissez_faire)
- cp_layla.124 — ministry comes for the stall (command_economy)
- cp_layla.71 — the small concern (ownership crossroads)
- cp_layla.73 — the mill closes (downturn crossroads)
- cp_layla.81 — the foreman's runner (worker accident)
- cp_layla.111 — the guard has been installed (worker_protections)
- cp_layla.112 — the meeting after shift (right_to_associate)
- cp_layla.113 — the strike

### Arc M — Health & Mortality
- cp_layla.5 — the first cry (survived childbirth)
- cp_layla.82 — the child (child mortality)
- cp_layla.108 — doctor at the mosque (charitable_health)
- cp_layla.109 — the man with the bag (private_health)
- cp_layla.110 — doctor in the next village (public_health)
- cp_layla.80 — the last morning (her death)

### Arc N — Seasonal / Ambient (the year's rhythm)
- cp_layla.13 — a day with no wind
- cp_layla.14 — neighbour's boy
- cp_layla.15 — her mother's left hand
- cp_layla.16 — hen that will not lay
- cp_layla.18 — Friday, the river low
- cp_layla.19 — old woman who sees through walls
- cp_layla.20 — bread that did not rise
- cp_layla.21 — dust on the water
- cp_layla.23 — mule that will not move
- cp_layla.25 — Ramadan
- cp_layla.26 — Nile rises
- cp_layla.27 — Hajj returnees
- cp_layla.28 — midwife's lamp
- cp_layla.29 — date harvest

---

## 4. The conversation layer

`cp_conversation.*` is Act V's interior — the Pasha she invents at the kitchen stool. Root is `cp_conversation.1`. Every topic cluster is: **opener → three Pasha voices → closer (`cp_conversation.90`)**.

| Cluster | Opener | Gate |
|---------|--------|------|
| .10-19 | The Land | rural (peasant OR farmer OR owns_land OR under_serfdom) |
| .20-23 | Ahmed | cp_married |
| .30-33 | The Children | cp_children ≥ 1 |
| .40-43 | The Room | cp_in_city |
| .50-53 | The Paper | cp_owns_land |
| .60-63 | What I Think of the Country | cp_radical > 0 OR cp_loyalist > 0 |
| .70-73 | The Mill | profession=laborers AND cp_in_city |
| .80-82 | A Small Thing | always (fallback) |
| .100-103 | The Distance | cp_sol ≥ 25 |
| .110-113 | The Envelope | cp_receives_welfare |
| .120-123 | The Rolls | cp_has_voted |
| .130-133 | The Stall | cp_self_employed |
| .140-143 | The River | rural |
| .150-153 | The One We Lost | cp_lost_a_child |
| .160-163 | The School | cp_daughter_at_school |

Total conversation events ≈ 63.

---

## 5. Known gaps (Stage 2 will address some)

**Weak callbacks** — events that should remember each other but don't yet:

- **cp_layla.3 (serfdom restored)** should reference cp_layla.2 (the deed), not just describe the bey. When the bey returns, the deed exists somewhere; the event should show her touching it.
- **cp_layla.40 (Ahmed homecoming)** should remember cp_layla.4 (the marching). A year has passed; the clothes don't fit the same way.
- **cp_layla.41 (Ahmed killed)** should remember cp_layla.4. The last thing she saw of him was a back.
- **cp_layla.80 (her death)** should be the only event that remembers EVERYTHING — the rug of .114, the tin of .124, the envelope of .90, the deed of .2. It is the catalogue.
- **cp_layla.91 (welfare up)** and **cp_layla.92 (welfare down)** should both reference .90 — the first envelope is the original story.
- **cp_layla.120 (rifles in square)** should remember .116 (right of assembly). The one repealed the other.
- **cp_layla.117 (outlawed dissent)** should remember .116. The square that didn't empty is now a square that empties.
- **cp_layla.123 (market eats village)** should remember .50 (first mill). The smoke became a company.
- **cp_layla.124 (command economy)** should remember .97 (her own stall) and .123.

**Image orphans** — events sharing the same 8 DDS files:
- Most reaction events currently reuse `cp_layla_intro.dds`, `cp_layla_neighbours_boy.dds`, `cp_layla_serfdom_restored.dds`, `cp_layla_homesteading.dds`, `cp_layla_no_wind.dds`, `cp_layla_mothers_hand.dds`. Stage 3 will write per-event prompts so every event can have its own image.

**Missing events worth adding in a later slice** (not Stage 1–4's scope):
- A first-rain event (the felt body of the delta changing season)
- A letter-FROM-the-daughter-in-Cairo pulse (after .70 option A is chosen)
- A grandchild-born event (sequel to .72)
- A Layla-returns-to-visit-her-old-village event (urban, sequel to .70)

---

## 6. How this doc is used

- **When adding a new event**: place it under the right act AND at least one arc. If it doesn't fit any arc, ask whether it should exist at all.
- **When debugging narrative**: grep this file for the event ID. The table tells you what context to expect.
- **When regenerating images**: the arc tells you what the image register should be. A rural pulse image is not a city-laborer image, even if the composition is similar.
- **When the user asks "is this shipping?"**: the act/arc coverage in this file is the answer. We are Act-I–IV-saturated. Act V is Layla's death + the conversation tree, which is written but not yet deeply imaged.

---

**Last updated: 2026-04-19.** Rev 1 — initial pass. Update this file whenever a slice ships.
