# Superseded event picture archive - v0.6

This folder holds shipped DDS files removed from `mod/gfx/event_pictures/` because a newer generated candidate replaced them.

Current contents:

- `cp_layla_conversation_audience_v05.dds` — superseded by `cp_layla_conversation_audience_v06.dds`.
- `cp_layla_ahmed_conscripted_v05.dds` — superseded by `cp_layla_ahmed_conscripted_v06.dds`.
- `cp_layla_clerks_letter_v05.dds` — superseded by `cp_layla_clerks_letter_v06.dds`.
- `cp_soldier_return.dds` — superseded by `cp_soldier_return_v02.dds`.
- `cp_bey_commercialized.dds` — superseded by `cp_bey_commercialized_v02.dds`.
- `cp_layla_intro_v05.dds` — superseded by `cp_layla_intro_v06.dds`.

The source PNGs and contact sheet for the v0.5 candidate remain under `image/generated/layla/v0.5/`. Keep this folder out of the shipped mod tree so `script/audit-event-images.py --strict-size --strict-unused` stays green.
