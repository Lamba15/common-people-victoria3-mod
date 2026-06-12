# Mansur al-Mahalla

Mansur is a conditional factory-migration person: a young Misri laborer who
appears when manufacturing and urban pull make leaving the village for wage
work part of the player's Egypt.

He exists to cover a lane Layla, Samier, Tarek, and Karim should not own. Layla
is still rooted in land. Samier carries labor-law anger. Tarek owns the mill
ledger. Karim owns skill at the machine bench. Mansur is the first week in a
loom room, the mat beside spare bobbins, the first wage token, and the money
sent home by a driver who may not know the village road.

## Game Hooks

- Token: `mansur`
- Country: `EGY`
- Culture/religion: `misri` / `sunni`
- Home state: selected from the actual manufacturing/factory-migration state when possible, with `STATE_LOWER_EGYPT` as the default fallback.
- Work/pop cohort: factory laborer, using the shared manufacturing workplace profile and later machine-industry checks.
- Enters through `cp_mansur_try_spawn`, with a 42/58 chance each eligible check.
- Eligibility comes from `cp_country_has_factory_migration`, which combines
  manufacturing, urban growth, machine industry, and the mid/late century.
- Called from yearly, technology, and building dispatch so he can appear after
  factories become real rather than at every campaign start.
- Ambient appearances route through `cp_roll_for_event`, under the shared
  global/person cooldown budget.

## Event Surface

- `cp_mansur.10` -- intro, the mat beside the loom room.
- `cp_mansur.20` -- first wage token and remittance arithmetic.
- `cp_mansur.30` -- machine-belt injury as the rhythm of work.
- `cp_mansur.40` -- money sent home by road.
- `cp_mansur.50` -- bed rent in worker lodging.
- `cp_mansur.60` -- the meal tin and shift hunger.

All visible events use authored Mansur-specific GPT-image-2 stills with the
important face/action/object kept in the left or center-left event-window safe
area. Vanilla motion plates were removed after runtime testing showed they read
as generic footage under the text panel.
