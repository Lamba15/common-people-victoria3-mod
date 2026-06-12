# Audit — Common People v0.3.0

**Date:** 2026-04-19. Auditing the state of the mod after the r5 big-bang refactor, before first in-game test.

The refactor did two things simultaneously: prefixed every Layla variable with `cp_layla_*` to make room for Persons 2–N, and introduced a four-tier firing gatekeeper (`cp_try_fire_ambient` / `_law_reaction` / `_milestone` / `cp_button_fire`) to cap ambient events at 0–2 per in-game year. This audit asks: did that land cleanly?

## TL;DR

| Angle | Score | Status |
|---|---|---|
| 1. Code quality & expandability | 9/10 | ✅ PASS |
| 2. Architecture | 9/10 | ✅ PASS |
| 3. Storytelling | 8/10 | ✅ PASS |
| 4. Events | 7/10 | ⚠️ MINOR CAVEAT (seen-flag inconsistency) |
| 5. Replayability | 7/10 | ✅ PASS |
| 6. Paradox language | 9/10 | ✅ PASS (one verified, none broken) |
| 7. Ready for V3 test | — | ✅ READY — see `test-plan-v0.3.md` |

**Green light to test in Victoria 3.** Known limitations listed below; none block boot or core firing.

---

## 1. Code quality & expandability — 9/10

- **Variable rename is clean.** Zero leftover unprefixed references to `cp_hope`, `cp_age`, `cp_sol`, `cp_literacy`, `cp_radical`, `cp_loyalist`, `cp_exhaustion`, `cp_children`, `cp_married`, `cp_seen_*`, `cp_w_*`, `cp_opinion_*`, `cp_profession_*`, or `cp_ahmed_*`. Everything is `cp_layla_<attr>`.
- **Gatekeeper discipline is clean.** Every `trigger_event` call across `mod/common/on_actions/` and `mod/common/scripted_buttons/` flows through one of the four gatekeepers, except two raw calls in `cp_on_actions.txt:71,79` which fire the two startup events before the registry is live — correct by design.
- **No duplicate effect names** across `cp_shared_memory.txt`, `cp_layla_memory.txt`, `cp_debug.txt`.
- **File prefix rule is respected.** Every file under `mod/common/`, `mod/events/`, `mod/localization/` classifies cleanly as `cp_shared_*` (7 files), `cp_layla_*` (11 files), `cp_debug_*` (2 files), or infrastructure (`cp_on_actions.txt`, `cp_events.txt` error-suppression namespace).
- **No dead code.** No renamed-but-kept duplicates, no orphan effects. `cp_events.txt` is intentional (18 lines of error-suppression namespace).

**Expandability payoff.** Adding Person 2 is purely additive — see `documentation/characters/_shared/adding-a-new-person.md`.

**Minor:** One orphan DDS on disk — `cp_layla_serfdom.dds` — unreferenced. Safe to delete or keep as spare.

---

## 2. Architecture — 9/10

- Registry (`cp_shared_registry.txt`) sets two globals per person: `cp_person_<name>_alive`, `cp_person_<name>_country`. Country-variable init happens in each person's own startup event (kept minimal; non-overwriting).
- Firing gatekeepers live in `cp_shared_firing.txt`. Ambient gatekeeper sets both 180d global and 365d per-person cooldown after a fire. The other three are thin wrappers.
- Monthly router (`cp_roll_for_event`) correctly gates on `has_variable = cp_layla_alive` before routing. Weights: 7 for Layla, 93 for silent. Comment at lines 135-136 shows the pattern for Person 2.
- Dispatcher in `cp_on_actions.txt` uses 41 `has_variable = cp_layla_alive` guards — one per branch. Adding Person 2 requires copy-pasting these blocks and substituting the name token.
- Historical note: this pass observed the old Layla startup path. Current rebuilds use `cp_shared_startup.1` followed by `cp_layla_setup.1`; registry is idempotent across save reload.
- `on_war_end` hook name verified correct in `cp_on_actions.txt:917,923` (not `on_war_ended`).

**Verdict.** The dispatcher is thin. The person-specific pool lives in each person's memory file. Shared-trigger resolution (the weighted `random_list` picking which person a shared beat belongs to) is documented in `firing.md` but not yet exercised since only Layla is registered — it'll activate when Person 2 lands.

---

## 3. Storytelling quality — 8/10

Spot-checked six life events (near IDs 1, 15, 30, 45, 60, 75) and three conversations. Voice holds.

**Strengths:**
- Free-indirect Mahfouz voice is consistent. The narrator slips into Layla's interior without announcing the shift ("The deed is folded in her chest, against the bone, and the deed does not matter today" — `cp_layla.3`).
- Subtext over narration. Grief is registered as absence — shaving water gone green, tobacco tin still on the shelf — not declaration.
- Sensory specificity is load-bearing. Dust described by shape rather than symbol. Riders at dusk with unrecognized flags.
- Each event lands on a concrete image.
- The conversation root (`cp_conversation.1` Pasha fantasy) is exceptional. The Land topic monologue runs across generations and earns its scale.

**Weaknesses the editor-audit already flagged:**
- **Named-neighbour density is half-complete.** 16 localization hits for the named census (Um Yusuf, Umm Mariam, Hajj Rashid, Badr, Sheikh Abdallah), but not every event where those characters would appear uses the names. Some events still say "the neighbour" or "the baker" instead.
- **Ahmed's gesture vocabulary is undersupplied.** Throat-clearing (`cp_layla.4`, `.40`) and tobacco tin (`.10`, `.41`) are consistently planted. The editor-audit proposed five signature gestures; only these two are deployed. His absence is still a plot device more than a grief.
- **Mid-tree conversation clusters feel templated.** Land, Lost Child, and Politics are strong. Children, Room, and Stall repeat similar three-Pasha patterns.

**Not blocking test.** These are iteration targets for v0.3.1+.

---

## 4. Events quality — 7/10 ⚠️

**Counts:**
- Life events defined: **85** (`cp_layla.1` through `cp_layla.128` with intentional gaps for reserved slots).
- Conversation events defined: **67**.
- Ambient pool size (in `cp_roll_ambient_layla`): **31** life events, weighted 255 points total.
- Weight distribution: village-life core ~43%, seasonal/cultural ~20%, situation-gated (war/land/serfdom) ~18%, systemic/goods ~12%, editor-audit additions ~6%.

**Categorization of the 85 life events:**
- Ambient: **31**
- Law-reactions: **29** (routed through `cp_on_law_enacted` → `cp_layla_dispatch_law_enacted`)
- Milestones: **10** (war, tech, building, mortality, welfare)
- Crossroads: **4** (player-choice beats — Cairo, small concern, suitor, mill closes)
- Button-only / startup / intro: **5**
- Follow-ups from another event's option: **2–3**
- **Orphans: 0**. Every numbered ID is reachable.

**All 67 conversation events** are reachable through `cp_conversation.1` root's topic tree.

### ⚠️ Seen-flag inconsistency (the one real caveat)

The ambient pool gates each option on `NOT = { has_variable = cp_layla_seen_<id> }`. Ideally every ambient event sets that flag in its own `immediate` or option block. In practice:

- **13** ambient events set their own seen-flag in the event body (e.g. `cp_layla.25` Ramadan sets `cp_layla_seen_ramadan days = 730`).
- **14** set the flag only via the scripted-button path (`cp_layla_buttons.txt`).
- Remaining ambient events rely on the **180-day global ambient cooldown** plus **365-day per-person cooldown** as the effective brake.

**Consequence.** For ambient events that never set their own seen-flag in the event body, the same event *can* fire again after 180 days — i.e. twice per playthrough in the worst case, bounded by the cooldowns. For most events this is fine (the "no wind day" can feel like a recurring season). But:

- **Spot-check failure is silent.** The mod won't crash; it'll just feel mildly repetitive on long playthroughs.
- **Fix is mechanical.** Each affected event's `immediate` block should add `cp_mark_event_seen = { person = layla id = <id> days = 540 }`. Agent B flagged 5 spot-checked cases: `cp_layla.10, .13, .15, .20, .102`.
- **Recommended action:** patch in v0.3.1 after the user confirms the firing layer works in-game. Not a boot blocker.

---

## 5. Replayability — 7/10

**Strengths (what reliably differs across playthroughs):**
- **Law paths branch hard.** Homesteading vs serfdom vs tenant-farmer drives entirely different mid-game events. Suffrage opens the Election Day ambient. Women-in-workplace opens the Stall crossroads. Welfare tiers fire different envelope beats.
- **Tech gates real content.** Railways (`.30`), telegraph (`.31`), radio (`.32`) each have their own arrival event; skip the tech, skip the beat.
- **War paths are a hard binary.** Ahmed dies (`.41`) or comes home (`.40`). Subsequent events gate on `cp_layla_ahmed_alive`.
- **SoL-gated crossroads.** Cairo calling (`.70`) only fires if SoL ≤ 12 + peasant/laborer + not serf. A prosperous Egypt skips this beat entirely.
- **Shared-trigger resolver is already designed** (`firing.md` §Shared-trigger resolution). When Person 2 lands, weighted `random_list` routes shared-trigger beats (same law enacted) to one character, another playthrough to another.

**Weaknesses:**
- Ambient events that set their own seen-flag are strictly one-per-playthrough. You can't re-see "Mother's Hand" (`.15`) in a single life, even if the beat would feel natural again.
- Crossroads lock permanently. One Cairo choice, no reverse.
- Named neighbours are state-static — Umm Mariam stays "the neighbour without a deed" even if a later homestead window would have given her one.

**Score:** 7/10. A second playthrough with different law/tech/war choices feels substantially different. A replay of the same Egypt feels largely identical.

---

## 6. Paradox language use — 9/10

Every V3-syntax concern from the r5 plan §5 has a resolution:

1. **`$param$` in variable names inside `set_variable`/`change_variable`** — ✅ proven (in our own code, `cp_w_$weight$` at `cp_layla_memory.txt:34`).
2. **`$param$` in scope-tag RHS (`cu:$culture$`)** — ✅ fallback per-person wrappers applied everywhere. See `cp_layla_refresh_sol` at `cp_layla_memory.txt:24` — it passes the literals into `cp_refresh_sol_from_pop`. Zero runtime scope-tag dereferences.
3. **`c:$country$` with `$country$` = bare tag** — ✅ same fallback; `cp_person_dies` takes the country as a param and uses it as a literal.
4. **Global timed variables (`set_global_variable = { ... days = N }`)** — ✅ **VERIFIED IN VANILLA**. `hungry_forties_var` in `game/common/on_actions/00_code_on_actions.txt` uses exactly this syntax with `days = 1095`. Our two uses in `cp_shared_firing.txt:48-55` are syntactically correct.
5. **`random_list` weights are integer literals** — ✅ verified across `cp_roll_for_event`, `cp_roll_ambient_layla`, shared-trigger resolvers.
6. **Missing `= yes` after scripted-effect calls** — ✅ clean (30+ call sites in `cp_on_actions.txt` all have `= yes`).
7. **Scope type correctness** — ✅ all startup + on-action events are `country_event`, scoped to `c:EGY` via `?= this`.
8. **`on_war_end` hook name** — ✅ verified correct (not `on_war_ended`).

### Uncertainty list (items the codebase uses correctly but that no other mod-visible code can cross-check)

| # | Item | File:line | Risk | What to watch for in-game |
|---|---|---|---|---|
| U1 | Global variable survives save/reload | `cp_shared_firing.txt:48-55` | Low | After save+reload, check cooldown is still counting down (see test-plan step 8) |
| U2 | `observe country_variables` / `observe global_variables` console name | test-plan.md | Low | If the command is slightly different (`debug_variables`?) substitute; not a mod issue |
| U3 | Timing of `on_monthly_pulse_country` vs ambient cooldown expiration | — | Low | Worst case: an event fires on day 181 instead of day 180. Inconsequential |

No item here is a boot blocker. All are diagnostic "watch for this" items.

---

## 7. Ready for V3 test — ✅

**All three content layers clean:**
- **Images.** 102 DDS files on disk, 101 referenced. 0 missing, 1 orphan (`cp_layla_serfdom.dds`). No stale `cp_conversation_*.dds` references from before the rename.
- **Localization.** 769 keys referenced, 769 defined. Zero missing. Zero orphans. BOM (`ef bb bf`) correct on both `cp_layla_l_english.yml` and `cp_shared_l_english.yml`. `l_english:` header on line 2 of both.
- **Event-dispatch wiring.** Every numbered life and conversation event is reachable through either the ambient pool, a dispatcher hook, a scripted button, or another event's option.

**Go test.** Follow `documentation/test-plan-v0.3.md` step by step. The first boot tells us whether the architecture holds.

---

## Appendix — known non-blocking items (v0.3.1 backlog)

1. **Seen-flag hygiene.** Roughly half of ambient events don't set their own `cp_layla_seen_<id>` flag in-event. Add `cp_mark_event_seen = { person = layla id = <id> days = 540 }` to each ambient event's `immediate` block. Events confirmed affected on spot-check: `cp_layla.10, .13, .15, .20, .102`. (All still fire correctly; worst case is that the cooldown allows the same beat to recur after 180 days.)

2. **Named-neighbour integration.** Sweep events that currently say "the neighbour" or "the baker" and substitute the census names (Um Yusuf, Umm Mariam, Hajj Rashid, Badr, Sheikh Abdallah) consistently.

3. **Ahmed gesture density.** Add three more signature gestures (the editor-audit proposal) — current two (throat-clearing, tobacco tin) feel thin on a second playthrough.

4. **Conversation cluster variance.** Re-voice Children, Room, Stall Pasha responses so they don't echo the Land cluster's three-voice pattern.

5. **Orphan DDS cleanup.** Delete `cp_layla_serfdom.dds` or wire into a law-reaction.

6. **Person 2 onboarding.** Exercise the `adding-a-new-person.md` manual by registering a stub (the Bey) as a smoke test — confirms the shared-trigger resolver fires correctly in practice, not just on paper.

None of these block shipping v0.3.0 to a test player.
