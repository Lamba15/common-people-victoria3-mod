# Phase A verification test protocol

One play session, ~15 minutes. Confirms the foundation works before we build on it.

## Setup

1. Enable debug mode in Victoria 3:
   - Steam → right-click Victoria 3 → Properties → General → Launch Options → add `-debug_mode`
2. Make sure the mod is symlinked (or copied) into the V3 mods directory and enabled in the launcher.
3. Start a new game as **Egypt** at 1836.1.1.

## What should happen automatically on game start

- An event fires: **"The Farmer's Daughter"** (cp_layla.1). Picture of Layla in the doorway at dawn.
- A pinned journal entry appears on the right side: **Layla al-Sharif**. The body text describes her house and daily life. The status line shows a three-line "she is thinking / doing / hoping" paragraph.

Click through the intro. The JE stays pinned.

## Test 1 — Monthly pulse fires

1. Note the number shown on the JE's progress ring (the `current_value` — this is `cp_debug_tick`). It should be **0** or **1** at game start.
2. Unpause. Let the game run 3 in-game months.
3. Pause. The JE's ring value should now be **3** or **4**.
4. The status-line prose should have changed at least once in those 3 months (the monthly mood reroll).

**Fail condition**: the value stays at 0 or 1, or never changes. That means the JE's `on_monthly_pulse` is silently failing and we have a real bug to hunt.

## Test 2 — Law dispatcher fires Layla's reaction

1. Open the debug console (backtick key `` ` ``).
2. Run: `event cp_debug.2` — this force-enacts Homesteading in Egypt.
3. Within a day or two in-game, a second event should fire: **"The Deed"** (cp_layla.2). Picture of her holding the homestead deed.
4. Click through. The JE status line should now reflect the homesteader condition (different prose about walking the field, the word "mine" not sitting right in her mouth).

**Fail condition**: no event fires within a week in-game. Possible causes: dispatcher wiring wrong, trigger syntax wrong, `currently_enacting_law` doesn't expose what we expect.

## Test 3 — Yearly pulse fires (age)

1. Run: `event cp_debug.1` — this dumps Layla's state as a diagnostic event. Note her `age` value.
2. Close the event. Unpause. Let the game run 2 in-game years.
3. Pause. Run: `event cp_debug.1` again. `age` should have increased by 2.

**Fail condition**: age stays the same. Yearly pulse is silently failing.

## Test 4 — State persists across save/reload

1. Pause. Save the game (name it `p6-baseline`).
2. Quit to main menu.
3. Load the save.
4. The JE is still pinned, with the same status. Run `event cp_debug.1` — her state values match what they were before saving.
5. Unpause, let 1 month pass. The tick advances normally (JE pulse re-subscribed cleanly after reload).

**Fail condition**: JE gone, variables reset, or pulse doesn't resume.

## Test 5 — Restoring serfdom

1. With Homesteading active from Test 2, run: `effect activate_law = law_type:law_serfdom`
2. A new event should fire: **"The Bey Returns"** (cp_layla.3). Picture of her hiding behind a wall as the bey rides in.
3. Status line prose should now reflect serfdom.

## What to report back

- Pass/fail per test (1–5).
- Any events that fire that you didn't expect.
- Any console `script_error.log` entries (pop the log file from `~/.local/share/Paradox Interactive/Victoria 3/logs/script_error.log` or similar).
- Any visual glitches in the JE layout.

Any fail on tests 1–4 is a show-stopper I need to diagnose. Failure on test 5 alone is a smaller issue — we can fix just the dispatcher branch.

Once the gate closes cleanly, we tag v0.1.1, remove the `cp_debug_tick` value from the JE's `current_value`, and start Phase B (the reactive spine: sensors wired into pulse events, pop-tick, and the first real crossroads).
