# Motion Art Ledger

Generated from live event script. Rebuild with `python3 script/build-motion-art-ledger.py`.

This ledger records visible non-debug events that use Victoria 3 `.bk2` event videos. Still-image events remain covered by the image inventory and art provenance audits.

## Summary

- Visible non-debug events: 356
- Motion events: 0
- Custom/mod motion events: 0
- Vanilla video placeholder debt: 0
- Persons with motion events: 0
- Persons with vanilla video debt: 0
- Known event videos: 244
- Mod-shipped custom videos: 0
- Event window video support: yes
- Issues: 0

## Person Counts


## Vanilla Video Debt by Person

- none

## Video Reuse


## Vanilla Video Reuse

- none

## Motion Events

| Event | Person | Title | Video | Status | Source |
|---|---|---|---|---|---|

## Rules

- Use `event_image = { video = "<vanilla_or_mod_bk2>" }` only for known `.bk2` assets that resolve in `script/audit-event-motion.py`.
- Treat vanilla videos as temporary development placeholders. Release builds must pass `script/audit-generic-video-art.py --strict-no-vanilla-video`.
- Do not mix `texture` and `video` inside one `event_image` block.
- Use motion for public, institutional, technological, or crowd-scale beats. Use reviewed GPT stills for intimate person scenes.
- Custom moving GPT images need a real `.bk2` export path before they can be promoted into `mod/gfx/event_pictures/`.

## Checks

```bash
python3 script/build-motion-art-ledger.py --check
script/audit-event-motion.py
script/audit-generic-video-art.py --strict-no-vanilla-video
script/audit-event-images.py --strict-size --strict-unused
```
