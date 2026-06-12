# Common People v0.5 rebuild test plan

Date: 2026-05-26

Use this after every serious rebuild pass. The purpose is not to prove that the prose is good; it is to prove that Common People loads, routes events through the correct gatekeepers, respects the event budget, shows art, and plays event audio on the current Victoria 3 build.

## Pre-flight

1. Use two passes:
   - **Debug probe pass:** launch with Victoria 3 debug mode (`-debug_mode`) only when console selectors or log-oriented probes are needed. The engine will show its own debug labels such as journal-entry ids and event-editor buttons in this pass; do not use it for clean screenshots or art/prose acceptance.
   - **Clean visual/audio pass:** launch without `-debug_mode`, start a fresh save, and inspect the journal/events as a player would see them.
2. Enable **Common People** in the launcher.
3. Confirm `~/.local/share/Paradox Interactive/Victoria 3/content_load.json` contains `Common People` in `enabledMods`.
4. Start a new game as **Egypt**, 1836-01-01.

For a quick compile/log smoke proof without using the launcher, run:

```bash
script/run-victoria3-runtime-smoke.sh
```

This helper enables the local symlinked mod, launches the installed Victoria 3
binary directly, waits for fresh logs, runs
`script/audit-victoria3-logs.py --require-current-build`, and closes only the
Victoria 3 process it started. Use `--wait-seconds N` if script compilation is
slow on the machine.

For a direct-binary launch that should stay open after the log audit, use:

```bash
script/run-victoria3-runtime-smoke.sh --wait-seconds 90 --keep-running
```

In `--keep-running` mode the game is detached from the wrapper with
`nohup`/`setsid`; the timeout controls only when logs are audited, not when the
game closes. For manual launcher/Steam playtests, do not use the launch helper
at all. Use this non-launching watcher while the game is open or after saving:

```bash
script/audit-live-test-state.sh
script/audit-live-test-state.sh --require-egypt-save --save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"
script/audit-live-test-state.sh --release-gate --save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"
```

The live-test watcher reports process state, log proof, latest save path, and
save timestamp even when strict current-build log proof fails. A nonzero exit
then means at least one required proof is stale or failing, not that the helper
stopped before collecting the remaining available evidence.

This helper is not an Egypt gameplay test. It does not select Egypt, start an
1836 campaign, unpause, inspect event windows, verify JE state in-game, or
prove that the player hears/sees the event audio and art as intended. Treat a
passing direct-binary smoke as script-load evidence only; Egypt gameplay proof
still requires the manual clean visual/audio pass below. `--release-gate` is
also non-launching; after the save audit passes, it runs the full release
readiness gate against the same tested save.

Before launching:

```bash
script/audit-release-readiness.py --mode dev
script/audit-common-people.py
script/audit-production-debug-leaks.py
python3 script/audit-localization-dynamic-scope.py
python3 script/build-localization-dynamic-scope-ledger.py --check
script/audit-event-repeatability.py
python3 script/audit-event-pacing.py
python3 script/build-event-pacing-ledger.py --check
script/audit-person-roster.py
python3 script/build-event-firing-ledger.py --check
python3 script/build-world-response-ledger.py --check
script/audit-event-audio.py
script/build-audio-cue-ledger.py --check
python3 script/audit-audio-palette.py
python3 script/build-audio-palette-ledger.py --check
script/audit-event-images.py
python3 script/build-motion-art-ledger.py --check
script/audit-art-provenance.py
python3 script/audit-character-doc-contract.py
python3 script/audit-character-art-contract.py
python3 script/build-character-seed-prompt-ledger.py --version v0.1 --check
python3 script/export-character-seed-prompts.py --version v0.1 --check
script/audit-art-prompt-safety.py
script/audit-art-batch-plan.py
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py --check
.agents/skills/victoria3-event/scripts/check_boms.sh
```

The dev gate includes `script/audit-production-debug-leaks.py`, which rejects shipped localization values that contain engine-style debug text such as `Journal Entry ID`, `DEBUG:`, `Open Event in text editor`, or `Trigger description`. It also includes `script/audit-localization-dynamic-scope.py` and `documentation/localization-dynamic-scope-ledger.md`, which guard reviewed dynamic loc calls so ruler-audience scenes cannot regress to broken text like `ERROR:[c:EGY.GetRuler...]`.

After quitting:

```bash
script/audit-victoria3-logs.py
script/audit-victoria3-logs.py --require-current-build
script/audit-egypt-gameplay-save.py --save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"
script/audit-release-readiness.py --mode runtime --egypt-save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"
script/audit-release-readiness.py --mode release --egypt-save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"
```

Use `script/audit-victoria3-logs.py --history` only when comparing against old numbered logs.

The normal log audit scans the current `debug.log`, `dedicated_server.log`, `error.log`, `game.log`, `system.log`, and `warning.log` files under `~/.local/share/Paradox Interactive/Victoria 3/logs/`. It prints that list on every run so the proof record is explicit.
The Egypt gameplay save audit reads the tested `.v3` save and proves the save actually contains the Common People mod, has advanced to at least 1836.1.2 by default, contains the EGY Common People startup flags, contains the always-on person alive/global registry flags, gives every alive person exactly one state home marker, a journal home-state pointer stored as `type=state`, one home-place token, and one positive workplace profile, and has no more than three active JE people in unique slots 1-3. By default it also requires at least one active person with visible history; use `--allow-silent-first-contact` only when intentionally accepting the startup silent branch.
The strict `--require-current-build` mode must pass after the direct-binary
compile/log smoke test, and again after the real Egypt gameplay pass. If
`system.log` reflects an older Victoria 3 build, or `mod_run` says
`logs-predate-latest-mod-file`, treat that as stale proof and relaunch the
installed game before claiming runtime readiness.
The static audit validates installed-game `on_action` hooks and `law_type:law_*` references against the local Victoria 3 files, validates mod metadata `supported_game_version` against the detected installed build, and hard-fails visible non-debug event windows that lack an image or event audio hooks. The dynamic localization scope audit rejects unsafe ruler/tag expressions before they can show `ERROR:[...]` in player-facing text. The home-state effects audit proves every registered person has exactly routed residence/workplace setup, the shared assignment path clears stale residence markers before writing one `cp_<person>_lives_here` marker and one matching `type=state` journal pointer, the shared building sensors require both the person's home state and the matching workplace profile, every building dispatcher checks the person's home state and workplace profile, and building-sensitive conditional spawns mark the matching home-state candidate before registration: manufacturing/factory-migration gates mark manufacturing states, machine gates mark machine-industry states, port gates mark port states, office gates mark government-office states, electric/telephone gates mark electric-service states, rail gates mark railway states, and urban-growth gates mark urban states. The pacing audit proves routine automatic Common People events stay in the 1-2/year target lane with a hard cap of two across the whole roster, including startup first-contact, law-reaction, conditional-entry, technology, building, and noncritical yearly world-response popups in the shared cooldown lane; it also proves that the war-start and revolution hooks resolve to one authored target before person dispatchers run. The pacing ledger must be current so that proof stays reviewable. The audio audit and cue ledger must prove every visible event opens with one of the seven reviewed Victoria 3 event music stingers; the audio palette audit/ledger must pass so that stinger palette remains varied by person and the roster does not collapse back into generic tranquil cues. The person selection ledger must be current so first-contact, monthly ambient, and conditional-entry weights stay reviewable; the person hook ledger must be current so every registered person's active/no-op dispatcher surface is reviewable and visible event hooks cannot bypass the shared gatekeepers; the event firing ledger must be current so every visible event has a non-debug production route; the world-response ledger must be current so each visible event is classified by its startup, monthly, law, technology, building, war, revolution, yearly/date, button, or visible-chain source. The motion-art ledger must be current so moving event plates can be reviewed by event id, person, video, and source line. The character README contract audit must pass so every registered person documents their token, home/residence, work/pop cohort, entry/routing, and event surface, and cannot retain stale claims that visible events use generic moving video art. The character art contract audit, seed-prompt ledger, prompt export checks, and art prompt safety audit must pass so every registered person has a reusable historical-scene prompt/portrait direction, reviewable seed batch, generation-ready `gpt-image-2` manifests, and prompt text that keeps the essential subject/action/object left-safe while reserving the right side for Victoria 3's event text panel. The art acceptance ledger must be current so planned image replacements cannot drift away from the actual event references, generated PNGs, and shipped DDS files. A passing dev gate means the rebuild is aligned with the detected 1.13.8 script surface and no event window is obviously blank, silent, spammy, visually directionless, or debug-only.
For release-candidate work, use `script/audit-release-readiness.py --mode release --egypt-save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"`; release mode refuses to run without `--egypt-save` unless `--skip-egypt-save` is explicitly supplied for a non-acceptance dry-run. It adds strict image-size and unused-DDS checks on top of runtime proof and the save-based Egypt gameplay proof. The consolidated readiness gate checks the shared generated person debug QA files, runs `script/audit-person-roster.py`, and checks `documentation/person-selection-ledger.md`, `documentation/person-contract-ledger.md`, `documentation/person-hook-ledger.md`, `documentation/event-firing-ledger.md`, `documentation/world-response-ledger.md`, and `documentation/motion-art-ledger.md`; it should report full debug-QA coverage, current selection weights, production firing routes, classified hook/action surfaces, classified world-response hooks, and moving-art coverage for every registered person.

## Hard fail patterns

Stop immediately if any current log contains:

- `No default option in event cp_`
- `Detected hidden event with options`
- `Duplicated event ID`
- `Unexpected token`
- `Mod Common People ... does not match game version`
- missing localization for a `cp_` key
- `Badly read script value` from a `cp_` file
- `should be in utf8-bom encoding` from a `cp_` file
- `Variable 'cp_...' is used but is never set`

## Test matrix

| Area | Action | Expected result | Failure meaning |
|---|---|---|---|
| Load | Start Egypt and unpause one day. | `cp_shared_startup.1` registers the always-on roster, samples eligible conditional entrants without opening their setup intros, Layla JE appears, the first-contact roll either opens one eligible person event or takes its intentional silent branch, and no raw localization keys appear. | Startup, localization, image path, first-contact routing, or event syntax is broken. |
| Clean UI | In the clean visual/audio pass, open Layla's JE and a normal event without `-debug_mode`. | No engine debug labels, no event-editor buttons, and no Common People QA button unless a console selector was deliberately queued in the same save. | The test is still in debug mode, a debug selector variable leaked into the save, or shipped localization has a debug-text regression. |
| Launcher state | Quit and run `script/audit-victoria3-logs.py`, then `script/audit-victoria3-logs.py --require-current-build`. | Build line is current, `runtime: current-build`, `mod_run: logs-after-latest-mod-file`, `enabled` includes Common People, no current `cp_` failures, and strict runtime proof passes. | The test did not actually load the mod, loaded an older game build/tree, or logs show runtime failures. |
| Monthly pulse | Let 3 in-game months pass. | JE life progress advances; status prose changes. | `on_monthly_pulse_country` or JE update plumbing is broken. |
| Yearly pulse | Run `event cp_debug.6`, or let one year pass. | Layla age changes; SoL/tax/welfare snapshots remain coherent. | `cp_on_yearly` or variable math is broken. |
| Person 2 setup | After game start, inspect variables or wait for ambient routing. | `cp_bey_alive = 1`, `cp_person_bey_alive` global exists, `cp_bey_lives_here` marker exists, and no Bey event fires outside the shared budget. | Person registration, hidden setup, or state marker failed. |
| Person 3 setup | After game start, inspect variables or wait for ambient routing. | `cp_soldier_alive = 1`, `cp_person_soldier_alive` global exists, `cp_soldier_lives_here` marker exists, and no Yusuf event fires outside the shared budget. | Person registration, hidden setup, pop type, or state marker failed. |
| Person 4 conditional setup | Build or verify a manufacturing building under `law_no_workers_rights`, let the yearly pulse run, or use `event cp_debug.93`. | `cp_samier_alive = 1`, `cp_person_samier_alive` global exists, `cp_samier_lives_here` marker exists, and no Samier event fires before his industrial trigger or outside the shared budget. | Conditional registration, hidden setup, pop type, manufacturing trigger, or state marker failed. |
| Person 5 conditional setup | Build or verify a manufacturing building after land reform has moved beyond Serfdom and Tenant Farmers, let the yearly pulse run, or use `event cp_debug.96`. | `cp_tarek_alive = 1`, `cp_person_tarek_alive` global exists, `cp_tarek_lives_here` marker exists, and no Tarek event fires before his industrial trigger or outside the shared budget. | Conditional registration, hidden setup, pop type, manufacturing trigger, land-reform trigger, or state marker failed. |
| Person 6 setup | After game start, inspect variables or use `event cp_debug.100`. | `cp_nour_alive = 1`, `cp_person_nour_alive` global exists, `cp_nour_lives_here` marker exists, and no Nour event fires outside the shared budget. | Person registration, hidden setup, pop type, or state marker failed. |
| Person 7 setup | After game start, inspect variables or use `event cp_debug.103`. | `cp_mina_alive = 1`, `cp_person_mina_alive` global exists, `cp_mina_lives_here` marker exists, and no Mina event fires outside the shared budget. | Person registration, hidden setup, pop type, or state marker failed. |
| Person 8 setup | After game start, inspect variables or use `event cp_debug.106`. | `cp_zaynab_alive = 1`, `cp_person_zaynab_alive` global exists, `cp_zaynab_lives_here` marker exists, and no Zaynab event fires outside the shared budget. | Person registration, hidden setup, pop type, or state marker failed. |
| Person 9 conditional setup | Research railways/telegraphy, build a railway, or queue a generated Farid selector after setup. | `cp_farid_alive = 1`, `cp_person_farid_alive` global exists, `cp_farid_lives_here` marker exists, and Farid does not appear before rail/telegraph eligibility. | Conditional registration, hidden setup, railway/telegraph trigger, or state marker failed. |
| Person 10 conditional setup | Build/verify a port, research paddle steamers/cranes, or queue a generated Dawud selector after setup. | `cp_dawud_alive = 1`, `cp_person_dawud_alive` global exists, `cp_dawud_lives_here` marker exists, and Dawud does not appear before port/steam eligibility. | Conditional registration, hidden setup, port/steam trigger, or state marker failed. |
| Person 11 conditional setup | Build/verify government administration, research central archives / identification documents, or queue a generated Rashid selector after setup. | `cp_rashid_alive = 1`, `cp_person_rashid_alive` global exists, `cp_rashid_lives_here` marker exists, and Rashid does not appear before office/records eligibility. | Conditional registration, hidden setup, government-office/records trigger, or state marker failed. |
| Person 12 conditional setup | Research electrical generation / telephone / radio, build a power plant or electrics industry, or queue a generated Salma selector after setup. | `cp_salma_alive = 1`, `cp_person_salma_alive` global exists, `cp_salma_lives_here` marker exists, and Salma does not appear before electric/telephone eligibility. | Conditional registration, hidden setup, electric/telephone trigger, or state marker failed. |
| Person 13 conditional setup | Research mechanical tools / rotary valve engine / combustion engine, build a tooling workshop / steel mill / motor industry, or queue a generated Karim selector after setup. | `cp_karim_alive = 1`, `cp_person_karim_alive` global exists, `cp_karim_lives_here` marker exists, and Karim does not appear before machine-industry eligibility. | Conditional registration, hidden setup, machine-industry trigger, or state marker failed. |
| Person 14 conditional setup | Research urban planning / modern sewerage / paved roads / steel-frame buildings, build construction/trade/urban-center capacity after eligibility, or queue a generated Huda selector after setup. | `cp_huda_alive = 1`, `cp_person_huda_alive` global exists, `cp_huda_lives_here` marker exists, and Huda does not appear before urban-growth eligibility. | Conditional registration, hidden setup, urban-growth trigger, or state marker failed. |
| Person 15 conditional setup | Enact dedicated police, militarized police, right of assembly, outlawed dissent, censorship, start a revolution, or queue a generated Nabil selector after setup. | `cp_nabil_alive = 1`, `cp_person_nabil_alive` global exists, `cp_nabil_lives_here` marker exists, and Nabil does not appear before public-order eligibility. | Conditional registration, hidden setup, law/revolution trigger, or state marker failed. |
| Person 16 conditional setup | Build/verify manufacturing plus urban-growth pressure, research machine-industry tech, or queue a generated Mansur selector after setup. | `cp_mansur_alive = 1`, `cp_person_mansur_alive` global exists, `cp_mansur_lives_here` marker exists, and Mansur does not appear before factory-migration eligibility. | Conditional registration, hidden setup, factory-migration trigger, or state marker failed. |
| Cohort SoL | Run `event cp_debug.13`, `event cp_debug.20`, then `event cp_debug.22`. | SoL reads a plausible cohort value and survives moving away/back. | Pop cohort/state marker pipeline is broken. |
| Law reaction | Run `event cp_debug.5` or pass Homesteading through the UI. Use `event cp_debug.87`, `.88`, `.89`, `.95`, `.98`, `.102`, `.105`, and `.108` for direct Bey/Samier/Tarek/Nour/Mina/Zaynab probes. | Shared resolver fires either `cp_layla.2` or `cp_bey.20` once for Homesteading; women's property law routes one of Layla or Nour; public schools route one of Layla or Mina; public health routes one of Layla or Zaynab; Bey Serfdom Restored and Commercialized Agriculture probes fire once; the worker-protection resolver chooses Samier or Tarek when both are alive/unseen and falls back cleanly when only one is eligible. | Law dispatcher, seen flag, shared resolver, person dispatch, or gatekeeper failed. |
| Welfare up/down | Run `event cp_debug.38`, then `event cp_debug.39`. | First-envelope/up/down welfare events route once each. | Welfare tier snapshot or law dispatcher failed. |
| War start/end | Start an Egypt war, or use `event cp_debug.27`, `.28`, `.91`, and `.92` for direct prose/effect checks. | Ahmed homecoming/death effects mutate `cp_layla_ahmed_alive` correctly; Yusuf notice/return events set and clear `cp_soldier_at_war`; dead Ahmed scenes no longer route. | Ahmed state, Yusuf state, war hook, or alive guard failed. |
| Mortality | Run `event cp_debug.33`. | Layla death event fires; `cp_layla_alive = 0`; `cp_person_layla_alive` global is removed; any legacy Layla JE completes; ambient routing stops. | Death registry, legacy JE migration, or numeric alive guards failed. |
| First child | Run `event cp_debug.99`, or let the yearly pulse roll while Layla is 23-32, married, Ahmed alive and home, and `cp_layla_children = 0`. | `cp_layla.5` fires, `cp_layla_seen_childbirth` is set, `cp_layla_children` increments, and daughter/child conversation branches become eligible. | Yearly family milestone, one-shot gate, or household-state mutation failed. |
| Child mortality | Ensure `cp_layla_children >= 1`, then run `event cp_debug.35`. | Child count decreases, loss flag set, future grief content can route. | Family mechanics or child-loss effect failed. |
| Legacy Layla vox QA | Queue a generated `cp_layla_vox.*` selector, then click **Open queued QA event** on the shared Common People JE. | A `cp_layla_vox.*` scene opens, has one default option, image renders, audio hook plays. | Vox ids, options, generated QA bridge, or audio hook failed. |
| Routine event budget | Fresh save, no debug events/buttons, run 12 months while passing no more than one qualifying law and one major modernization trigger. | At most 2 automatic Common People popups, including the first-contact opener and any law/world-response reaction; if an opener fires at game start, at most 1 later ambient, law-reaction, or world-response beat should fire in year one. | Startup/law/world-response budget marking or global/person cooldown budget may be broken. |
| Art QA | Inspect intro, deed, Ahmed conscripted, clerk's letter, death, one vox audience scene, the four Bey scenes, Yusuf's three scenes, and at least one event per non-Layla person, prioritizing the newest replacement sets for Samier, Tarek, Zaynab, Salma, Farid, Dawud, Rashid, Karim, Mansur, and Nabil. | Active DDS images are readable at 600x400, still images keep the subject visible on the left side of the event window, and no visible event uses a generic vanilla video placeholder. | Image needs regeneration, downscale, DDS conversion review, or event-window composition retuning. |
| Audio QA | Listen to intro, law reaction, war/death, spiritual, breakthrough, and vox scenes. | No silent visible event; music stinger matches the category in `documentation/audio-rebuild.md`. | Stinger assignment needs direct event-id retuning. |

## Console probes to prioritize

These are the fastest probes for the rebuild spine:

```text
event cp_debug.1   # console sanity
event cp_debug.5   # Homesteading/law reaction
event cp_debug.13  # cohort SoL read
event cp_debug.20  # move to Sinai + resample
event cp_debug.22  # move back to Lower Egypt
event cp_debug.27  # Ahmed homecoming
event cp_debug.28  # Ahmed death
event cp_debug.33  # Layla death
event cp_debug.99  # first-child milestone
event cp_debug.35  # child death, after children exist
event cp_debug.38  # welfare up
event cp_debug.39  # welfare down
event cp_debug.85  # shared person registration/setup
event cp_debug.86  # Bey intro
event cp_debug.87  # Bey Homesteading reaction
event cp_debug.88  # Bey Serfdom Restored reaction
event cp_debug.89  # Bey Commercialized Agriculture reaction
event cp_debug.90  # Yusuf intro
event cp_debug.91  # Yusuf war notice
event cp_debug.92  # Yusuf return
event cp_debug.93  # Samier setup
event cp_debug.94  # Samier intro
event cp_debug.95  # Samier labor-law reaction
event cp_debug.96  # Tarek setup
event cp_debug.97  # Tarek intro
event cp_debug.98  # Tarek labor-law reaction
event cp_debug.100 # Nour setup
event cp_debug.101 # Nour intro
event cp_debug.102 # Nour property-rights reaction
event cp_debug.103 # Mina setup
event cp_debug.104 # Mina intro
event cp_debug.105 # Mina public-schools reaction
event cp_debug.106 # Zaynab setup
event cp_debug.107 # Zaynab intro
event cp_debug.108 # Zaynab public-health reaction
```

Popup probes in this list now queue the event instead of opening it from the console thread. After running one, click **Open queued QA event** to review the prose, art, and audio.

For exhaustive event-window QA, use the shared generated queue in `cp_debug_person_events.txt` and the generated dispatcher in `cp_debug_person_fire_selected.txt`. The Layla mapping is stable inside that shared namespace: `cp_layla.N` -> `event cp_debug_person.(1000+N)`, and `cp_layla_vox.N` -> `event cp_debug_person.(2000+N)`.

For the other persons, the wrapper mapping uses the character's `Person N` header when that range is free: Bey `cp_bey.10` is `event cp_debug_person.210`, Soldier `cp_soldier.10` is `event cp_debug_person.310`, Mina `cp_mina.20` is `event cp_debug_person.720`, Zaynab `cp_zaynab.20` is `event cp_debug_person.820`, and Farid `cp_farid.10` is `event cp_debug_person.910`. If a later person number would collide with Layla's reserved ranges, the generator shifts that wrapper to the next unused 100-block; Rashid's generated wrappers currently demonstrate that collision-safe shifting, so use `cp_debug_person_events.txt` as the source of truth. The selected-event values remain the old friendly dispatcher numbers such as `30010`, `80020`, and `90020`, so existing `cp_debug.*` shortcuts still work.

Workflow: run the console selector, then click **Open queued QA event**. The selector itself only stores `cp_debug_selected_event`; the QA button fires the popup through `cp_button_fire` in game-thread context.

Regenerate the QA files after any visible person event-id changes:

```bash
python3 script/generate-person-debug-wrappers.py
python3 script/generate-person-debug-wrappers.py --check
script/audit-person-roster.py
```

Avoid direct console firing of visible popup events; prior V3 testing showed console-thread popup events can crash in some cases. Prefer generated queue selectors plus the shared Common People JE QA button, UI law enactments, or non-popup state probes.

## Completion notes

Record each run in the rebuild ledger with:

- Victoria 3 build from `system.log`.
- Whether `enabledMods` included Common People.
- Which tests passed/failed.
- Any current-log failures from `script/audit-victoria3-logs.py`.
- Art/audio notes by event id.
