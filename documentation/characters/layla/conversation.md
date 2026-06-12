# Layla Voice System

Status: legacy Layla-only conversation design, retained for debug review and future salvage.

The old `cp_conversation.*` audience tree is gone from the shipped event tree. Layla's `cp_layla_vox.*` layer still exists, but the Layla-only JE button **A word between** has been retired because the persistent journal surface is now shared by the roster. Do not re-add a Layla-only button. The next version of this system should be a shared conversation lane that can choose any eligible person.

This button is not a menu and the player is not cast as the ruler. The player witnesses a scene and steers Layla's answer inside it. The surprise is the point: one click might bring Ahmed home from the fields, another her mother in memory, another the Bey, another the ruler's room, another only Layla speaking to herself.

## Runtime Flow

1. Debug selectors or future shared conversation infrastructure choose a Layla-vox picker.
2. `cp_layla_roll_interlocutor` in `mod/common/scripted_effects/cp_layla_memory.txt` remains as legacy routing material.
3. Rolls one eligible interlocutor with `random_list`
4. Fires a hidden scenario picker: `cp_layla_vox.10`, `.20`, `.30`, ... `.100`
5. The picker opens one visible scenario and its branch follow-ups
6. The scenario sets cooldowns and seen-flags so the same scene does not repeat too quickly

All entry points from the button use `cp_button_fire`; direct `trigger_event` is allowed only inside a scene chain after the first visible popup is already open.

## Interlocutors

| Index | Interlocutor | Gate / Weight Shape |
|---:|---|---|
| 10 | Ahmed | Requires `cp_layla_ahmed_alive > 0`; high weight while alive |
| 20 | Daughter / children | Requires `cp_layla_children > 0` |
| 30 | Her mother | Always eligible; memory/interiority |
| 40 | Um Yusuf | Rural neighbour; not city |
| 50 | Umm Mariam | Rural + Layla owns land |
| 60 | The Bey | Serfdom, ownership, or peasant pressure |
| 70 | Factory owner / mill world | Laborer, machinist, or Ahmed laborer state |
| 80 | Stranger | Always eligible, low weight |
| 90 | Herself / God | Always eligible, inward scenes |
| 100 | The ruler | Always eligible, low weight; era-aware localization |

## Numbering

`cp_layla_vox.<interlocutor>0` is the hidden picker.

Visible scenarios use that interlocutor's decade:

- `11..16`, `19`: Ahmed
- `21..25`, `29`: daughter / children
- `31..35`, `39`: her mother
- `41..44`, `49`: Um Yusuf
- `51..54`, `59`: Umm Mariam
- `61..65`, `69`: Bey
- `71..75`, `79`: factory owner / mill world
- `81..86`, `89`: stranger
- `91..96`, `99`: herself / God
- `101..106`, `109`: ruler

Follow-ups are `scenario * 100 + branch`, for example `cp_layla_vox.1021`, `.1022`, `.1023`.

## Pacing

- `cp_layla_audience_cooldown`: 180 days, set by each visible scenario.
- `cp_layla_spoke_<topic>`: 540 days, per scenario.
- The former button paced this to roughly two player-initiated scenes per in-game year.
- Ambient events still use the shared 1-2/year target with a hard mod-wide cap of two passive beats; the button is player-initiated and uses `cp_button_fire`.

## Localization Contract

Use country-root dynamic loc in country events:

```text
[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]
[ROOT.GetCountry.GetRuler.GetFullName]
```

Do not use direct tag loc such as `[c:EGY...]`, and do not use `GetRuler.GetTitle`. `script/audit-common-people.py`, `script/audit-localization-dynamic-scope.py`, and `documentation/localization-dynamic-scope-ledger.md` reject both because they caused in-game `ERROR:[c:EGY.GetRuler...]` text.

Do not hardcode the active ruler as Pasha in shipped localization. Use ruler, Cairo, the room, the office, or the dynamic title/full name unless the line is explicitly historical research or archived design context.

## Art Contract

The active event-art pool is now generated-source covered and/or motion-backed; replacement still happens in versioned batches:

```text
documentation/characters/layla/prompts/replacement-batch-v0.7.md
image/generated/layla/v0.7/prompts/
```

The old bulk generator was deleted. Do not generate `cp_conversation_*` source files; `script/convert-images-to-dds.sh` rejects that naming. New accepted images should be versioned (`_v07`, `_v08`, etc.) and superseded DDS files should move to `image/archive/legacy-event-pictures/<version>-superseded/`.

## Debug QA

Visible Layla and Layla-vox events are covered by the shared generated person debug selectors:

```bash
python3 script/generate-person-debug-wrappers.py --check
```

Console selectors queue the target event. The shared QA button opens the popup from button context, avoiding the Victoria 3 console-thread popup crash. Direct debug events must not fire visible popups directly; `script/audit-common-people.py` enforces this with `DEBUG_POPUP_THREAD`.

## Adding Or Salvaging A Scene

1. Add the visible scenario in `mod/events/cp_layla_vox_events.txt`.
2. Add localization in `mod/localization/english/cp_layla_vox_l_english.yml`.
3. Give exactly one option `default_option = yes`.
4. Add `event_image`, `on_created_soundeffect`, and `on_opened_soundeffect`.
5. Set `cp_layla_audience_cooldown` and a scenario-specific `cp_layla_spoke_*` timed flag.
6. Route the scenario only through its hidden picker; do not add a Layla-only journal button.
7. Rerun the debug wrapper generator and the dev readiness gate.
