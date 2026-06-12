# Victoria 3 manual test plan — v0.3.0

> Historical r5 smoke-test plan. For current v0.5 rebuild testing on Victoria 3 1.13.x, use [test-plan-v0.5-rebuild.md](test-plan-v0.5-rebuild.md).

**Use this checklist the first time you boot the mod after the r5 refactor.** Run each step in order. Each has an action, an expected result, and a failure indicator. If a step fails, stop and check `error.log` — don't continue past a broken foundation.

## Setup

- Fresh V3 1.13.x session.
- Mod enabled (Common People).
- Start date: **1 January 1836**. Country: **Egypt**.
- Press `` ` `` or `Shift+2` to open the console. If console won't open: launch V3 with `-debug_mode` in launch options.

Keep `Documents/Paradox Interactive/Victoria 3/logs/error.log` open in a text editor. It's the authoritative source for "did this break?"

---

## Step 1 — Boot sanity

**Action.** Start the game as Egypt. Let it tick one in-game day (unpause → pause immediately).

**Expected.**
- Event `cp_layla.1` fires ("The Farmer's Daughter"). Image: Layla's portrait. 3-day duration. Main pop-up.
- After dismissing: "Layla" journal entry appears in the top-left journal panel, not yet pinned. Status line reads something like "She rises before light and works until dark."
- `error.log` has zero `cp_*` entries.

**Failure indicators.**
- No event pops up → `cp_layla_setup.1`, `cp_shared_startup.1`, or `cp_on_start` not running. Check `error.log` for "unknown on_action" or "unknown event".
- Raw key like `cp_layla.1.t` shows in title → loc BOM broken or wrong l_english header.
- Missing image / pink placeholder → DDS not loading; check `cp_layla_intro.dds` in `mod/gfx/event_pictures/`.

---

## Step 2 — Variable initialization

**Action.** V3 has no clean console command to dump variables. Two indirect checks instead:

1. **Proxy check via Step 1.** If the intro event rendered with no raw keys and the JE pinned, every country variable the event/JE reads IS set. Localization substitution fails loudly — missing vars leave the text malformed. A clean Step 1 tells you the `immediate` block ran.
2. **Hover the JE status line.** The custom_loc in `cp_layla_custom_loc.txt` reads her age, SoL tier, hope band, profession, housing, possessions, routine. If the tooltip renders coherent English (not raw keys or blanks), the variables are set and the custom_loc binding works.

**What the JE should show.** Something like "She rises before light and works until dark" + status variant + mood band + SoL descriptor. The numbers aren't shown to the player, but the *descriptions* must pick a band (e.g. "Struggling" vs "Comfortable").

**Expected variable state (for reference if you want to verify manually via a debug event later):**

| Variable | Value |
|---|---|
| `cp_layla_alive` | 1 |
| `cp_layla_age` | 22 |
| `cp_layla_hope` | 5 |
| `cp_layla_exhaustion` | 3 |
| `cp_layla_sol` | ~7–9 (from pop cohort SoL on Egypt 1836) |
| `cp_layla_literacy` | 0 |
| `cp_layla_radical` | 0 |
| `cp_layla_loyalist` | 0 |
| `cp_layla_profession_peasants` | 1 |
| `cp_layla_ahmed_alive` | 1 |
| `cp_layla_married` | 1 |
| `cp_layla_children` | 0 |

**Expected — global variables.**
- `cp_person_layla_alive` = yes
- `cp_person_layla_country` = EGY
- `cp_is_loaded` = yes

**Failure indicators.**
- Any var missing → `cp_layla_setup.1` immediate block didn't run, or `cp_register_person` didn't fire.
- `cp_layla_sol` = 0 → `cp_refresh_sol_from_pop` is broken; check pop query in `cp_shared_memory.txt`.
- Globals missing → `cp_shared_startup.1` didn't run or its trigger (`c:EGY ?= this`) failed.

---

## Step 3 — Law reaction fires + is one-shot

**Action.** Run in console:
```
event cp_debug.5
```
This activates `law_homesteading` in Egypt, which should route through `cp_on_law_enacted` → `cp_layla_dispatch_law_enacted` → `cp_try_fire_law_reaction` and fire `cp_layla.2`.

**Expected.**
- `cp_layla.2` fires ("The Deed"). Image: `cp_layla_homesteading.dds`.
- Dismiss. Check `observe c:EGY` — `cp_layla_seen_homesteading` should now be set with ~540 days remaining.
- Revert the law via console (`activate_law = law_type:law_tenant_farmers`) then re-enact homesteading with `cp_debug.5` again.
- **`cp_layla.2` should NOT re-fire** (seen-flag blocks it).

**Failure indicators.**
- Event doesn't fire → dispatcher guard is failing; check `cp_on_actions.txt` `cp_on_law_enacted` block guards `has_global_variable = cp_person_layla_alive`.
- Event fires twice → seen-flag not set or not checked. Check `cp_layla.2`'s immediate block.

---

## Step 4 — Ambient firing + cooldown

**Action.** Run in console:
```
event cp_layla.13
```
This fires "The No-Wind Day" directly (bypassing the 7% monthly roll).

**Expected.**
- Event fires, standard ambient popup.
- Dismiss. Check globals: `cp_global_ambient_cooldown` set with ~180 days remaining; `cp_person_layla_ambient_cooldown` set with ~365 days remaining.

**Now test the cooldown.** Advance time 1 month (unpause briefly, then pause). Try:
```
event cp_layla.14
```

**Expected** — this bypasses the monthly roll and fires directly (because you called it explicitly). But if instead you wait 6 months without doing anything and the monthly router tries to pick Layla, `cp_try_fire_ambient` will no-op because `cp_global_ambient_cooldown` is still active. You won't see another ambient event fire organically until the cooldown expires (~180 days).

**Failure indicators.**
- Cooldown variables don't get set → `cp_try_fire_ambient` effect is broken; check the `set_global_variable` blocks in `cp_shared_firing.txt:48-55`.
- Cooldown variables get set but have no `days` counter → **STOP**. This means V3 silently dropped the `days` parameter. The ambient budget is broken. Open an issue.

---

## Step 5 — Button bypasses ambient cooldown

**Action.** With the 180-day cooldown still active from Step 4, find the "Check on Layla" button on her JE (bottom of the journal panel). Click it.

**Expected.**
- An ambient event fires immediately (picks one at random from the button's eligible pool). Cooldown is ignored — the button calls `cp_button_fire`, which doesn't check the gatekeeper.
- Clicking the button a second time within a few seconds: a *different* event fires (seen-flags on the just-fired event prevent re-picking it).

**Failure indicators.**
- Button greyed out → check JE scripted_button block.
- Same event fires on both clicks → seen-flag isn't set by the button path; check `cp_layla_buttons.txt` for the `set_variable` in each option.

---

## Step 6 — Milestone fires regardless of cooldown

**Action.** Run:
```
event cp_debug.6
```
Five times. This ages Layla by 50 years (22 → 72). Then:
```
event cp_debug.36
```
Forces a mortality recompute.

**Expected.**
- After Layla reaches 60+, the yearly mortality dispatcher rolls against her age curve. With age 72, mortality pressure is high.
- An age-mortality milestone fires (e.g. `cp_layla.80` or `cp_layla.83`, "The Last Morning" or similar). **Fires despite ambient cooldown** because milestones use `cp_try_fire_milestone` which bypasses all budgets.
- Eventually `cp_layla_alive` = 0 and `cp_person_layla_alive` global is removed. JE closes cleanly.

**Failure indicators.**
- No mortality event after age 72 → yearly dispatcher not checking age thresholds. Check `cp_on_yearly` in `cp_on_actions.txt` (search `cp_layla_age`).
- JE stays active after death → JE trigger doesn't guard on `cp_layla_alive = 1`. Check `cp_layla_journal_entries.txt`.

---

## Step 7 — Monthly pulse budget test

**Action.** Start a **fresh** game (don't carry cooldowns from previous steps). Unpause at x5 speed. Let 12 in-game months pass without clicking buttons or firing debug events.

**Expected.**
- **1–2 ambient events fire over 12 months.** Target rate per design: 0–2/year (budget rules in `firing.md`).
- Events are picked randomly from `cp_roll_ambient_layla` and each sets the global + per-person cooldown.
- Best case: first fires around month 1–3 (7% monthly chance, expected ~14 months until first fire, but variance high); second fires 6+ months after the first (global cooldown expires).
- Law enactments, war events, tech, etc. can add 0–3 more events on top (they bypass ambient budget).

**Failure indicators.**
- **Zero events in 12 months** → monthly router not firing. Check `cp_on_monthly` in `cp_on_actions.txt` calls `cp_roll_for_event = yes`. Check `error.log`.
- **5+ ambient events in 12 months** → cooldown gate broken (likely Step 4 failure mode; `days` parameter silently dropped).

---

## Step 8 — Save / reload persistence

**Action.** Play until an ambient event fires (so cooldowns are active). Save. Quit to main menu. Reload.

**Expected.**
- On reload: `cp_global_ambient_cooldown` still has correct days remaining (if 30 days passed in-game after the fire and before save, should show ~150 days remaining).
- `cp_layla_seen_*` flags persist with correct remaining days.
- JE status line unchanged.
- No events re-fire from the reload.

**Failure indicators.**
- Cooldowns reset to 180/365 on reload → `days` parameter behavior different under save/load. Flag as verified-but-concerning; substantive issue.
- Cooldowns vanish entirely on reload → `set_global_variable` doesn't save. Architecture broken; open issue.
- Layla intro re-fires → `cp_layla_setup.1` or first-contact routing is not respecting `cp_layla_alive`, `cp_layla_met_player`, or the global registry flag.

---

## Step 9 — Multi-person readiness (smoke test, no Person 2 code required)

Only Layla is registered in v0.3.0. This step validates that the router and dispatcher shape is ready for Person 2 without actually implementing one.

**Action.** Read `mod/common/scripted_effects/cp_shared_firing.txt` at lines 129-139 (the `cp_roll_for_event` router). Verify:
- Layla's branch weight is `7`.
- There's a `93 = { }` silent branch.
- A comment explicitly shows the pattern for adding Person 2 (`7 = { trigger = { has_variable = cp_bey_alive } cp_roll_ambient_bey = yes }`).

Read `mod/common/on_actions/cp_on_actions.txt`. Search `cp_person_layla_alive`. Every `if`-block guard follows the pattern:
```
if = {
    limit = {
        has_global_variable = cp_person_layla_alive
        c:EGY ?= this
        has_variable = cp_layla_alive
    }
    cp_layla_dispatch_<hook> = yes
}
```

**Expected.**
- 41 such guarded if-blocks (one per hook per person — currently all Layla).
- The pattern is self-documenting: to add Person 2, copy-paste a block with the name substituted.

**Failure indicator.**
- Guards are missing or inconsistent → adding Person 2 will require refactoring, not just appending. Block shipping Person 2 until fixed.

**Optional deep test.** If you want to actually validate multi-person resolution, follow `documentation/characters/_shared/adding-a-new-person.md` to register a stub Person 2 (the Bey) with just one intro event and one ambient. That's a half-day of work and confirms the shared-trigger `random_list` resolver works in practice.

---

## Step 10 — `error.log` audit

**Action.** After running Steps 1–8, quit V3. Open `Documents/Paradox Interactive/Victoria 3/logs/error.log` in a text editor. Search for:

- `cp_`
- `common.people`
- `Unknown script command`
- `unknown key`

**Expected.**
- Zero `cp_*` or `common.people` entries.
- Any unrelated vanilla errors (AI, diplomacy, modifier warnings) are fine — not our problem.

**Failure indicators.**

| Log pattern | Likely cause |
|---|---|
| `Unknown variable: cp_layla_*` | Var never initialised; `cp_layla_setup.1` immediate block missed it |
| `Unknown effect: cp_*` | Effect not defined in `scripted_effects/` |
| `Unknown localization key: cp_layla.*` | Key missing from `cp_layla_l_english.yml` |
| `Unknown texture: cp_layla_*.dds` | Image file missing from `mod/gfx/event_pictures/` |
| `Unknown on_action: cp_*` | Hook not subscribed in `cp_on_actions.txt`, or typo |
| Paradox script parse error | Syntax error (usually unbalanced `{` `}`) in a .txt file |

Any `cp_*` line in `error.log` is a ticket. Fix before v0.3.1 tag.

---

## Post-test

If Steps 1–8 all pass:
- ✅ Architecture is sound.
- ✅ Gatekeepers work.
- ✅ Cooldowns hold.
- ✅ Save/reload preserves state.

You're cleared to:
1. Play a full Egypt campaign with Layla as background narrative.
2. Start work on Person 2 using `documentation/characters/_shared/adding-a-new-person.md`.
3. Patch the v0.3.1 backlog items from `documentation/audit-v0.3.md` §Appendix.

If any step fails: stop, read `error.log`, diagnose the specific breakage. Don't paper over it — the whole point of the r5 refactor is that these layers are orthogonal, so one failure should be localized.
