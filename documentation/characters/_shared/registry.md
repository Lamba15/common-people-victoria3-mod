# Person registry — the protocol

**How a new person joins the mod.**

## The concept

A "person" in Common People is a narrative object owned by the mod — a character whose life we narrate through events, not a V3 `character` entity. Each person has:

- a **name token** (lowercase, e.g. `layla`, `bey`, `pierre`), used as the `$person$` parameter everywhere
- a **country** they live in (their events fire when that country scope matches)
- a **culture, religion, profession** (bakes into cohort reads at load time)
- a **home state** (a state-region pointer stored as `cp_<person>_lives_here`)
- a **starting age**

## Where the person's data lives

1. **Global registry flags** (cross-country): `cp_person_<name>_alive`, `cp_person_<name>_country`. Set by `cp_register_person`. Read by the shared dispatcher to know which persons exist.

2. **Country variables** on the person's current country, all prefixed with the name token:
   - `cp_<name>_alive` — 1 while they live
   - `cp_<name>_age`, `cp_<name>_hope`, `cp_<name>_exhaustion`, `cp_<name>_sol`, `cp_<name>_literacy`, `cp_<name>_radical`, `cp_<name>_loyalist`
   - `cp_<name>_profession_<poptype>` — flag set (peasants, laborers, etc.)
   - `cp_<name>_w_<topic>` — weight variables (revolution, land_reform, etc.)
   - `cp_<name>_opinion_<tag>` — nation-opinion variables
   - `cp_<name>_seen_<id>` — timed event-seen flags
   - `cp_<name>_recent_joy`, `cp_<name>_recent_hardship` — timed mood flags
   - Plus household furniture (e.g. `cp_layla_ahmed_*` for Layla's husband — Ahmed is not a registered person, just narrative objects owned by Layla)

3. **State marker** on their home state: `cp_<name>_lives_here`, plus a country-side pointer `cp_<name>_state_pointer` for journal localization. Setup must call `cp_set_person_home_state = { person = <name> country = <tag> state = <STATE> }` or `cp_set_person_home_state_from_spawn_marker_or_default = { person = <name> country = <tag> state = <STATE> }`, which clears any previous marker, plants exactly one new marker, and stores the selected region_state pointer for the shared journal's `State` line. Building-triggered conditional spawns should first call `cp_mark_building_spawn_home = { person = <name> }` in building scope, so the new person inherits the actual building state instead of the default. Startup/yearly/technology conditional spawns whose eligibility depends on local buildings must call the matching `cp_mark_person_spawn_home_from_<profile>` effect before `cp_register_person`, so an already-built factory, railway, port, office, power plant, or urban center can place the person in the relevant state. `cp_refresh_sol_from_pop` reads this marker, so a factory in Lower Egypt can only reach people whose marker is in Lower Egypt.

4. **Home-place and workplace profile** on the country: `cp_<name>_home_place_<token>` and `cp_<name>_workplace_<profile>`. Setup must call `cp_set_person_home_place = { person = <name> place = <token> }` and `cp_set_person_workplace_profile = { person = <name> profile = <profile> }`; both shared setters clear old tokens before assigning the new one, so a living person has exactly one home place and exactly one workplace profile. Local building dispatchers use `cp_building_affects_person_workplace`, which requires both the person's home state and a matching workplace profile. This keeps "built a factory in Lower Egypt" from becoming "every person in Egypt gets a factory story"; only factory/workshop lives in that state should react.

Country variables survive save/reload without ceremony. The `$person$` token makes all primitives reusable.

## Registering a person

From a startup event (or a conditional event later — e.g. a French physician only after France gains a colonial interest in Egypt):

```
cp_register_person = {
    person = layla
    country = EGY
}
```

This sets the two global registry flags (`cp_person_<name>_alive` and `cp_person_<name>_country`). **Country-variable initialisation is done separately** by a hidden setup event/effect for that person, which bakes in culture / religion / home_state / profession / starting age as literals. Always-on persons register in `cp_shared_startup.1` and then trigger their hidden setup event from the same startup path; Layla now uses `cp_layla_setup.1`, so her setup is person-owned like the rest of the roster.

On startup/reload, wrap each registration so a person whose local `cp_<name>_alive` variable is already `0` is not resurrected as a global alive flag:

```
if = {
    limit = {
        OR = {
            NOT = { has_variable = cp_<name>_alive }
            AND = {
                has_variable = cp_<name>_alive
                var:cp_<name>_alive > 0
            }
        }
    }
    cp_register_person = { person = <name> country = <TAG> }
}
```

**Why only two args?** V3's script compiler rejects scripted_effects that declare macro parameters the body doesn't reference. Since `cp_register_person` only touches `$person$` and `$country$`, only those two can be passed — extra args break compilation silently (every call to the effect becomes a no-op).

## Registering another person

1. Create the required person files: `mod/events/cp_<name>_events.txt`, `mod/common/scripted_effects/cp_<name>_memory.txt`, and `mod/localization/english/cp_<name>_l_english.yml`. Do not add a per-person JE by default; the persistent journal surface is shared by `cp_je_common_people`.
2. For always-on persons, add a death-safe `cp_register_person = { person = <name> country = <tag> }` block to `cp_shared_startup.1` in `mod/events/cp_shared_startup_events.txt`, followed by `trigger_event = { id = cp_<name>.1 }` or `trigger_event = { id = cp_<name>_setup.1 }` for the hidden setup event. Conditional persons do the same register-then-setup sequence in `cp_<name>_try_spawn`, and the relevant shared hooks call that spawn effect whenever the world state might have become true.
3. Add their dispatch blocks: one lean `if { limit = { c:<TAG> ?= this  cp_person_is_alive = { person = <name> } ... } cp_<name>_dispatch_<hook> = yes }` per hook in `cp_on_actions.txt`, plus the shared war helper if the hook enters EGY through `cp_shared_war.txt`.
4. Add their context-weighted monthly branch to `cp_roll_for_event` in `cp_shared_firing.txt` using the shared sensors documented in `selection.md`.
5. Create any reusable shared sensor in `cp_shared_sensors.txt` only if more than one person can plausibly use it; otherwise keep details inside the person file.
6. Create their per-person cohort wrapper in `cp_<name>_memory.txt`:
   ```
   cp_<name>_refresh_sol = {
       cp_refresh_sol_from_pop = {
           person = <name>
           culture = <culture>
           religion = <religion>
           poptype = <starting-profession>
       }
   }
   ```
7. Create `cp_<name>_dispatch_yearly` in `cp_<name>_memory.txt`. It should at minimum call `cp_age_increment = { person = <name> }`, `cp_<name>_refresh_sol = yes`, and `cp_person_yearly_lifecycle = { person = <name> country = EGY }` unless the person has a bespoke authored death/milestone path like Layla.
8. Write their events. Wrap fires in `cp_try_fire_*` (see `firing.md`).

## Dying

```
cp_person_dies = {
    person = <name>
    country = <tag>     # where they lived at death
}
```

Clears the `cp_<name>_alive` country var and the `cp_person_<name>_alive` global. **Other variables stay** so post-death prose (e.g. "The Forty Days") can still read them.

## V3 syntax constraints

- `$person$` is a **load-time macro substitution**, not runtime. `cp_$person$_hope` becomes literal `cp_layla_hope` at each callsite.
- `culture = cu:$culture$` — only works if `$culture$` is a literal passed in at the callsite. Per-person wrappers are the idiomatic way to bake these in.
- `c:$country$` — same constraint. Use per-person wrappers for country-scoped effects.
- `has_global_variable` works inside on-action effects; timed globals (`set_global_variable = { ... days = N }`) confirmed working in vanilla (`hungry_forties_var` in `game/common/on_actions/00_code_on_actions.txt`).
- Shared on-actions should not write `cp_<name>_*` variables directly. Put startup migrations, monthly JE/display state, yearly lifecycle, and hook-specific mutations in the person's `cp_<name>_memory.txt`, then call a `cp_<name>_dispatch_*` effect from the shared router.
- `script/build-person-contract-ledger.py --check` enforces the live roster contract from script: hidden setup must initialize baseline life variables, profession, and home marker; every dispatcher hook must exist and be called; yearly dispatch must age and refresh SoL; visible events must have audio, image, and generated QA coverage; and conditional entrants must keep visible and silent first-appearance weights. The generated proof lives at `documentation/person-contract-ledger.md`.
- `python3 script/build-person-hook-ledger.py --check` classifies what every dispatcher hook actually does (`noop`, lifecycle maintenance, law reaction, world response, milestone, or raw trigger) and fails if a visible event bypasses the shared gatekeepers. The generated proof lives at `documentation/person-hook-ledger.md`.

## Do not add

Do not register Ahmed (Layla's husband), the Bey's secretary, or any other "household furniture" character as a person. A person in the registry:
- has their own events
- has their own ambient pool
- has the standard dispatcher hook surface
- may have their own conversation tree if the content warrants it; per-person JEs/buttons require an explicit design exception because the default persistent UI is shared.

Otherwise they're just variables on the primary person's block (e.g. `cp_layla_ahmed_alive`).
