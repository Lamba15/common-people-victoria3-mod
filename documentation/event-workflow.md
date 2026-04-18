# Event Creation Workflow (0 → 100)

> From "I want Layla to react when Ahmed is conscripted" to "the event fires in-game with the right portrait, prose, and mechanical effect." End-to-end. Every step.
>
> This file is the operating manual. For deep references see:
> - [anchors.md](characters/layla/anchors.md) -- state model, variables, scripted triggers
> - [reactions.md](characters/layla/reactions.md) -- 50-entry reaction catalog
> - [pulse.md](characters/layla/pulse.md) -- ~110-entry monthly pool
> - [the-holy-grail.md](the-holy-grail.md) -- design philosophy
> - `.claude/skills/victoria3-event/reference.md` -- V3 script reference (verbatim vanilla examples)

---

## At a glance (the 9 steps)

| # | Step | Outputs | Verify with |
|---|---|---|---|
| 1 | Pick or draft the event | a prose kernel in `reactions.md` or `pulse.md` | grep the catalog, no duplicate id |
| 2 | Design the mechanics | trigger + state-change list | sanity-check against `anchors.md` |
| 3 | Generate the image | 600x400 PNG in `Pictures/common-people-mod-images/<char>/` | open it and look at it |
| 4 | Convert PNG → DDS | `.dds` in `mod/gfx/event_pictures/` | `file <name>.dds` shows DDS data |
| 5 | Write the event script | block in `mod/events/cp_<char>_events.txt` | game loads without syntax errors |
| 6 | Write the localization | keys in `mod/localization/english/cp_<char>_l_english.yml` | `scripts/check_boms.sh` passes |
| 7 | Wire the trigger | on_action subscription or pulse dispatcher entry | `effect_debug` or console force-fire |
| 8 | Test in-game | event fires with correct text, portrait, and state change | save/reload preserves variables |
| 9 | Commit | `git add` + message | `git log` and a playtest of the new save |

If any step fails, you fall back to the troubleshooting section at the bottom.

---

## Step 0: Prerequisites

You only do this once.

### Required

- **Victoria 3 installed** (Steam or standalone). Verify the game version matches `mod/.metadata/metadata.json`'s `supported_game_version` (currently `1.12.*`).
- **Mod symlink** from `mod/` into the game's mod directory:
  ```
  Linux:   ~/.local/share/Paradox Interactive/Victoria 3/mod/common-people
  Windows: Documents/Paradox Interactive/Victoria 3/mod/common-people
  ```
  The symlink target is this repo's `mod/` folder. That way edits in the repo are live in the game. A `.mod` descriptor pointing at the same folder also goes in the game's mod directory.
- **Codex CLI 0.121.0+**, logged in via ChatGPT with `features.image_generation = true` in `~/.codex/config.toml`. See [image-generation-workflow.md](image-generation-workflow.md) for details.
- **DDS conversion tool.** Install once:
  ```bash
  sudo apt install libnvtt-bin   # provides nvcompress (recommended)
  ```
  Fallback (if `libnvtt-bin` isn't available on your system): `sudo apt install imagemagick`. The bulk-convert script auto-detects which is present. **Do not use GIMP manually** -- the whole point of the workflow is that step 4 is one command.
- **A text editor** that shows invisible characters (to spot missing BOM). Vim / Emacs / VS Code all fine.

### Verify before starting

```bash
# Version + mod folder
victoria3 --version 2>/dev/null || echo "V3 not on PATH (fine, launch from Steam)"
ls ~/.local/share/Paradox\ Interactive/Victoria\ 3/mod/

# Codex
codex --version
grep image_generation ~/.codex/config.toml

# DDS tooling
which nvcompress || which magick
```

---

## Step 1: Pick or draft the event

Every event we ship is an entry in `reactions.md` (reactions to the world) or `pulse.md` (monthly vignettes). Those files are the source of truth. If the story beat doesn't exist there yet, **draft it there first** -- script and localization should be the *translation* of a prose kernel, never a place where the prose is first invented.

### Case A: implementing an entry that already exists

```bash
grep -n "cp_layla.homesteading" documentation/characters/layla/reactions.md
```

Re-read the entry. Note:
- The event ID (e.g. `cp_layla.homesteading`)
- The trigger spec (e.g. `on_law_enacted` → `law_homesteading`)
- The state-change list
- The default prose + any variants keyed to branch/anchor

### Case B: drafting a new entry

Open `reactions.md` (or `pulse.md`) in the appropriate section. Use the existing entries as templates. Each entry has 3 or 5 required fields:

- **Reaction**: trigger, state-change block, prose variants (default + keyed).
- **Pulse**: anchors list, branch requirements, flag requirements, cooldown, weight, prose kernel.

Once drafted, commit the docs edit separately from the code edit. That keeps *design* commits separate from *implementation* commits, which helps when a later change is purely mechanical.

### Case C: the event is an existing V3 on_action you want to hook

Check the vanilla on_actions list before inventing a trigger:

```bash
.claude/skills/victoria3-event/scripts/fetch_vanilla.sh \
  common/on_actions/00_on_actions.txt | grep -i "^on_" | head -40
```

Use an existing hook (e.g. `on_monthly_pulse_country`, `on_war_started`, `on_law_enacted`) wherever possible. Custom triggers add complexity.

---

## Step 2: Design the mechanics

Translate the prose entry into a concrete spec. For each event, fill in:

1. **Trigger.** Which `on_action` hook it subscribes to, plus any additional guards (`has_law`, `is_alive`, `cp_anchor_is_*`).
2. **Fires once or many times.** Use a scripted effect (`cp_mark_<event>_fired`) to gate one-shots. Pulse events use cooldown timers instead.
3. **State changes.** A list of calls to scripted effects -- `cp_set_anchor`, `cp_resolve_h1`, `cp_shift_weight`, `cp_shift_opinion`, `cp_mark_hardship`. *No raw `set_variable` in event blocks.* If a change isn't already in the scripted-effects library, add it to the library first -- see `anchors.md §6`.
4. **Options.** What the player clicks. Reactions usually have 1-3 options; pulse events typically have one `default_option = yes` "continue" option. Each option may add its own effect on top of the event's immediate effect.
5. **Variants.** Which prose variant fires -- resolved at display time via `triggered_desc` blocks keyed off branch letters and anchor variables.

Write the spec as 5-10 lines at the top of a scratch file, or in the event's entry in `reactions.md` / `pulse.md` if you want to keep the spec alongside the prose. Getting this clear *before* you start writing Paradox script saves ~30 minutes per event.

### Sanity check

- Does the trigger's scope match what your effect expects? `on_law_enacted` gives you country scope, not character scope -- you'll need `scope:cp_layla = { ... }` to reach the character.
- If you're setting a branch letter, does a reaction that *consumes* that letter exist, or will exist soon? Writing state that nothing reads is dead weight.
- If you're moving an anchor, is the new anchor a valid one per `anchors.md §2`?

---

## Step 3: Generate the image

Full detail in [image-generation-workflow.md](image-generation-workflow.md). Short version:

```bash
cat <<'PROMPT_EOF' | codex exec --full-auto \
  -i /home/aboelsoud/Pictures/common-people-mod-images/Layla/layla.png \
  -i /home/aboelsoud/Pictures/common-people-mod-images/Layla/cp_layla_serfdom.dds.png
Generate ONE event image for a Victoria 3 mod about Egyptian peasants.
Event: "<Event title>" (<event_id>) -- <one-sentence context>.

<describe scene, specific objects, lighting, mood -- see image-generation-workflow.md>

Save the final PNG to: /home/aboelsoud/Pictures/common-people-mod-images/<Character>/<event_id>.dds.png
Report the final saved file path in your reply.
PROMPT_EOF
```

Codex saves to `/tmp` under the current sandbox; copy it to the target folder from outside the codex session (or use `--dangerously-bypass-approvals-and-sandbox`). Keep both the 600x400 (`<id>.dds.png`) and the 1536x1024 archive (`<id>_1536.png`).

**Caveat:** Codex's image tool does *not* lock the character's face. Expect ~20% drift per generation. For shipping-quality per-character consistency you'll eventually need Midjourney `--cref`, Ideogram Character Reference, or a ComfyUI + InstantID / PuLID pipeline. Proof-of-concept is fine with Codex.

---

## Step 4: Convert PNG → DDS

Victoria 3 requires DDS for event pictures. The source PNG stays in the asset library; the DDS goes into the mod. One command does this for every image:

```bash
./script/convert-images-to-dds.sh
```

The script walks `~/Pictures/common-people-mod-images/` for any `*.dds.png`, produces sibling `*.dds` files in `mod/gfx/event_pictures/`, and skips files whose DDS is already newer than the source (idempotent -- safe to run every time). Output looks like:

```
converter: nvcompress
src:       /home/aboelsoud/Pictures/common-people-mod-images
dst:       mod/gfx/event_pictures

  ok:   cp_layla_homesteading.dds
  skip: cp_layla_serfdom.dds (dds newer than png)

converted: 1  skipped: 1  failed: 0
```

### How the script picks the converter

- **`nvcompress`** (from `libnvtt-bin`) is preferred -- purpose-built for DDS, silent, fast, produces BC3/DXT5 with alpha support.
- **ImageMagick's `magick`** is the fallback if `nvcompress` isn't on the system.
- If neither is installed, the script prints the install command and exits.

### Verify one file manually

```bash
file mod/gfx/event_pictures/cp_layla_homesteading.dds
# expect: Microsoft DirectDraw Surface, DXT5, mipmap levels: 0, 600 x 400
```

### Environment overrides

`CP_IMAGES_SRC` changes the source root (default `~/Pictures/common-people-mod-images`). `CP_IMAGES_DST` changes the destination (default `mod/gfx/event_pictures`). Useful if you keep assets somewhere else or want to stage conversions elsewhere before copying in.

### Naming rule the script relies on

Only files named `*.dds.png` are converted. The portrait reference (`layla.png`) and the full-resolution archive (`cp_layla_<event>_1536.png`) are ignored. If you add a new source image, give it the `.dds.png` extension so the bulk-convert picks it up; otherwise it stays in the asset library but doesn't ship with the mod.

---

## Step 5: Write the event script

Event files live in `mod/events/`. Each character has its own `cp_<character>_events.txt`.

### Skeleton (reaction example)

```
namespace = cp_layla

cp_layla.homesteading = {
    type = country_event
    placement = ROOT
    hidden = no
    duration = 3    # event window open 3 days before auto-resolving to default

    title = cp_layla.homesteading.t
    desc = cp_layla.homesteading.desc
    flavor = cp_layla.homesteading.f

    gui_window = event_window_1char_tabloid
    left_icon = scope:cp_layla

    icon = "gfx/interface/icons/event_icons/event_default.dds"
    # (if we end up with custom icons, point at gfx/interface/icons/event_icons/cp_...)

    picture = {
        texture = "gfx/event_pictures/cp_layla_homesteading.dds"
    }

    trigger = {
        exists = scope:cp_layla
        scope:cp_layla = { is_alive = yes }
        # H1 unset -- this is the A.H resolution, first time only
        NOT = { scope:cp_layla = { has_variable = cp_h1 } }
    }

    immediate = {
        scope:cp_layla = {
            cp_resolve_h1 = { letter = A sub = H }
            cp_set_land_anchor = landowner_wife
            cp_shift_weight = { name = cp_w_land_reform delta = 2 }
            cp_shift_weight = { name = cp_hope delta = 2 }
            cp_shift_opinion = { tag = EGY delta = 10 }
            cp_mark_joy = yes
        }
    }

    option = {
        name = cp_layla.homesteading.a
        default_option = yes
        # additional opt-specific effects (if any)
    }
}
```

### Key rules (surface the ones people forget)

- **`type = country_event`** even for character-focused events -- vanilla convention. Reach the character via saved scope, not root.
- **`trigger` guards `exists = scope:cp_layla`** -- no exceptions. Dereferencing a missing scope crashes the event.
- **`gui_window` matches portrait count** -- `event_window_1char_tabloid` (one portrait), `event_window_2char_tabloid` (two). Mismatch = empty portrait frame.
- **`left_icon` takes a scope reference** (`scope:cp_layla`), not `root`, not `this`.
- **Every option has a `name`**, and exactly one option has `default_option = yes`.
- **Mechanical effects inside options use explicit scope** -- `scope:cp_layla = { ... }`, not bare effects. Option root in a `country_event` is the country.

### Pulse event skeleton

Pulse events are hidden character events the dispatcher fires. Minimal:

```
cp_layla_pulse.fajr_in_the_dark = {
    type = country_event
    hidden = yes

    trigger = {
        exists = scope:cp_layla
        scope:cp_layla = {
            is_alive = yes
            # per-event gates from pulse.md: anchor, branch, flags
            cp_in_rural_anchor = yes
            OR = {
                has_variable = cp_cooldown_fajr_in_the_dark_expired
                NOT = { has_variable = cp_last_pulse_fajr_in_the_dark }
            }
        }
    }

    immediate = {
        # Record last-fired to support cooldown. The dispatcher picks and this just fires.
        scope:cp_layla = {
            set_variable = { name = cp_last_pulse_fajr_in_the_dark years = 100 }
        }
        # Optional: small personality drift per pulse
    }

    title = cp_layla_pulse.fajr_in_the_dark.t
    desc = cp_layla_pulse.fajr_in_the_dark.desc
    flavor = cp_layla_pulse.fajr_in_the_dark.f
    gui_window = event_window_1char_tabloid
    left_icon = scope:cp_layla
    icon = "gfx/interface/icons/event_icons/event_default.dds"
    picture = { texture = "gfx/event_pictures/cp_layla_pulse_fajr.dds" }

    option = { name = cp_layla_pulse.fajr_in_the_dark.a  default_option = yes }
}
```

Cooldown logic lives in the dispatcher's filter: the dispatcher only picks pulse events whose `cp_last_pulse_<id>` timer has expired.

---

## Step 6: Write the localization

### Create the localization file (first time for a new character)

```bash
.claude/skills/victoria3-event/scripts/new_loc.sh \
  mod/localization/english/cp_<character>_l_english.yml
```

This creates the file with the required UTF-8 BOM and `l_english:` header. Never create localization files by hand -- the BOM is too easy to miss, and without it V3 silently displays the raw key (`CP_LAYLA.HOMESTEADING.T`) instead of text.

### Add the keys

```yaml
l_english:
 cp_layla.homesteading.t:0 "The Deed"
 cp_layla.homesteading.desc:0 "[cp_layla_homesteading_desc]"
 cp_layla.homesteading.f:0 "The paper is still in the chest."
 cp_layla.homesteading.a:0 "Mine."
```

The `desc` here is a custom-loc key (`[cp_layla_homesteading_desc]`) so we can vary the prose based on branch/anchor. Define the custom loc:

```
# mod/common/customizable_localization/cp_layla_homesteading_desc.txt
cp_layla_homesteading_desc = {
    type = country

    text = {
        trigger = { scope:cp_layla = { cp_is_sultanate = yes } }
        localization_key = cp_layla.homesteading.desc_alpha
    }

    text = {
        trigger = { scope:cp_layla = { cp_is_sovereign_egypt = yes } }
        localization_key = cp_layla.homesteading.desc_beta
    }

    # default (no trigger) -- must come last
    text = {
        localization_key = cp_layla.homesteading.desc_default
    }
}
```

And add the keyed desc entries in the .yml:

```yaml
 cp_layla.homesteading.desc_default:0 "The clerk's hand on the paper..."
 cp_layla.homesteading.desc_alpha:0 "The imam signs below the Sultan's seal..."
 cp_layla.homesteading.desc_beta:0 "There is only one seal. It is new and green..."
```

### Verify BOM after saving

```bash
.claude/skills/victoria3-event/scripts/check_boms.sh
```

Must output `ok: all N localization file(s) have BOM`. If it fails, the .yml was saved without BOM (common when editing and "Save As"-ing in some editors). The script prints the fix command.

### Other languages

Run the translation script when ready to ship:

```bash
cd script && ./generate-localization.sh english ../mod/
```

Copies all English .yml files to braz_por, french, japanese, polish, russian, turkish with appropriate header replacement. The texts are the English strings -- actual translation is a human pass later.

---

## Step 7: Wire the trigger

### Reactions: subscribe to the on_action

Edit `mod/common/on_actions/cp_on_actions.txt` (or add a new file). Subscribe via nesting -- **never replace vanilla's on_action block.**

```
on_law_enacted = {
    on_actions = {
        cp_on_law_enacted_dispatch
    }
}

cp_on_law_enacted_dispatch = {
    effect = {
        # root = country, scope:law = the law that just passed
        if = {
            limit = {
                exists = scope:cp_layla
                scope:cp_layla = { is_alive = yes }
                scope:law = { is_law_type = law_homesteading }
                THIS = c:EGY
            }
            scope:cp_layla = {
                trigger_event = { id = cp_layla.homesteading }
            }
        }
    }
}
```

### Pulse events: register with the dispatcher

Pulse events don't need their own on_action -- the dispatcher in `cp_on_actions.txt` (`on_monthly_pulse_country → cp_layla_pulse.dispatch`) picks them. Adding a new pulse event means:

1. Writing the event (Step 5).
2. Adding it to the dispatcher's event list (if using an enumerated dispatcher), OR relying on the event's own `trigger` block (if the dispatcher tries events in order and lets the first-valid fire).

See `anchors.md §5` for the dispatcher pseudocode; the exact mechanism is an eventify-pass decision and will be documented in the dispatcher's source file once it exists.

### Check for trigger conflicts

```bash
grep -rn "on_law_enacted" mod/common/on_actions/
```

There should only be one `on_law_enacted = { ... }` block in the mod, and it should use the `on_actions = { cp_... }` nesting pattern. If you find a top-level override, fix it -- it's overwriting the vanilla handler and silently breaking base-game events.

---

## Step 8: Test in-game

### Launch with debug

Add `-debug_mode` to V3's launch options (Steam: right-click → Properties → Launch Options). This enables the console (`~` tilde key) and verbose error logging.

### New game or saved game

Two test modes:

1. **Fresh game as EGY**: lets you verify character spawn (`cp_startup.1`), initial scope save, and early events.
2. **Existing save**: faster to test a specific trigger. Console a force-fire.

### Force-fire the event

Open console (`~`), then:

```
event cp_layla.homesteading
```

Verify:
- The portrait shows up (not an empty frame).
- The title and desc render as text, not as raw keys.
- The icon/picture loads (not a pink missing-texture block).
- Each option's name renders.
- Clicking an option closes the window and applies the effect.

### Verify state change

After clicking through, open the console and query:

```
Observe.Variables scope:cp_layla
```

Or use `Observe.Show` inspect commands. Verify the variables you set in `immediate` are now present on Layla.

### Save-and-reload test

The persistence test most bugs hide in:

1. Save the game.
2. Exit to main menu.
3. Reload the save.
4. Re-open the variable inspector.

If `cp_layla` scope doesn't exist after reload, the initial save-scope in `cp_startup.1` is missing or scoped wrong. If variables exist but are reset, the eventify pass wrote a new `cp_layla` over the saved one.

### Monitor the error log

```bash
tail -f ~/.local/share/Paradox\ Interactive/Victoria\ 3/logs/error.log
```

Common messages and what they mean:

| Message | Cause |
|---|---|
| `Invalid scope: cp_layla` | Guard missing or character dead when event fired |
| `Event ... has a desc but no localization` | `.desc` key missing from .yml |
| `Texture not found: gfx/event_pictures/cp_layla_...dds` | DDS wasn't converted / wrong path |
| `Variable cp_h1 has non-string value ...` | Assigning a number to a flag_variable or vice versa |
| `Unknown scripted trigger cp_resolve_h1` | Library not loaded; add to `mod/common/scripted_effects/` |

### Hot reload

Edits to .yml, .txt under `mod/` can often be picked up with the console command:

```
reload localization
reload events
```

No need to restart the game for most iteration loops.

---

## Step 9: Commit

Keep commits narrow -- one event per commit is fine, or one "event + image + loc" group per commit. Git blame stays useful.

```bash
git add \
  documentation/characters/layla/reactions.md \
  mod/events/cp_layla_events.txt \
  mod/localization/english/cp_layla_l_english.yml \
  mod/common/customizable_localization/cp_layla_homesteading_desc.txt \
  mod/gfx/event_pictures/cp_layla_homesteading.dds
git commit -m "layla: homesteading event (R2, 'The Deed')"
```

Don't `git add -A` -- the `Pictures/common-people-mod-images/` folder is outside the repo, but the `.codex/generated_images/` archives and other junk can sneak in if you have symlinks or stray files. Explicit adds only.

Before pushing, a quick smoke test:

- `scripts/check_boms.sh` still passes.
- The mod still loads with no new errors in `error.log`.
- Your new event still force-fires cleanly.

---

## Troubleshooting (the usual suspects)

### Event fires but shows `CP_LAYLA.HOMESTEADING.T` in the window

Localization BOM is missing, the key is missing, or the .yml is in the wrong folder.

```bash
.claude/skills/victoria3-event/scripts/check_boms.sh
grep "cp_layla.homesteading.t" mod/localization/english/*.yml
```

### Event fires but portrait is empty

`left_icon` isn't referencing a saved scope, OR the character scope doesn't exist at fire time.

```bash
# Inspect in console:
# Observe.Characters
# ObserverCharacters.FindByVariable cp_is_layla=1
```

Or grep for the save_scope_as:

```bash
grep "save_scope_as = cp_layla" mod/events/
```

Must exist in `cp_startup.1` or the character-creation event, and the guarding `exists = scope:cp_layla` must be on every event that references her.

### Event doesn't fire at all

Trigger guard too tight, or the on_action isn't subscribed.

```
# Console:
trigger_event cp_layla.homesteading
# If this works, the event is OK but the trigger chain is broken -- check your on_action.
```

### Variables persist but state-change reactions aren't firing

The scripted effects library isn't being loaded, or the effect names are misspelled. Check `mod/common/scripted_effects/` exists and is being read (a file starting with a digit loads first; use `cp_000_effects.txt` if ordering matters).

### The mod silently doesn't appear in the launcher

`metadata.json` is malformed, OR the mod folder isn't where V3 expects. Check:

```bash
cat mod/.metadata/metadata.json
ls ~/.local/share/Paradox\ Interactive/Victoria\ 3/mod/common-people
```

### `error.log` shows thousands of entries before the mod even loads

A top-level override of a vanilla on_action (the #4 gotcha in the skill). `grep -r "^on_" mod/common/on_actions/` -- every `on_*` block must contain `on_actions = { ... }`, not a direct `effect = { ... }` at the top level.

---

## Scaling: from 1 event to ~150

Everything above is written around one event. Scaled up, the bottlenecks shift:

1. **Image consistency** at 150 events needs a face-lock pipeline. Codex drift is fine for one hero shot; unacceptable for 50 Layla images side-by-side. See [image-generation-workflow.md](image-generation-workflow.md#scaling).
2. **Prompt-writing fatigue.** Automate it: a script that reads `reactions.md` + `pulse.md` and emits one codex command per event, with the prose kernel already wired into the prompt.
3. ~~**PNG → DDS in bulk.**~~ Done -- `script/convert-images-to-dds.sh`.
4. **Localization churn.** Every event's .yml entries read the same structure. Consider a script that stubs `title/desc/flavor/a` keys with placeholder text from the prose kernel, then you only edit the ones that need polish.
5. **In-game testing.** A test harness event (`cp_debug.spawn_everything`) that force-spawns Layla in a known state and console-fires her events in sequence, so you can eyeball the full arc in a 10-minute run.

None of these are blocking for the first dozen events. They become blocking at ~25-50 events. Don't build them early.

---

## Where each step lives in the repo

```
Step 1 (design)       → documentation/characters/<char>/reactions.md, pulse.md, anchors.md
Step 2 (mechanics)    → same; spec alongside the prose entry
Step 3 (image gen)    → Pictures/common-people-mod-images/<Character>/<id>.dds.png (outside repo)
Step 4 (DDS)          → mod/gfx/event_pictures/<id>.dds
Step 5 (script)       → mod/events/cp_<character>_events.txt
Step 6 (loc)          → mod/localization/english/cp_<character>_l_english.yml
                      → mod/common/customizable_localization/cp_<id>_desc.txt (for variants)
Step 7 (trigger)      → mod/common/on_actions/cp_on_actions.txt
                      → mod/common/scripted_triggers/cp_<topic>_triggers.txt
                      → mod/common/scripted_effects/cp_<topic>_effects.txt
Step 8 (test)         → ~/.local/share/Paradox Interactive/Victoria 3/logs/error.log
Step 9 (commit)       → git
```

---

*This workflow is version 1, born from the Layla "homesteading" proof-of-concept on 2026-04-17. It will be wrong in places the second time we use it; update it in place rather than write workarounds downstream.*
