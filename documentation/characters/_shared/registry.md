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

3. **State marker** on their home state: `cp_<name>_lives_here`. Used by `cp_refresh_sol_from_pop` to find the cohort.

Country variables survive save/reload without ceremony. The `$person$` token makes all primitives reusable.

## Registering a person

From a startup event (or a conditional event later — e.g. a French physician only after France gains a colonial interest in Egypt):

```
cp_register_person = {
    person = layla
    country = EGY
    culture = misri
    religion = sunni
    home_state = STATE_LOWER_EGYPT
    profession = peasants
    age = 22
}
```

This sets the global registry flags. **Country-variable initialisation is done separately** by that person's own startup event (e.g. `cp_startup.1` for Layla). This way, `cp_register_person` stays minimal and each person's rich init can do whatever they need.

## Registering a second person

1. Create `mod/events/cp_<name>_events.txt`, `cp_<name>_conversation_events.txt`, `cp_<name>_memory.txt`, `cp_<name>_buttons.txt`, `cp_<name>_journal_entries.txt`, `cp_<name>_l_english.yml`, `cp_<name>_custom_loc.txt`, `cp_<name>_sensors.txt`.
2. Add a `cp_register_person = { person = <name> country = <tag> ... }` call to `cp_shared_startup.1` in `mod/events/cp_shared_startup_events.txt`.
3. Add their dispatch blocks: one `if { limit = { has_global_variable = cp_person_<name>_alive ... } cp_<name>_dispatch_<hook> = yes }` per hook in `cp_on_actions.txt`.
4. Create their per-person cohort wrapper in `cp_<name>_memory.txt`:
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
5. Write their events. Wrap fires in `cp_try_fire_*` (see `firing.md`).

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

## Do not add

Do not register Ahmed (Layla's husband), the Bey's secretary, or any other "household furniture" character as a person. A person in the registry:
- has their own events
- has their own JE
- has their own button
- has their own ambient pool

Otherwise they're just variables on the primary person's block (e.g. `cp_layla_ahmed_alive`).
