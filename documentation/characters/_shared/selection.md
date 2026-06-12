# Person Selection Infrastructure

Common People should never have a "Layla lane" and a "everyone else lane." The active rule is:

- every person is registered through the shared registry
- every person setup/spawn path triggers that person's hidden setup event
- every person exposes the same dispatcher hook surface, even if some hooks
  are no-ops until that person's content exists
- person-variable writes live in `cp_<name>_*` files, not shared on-actions
- every person has a person-owned `cp_<name>_dispatch_yearly`
- every visible person event is covered by the shared QA generator
- every ambient appearance enters through `cp_roll_for_event`
- every router/gatekeeper alive check goes through `cp_person_is_alive`
- each person's chance is shaped by the current game, not by hand preference

## First Contact Model

Game start has one shared visible-person roll: `cp_shared_startup.2`.
`cp_shared_startup.1` registers and initializes the always-on roster first,
then runs a one-day startup scan for conditional people whose world gates are
already true for the selected start date or save state. Their setup events
suppress their own immediate visible intro during that scan, so
`cp_shared_startup.2` still picks one clean opener. Layla is one candidate in
the first-contact table, not the campaign owner. No person-owned hidden setup
event may directly claim the campaign opening.
The dev gate enforces the shape of that roll: at least sixteen possible
visible openers overall, at least six always-on visible openers when no
conditional startup gate succeeds, and no one person above twenty percent of
first-contact weight in either calculation.
When a visible opener fires, its branch calls `cp_mark_first_contact_budget`
first. The opener therefore starts the same 183-day global / 365-day
per-person cooldown lane as ambient and law-reaction events, so the first
campaign year stays within the 1-2 routine automatic event target.

Conditional entrants are different: they are born from a game-state trigger.
Samier and Tarek can appear when factories make their lives legible, and their
own setup events may roll an immediate first appearance after non-startup
spawn. That is still person-owned routing: the factory condition chooses who
can enter, then the person file decides whether this is the moment the player
meets them.
Karim does the same for machine tools and engines. Farid does it for railways
and telegraphy. Dawud does it for ports, steamships, and cargo cranes. Rashid
does it for government administration, archives, and identity papers. Salma
does it for electric service, telephone networks, and radio. Huda does it for
urban growth, construction, trade centers, and city-planning technologies.
Mansur does it for factory migration, where manufacturing and city pull make
rural wage work legible. Nabil does it for policing, dissent, assembly, and
revolution. The shared startup, yearly, technology, building, law, and
revolution hooks call conditional spawn checks where relevant, so game-state
changes can introduce people soon after their lives become legible instead of
waiting for a Layla-owned milestone lane.

## Monthly Appearance Model

`cp_roll_for_event` in `mod/common/scripted_effects/cp_shared_firing.txt` runs monthly. It uses one active weighted branch per registered person, plus a positive silent branch. The branch choice answers: "whose life is most legible in this game state?"
The 183-day global cooldown is the hard pacing cap: the shared roster can
surface at most two routine automatic beats in a normal in-game year,
regardless of how many people are alive.

The shared context sensors live in `mod/common/scripted_triggers/cp_shared_sensors.txt`:

- `cp_era_before_1850`, `cp_era_1850_to_1880`, `cp_era_after_1880`
- `cp_country_has_manufacturing`
- `cp_country_has_factory_migration`
- `cp_country_has_machine_industry`
- `cp_country_has_rail_infrastructure`
- `cp_country_has_telegraph`
- `cp_country_has_port`
- `cp_country_has_steam_trade`
- `cp_country_has_government_office`
- `cp_country_has_modern_records`
- `cp_country_has_electric_service`
- `cp_country_has_telephone_network`
- `cp_country_has_urban_growth`
- `cp_country_has_public_order_pressure`
- `cp_country_old_land_order`
- `cp_country_workers_unprotected`
- `cp_country_women_property_rights`
- `cp_country_public_schools`
- `cp_country_public_health`

Those sensors are deliberately broad. The shared router picks the person; the person's own `cp_roll_ambient_<name>` pool picks the exact event. Every branch starts with `cp_person_is_alive = { person = <name> }`, which checks both the global registry flag and the local country variable.

## Lifecycle Model

The shared on-actions in `mod/common/on_actions/cp_on_actions.txt` are intentionally thin. They should only guard the country/person and call person-owned dispatchers:

```
cp_<name>_dispatch_yearly = yes
```

Every registered person defines the same hook names:

```
cp_<name>_dispatch_startup
cp_<name>_dispatch_monthly
cp_<name>_dispatch_law_enacted
cp_<name>_dispatch_yearly
cp_<name>_dispatch_war_started
cp_<name>_dispatch_war_end
cp_<name>_dispatch_tech
cp_<name>_dispatch_building
cp_<name>_dispatch_revolution
```

Hooks with no content call `cp_person_hook_noop = yes`. That is intentional: the shape is the same for every person, while the amount of authored story can differ. The person file owns everything that makes that life progress: age, SoL refresh, literacy drift, annual milestone rolls, death pressure, and household state. Layla now follows this same rule through `cp_layla_dispatch_yearly`; her larger event surface is content, not a separate infrastructure lane.

The same ownership rule applies to startup and monthly display state. Shared on-actions may guard a country/person and call `cp_<name>_dispatch_startup`, `cp_<name>_dispatch_monthly`, or another person-owned dispatcher, but they must not directly `set_variable` / `change_variable` / `remove_variable` on `cp_<name>_*`. The static audit enforces this so a prototype cannot silently become a permanent special lane.

Shared law moments that can belong to more than one person should use a
weighted resolver before person-owned dispatchers run. Public-order laws use
`cp_roll_public_order_law_reaction`, which chooses between Layla's street-level
law beats and Nabil's watchman beats and then sets
`cp_shared_public_order_law_handled` so the later person-owned law dispatchers
cannot open a second event for the same law.

## Current Weight Intent

Layla is the early agrarian anchor and remains present later at a lower weight.

The Bey is strongest before 1860 while Serfdom or Tenant Farmers still define the countryside.

Yusuf rises when war has actually touched the roster.

Samier rises with manufacturing, especially while workers have no protections.

Tarek rises when factories exist and the old land order has receded.

Karim rises when machine tools, steel, and engines make skilled factory labor
part of ordinary work.

Farid rises when railways and telegraphy make infrastructure part of ordinary
work.

Dawud rises when ports, steamships, and cranes make trade part of ordinary
work.

Rashid rises when government offices, archives, and identity papers make the
state part of ordinary paperwork.

Salma rises when electricity, telephones, and radio make communication part of
ordinary clerical labor.

Huda rises when construction, trade centers, sewers, roads, and planning make
the city a rented-room problem instead of a map color.

Mansur rises when manufacturing plus city growth makes rural-to-factory
migration visible through wages, boarding rooms, and money sent home.

Nabil rises when policing, dissent, public assembly, and revolution make
ordinary streets part of state power.

Nour rises around women's property rights.

Mina rises around schools, print, and the mid/late century.

Zaynab rises while public health is absent and household medicine still carries the burden.

## Adding A Person

When adding an always-on person, add them to `cp_shared_startup.2` only if they
should be eligible to become the first visible face of a campaign. When adding
a conditional person, call their `cp_<name>_try_spawn` from the startup scan if
their conditions can already be true at game start, add their intro to
`cp_shared_startup.2`, and keep their non-startup first-appearance chance in
the person-owned setup path that made them eligible.

For long-run appearances, add their branch to `cp_roll_for_event` using shared
sensors first. Add a new shared sensor only when the same idea will matter to
more than one person. Keep their own event-specific details inside
`cp_roll_ambient_<name>`.

After changing visible events or router structure, run:

```bash
python3 script/generate-person-debug-wrappers.py --check
python3 script/audit-event-pacing.py
python3 script/build-person-selection-ledger.py --check
python3 script/build-person-contract-ledger.py --check
python3 script/build-event-firing-ledger.py --check
python3 script/build-world-response-ledger.py --check
script/audit-person-roster.py
script/audit-common-people.py
```
