# Layla Story Map

Status: current r5/r6 map. The old `cp_conversation.*` tree has been removed from the shipped event tree.

Current audit evidence:

- `cp_layla.*`: 85 event definitions in `mod/events/cp_layla_events.txt`
- `cp_layla_setup.*`: 1 hidden setup definition in `mod/events/cp_layla_setup_events.txt`
- `cp_layla_vox.*`: 192 event definitions in `mod/events/cp_layla_vox_events.txt`
- Layla-owned total: 278 events, 267 visible windows, 267 debug-visible windows
- Source of truth for counts: `script/audit-person-roster.py --show-missing-debug`

This file is a narrative map, not the firing contract. For mechanical onboarding and dispatch rules, use:

- `documentation/characters/_shared/registry.md`
- `documentation/characters/_shared/firing.md`
- `documentation/characters/_shared/adding-a-new-person.md`
- `documentation/characters/layla/conversation.md`

## Shape Of The Life

Layla begins in 1836 as a 22-year-old Misri Sunni peasant woman in Lower Egypt. She is a person-object owned by the mod, not a Victoria 3 `character` entity. Her state lives in country variables with the `cp_layla_` prefix.

The current story is not a single linear biography. It is a life surface: law reactions, seasonal pulses, mortality, family changes, state drift, and the `cp_layla_vox.*` voice layer all choose from the state she has actually lived through.

## Event Families

### `cp_layla.*`

Core visible life events:

- Hidden setup: `cp_layla_setup.1`
- Introduction: `cp_layla.1`
- Land and law reactions: `cp_layla.2`, `.3`, `.7`, `.8`, `.93..124`
- War and Ahmed milestones: `cp_layla.4`, `.10`, `.40`, `.41`, `.81`
- Household and ambient life beats: `cp_layla.5`, `.6`, `.11..29`, `.33..35`
- Industry, migration, and crossroads: `cp_layla.50`, `.70..73`, `.97`, `.123`, `.124`
- Welfare and state support: `cp_layla.90..92`, `.108..110`
- Rights, policing, dissent, religion: `cp_layla.24`, `.95`, `.96`, `.105..120`
- Mortality and afterlife of the household: `cp_layla.80`, `.82`, `.83`, `.125..128`

### `cp_layla_vox.*`

The legacy conversation/interiority layer formerly opened by **A word between**. It is now debug-review/salvage material until a shared roster-level conversation lane exists:

- Ahmed: `10` picker, `11..16`, `19`
- Daughter / children: `20` picker, `21..25`, `29`
- Her mother: `30` picker, `31..35`, `39`
- Um Yusuf: `40` picker, `41..44`, `49`
- Umm Mariam: `50` picker, `51..54`, `59`
- The Bey: `60` picker, `61..65`, `69`
- Factory owner / mill world: `70` picker, `71..75`, `79`
- Stranger: `80` picker, `81..86`, `89`
- Herself / God: `90` picker, `91..96`, `99`
- The ruler: `100` picker, `101..106`, `109`

Follow-ups use the `scenario * 100 + branch` pattern, e.g. `cp_layla_vox.1021`.

## Acts

### Act I - The Young Wife

The house, the lane, the field, the canal. This act covers early marriage, childbirth, mother-memory, small household pressure, and first rural pulses.

Representative events: `cp_layla.1`, `.5`, `.6`, `.11..23`, `.25..29`.

Representative variables: `cp_layla_age`, `cp_layla_children`, `cp_layla_hope`, `cp_layla_profession_peasants`, `cp_layla_literacy`.

### Act II - The Claim On Land

Land law is the first large force that can change her household. Homesteading, serfdom restoration, taxes, ownership, and exclusion from the deed all live here.

Representative events: `cp_layla.2`, `.3`, `.7`, `.8`, `.93`, `.94`, `.99`, `.123`.

Representative variables: `cp_layla_owns_land`, `cp_layla_under_serfdom`, `cp_layla_seen_homesteading`, `cp_layla_seen_not_on_deed`.

### Act III - The World Arrives

War, railways, telegraph, radio, textiles, imported goods, migration, and factory work begin to push through the village wall.

Representative events: `cp_layla.4`, `.30..35`, `.40`, `.41`, `.50`, `.70`, `.71`, `.73`, `.121`, `.122`.

Representative variables: `cp_layla_ahmed_at_war`, `cp_layla_ahmed_alive`, `cp_layla_in_city`, `cp_layla_profession_laborers`, `cp_layla_ahmed_profession_laborer`.

### Act IV - The Counted Woman

Layla is older and the state now reaches the household directly: welfare, votes, education, health, policing, assemblies, dissent, and women's rights.

Representative events: `cp_layla.24`, `.90..97`, `.100..120`.

Representative variables: `cp_layla_has_voted`, `cp_layla_receives_welfare`, `cp_layla_literacy`, `cp_layla_radical`, `cp_layla_loyalist`.

### Act V - The Long Evening

Mortality, widowhood, old age, memory, and the transfer of the household forward.

Representative events: `cp_layla.80`, `.81`, `.82`, `.83`, `.125..128`, plus the older-weighted `cp_layla_vox` scenes.

Representative variables: `cp_layla_alive`, `cp_person_layla_alive`, `cp_layla_ahmed_alive`, `cp_layla_recent_hardship`, `cp_layla_recent_joy`.

## Cross-Cutting Arcs

### Ahmed

Starts as a narrative husband, not a separate registered person. His state gates war, homecoming, death notice, mill work, and many `cp_layla_vox.10..19` scenes.

Key variables: `cp_layla_ahmed_alive`, `cp_layla_ahmed_at_war`, `cp_layla_ahmed_profession_laborer`.

### Land

The deed, serfdom rollback, bey's pressure, exclusion from legal ownership, and commercialized agriculture all return to the same question: who gets to name the field?

Key variables: `cp_layla_owns_land`, `cp_layla_under_serfdom`, `cp_layla_profession_peasants`, `cp_layla_profession_farmers`.

### Literacy And Daughter

Public schools, compulsory school, daughter-reading beats, letters, and the child/daughter interlocutor all depend on whether reading has reached the household.

Key variables: `cp_layla_literacy`, `cp_layla_children`, `cp_layla_daughter_at_school`.

### Welfare And Health

The first envelope, welfare tier movement, charitable care, private insurance, and public health are written as practical household encounters, not policy summaries.

Key variables: welfare and health seen-flags in `cp_layla_memory.txt`; current law checks in dispatchers.

### Politics, Dissent, And Police

The vote, single-party state, assemblies, outlawed dissent, dedicated police, and militarized police shape whether she becomes more loyal, radical, exhausted, or careful.

Key variables: `cp_layla_has_voted`, `cp_layla_radical`, `cp_layla_loyalist`, `cp_layla_exhaustion`.

### Work And The City

The first mill, Cairo crossroads, mill closure, labor protections, association rights, and strike material decide whether Layla's household is still land-shaped or wage-shaped.

Key variables: `cp_layla_in_city`, profession markers, Ahmed laborer markers, and SoL variables.

## Current Production Gaps

- Art: 95 active Layla DDS references still have no generated source coverage. v0.7 has 11 audited prompt exports but 0/11 generated/shipped replacements.
- Runtime: static/dev checks pass, but current runtime proof is pending because the game has not been relaunched against the latest mod tree.
- Prose QA: `cp_layla_vox.*` is broad enough to need in-game spot checks across multiple eras and law states.
- Future roster scale: Layla is now one person among sixteen registered persons, but she remains the only full-depth life. New persons have working scaffolds and first event sets, not Layla-scale story surfaces.
