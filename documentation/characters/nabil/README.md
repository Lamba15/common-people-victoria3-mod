# Nabil al-Haras

Nabil is a conditional public-order person: a Misri night watchman who appears
when policing, dissent, assembly, or revolution makes state force visible in the
street.

He is not meant to be the state, and he is not meant to be the crowd. He is the
man between them, paid badly enough to fear both sides and old enough to know
when a quiet lane has learned a new sound.

## Game Hooks

- Token: `nabil`
- Country: `EGY`
- Culture/religion: `misri` / `sunni`
- Home state: `STATE_LOWER_EGYPT`
- Work/pop cohort: night watchman / public-order worker, using the shared public-service workplace profile.
- Enters through `cp_nabil_try_spawn`, with a 40/60 chance each eligible check.
- Eligibility comes from `cp_country_has_public_order_pressure`.
- Called from yearly, law-enactment, and revolution dispatch so law changes and
  political rupture can introduce him.
- Ambient appearances route through `cp_roll_for_event`, under the shared
  global/person cooldown budget.

## Event Surface

- `cp_nabil.10` -- intro, the night lamp at the corner.
- `cp_nabil.20` -- dedicated police / station paperwork.
- `cp_nabil.30` -- militarized police or outlawed dissent.
- `cp_nabil.40` -- assembly or revolution aftermath.
- `cp_nabil.50` -- personal night patrol, returning a lost child.
- `cp_nabil.60` -- dedicated-police bureaucracy, the complaint bench.

All visible events use authored Nabil-specific GPT-image-2 stills with the
important face/action/object kept in the left or center-left event-window safe
area. Vanilla motion plates were removed after runtime testing showed they read
as generic footage under the text panel.
