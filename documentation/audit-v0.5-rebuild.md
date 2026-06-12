# Common People rebuild audit - v0.5 production ledger

Date: 2026-05-26

This is the working ledger for the full rebuild request: make event firing reliable, replace the current art direction with GPT image 2 era assets, add event audio/music, update the mod for current Victoria 3, and scale beyond Layla.

## Current target

- Installed local Victoria 3 files report `release/1.13.8`, Steam build `23451701`, checksum suffix `ce22`, updated 2026-05-28 23:21:24.
- Current local run logs are for the installed 1.13.8 build (`system.log` shows `release/1.13.8 : 175c4751c`) and Common People is mounted from the local symlink, but the logs now predate the latest no-launch mod edits. Strict runtime proof must be rerun after the user allows another launch.
- `mod/.metadata/metadata.json` now targets `supported_game_version = 1.13.*`.
- The current launcher file at `~/.local/share/Paradox Interactive/Victoria 3/content_load.json` now has `"Common People"` in `enabledMods`; the latest pre-launch file was backed up as `content_load.json.cp-backup-20260529-012243`.

## Fixed in the first rebuild pass

- Added `script/audit-common-people.py`, a repeatable static audit for event ids, duplicate ids, 5+ digit event numbers, default options, hidden-event options, missing event pictures, missing localization, duplicate localization, audio hooks, undefined trigger targets, and uncalled non-orphan events.
- Extended `script/audit-common-people.py` with registered-person checks so each person must have memory/localization files, alive initialization, an ambient pool, and a monthly router branch.
- Added `script/audit-victoria3-logs.py`, a current-log audit for launcher state, installed Victoria 3 build/checksum, last-run Victoria 3 build, runtime freshness, version mismatches, event default-option failures, hidden-event option failures, duplicate event ids, unexpected tokens, and missing Common People localization.
- Added `documentation/test-plan-v0.5-rebuild.md`, the current in-game proof matrix for startup, monthly/yearly pulses, law reactions, war/death paths, conversation routing, ambient budget, art QA, and audio QA.
- Added `documentation/audio-rebuild.md`, the current event music-stinger palette and audio QA contract.
- Added `documentation/art-bible-v0.5.md`, the stricter image direction for GPT image 2 era regeneration.
- Added `script/audit-event-images.py`, a production inventory for referenced/shipped DDS files, unused images, and event-art dimensions.
- Added `script/audit-art-provenance.py`, a generated-source coverage report for active event art so the remaining legacy Layla image backlog is explicit.
- Extended `script/audit-art-provenance.py --rank-missing`, ranking legacy/no-source assets by active event-window usage, and added `documentation/characters/layla/prompts/replacement-batch-v0.7.md` for the next eleven high-impact Layla replacement prompts, including the in-game observed `cp_layla_vox.102` land-petition blocker.
- Added `script/audit-art-batch-plan.py`, which parses the v0.7 replacement ledger, verifies target priority/prompt counts, checks each planned `_v07` asset against active legacy event usage, reports source/DDS readiness, and rejects the retired Layla bulk generator / `cp_conversation_*` source naming path.
- Removed the old `script/gen-layla-event-images.sh` bulk generator, which still contained pre-r5 palace/Pasha conversation prompts and external writes, and replaced it with `script/export-art-batch-prompts.py` plus checked prompt exports under `image/generated/layla/v0.7/prompts/`.
- Added `script/audit-event-audio.py`, a focused audio proof that every visible non-debug event has the creation cue plus one validated Victoria 3 music stinger.
- Hardened `script/audit-event-audio.py` so it also proves the installed event window reads `Event.GetOnOpenedSoundEvent`, identifies the exact `sound/GUIDs.txt` used for GUID validation, and separates event stingers from the long-form `game/music/` track system.
- Added `script/build-image-contact-sheets.py` and generated review sheets for every current generated image set, with first-pass visual findings recorded in `documentation/art-review-v0.5.md`.
- Hardened `script/build-image-contact-sheets.py --check` and added it to the consolidated dev gate, so image-generation batches cannot skip or stale their review contact sheets.
- Added `script/audit-person-roster.py`, a roster-scalability audit for per-person files, setup events, yearly dispatch, ambient router weights, localization, images, and debug QA coverage.
- Added `script/build-person-selection-ledger.py`, generated `documentation/person-selection-ledger.md`, and wired its freshness check into the dev gate so first-contact, monthly ambient, and conditional-entry weights are visible and cannot drift silently.
- Added `script/build-person-contract-ledger.py`, generated `documentation/person-contract-ledger.md`, and wired its freshness check into the dev gate so every registered person must keep the same setup variables, dispatcher hook surface, yearly lifecycle, ambient router coverage, visible-event audio/art, and generated debug QA contract.
- Added `script/build-person-hook-ledger.py`, generated `documentation/person-hook-ledger.md`, and wired its freshness check into the dev gate so every registered person's active/no-op hook surface is reviewable and visible hook-fired events cannot bypass shared gatekeepers.
- Added `script/build-event-firing-ledger.py`, generated `documentation/event-firing-ledger.md`, and wired its freshness check into the dev gate so every visible non-debug event must have a non-debug production route.
- Added `script/build-world-response-ledger.py`, generated `documentation/world-response-ledger.md`, and wired its freshness check into the dev gate so every visible non-debug event is classified by its startup, monthly, law, technology, building, war, revolution, yearly/date, button, hidden-router, or visible-chain source.
- Hardened the residence/workplace layer: conditional people spawned from existing local buildings now mark a matching home-state candidate before registration, shared home-state assignment clears old residence markers, assigns exactly one `cp_<person>_lives_here` state marker, stores a matching `cp_<person>_state_pointer` rendered in the JE next to the authored home place, building dispatch and physical yearly/ambient/action gates use the person's home-state + workplace profile instead of country-wide building existence, and `script/audit-home-state-effects.py` now fails broken shared residence assignment, broken shared home/workplace sensor definitions, building-sensitive spawn gates without the matching home-state candidate marker, or non-spawn person effects that use country-wide infrastructure sensors for local physical beats.
- Added `script/audit-character-doc-contract.py` and wired it into the dev gate so every registered person README must document the token, home/residence, work or pop cohort, entry/routing, and event surface. The audit also rejects stale claims that visible events use generic moving video art, keeping character docs aligned with the current authored-still art direction.
- Added `script/audit-event-repeatability.py`, a repeat-control audit proving visible event windows are covered by a seen/latch variable, a cooldown, a visible parent chain, a terminal state change, startup-only routing, or an explicitly intentional repeatable transition.
- Added `script/audit-event-pacing.py` and wired it into the dev gate so routine automatic Common People events remain in the 1-2/year target lane with a hard cap of two across the whole roster, including startup first-contact, law-reaction, and routine world-response popups in the shared cooldown lane.
- Added `script/build-event-pacing-ledger.py`, generated `documentation/event-pacing-ledger.md`, and wired its freshness check into the dev gate so the 1-2 routine-events/year contract has a readable proof record.
- Hardened `script/audit-person-roster.py` so person-owned subnamespaces like `cp_layla_vox.*` count in the owning person's event, image, localization, and debug-QA surface.
- Added `script/generate-person-debug-wrappers.py`, generated `mod/events/cp_debug_person_events.txt`, and generated `mod/common/scripted_effects/cp_debug_person_fire_selected.txt`, giving every visible registered-person event a safe queue-plus-JE-button popup QA path without hand-maintaining individual entries in `cp_debug_events.txt`.
- Folded the older hand-written Layla `cp_debug.N` popup probes into the same queue-plus-JE-button path, so they prepare state from console but open the visible window only after the debug button is clicked.
- Folded the smaller Bey/Yusuf/Samier/Tarek popup probes into the same JE-button debug queue and added a static `DEBUG_POPUP_THREAD` guard so `cp_debug*_events.txt` cannot direct-trigger visible popups again.
- Added `script/audit-release-readiness.py`, a consolidated gate with `dev`, `runtime`, and `release` modes so the current rebuild state is explicit.
- Updated the consolidated readiness gate to check the shared generated person debug QA files with `--check` and to run the roster audit, so generated coverage is checked for every registered person together.
- Replaced the placeholder launcher/workshop thumbnails with generated Common People art, archived the source/variants under `image/generated/thumbnail/v0.1/`, and added thumbnail size validation to `script/audit-common-people.py`.
- Added metadata game-version validation to `script/audit-common-people.py`, so `supported_game_version` must match the latest locally installed Victoria 3 branch currently detected as `1.13.8`.
- Normalized every Paradox script file under `mod/common/` and `mod/events/` to UTF-8 BOM and added `SCRIPT_BOM` validation so newly generated event/effect files cannot reintroduce Victoria 3's "should be in utf8-bom encoding" warnings.
- Removed signed positive macro call values such as `delta = +2` from live Paradox script and added `SIGNED_POSITIVE_NUMBER` validation, because Victoria 3 logged those expansions as "Badly read script value +N".
- Updated `script/audit-victoria3-logs.py` to hard-fail current logs on `SCRIPT_BOM_WARNING` and `BAD_SCRIPT_VALUE`, then confirmed the 06:03 smoke launch reports zero of both.
- Added `CP_VARIABLE_UNSET_READ` static validation and `CP_VARIABLE_USED_NEVER_SET` runtime-log validation, fixed `cp_layla_ahmed_conscripted` so the war-audience branch has a real 540-day marker, and rewired the unused radio-house sensor to the actual `cp_layla_seen_radio` state.
- Moved the current-log scan from `script/audit-release-readiness.py --mode dev` into runtime/release modes, so dev stays a static/local gate while runtime proof remains strict about loaded Victoria 3 logs.
- Added `script/normalize-event-dds-size.py` and rebuilt the 42 referenced oversized DDS files to the production 600x400 DXT5 target.
- Archived the seven unused legacy Layla DDS files out of `mod/gfx/event_pictures/` and into `image/archive/legacy-event-pictures/v0.5/`, so the shipped event-art pool has no unused assets.
- Generated the six-image Layla v0.5 prototype set from the new art bible, saved both 600x400 candidates and 1536x1024 archives under `image/generated/layla/v0.5/`, converted them to DXT5 DDS, and wired them into their prototype events with `_v05` filenames.
- Regenerated the soft Layla intro proof as `cp_layla_intro_v06`, archived the superseded `_v05` DDS, updated the v0.6 prompt ledger/contact sheet, and rewired `cp_layla.1`.
- Regenerated the weak Layla Ahmed-conscripted proof as `cp_layla_ahmed_conscripted_v06`, archived the superseded `_v05` DDS, updated the v0.6 prompt ledger/contact sheet, and rewired `cp_layla.4`.
- Regenerated the weak Layla conversation-audience proof as `cp_layla_conversation_audience_v06`, archived the superseded `_v05` DDS, built a v0.6 contact sheet, and rewired the vox audience events to the new asset.
- Regenerated the weak Layla clerk's-letter proof as `cp_layla_clerks_letter_v06`, archived the superseded `_v05` DDS, updated the v0.6 prompt ledger/contact sheet, and rewired `cp_layla.41`.
- Regenerated Yusuf's weak return image as `cp_soldier_return_v02`, archived the superseded `cp_soldier_return.dds`, built a v0.2 contact sheet, and rewired `cp_soldier.21`.
- Regenerated the repetitive Bey commercialized-agriculture desk scene as `cp_bey_commercialized_v02`, archived the superseded `cp_bey_commercialized.dds`, built a v0.2 contact sheet, and rewired `cp_bey.22`.
- Expanded Person 2's first scaffold: Hassan Bey al-Sayyid (`bey`) now has hidden setup, four generated event images, a first ambient beat, three land-reform reactions, localization, yearly aging/SoL refresh, debug probes, and weighted shared Homesteading/Serfdom-restored resolvers with Layla.
- Added Person 3's first scaffold: Yusuf ibn Mahmud (`soldier`) now has hidden setup, three generated event images, an ambient barracks beat, war-start and war-end milestone beats, localization, yearly aging/SoL refresh using the local 1.13 `soldiers` pop type, guarded war hooks, and debug probes.
- Added Person 4's first scaffold: Samier (`samier`) now conditionally registers when Egypt has manufacturing under `law_no_workers_rights`, with a factory-arrival opener, workers-rights law reaction, unsafe-machine world response, shared-bread ambient beat, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 5's first scaffold: Tarek al-Rashidi (`tarek`) now conditionally registers when Egypt has manufacturing and land reform has moved beyond Serfdom/Tenant Farmers, with a mill-ledger opener, worker-protection law reaction, new-boiler modernization response, account-book ambient beat, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 6's civic spine: Nour (`nour`) now registers in Egypt, with cedar-chest and key-under-pillow ambient beats, `law_women_own_property` and rent-receipt property-rights responses, localization, yearly aging/SoL refresh, generated debug QA coverage, and prompt/source archives.
- Added Person 7's civic spine: Mina (`mina`) now registers in Egypt, with print-shop and night-proof ambient beats, a `law_public_schools` reaction shared with Layla through weighted routing, a modern-records notice-sheet response, localization, yearly aging/SoL refresh, generated debug QA coverage, and prompt/source archives.
- Added Person 8's civic spine: Zaynab (`zaynab`) now registers in Egypt, with brass-basin and long-night ambient beats, a `law_public_health_insurance` reaction shared with Layla, a no-public-health fever-bowl response, localization, yearly aging/SoL refresh, generated debug QA coverage, and prompt/source archives.
- Added Person 9's first scaffold: Farid al-Haddad (`farid`) now conditionally registers when Egypt has railways, telegraphy, or a railway building, with four moving event windows, an ambient platform beat, railway/telegraph world responses, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 10's first scaffold: Dawud Hanna (`dawud`) now conditionally registers when Egypt has a port, paddle steamers, or cargo-crane technology, with four moving event windows, an ambient dock beat, steamship/crane world responses, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 11's first scaffold: Rashid al-Katib (`rashid`) now conditionally registers when Egypt has government administration, central archives, or identification papers, with four moving event windows, an ambient office-exhaustion beat, records/identity world responses, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 12's first scaffold: Salma Farag (`salma`) now conditionally registers when Egypt has electric service, telephone networks, radio, a power plant, or electrics industry, with four moving event windows, an ambient night-exchange beat, electric/telephone/radio world responses, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 13's first scaffold: Karim al-Nahhas (`karim`) now conditionally registers when Egypt has machine tools, steel, engines, or mid-century manufacturing, with four moving event windows, an ambient factory-injury beat, tool/engine world responses, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 14's first scaffold: Huda al-Matariya (`huda`) now conditionally registers when Egypt has urban growth, construction/trade/urban-center capacity, or city-planning/sewerage/roads technologies, with four moving event windows, a chance-based entry roll, an ambient rent-pressure beat, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 15's first scaffold: Nabil al-Haras (`nabil`) now conditionally registers when Egypt has policing, dissent, assembly, censorship, or revolution pressure, with four moving event windows, law/revolution entry hooks, an ambient public-order beat, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Added Person 16's first scaffold: Mansur al-Mahalla (`mansur`) now conditionally registers when manufacturing and urban pull create factory-migration pressure, with four moving event windows, a chance-based entry roll, yearly/technology/building hooks, an ambient remittance beat, localization, yearly aging/SoL refresh, and generated debug QA coverage.
- Hardened `script/audit-person-roster.py` so first contact must retain at least five non-Layla candidates, the conditional roster must retain at least ten entrants, and each conditional entrant must randomize its first visible appearance with a positive silent branch.
- Added a startup conditional scan before first contact: eligible conditional people can now register at game start if the selected start date/save state already satisfies their world gates, their setup intros are suppressed during that scan, and `cp_shared_startup.2` can choose any of the 16 registered persons as the clean campaign opener. The roster audit now enforces startup-scan and first-contact coverage for conditional entrants.
- Made visible first-contact branches call `cp_mark_first_contact_budget`, so the campaign opener starts the same 183-day global and 365-day per-person cooldown lane as ambient events instead of stacking a second passive story beat immediately after game start.
- Added `cp_roll_public_order_law_reaction`, a shared weighted resolver for `law_right_of_assembly`, `law_outlawed_dissent`, `law_dedicated_police`, and `law_militarized_police`, so Layla and Nabil cannot both fire a visible event for the same public-order law; the roster audit now validates the resolver and direct-dispatch guards.
- Moved Layla's hidden country-variable setup from the old legacy startup namespace into `cp_layla_setup.1`, deleted the legacy startup event file, and hardened the roster audit so Layla's setup must remain person-owned and cannot directly claim first contact.
- Hardened `script/audit-common-people.py` so registered persons are discovered from every script file, not just startup, which lets conditional mid-game persons get the same file/router/alive checks.
- Added installed-game on_action validation to `script/audit-common-people.py` and fixed the war-start subscription from nonexistent `on_war_started` to vanilla 1.13's `on_diplo_play_war_start` (`scope:actor` / `scope:target` -> EGY).
- Added scripted-call validation to `script/audit-common-people.py`, so `cp_* = yes` calls must resolve to a scripted effect or scripted trigger definition.
- Added raw `trigger_event` validation to `script/audit-common-people.py`, so common-script direct fires can only target hidden setup events; visible events must route through the shared firing gatekeepers.
- Split production reachability from debug-only reachability in `script/audit-common-people.py`, so a `cp_debug.*` wrapper can no longer mask an event that lacks a real dispatcher/button/chain path.
- Added installed-game law validation to `script/audit-common-people.py`, so every `law_type:law_*` reference must exist in the local Victoria 3 `common/laws/` definitions before the dispatcher can be considered reliable.
- Added visible event image/audio hook validation to `script/audit-common-people.py`, so every non-debug event window with options must declare an `event_image`, an `on_created_soundeffect`, and an `on_opened_soundeffect`.
- Updated `script/audit-victoria3-logs.py` to print the exact current log files it scans, added `--require-current-build` for strict current-build runtime proof, and added latest-mod-file timestamp checks so stale logs cannot prove a newer mod tree.
- Added `script/enable-common-people-local.sh`, a local smoke-test helper that verifies/creates the mod symlink, backs up `content_load.json`, and enables Common People without touching DLC settings.
- Fixed `cp_layla_vox.*` visible events that had options but no `default_option = yes`.
- Renumbered the 18 `cp_layla_vox` five-digit event ids that were colliding in logs.
- Removed the option block from hidden startup event `cp_shared_startup.1`.
- Removed unsupported `should_be_pinned_by_default = yes` from `cp_je_layla`.
- Removed duplicate localization keys in `cp_layla_vox_l_english.yml`.
- Replaced the temporary one-size event sound hook with validated Victoria 3 music stingers on 267 visible Layla and Layla-vox events.
- Tightened shared firing gatekeepers so they require `cp_<person>_alive > 0`, not merely the presence of an alive variable.
- Tightened Layla's buttons and Ahmed conversation routing so dead Layla or dead Ahmed branches cannot keep firing.
- Wired `cp_layla.5` (`The First Cry`) into the yearly milestone dispatcher with a young-family one-shot gate, moved its state mutation into `cp_layla_first_childbirth`, and added `cp_debug.99` for direct QA.
- Routed `cp_layla_dies` through the shared person registry death effect, so her global alive registry flag is removed at death.
- Added a death completion condition to `cp_je_layla`, so Layla's journal entry resolves instead of lingering after `cp_layla_alive = 0`.
- Added an `ALIVE_GUARD` audit rule and updated shared Person-N onboarding docs so future persons copy the `has_variable` + `var:... > 0` pattern.
- Re-ran the alive-guard sweep after adding the eight-person router: live-person checks now pair existence with numeric `> 0` checks, while setup-only `NOT = { has_variable = ... }` cases remain allowed.
- Replaced the remaining Layla yearly special case with `cp_layla_dispatch_yearly`, removed Layla's JE-owned age tick, and made `cp_on_yearly` call one `cp_<person>_dispatch_yearly` per alive registered person.
- Strengthened `cp_person_is_alive` so it requires both the global registry flag and the local country alive variable, then routed shared firing gatekeepers, monthly selection branches, and yearly dispatch guards through that one sensor.
- Hardened `script/audit-person-roster.py` so Layla no longer gets a yearly-dispatch exception; every registered person must have `cp_<name>_dispatch_yearly`, a hidden setup path, router coverage, generated debug QA coverage, and `cp_person_is_alive` guards in the monthly and yearly shared infrastructure.
- Moved Layla-only law reactions out of `cp_on_law_enacted` and into `cp_layla_dispatch_law_enacted`; `cp_on_law_enacted` now keeps only shared law contests and per-person dispatcher calls.
- Added `LAW_DIRECT_SINGLE_PERSON` validation to `script/audit-common-people.py`, so future one-person law reactions cannot be direct-fired from the shared law dispatcher.
- Moved Layla's war-start, war-end, technology, building-built, and revolution routing into `cp_layla_dispatch_war_started`, `cp_layla_dispatch_war_end`, `cp_layla_dispatch_tech`, `cp_layla_dispatch_building`, and `cp_layla_dispatch_revolution`, leaving the shared on-action layer as guarded dispatcher calls.
- Added `SHARED_DIRECT_GATEKEEPER` validation to `script/audit-common-people.py`, so shared infrastructure cannot direct-fire non-law person events instead of delegating to `cp_<person>_dispatch_*`.
- Moved Layla startup/save-migration and monthly JE display-state mutation into `cp_layla_dispatch_startup` and `cp_layla_dispatch_monthly`; `cp_on_start` / `cp_on_monthly` now guard and delegate instead of writing `cp_layla_*` variables directly.
- Added `ON_ACTION_PERSON_MUTATION` validation to `script/audit-common-people.py`, so shared on-actions cannot directly mutate `cp_<person>_*` variables instead of calling person-owned dispatchers.
- Hardened `script/audit-person-roster.py` so each registered/startup or conditional-spawned person must have its hidden setup event triggered by the actual entry path.
- Replaced broken `c:EGY` ruler localization in Layla ruler-audience conversations with vanilla-proven `ROOT.GetCountry.GetRuler` loc calls, and added a static audit rule so direct `c:TAG` localization references cannot return.
- Removed hardcoded active `Pasha` wording from the shipped mod tree's Layla localization/events, replacing it with ruler/Cairo/room wording so the ruler-audience material no longer freezes late-era saves in 1836 language.
- Updated `script/convert-images-to-dds.sh` to default to the in-repo `image/generated/` source library and fail fast on retired `cp_conversation_*` source names instead of silently mapping them back into shipped Layla DDS assets.
- Replaced `documentation/characters/layla/conversation.md`, which still described the old `cp_conversation.*` audience tree, with the current `cp_layla_vox.*` voice-system contract, routing flow, localization rules, art rules, and QA checklist.
- Replaced `documentation/characters/layla/story-map.md`, which still described a pre-r5 Layla map, with the current r5/r6 event-family map and audit-backed Layla counts: 85 `cp_layla.*` definitions, 1 `cp_layla_setup.*` setup definition, 192 `cp_layla_vox.*` definitions, 278 total Layla-owned events, and 267 visible/debug-visible windows.
- Generalized `script/export-art-batch-prompts.py` and `script/audit-art-batch-plan.py` across all `replacement-batch-vNN.md` ledgers, so prompt exports, gpt-image-2 JSONL manifests, and plan audits scale beyond the first v0.7 batch.
- Added `documentation/characters/layla/prompts/replacement-batch-v0.8.md`, a second eleven-image replacement queue for the next ranked Layla legacy/no-source assets: children leaving the factory floor, election day, Ahmed's foreman runner, rifles in the square, strangers in the lane, old ruler/country memory, lost child, paper, mill rolls, dark room, and daughter reading.
- Added `documentation/characters/layla/prompts/replacement-batch-v0.9.md`, a third eleven-image replacement queue for the next ranked Layla legacy/no-source assets: quiet check-in, neighbor's boy, no-wind scarcity, failed bread, brother's letter, burning letters, Cairo offer, chains, child fever, childbirth, and children at school.
- Added `documentation/characters/layla/prompts/replacement-batch-v0.10.md`, a fourth eleven-image replacement queue for the next ranked Layla legacy/no-source assets: cloth from the port, coffee, Ahmed's column return, the compound wall, face in the water, official papers at the door, wrapped Qur'an, walking home alone, daughter reading, nothing tonight, and traveler news.
- Added `script/audit-production-debug-leaks.py` and wired it into the dev gate, so shipped localization cannot reintroduce engine-style debug text such as `Journal Entry ID`, `DEBUG:`, `Open Event in text editor`, or `Trigger description`; the Layla QA button label is now `Open queued QA event` instead of `Debug: fire selected event`.
- Hardened `script/audit-production-debug-leaks.py` to also reject literal `ERROR:` strings and raw `cp_*` key-shaped text in player-facing localization, while allowing legitimate V3 loc calls such as `Var('cp_layla_age')` and `GetCustom('cp_layla_status')`.
- Hardened `script/audit-release-readiness.py --mode release` so release now fails while any active event art lacks generated-source provenance or while planned v0.7-v0.12 replacement assets are not generated, converted, and shipped.
- Added `script/promote-art-batch.py`, a non-destructive-by-default promotion tool that counts active legacy references for each replacement target, verifies the generated PNG and shipped DDS exist, rewires accepted event images to versioned `_vNN` DDS files, and archives superseded DDS files under `image/archive/legacy-event-pictures/<version>-superseded/`.
- Added `script/build-audio-cue-ledger.py`, generated `documentation/audio-cue-ledger.md`, and wired the ledger freshness check into the dev gate so every visible non-debug event's chosen music stinger has a reviewable event-id/title/source-line record.
- Added `script/audit-audio-palette.py`, generated `documentation/audio-palette-ledger.md`, and wired the audit plus ledger freshness check into the dev gate so event audio is checked for palette variety by person, not just cue presence.
- Hardened the event-audio contract so visible events must open with one of the seven reviewed Victoria 3 `event:/MUSIC/Stingers/events/` cues. Vanilla `event:/SFX/Events/...` paths are no longer accepted as replacements for music stingers; secondary SFX can be added only after a separate proven pattern exists.
- Added `script/audit-localization-dynamic-scope.py`, generated `documentation/localization-dynamic-scope-ledger.md`, and wired both into the dev gate so player-facing dynamic localization cannot reintroduce the observed `ERROR:[c:EGY.GetRuler...]` ruler-audience regression.
- Added a first curated motion-art pass: six visible events now use validated vanilla `.bk2` videos for rail, factory, crowd, cafe, and public-health beats, with `script/audit-event-motion.py` wired into the dev gate and superseded stills archived under `image/archive/motion-replaced-event-pictures/v0.16/`.
- Extended the motion-art pass to thirty-eight visible events by adding Farid's train/telegraph scenes, Dawud's port/steam/crane scenes, Rashid's paperwork/archive scenes, Salma's switchboard/electric/radio scenes, Karim's machine-tool/engine scenes, Huda's urban-growth scenes, Mansur's factory-migration scenes, and Nabil's public-order scenes, all using validated vanilla `.bk2` event videos.
- Added `cp_try_fire_world_response` and rerouted noncritical technology, building, conditional first-appearance, yearly, and public-order reactions through the shared 183-day/365-day visible-story cooldown lane, leaving only critical life beats on milestone routing.
- Added `cp_roll_revolution_response`, so a revolution chooses one authored person target before dispatchers run instead of letting Layla and Nabil both surface from the same rupture.
- Added `cp_roll_war_start_response`, so one war-start chooses Layla's Ahmed-conscripted beat or Yusuf's notice beat instead of opening both from the same diplomatic play.
- Added `script/build-motion-art-ledger.py`, regenerated `documentation/motion-art-ledger.md`, and wired its freshness check into the dev gate so moving event plates stay reviewable by event id, person, video asset, and source line.
- Retuned the observed `cp_layla_vox.102` land-petition scene and its follow-ups away from generic tranquil cues: the petition and listening response are now political, the dismissal is sadness, and the cruel reply is dramatic.
- Added `script/build-art-acceptance-ledger.py`, generated `documentation/art-acceptance-ledger.md`, and wired its freshness check into the dev gate so the v0.7-v0.12 replacement queue tracks generated source PNGs, shipped DDS files, reference counts, promotion state, and the next production gate.
- Refreshed `documentation/audio-rebuild.md` and `documentation/art-bible-v0.5.md` against the then-current static evidence: 356 visible audio-scored events, 131 active generated-source DDS references, 12 referenced `.bk2` event videos, and 60 vanilla video placeholders tracked as release art debt. Later replacement passes removed that video debt entirely.
- Added `script/audit-character-art-contract.py` and roster-wide seed prompt catalogs so every registered person has at least one reusable historical-scene prompt contract before custom stills or portraits are generated.
- Added `script/build-character-seed-prompt-ledger.py`, generated `documentation/character-seed-prompt-ledger.md`, and wired the ledger freshness check into the dev gate so the `gpt-image-2` seed batch is reviewable by person, prompt, export file, and target PNG before image generation.
- Added `script/export-character-seed-prompts.py`, exported 48 character seed prompts plus `image/generated/character-seeds/v0.1/gpt-image-2-seed-batch.jsonl`, and wired the export freshness check into the dev gate so the seed prompt contracts are immediately usable for gpt-image-2 generation.
- Hardened `script/build-character-seed-prompt-ledger.py` so the active seed version must cover every registered person and include one canonical portrait prompt per person. The v0.1 batch now covers all 16 registered persons with 16 portraits and 32 first-scene prompts.
- Added `script/audit-art-prompt-safety.py` and wired it into the dev gate so generated prompt exports and `gpt-image-2` manifests must preserve 600x400 readability, keep the essential face/action/object left-safe, reserve the right side for Victoria 3's event text panel, and forbid generated text/UI.
- Added `documentation/characters/layla/prompts/replacement-batch-v0.11.md`, an eleven-image queue for the next ranked Layla legacy/no-source assets: date harvest, district office, khamaseen cistern, universal male suffrage, factory field, first welfare envelope, forty-day mourning, machine guard, Hajj returnees, the old hen, and the imam's visit.
- Added `documentation/characters/layla/prompts/replacement-batch-v0.12.md`, an eleven-image queue for the next ranked Layla legacy/no-source assets: insurance list, welfare law, closed-border letter, bread tax, Mariam's Cairo letter, union meeting, merchant's scale, midwife lamp, first mill smoke, minaret silence, and command-economy stall.
- Refreshed `documentation/art-acceptance-ledger.md` and v0.12 prompt exports, bringing the active planned art queue to 66 targets across 6 ledgers with 228 legacy event-window references queued.
- Hardened `script/generate-person-debug-wrappers.py` so Person 10+ wrapper ids cannot collide with Layla's reserved `1000+N` and `2000+N` ranges; colliding non-Layla wrappers shift to the next unused 100-block while selected-event values remain stable.

Verification after this pass:

```text
Common People static audit
Events: 759
Registered persons: 16
Localization keys: 1606
Audio GUID validation: enabled
On-action validation: enabled
Law type validation: enabled
Metadata game-version validation: enabled: 1.13.8
Thumbnail validation: enabled
Paradox script BOM validation: enabled
Localization dynamic-scope validation: enabled
Scripted call validation: enabled
CP variable read/write validation: enabled
Visible event image/audio hook validation: enabled
Raw trigger_event validation: enabled
Shared law-dispatch validation: enabled
Shared non-law gatekeeper validation: enabled
On-action person-mutation validation: enabled
Production reachability validation: enabled
Issues: 0
Warnings: 0
```

```text
python3 script/generate-person-debug-wrappers.py --check
ok: 316 generated person debug QA target(s) are current
```

```text
python3 script/audit-localization-dynamic-scope.py
Common People dynamic localization scope audit
Localization files: 19
Reviewed dynamic expressions: 32
Allowed categories:
    2  Layla SoL delta variable
    1  Layla SoL variable
    1  Layla age variable
   12  Layla custom localization
    1  Layla home state pointer
    1  Layla hope variable
    7  country ruler full name
    7  country ruler role title
Issues: 0
```

```text
python3 script/build-localization-dynamic-scope-ledger.py --check
ok: documentation/localization-dynamic-scope-ledger.md is current
```

```text
python3 script/audit-event-pacing.py
Common People event pacing audit
Ambient global cooldown days: 183
Ambient per-person cooldown days: 365
First-contact global cooldown days: 183
First-contact per-person cooldown days: 365
Law-reaction global cooldown days: 183
Law-reaction per-person cooldown days: 365
World-response global cooldown days: 183
World-response per-person cooldown days: 365
Monthly router calls: 1
Monthly silent branch weights: 32
Ambient pool calls: 57
Persons with ambient pools: 16
World-response calls: 51
War-start resolver targets: layla, soldier
Revolution resolver targets: layla, nabil
Startup first-contact visible branches: 16
Max ambient fires/year from monthly cadence: 2
Max routine automatic fires/year from shared cooldown: 2
Max passive fires in first campaign year: 2
Issues: 0
```

```text
python3 script/build-event-firing-ledger.py --check
ok: documentation/event-firing-ledger.md is current
```

```text
python3 script/build-world-response-ledger.py --check
ok: documentation/world-response-ledger.md is current
```

```text
World Response Ledger
Visible non-debug events: 316
Events with unclassified or missing routes: 0
Persons with visible events: 16
Startup first-contact persons: 16 (15 non-Layla)
Persons with world-state response hooks: 16 (15 non-Layla)
Hook counts: building_built=11, button=15, conditional_setup=10, hidden_person_router=62, law_enacted=49, monthly_ambient=57, revolution=2, startup_first_contact=16, technology=18, visible_chain=121, war_end=7, war_started=2, yearly_or_date=28
```

```text
python3 script/build-motion-art-ledger.py --check
ok: documentation/motion-art-ledger.md is current

Motion Art Ledger
Motion events: 38
Persons with motion events: 12
Event window video support: yes
Issues: 0
```

```text
python3 script/audit-character-art-contract.py
Common People character art contract audit
Registered persons: 16
Character docs matched: 16
Persons with prompt docs: 16
Persons with prompt contracts: 16
Issues: 0
```

```text
python3 script/audit-audio-palette.py
Common People audio palette audit
Visible non-debug events: 316
Music cue categories used: 7/7
Tranquil share: 191/316 (60.4%)
Non-tranquil share: 125/316 (39.6%)
Issues: 0
```

```text
python3 script/build-audio-palette-ledger.py --check
ok: documentation/audio-palette-ledger.md is current
```

```text
python3 script/build-event-pacing-ledger.py --check
ok: documentation/event-pacing-ledger.md is current
```

```text
python3 script/build-character-seed-prompt-ledger.py --version v0.1 --check
ok: documentation/character-seed-prompt-ledger.md is current
```

```text
python3 script/export-character-seed-prompts.py --version v0.1 --check
ok: 48 character seed prompt export(s) and gpt-image-2 manifest(s) are current
```

Historical dev/runtime snapshot before later residence, audio, art-safety, and
live-test hardening:

```text
Common People release readiness audit
mode: dev
Summary
passed: 29
failed: 0
```

Historical release dry-run after an earlier controlled direct-binary smoke test.
This is not current proof for the latest no-launch mod tree; the current runtime
gate below now rejects stale logs until Victoria 3 is relaunched.

```text
script/audit-victoria3-logs.py --require-current-build
installed:release/1.13.8 checksum=ce22 buildid=23451701 updated=2026-05-28T23:21:24
runtime:  current-build
mod_run:  logs-after-latest-mod-file
enabled:  ['Common People']
VERSION_MISMATCH: 0
NO_DEFAULT_OPTION: 0
HIDDEN_WITH_OPTIONS: 0
DUPLICATE_EVENT_ID: 0
UNEXPECTED_TOKEN: 0
MISSING_LOCALIZATION: 0
SCRIPT_BOM_WARNING: 0
BAD_SCRIPT_VALUE: 0
CP_VARIABLE_USED_NEVER_SET: 0
RUNTIME_PROOF_FAILURES: 0
```

Current runtime gate:

```text
script/audit-victoria3-logs.py --require-current-build
installed:release/1.13.8 checksum=ce22 buildid=23451701 updated=2026-05-28T23:21:24
runtime:  current-build
mod_run:  logs-predate-latest-mod-file
enabled:  ['Common People']
RUNTIME_PROOF_FAILURES: 1
  current system.log predates latest shipped mod file; relaunch Victoria 3 before claiming this tree was loaded
```

Historical release/art snapshot before later v0.13-v0.15 promotion:

```text
Common People release readiness audit
mode: release
Summary
passed: 17
failed: 3
```

```text
python3 script/export-art-batch-prompts.py --all --check
ok: 66 art prompt export(s) and gpt-image-2 batch manifest(s) are current
```

```text
Common People event repeatability audit
Visible non-debug events: 316
self_seen_marker: 52
self_latch: 47
self_cooldown: 77
upstream_latch: 12
visible_chain_followup: 121
terminal_or_state_change: 5
intentional_repeatable: 2
Issues: 0
```

```text
Common People art provenance audit
Active event DDS references: 112
Generated source coverage:  112
Legacy/no generated source: 0
Coverage by person:
  bey: generated=4 legacy_or_missing_source=0
  layla: generated=98 legacy_or_missing_source=0
  mina: generated=2 legacy_or_missing_source=0
  nour: generated=2 legacy_or_missing_source=0
  samier: generated=1 legacy_or_missing_source=0
  soldier: generated=3 legacy_or_missing_source=0
  tarek: generated=1 legacy_or_missing_source=0
  zaynab: generated=1 legacy_or_missing_source=0
```

No ranked no-source assets remain in the active shipped event-art set:

```text
Legacy/no generated source: 0
```

Historical v0.7-v0.12 batch readiness before later v0.13-v0.15 promotion:

```text
Common People art batch plan audit
Targets: 66 across 6 ledgers
Prompts: 66
Ready planned assets: 0/66
Issues: 0
```

Historical v0.7-v0.12 promotion status before later v0.13-v0.15 promotion:

```text
script/promote-art-batch.py --all
Targets: 66
Promoted: 0
Waiting: 66
Legacy event-window references queued for replacement: 228
```

```text
ok: all 19 localization file(s) have BOM
```

```text
Common People person roster audit
Registered persons: 16
Monthly router branches: 35 weighted person entries (16 persons) + 32 silent weight
First-contact candidates: 16 (15 non-Layla)
First-contact weights: visible=166 silent=14 top=bey=16
Conditional entrants: 10 (dawud:startup/yearly/tech/building, farid:startup/yearly/tech/building, huda:startup/yearly/tech/building, karim:startup/yearly/tech/building, mansur:startup/yearly/tech/building, nabil:startup/yearly/law_enacted/revolution, rashid:startup/yearly/tech/building, salma:startup/yearly/tech/building, samier:startup/yearly/tech/building, tarek:startup/yearly/tech/building)
- bey: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- dawud: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- farid: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- huda: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- karim: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- layla: events=278 visible=267 images=267 loc_keys=1315 debug_visible=267
- mansur: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- mina: events=3 visible=2 images=2 loc_keys=8 debug_visible=2
- nabil: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- nour: events=3 visible=2 images=2 loc_keys=8 debug_visible=2
- rashid: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- salma: events=5 visible=4 images=4 loc_keys=16 debug_visible=4
- samier: events=3 visible=2 images=2 loc_keys=8 debug_visible=2
- soldier: events=4 visible=3 images=3 loc_keys=12 debug_visible=3
- tarek: events=3 visible=2 images=2 loc_keys=8 debug_visible=2
- zaynab: events=3 visible=2 images=2 loc_keys=8 debug_visible=2
Issues: 0
Warnings: 0
```

`script/audit-person-roster.py` now passes with generated queue-plus-button QA coverage for all visible registered-person windows.

```text
Common People event audio audit
Visible non-debug events: 316
Game dir: /media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game
Audio GUID validation: enabled: /media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game/sound/GUIDs.txt
Event window opened hook: enabled
Music definition files: 3
Created sounds:
  316  event:/SFX/UI/Alerts/event_appear
Opened cues:
   14  civil
   30  dramatic
   23  enthusiastic
   17  political
   34  sadness
    7  spiritual
  191  tranquil
Issues: 0
```

```text
Common People event image audit
Referenced DDS: 191
Referenced BK2: 0
Shipped DDS:    191
Missing:        0
Missing videos: 0
Unused shipped: 0
Dimensions:     191 at 600x400
Non-standard referenced images: 0
```

## Known gaps

- Current-build runtime proof is not current after the latest no-launch edits. The last logs are for local Victoria 3 `release/1.13.8` and show Common People mounted from the local symlink, but `script/audit-victoria3-logs.py --require-current-build` now rejects them because `system.log` predates the latest shipped mod file. Strict runtime proof needs a fresh relaunch, then a real Egypt gameplay save after visible first contact.
- Clean UI proof is still pending. Debug-mode runs deliberately show Victoria 3 engine overlays such as journal-entry ids and event-editor buttons; final art/prose acceptance needs a no-`-debug_mode` visual pass.
- Event audio now uses vanilla Victoria 3 music stingers. This is not yet a custom scored FMOD/music-bank pass.
- The event audio cue ledger and palette ledger are current; static proof now checks every visible event's cue plus overall/person-level stinger variety. It still needs an in-game listening pass before the palette is final.
- `cp_layla.5` childbirth is now reachable as a yearly first-child milestone, but full pregnancy, stillbirth, and childbirth-fatality variants remain future family mechanics.
- Layla now has full roster visibility and shared generated debug QA coverage in the audit, including 182 visible `cp_layla_vox.*` conversation windows. Rerun `python3 script/generate-person-debug-wrappers.py` after changing any visible person event ids; wrapper event ids stay under the four-digit audit limit while selected-event values preserve the old `30010`/`80020`/`90020` debug-button path for existing shortcuts.
- Art coverage is no longer a missing-file/source problem: 191 active DDS references resolve at 600x400 with generated-source coverage. The visible motion placeholder layer has been removed: 0 events use vanilla `.bk2` placeholders, 0 events use shipped custom motion, and `script/audit-generic-video-art.py --strict-no-vanilla-video` is green.
- The v0.7-v0.15 gpt-image-2 replacement batches are generated, reviewed, converted, and promoted, except for the intentional motion-replaced stills recorded in `documentation/art-acceptance-ledger.md`.
- First-pass art review's weakest proof points now have stronger replacements wired: Layla intro v0.6, Layla Ahmed conscripted v0.6, Layla clerk's letter v0.6, Layla conversation audience v0.6, Yusuf return v0.2, and Bey commercialized agriculture v0.2. In-game art QA still needs to confirm them at event-window scale.
- The image source library now has generated-source coverage for every active event DDS across all 16 registered persons. All former vanilla motion placeholders for Farid, Dawud, Rashid, Salma, Karim, Mansur, Nabil, Samier, Tarek, and Zaynab have been replaced by custom still art.
- Seven unused legacy DDS files have been moved out of the shipped mod tree and kept under `image/archive/legacy-event-pictures/v0.5/` for comparison.
- 1.13 compatibility is metadata-clean and install-target-clean for local 1.13.8; current-log proof is stale until Victoria 3 is relaunched against this exact mod tree.
- `script/audit-release-readiness.py --mode dev` currently passes all 38 static/local checks. `script/audit-release-readiness.py --mode release --skip-egypt-save` is a runtime/art dry-run, not full release acceptance, and should fail while current-build log proof is stale. Full release acceptance intentionally requires both fresh current-build logs and `--egypt-save <tested-save>.v3` from a manual Egypt playtest.

## Rebuild tracks

### 1. Event reliability

Definition of done:

- `script/audit-common-people.py` stays at 0 issues and 0 warnings.
- Installed-game on_action validation and scripted-call validation stay enabled.
- Localization BOM check stays green.
- Paradox script BOM validation and signed-positive-number validation stay green.
- CP variable read/write validation stays green, and fresh current-build logs contain no `cp_` "used but never set" warnings.
- A fresh current-build 1.13.x in-game run loads Common People with no `No default option`, duplicate event id, hidden-event-options, unsupported journal-entry token, or missing localization errors.
- Console probes in `cp_debug_events.txt` can fire the main law, milestone, death, and conversation paths; generated `cp_debug_person.*` selectors cover every visible registered-person window while keeping popup review in button context.
- The shared Common People journal removes dead people from the active roster; Layla no longer owns a separate persistent journal or live-action button lane.
- The routine automatic event budget remains in the 1-2 visible-beats/year target lane with a hard cap of two across all persons; year one counts the startup first-contact opener, law reactions, and routine world responses against that same budget.

Next work:

- Run `documentation/test-plan-v0.5-rebuild.md` with Common People enabled in the launcher.
- Keep `ALIVE_GUARD` green when adding new events; death-state reads should use explicit `var:... = 0` checks rather than treating variable existence as life.

### 2. Victoria 3 1.13 compatibility

Definition of done:

- Metadata targets `1.13.*`.
- In-game logs confirm no mod-version mismatch on 1.13.x.
- Vanilla on_action and event syntax touched by this mod is checked against 1.13 vanilla files, not 1.12 assumptions.

Next work:

- Keep rerunning `script/audit-release-readiness.py --mode release --skip-egypt-save` after Paradox script, image, audio, or metadata changes when no fresh gameplay save exists. Use full `--mode release --egypt-save <tested-save>.v3` for release-candidate acceptance.
- Use `script/run-victoria3-runtime-smoke.sh` for quick direct-binary compile/log smoke tests; it enables the local mod, launches Victoria 3, waits for fresh logs, runs `script/audit-victoria3-logs.py --require-current-build`, and closes the process it started. With `--keep-running`, the launch is detached with `nohup`/`setsid` so the audit timeout does not close the game. This is script-load evidence only, not an Egypt gameplay pass.
- Use `script/audit-live-test-state.sh` during manual launcher/Steam playtests; it never launches or closes Victoria 3, audits current logs, reports the latest save plus file timestamp even when log proof is stale, can require save-based Egypt gameplay proof with `--require-egypt-save`, and can run the full non-launching release gate against that same save with `--release-gate`.
- Use `script/audit-egypt-gameplay-save.py --save <tested-save>.v3` after a real Egypt pass; it verifies the save is Common People-enabled, advanced past campaign start, has EGY startup/first-contact markers, has the always-on person registry variables, gives every alive person exactly one state home marker, a journal home-state pointer stored as `type=state`, one home-place token, and one positive workplace profile, and keeps the active JE roster at three people or fewer in unique slots.
- Use `script/audit-release-readiness.py --mode runtime --egypt-save <tested-save>.v3` to combine static checks, current-build log proof, and save-based Egypt gameplay proof in one gate. Use `script/audit-release-readiness.py --mode release --egypt-save <tested-save>.v3` for release-candidate acceptance; release mode now refuses to run without either `--egypt-save` or the explicit dry-run escape hatch `--skip-egypt-save`.
- Use `script/audit-victoria3-logs.py --require-current-build` after each manual in-game smoke test to prove the active logs still match the installed build and enabled mod.
- Compare the mod's subscribed on_actions against 1.13 vanilla before adding more hooks for new persons.

### 3. Audio and music

Definition of done:

- Every visible event has an event-open sound hook.
- Major event categories have a deliberate audio palette: intimate life, law shock, war, city/industry, death, spiritual ritual, breakthrough, and conversation.
- Audio paths are validated against the installed game's `sound/GUIDs.txt` when available.
- If Victoria 3 supports modded FMOD/music banks for event use in this context, the mod ships custom cues. If not, the fallback is a curated vanilla sound palette with no silent events.

Next work:

- Run the in-game listening pass in `documentation/audio-rebuild.md`.
- Retune any event id whose stinger feels wrong in context.
- Research custom FMOD/music-bank support only after the vanilla stinger pass is proven in-game.

### 4. Image rebuild

Definition of done:

- GPT image 2 is the default generation path for new raster art.
- Each person has a canonical portrait, a style reference, and a prompt catalog.
- Existing images are not overwritten until a replacement has been selected.
- Each selected PNG source is converted to DDS and wired into its event.
- The in-game event image is readable at 600x400.

Next work:

- Run the in-game art readability pass against the current 191 active DDS references, prioritizing the event-window-safe left-half composition on the newest Samier, Tarek, Zaynab, Salma, Farid, Dawud, Rashid, Karim, Mansur, and Nabil stills.
- Keep or regenerate individual candidates based on in-game readability.
- Keep `documentation/art-acceptance-ledger.md` current after every generated source, DDS conversion, and promotion step.
- Keep the shipped event-art pool clean: `script/audit-event-images.py --strict-size --strict-unused` must stay green.
- Expand the prompt catalog to every Layla event picture reference, then repeat for Person 2.

### 5. Character expansion

Definition of done:

- Person 2 is added through the r5 recipe: new `cp_<name>_*` files, one startup registration, one `cp_roll_for_event` branch, and one guarded on_action block per hook.
- Existing `cp_layla_*` files are not edited for new-person content.
- Each person has their own variables, event ids, art, localization, generated QA selector coverage, and shared active-roster journal button. Person-owned journal entries should not be added.
- `script/audit-person-roster.py` stays green as more people are added, with every registered person represented in the monthly router and a positive silent branch preserving the ambient budget.

Recommended order:

- Person 2: Al-Sayyid / the Bey has landed with his initial land-reform spine; expand him with JE/buttons/conversation and Landowners/industrialization milestones only after the in-game smoke test passes.
- Person 3: Yusuf / the Soldier has landed with his initial war spine; expand him with battle/letter/veteran branches only after the in-game smoke test passes.
- Person 4: Samier now has an industrial-labor spine with opener, labor-law, unsafe-machine, and shared-bread beats; expand him next with strike/radicalization/death branches after the in-game smoke test passes.
- Person 5: Tarek now has an industrial-capital spine with opener, labor-law, new-boiler, and account-book beats; expand him next with profitability, strike, and Samier crossover branches after the in-game smoke test passes.

## Operating loop

Every rebuild pass should end with:

```bash
script/audit-release-readiness.py --mode dev
script/audit-common-people.py
script/audit-person-roster.py
python3 script/audit-event-pacing.py
script/audit-event-audio.py
script/build-audio-cue-ledger.py --check
python3 script/audit-audio-palette.py
python3 script/build-audio-palette-ledger.py --check
script/audit-event-images.py
python3 script/audit-character-art-contract.py
python3 script/export-character-seed-prompts.py --version v0.1 --check
script/build-art-acceptance-ledger.py --check
script/audit-victoria3-logs.py
.agents/skills/victoria3-event/scripts/check_boms.sh
git status --short
```

Before calling a release candidate ready:

```bash
script/audit-release-readiness.py --mode release --egypt-save "$HOME/.local/share/Paradox Interactive/Victoria 3/save games/<tested-save>.v3"
```

Every in-game test pass should record:

- Victoria 3 build from `system.log`.
- Whether Common People is enabled in `content_load.json`.
- Any new `error.log`, `debug.log`, `game.log`, or `system.log` findings.
- Which debug probes or live hooks were exercised.
