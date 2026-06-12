# Huda al-Matariya

Huda is a conditional urban-growth person: a Misri lodger and day laborer who
appears when construction, trade centers, urban planning, sewerage, or late city
growth make rented rooms part of the player's Egypt.

She exists to cover a lane Layla should not own: the move from village scarcity
to city pressure. Her story is not "modernity is good" or "the city is bad." It
is rent due on Thursday, water carried upstairs, bricks stacked beside a street
that used to be wide enough for shade.

## Game Hooks

- Token: `huda`
- Country: `EGY`
- Culture/religion: `misri` / `sunni`
- Home state: selected from the actual urban-growth state when possible, with `STATE_LOWER_EGYPT` as the default fallback.
- Work/pop cohort: urban laborer / day laborer, using the shared urban workplace profile.
- Enters through `cp_huda_try_spawn`, with a 45/55 chance each eligible check.
- Eligibility comes from `cp_country_has_urban_growth`.
- Called from yearly, technology, and building dispatch so she can appear after
  the relevant world-state changes rather than at every campaign start.
- Ambient appearances route through `cp_roll_for_event`, under the shared
  global/person cooldown budget.

## Event Surface

- `cp_huda.10` -- intro, the rented room over the alley.
- `cp_huda.20` -- construction and street disruption.
- `cp_huda.30` -- modern sewerage / clean water as domestic relief.
- `cp_huda.40` -- rent pressure as the city grows around her.
- `cp_huda.50` -- roof leaks and the fragility of rented shelter.
- `cp_huda.60` -- paved roads, dust, and city improvement at the threshold.

All visible events use authored Huda-specific GPT-image-2 stills with the
important face/action/object kept in the left or center-left event-window safe
area. Vanilla motion plates were removed after runtime testing showed they read
as generic footage under the text panel.
