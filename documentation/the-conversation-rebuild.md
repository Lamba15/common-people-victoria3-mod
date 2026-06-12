# The Conversation Rebuild

**A design plan for nuking `cp_conversation.1..160` and replacing it with the interlocutor-roster system.**

Plan date: 2026-04-19.

Authored during the v0.3.0 test session, when firing worked, the content didn't, and the user said: *"the whole imagine conversation thing needs to get nuked and rethought."*

---

## 1. Why we're doing this

The current conversation system has one framing: Layla imagines herself standing before the Pasha on a long carpet the colour of old blood, in a palace she has invented from rumour. She picks a topic (Land, Ahmed, Children, City, Paper, Politics, Mill, Small Thing, Distance, Envelope, Vote, Stall, Nile, Lost Child, School). The Pasha responds one of three ways (dismissive / engaged / cruel). The fantasy dissolves. She returns to the quern.

**What the Pasha audience did well** — it gave Layla a *voice*. She's silent in her own life. The fantasy was the one place her interior could expand into speech.

**Why it has to go:**

1. **It's a dress rehearsal, not a life.** She goes to Cairo in her mind to be articulate ABOUT her life. You watch her rehearse for a life she's already living.

2. **The frame repeats.** Every click opens the same door, walks the same carpet, sees the same ruler. The randomness is in which reply he gives, not in what kind of moment you get.

3. **It's deterministic.** Pick topic → pick Pasha response → fantasy dissolves. The player is running an interview, not overhearing a life.

4. **It doesn't react to the world.** Egypt in 1836 has a Pasha. Egypt in 1925 may have a president, a constitution, a parliament. The fantasy never changes. The woman is frozen in one fantasy for a hundred game-years.

5. **It doesn't react to her.** A peasant Layla and a homesteader Layla and an old-woman Layla all address the same imagined Pasha the same way, because the event doesn't know which Layla is clicking the button tonight.

6. **Only one person she's allowed to imagine speaking to.** Her actual life has many voices around her — Ahmed, Um Yusuf, the Bey, her daughter, her dead mother, the stranger at the well. The button channels all of her speech through a single distant ruler.

What we're rebuilding isn't a smaller version of the Pasha audience. It's a different contract with the player.

---

## 2. The new essence

**The button is the place where Layla's voice lives in its natural domain.**

She speaks with the people her voice is allowed to reach: her husband, her mother (as memory), her neighbour across the wall, the Bey standing over her field, the factory owner at the gate, the stranger at the well, herself alone. And — yes — still sometimes the distant ruler, because a woman like Layla *does* imagine that conversation, and her politics are partly built out of imagined audiences.

**Every click is a chance roll.** The player never picks who. State-gated random_list picks an eligible interlocutor; the scene opens; the player makes choices *inside* the scene; the scene closes. No menu. No pre-selection. The surprise is the feature.

**Inside the scene, the player steers the exchange.** Pick what she says. Pick how she answers him. Pick whether she stays or walks away. Two or three choice points per scene, each branching to different lines. This is the part where the button is a *conversation* and not just a vignette.

**The scene is state-aware everywhere.** The ruler's title is dynamic: Pasha in 1836, maybe Khedive later, maybe President after a revolution. Ahmed's scenes adapt to whether he's newly married, conscripted, back from war, old, dying. The Bey exists only when serfdom or tenant-farming applies. The factory owner exists only when she or Ahmed works in a factory.

**The player is always the silent witness to Layla's speech.** She does not address the player. When her lines contain "you," she's speaking to whoever is in the scene with her. The player reads the exchange the way a reader reads a passage in a novel.

---

## 3. Design principles (non-negotiable)

1. **Chance, not menu.** Clicking the button rolls the random_list. Never show a roster of interlocutors.

2. **State-aware at every level.** Who she's imagining, what they say, what she says, what options the player has — every one of these is gated on her current state and the world's current state.

3. **Branching happens *inside* the scene, not before.** Once the scene opens, the player's choices shape the exchange. Not before.

4. **Mahfouz register.** Free-indirect, sensory, subtext. No narration ("you see X"). No therapy-speak. No didactic politics. Specifics before abstractions.

5. **Short is better than long.** Each scene = 80–250 words of flavor + 2–3 choice points × 2–3 branches each. Not a novella per click. A paragraph overheard.

6. **Scenes can change her.** A scene that shifts no weight variable is vestigial. The button is a way her inner life grows or frays; each exchange should push one of: `cp_layla_hope`, `cp_layla_exhaustion`, `cp_layla_radical`, `cp_layla_loyalist`, `cp_layla_recent_joy`, `cp_layla_recent_hardship`, occasionally something topic-specific.

7. **Replayability is the design driver.** Across a 100-year playthrough the player will click the button ~20–40 times. No two playthroughs should feel the same. Interlocutor pools, era variants, state variants, and within-scene branching compound: the button is deliberately combinatorial.

8. **The Pasha fantasy is one voice, not the whole system.** Keep it. Rebuild it to match the new pattern. Don't let it hog the architecture.

9. **Never address the player directly.** If she says "you," she's saying it to a person in the scene. The player is not a character.

10. **Era-awareness via vanilla scope.** Rulers, titles, wars, laws — look them up via V3 scope references at loc time (`[ROOT.GetCountry.GetRuler.GetFullName]`, `has_law`, `has_technology_researched`) rather than hardcoding 1836 facts.

---

## 4. The interlocutor roster

Ten interlocutors at full scope. Each is a *pool* of scenes, not a single scene. The button's top-level `random_list` rolls against the roster; only eligible interlocutors (state-gated) are in play.

| Interlocutor | Gated by | Weight | What this pool carries |
|---|---|---|---|
| **Ahmed** (her husband) | `cp_layla_ahmed_alive = 1` | high when alive | Intimate, married, mostly wordless. Conversations with the body close by — at the door with the bucket, at the rim of the oven, under the blanket before sleep. |
| **Her daughter** | `cp_layla_children > 0` | medium | Generational. Teaching. Worry. Sometimes the daughter asks a question Layla cannot answer. Sometimes Layla makes the daughter wait. |
| **Her mother** (memory/dream) | always (scaling by her age) | rising with age | The dead speak. Her mother returns in the flour on her hands, in a smell, in a rhythm of folding. The mother's advice is never practical. It is always correct. |
| **Um Yusuf** (Coptic neighbor) | rural + `cp_layla_profession_peasants` or similar village gate | medium | Across faiths, ordinary friendship. They talk over the wall. Sometimes about nothing. Sometimes about the priest's son. |
| **Umm Mariam** (the landless neighbor) | rural + `cp_layla_owns_land` (for the contrast that the pool mines) | medium | Class guilt up close. Layla owns the field. Umm Mariam works the field next door and does not, today, have paper. They are friends. The friendship is uneven. |
| **The Bey** (her landlord / former landlord) | `cp_layla_under_serfdom` OR ex-serf within 10y window | medium, falling after homesteading | Power at three metres. He asks after her husband. She answers. The cup of tea he does not offer. When she is homesteader, he comes less, but when he comes, it is worse. |
| **The factory owner** | urban + `cp_layla_profession_laborers` OR Ahmed laborer | medium when urban | A man in a clean shirt who has never touched the machine. He knows her name because she is on a ledger. He speaks in the voice of the ledger. |
| **The stranger at the well / in the lane** | always | low | A traveler passes. Asks the road. Says one thing that stays. The world reaches her through strangers — news, rumor, gossip, dread. |
| **God / herself alone** | always, rising with `cp_layla_exhaustion` or after bereavement | rising in adversity | The fire, the dark, the Qur'an on the shelf. A prayer that is not a prayer. A line she says aloud to no one and then to no one again. |
| **The ruler of Egypt** (Pasha / Khedive / President / whoever) | always | low (~10% of rolls) | The imagined audience. Kept. Rebuilt. Era-aware. When Egypt has a Khedive, the fantasy has a Khedive. When Egypt has a parliament, it has a minister with a clerk and a telephone. |

Optional later additions (v0.4+):
- **A journalist** (when press laws open + late-era newspapers reach the village)
- **Her grown son** (if `cp_layla_children > 0` + male child flag + adult age)
- **A midwife / healer** (during pregnancies or illness)
- **A soldier** (if Ahmed enlisted or son enlisted, a memory of the unit)
- **A French agent** (if France has colonial interest in Egypt, era-gated)

---

## 5. The scene-variant taxonomy

Each interlocutor's pool is a matrix across **four axes** of variation:

### Axis A — Era (world state)

Era is derived from game state at click-time, not hardcoded:

- **Ruler title** → `[ROOT.GetCountry.GetRuler.GetFullName]` and `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` (Pasha, Khedive, Sultan, President). No hardcoded "the Pasha says."
- **Government form** → `has_law = law_type:law_autocracy` / `law_oligarchy` / `law_presidential_republic` / etc. Branches the setting (palace carpet vs ministry office vs parliament lobby).
- **Tech era** → `has_technology_researched = X`. Telephone on the desk only if telegraphy/telephony. Portrait on the wall of an earlier ruler only if that ruler has died.
- **Major events** → after an Egyptian defeat, the Ruler scene changes color. After a revolution, it changes again. State variables like `cp_layla_w_revolution` or `has_variable = recently_lost_war` gate specific lines.

### Axis B — Her state (who Layla is tonight)

- **Marital** → `cp_layla_ahmed_alive`, `cp_layla_ahmed_at_war`
- **Land** → `cp_layla_owns_land`, `cp_layla_under_serfdom`
- **Profession** → `cp_layla_profession_peasants` / `_laborers` / `_farmers` / `_shopkeepers` (self-employed)
- **Location** → `cp_layla_in_city` / `_in_cairo` / `_in_alexandria`
- **Material** → `cp_layla_sol` tier, `cp_layla_welfare_tier`, `cp_layla_tax_burden`
- **Political** → `cp_layla_radical > 0`, `cp_layla_loyalist > 0`, `cp_layla_has_voted`
- **Family** → `cp_layla_children`, `cp_layla_lost_a_child`, `cp_layla_daughter_at_school`
- **Biographical** → `cp_layla_age` bands (young wife / middle / old), `cp_layla_literacy`

### Axis C — Within-scene branching (player choice)

Each scenario has 2–3 choice points. Each choice reveals part of her:

- **What she says first** (dictates tone): "May I speak?" vs "I will speak, and you will hear."
- **How she answers him**: the pleading line, the argument, the stone-faced silence.
- **Whether she stays or leaves**: accepting his word, or refusing it, or going without answering.

Each branch sets different weight deltas. A Pasha scene where Layla *walks away* pushes `cp_layla_radical +1`. A Pasha scene where she *accepts his word* pushes `cp_layla_loyalist +1`. A scene where she *persists across his rebuff* pushes `cp_layla_exhaustion +1` AND `cp_layla_hope +1`.

### Axis D — Conversation history

She doesn't repeat herself. Each scenario sets a `cp_layla_spoke_<topic>` flag with a days=N cooldown (e.g. 540 days), and gates new scenes against it. When a pool has exhausted all eligible scenes, the button falls back to a general "alone with her thoughts" scene.

Also: *persistent* flags for significant moments. If she once walked out of the Pasha's chamber, a later Pasha scene references it. "Last time, you did not stay." This is where the system becomes memory, not just reaction.

---

## 6. Architecture

### 6.1 The button

Single button on the JE, renamed from "Imagine a conversation" to something closer to the new essence:

> **"A word between."**
>
> *Sometimes she lets the scene come: a voice at the door, a man on a carpet, her mother in the flour. Click.*

(Open to renaming. `"A word tonight."` / `"Who speaks to her."` / `"A few minutes overheard."`)

Trigger/cooldown: 90 days minimum between clicks (current `cp_layla_audience_cooldown` pattern, kept).

Button effect calls `cp_layla_roll_interlocutor = yes` — a scripted effect that random_lists over the roster.

### 6.2 The dispatcher — `cp_layla_roll_interlocutor`

Located in `mod/common/scripted_effects/cp_layla_memory.txt` (new block alongside `cp_roll_ambient_layla`).

```
cp_layla_roll_interlocutor = {
    random_list = {
        # Ahmed — high weight while alive, vanishes when dead
        25 = {
            trigger = {
                has_variable = cp_layla_ahmed_alive
                var:cp_layla_ahmed_alive = 1
                NOT = { has_variable = cp_layla_audience_cooldown }
            }
            cp_button_fire = { event = cp_layla_vox.10 person = layla }
        }

        # Her daughter — medium, gated on children exist
        15 = {
            trigger = {
                var:cp_layla_children > 0
            }
            cp_button_fire = { event = cp_layla_vox.20 person = layla }
        }

        # Her mother — always, rising with her age
        10 = {
            # weight scaled later via scripted trigger if we want age-banding
            cp_button_fire = { event = cp_layla_vox.30 person = layla }
        }

        # Um Yusuf — rural neighbor
        10 = {
            trigger = {
                NOT = { has_variable = cp_layla_in_city }
            }
            cp_button_fire = { event = cp_layla_vox.40 person = layla }
        }

        # Umm Mariam — rural + she owns land (class contrast)
        10 = {
            trigger = {
                NOT = { has_variable = cp_layla_in_city }
                has_variable = cp_layla_owns_land
            }
            cp_button_fire = { event = cp_layla_vox.50 person = layla }
        }

        # The Bey — serfdom or recently former
        10 = {
            trigger = {
                OR = {
                    has_variable = cp_layla_under_serfdom
                    has_variable = cp_layla_bey_still_near
                }
            }
            cp_button_fire = { event = cp_layla_vox.60 person = layla }
        }

        # The factory owner — urban laborer
        10 = {
            trigger = {
                has_variable = cp_layla_in_city
                OR = {
                    has_variable = cp_layla_profession_laborers
                    has_variable = cp_layla_ahmed_profession_laborer
                }
            }
            cp_button_fire = { event = cp_layla_vox.70 person = layla }
        }

        # The stranger — always
        8 = {
            cp_button_fire = { event = cp_layla_vox.80 person = layla }
        }

        # Herself / God — always, higher when exhausted
        8 = {
            cp_button_fire = { event = cp_layla_vox.90 person = layla }
        }

        # The ruler — lower weight, era-aware INSIDE the scenario
        8 = {
            cp_button_fire = { event = cp_layla_vox.100 person = layla }
        }
    }
}
```

Each `cp_layla_vox.X0` is the INTERLOCUTOR'S scenario-picker event. It in turn opens on the right scenario.

### 6.3 The interlocutor scenario event — e.g. `cp_layla_vox.10` (Ahmed)

Hidden event. Rolls for which *scene* with Ahmed to open, based on her and his state.

```
cp_layla_vox.10 = {
    type = country_event
    hidden = yes
    orphan = yes

    immediate = {
        random_list = {
            20 = {
                trigger = {
                    has_variable = cp_layla_ahmed_at_war
                    NOT = { has_variable = cp_layla_spoke_ahmed_letter }
                }
                trigger_event = { id = cp_layla_vox.11 popup = yes }
            }
            20 = {
                trigger = {
                    var:cp_layla_age <= 30
                    NOT = { has_variable = cp_layla_spoke_ahmed_newly_married }
                }
                trigger_event = { id = cp_layla_vox.12 popup = yes }
            }
            20 = {
                trigger = {
                    has_variable = cp_layla_ahmed_profession_laborer
                    NOT = { has_variable = cp_layla_spoke_ahmed_millbread }
                }
                trigger_event = { id = cp_layla_vox.13 popup = yes }
            }
            # ... 5-8 total scenarios for Ahmed
            # Fallback if all scenarios are on cooldown
            1 = {
                trigger = { always = yes }
                trigger_event = { id = cp_layla_vox.19 popup = yes }
            }
        }
    }
}
```

### 6.4 The scenario event — e.g. `cp_layla_vox.11` (Ahmed at war, the letter doesn't come)

This is where prose + choices live. One scenario event per scene. Structure:

```
cp_layla_vox.11 = {
    type = country_event
    placement = root
    title = cp_layla_vox.11.t
    desc  = { first_valid = { ... state variants ... } }
    flavor = { first_valid = { ... state variants ... } }
    event_image = { texture = "..." }
    duration = 5

    immediate = {
        set_variable = { name = cp_layla_spoke_ahmed_letter days = 540 }
    }

    # Choice 1 — what she says
    option = {
        name = cp_layla_vox.11.a
        # "Nothing. She lets the silence be."
        trigger_event = { id = cp_layla_vox.11.a1 popup = yes }
    }
    option = {
        name = cp_layla_vox.11.b
        # "Asks the neighbour if her son wrote this month."
        trigger_event = { id = cp_layla_vox.11.b1 popup = yes }
    }
    option = {
        name = cp_layla_vox.11.c
        # "Writes something to him in her head, does not send it."
        trigger_event = { id = cp_layla_vox.11.c1 popup = yes }
    }
}
```

Each follow-up (`.a1`, `.b1`, `.c1`) is another scenario event with its own flavor and another choice point, or a closer.

### 6.5 The closer pattern

Scenes end with one of a few closer types:

- **Wordless** — she turns back to the work. No option text, just a dismiss.
- **With weight** — the option applies a `cp_shift_*` effect before dismissing.
- **With memory** — sets a persistent flag the system can reference later ("last time you did not stay").

### 6.6 File layout

```
mod/events/
    cp_layla_conversation_events.txt    # DELETE after migration
    cp_layla_vox_events.txt             # NEW — all scenarios, ~400-500 events

mod/common/scripted_effects/
    cp_layla_memory.txt                 # + cp_layla_roll_interlocutor

mod/common/scripted_buttons/
    cp_layla_buttons.txt                # rename conversation button + rewire

mod/localization/english/
    cp_layla_conversation_l_english.yml # DELETE after migration  (or merge into main)
    cp_layla_vox_l_english.yml          # NEW — all scene loc (~2000-2500 keys)

mod/gfx/event_pictures/
    cp_layla_conversation_*.dds         # AUDIT and either reuse or retire
    cp_layla_vox_*.dds                  # NEW — per-interlocutor image palette
```

New namespace: `cp_layla_vox` (for "voice" — she speaks, or is spoken to). Avoids any legacy `cp_conversation.*` confusion.

### 6.7 Numbering convention

`cp_layla_vox.<interlocutor>0..<interlocutor>9X`:

- `cp_layla_vox.10-19` — Ahmed scenarios (11, 12, 13... ; .19 fallback)
- `cp_layla_vox.20-29` — Daughter
- `cp_layla_vox.30-39` — Her mother
- `cp_layla_vox.40-49` — Um Yusuf
- `cp_layla_vox.50-59` — Umm Mariam
- `cp_layla_vox.60-69` — The Bey
- `cp_layla_vox.70-79` — The factory owner
- `cp_layla_vox.80-89` — The stranger
- `cp_layla_vox.90-99` — Herself / God
- `cp_layla_vox.100-109` — The ruler
- Follow-ups use the same base + letter: `cp_layla_vox.11.a1`, `.11.a2`, `.11.b1`, etc.

**Critical naming rule:** option letters don't use `.f` (collides with `flavor = .f` loc convention). Use `.a`, `.b`, `.c`, `.d`, `.e`, `.g`, `.h`, `.i`, `.j`, `.k`, `.l`, `.m`, `.n`, `.o`, `.p`, `.q`, `.r`, `.s`, `.t`, `.u`, `.v`, `.w`, `.x`, `.y`, `.z` — skipping `.f` — and then `.a1`, `.a2` for nested branches.

---

## 7. Content scale (honest)

Per interlocutor, aiming for **5–8 distinct scenarios**, each with **2–3 choice points × 2–3 branches**. That gives:

- **Ahmed**: ~6 scenarios × ~2.5 avg branches × ~2 levels = ~30 events
- **Daughter**: ~5 × ~2 × ~2 = ~20 events
- **Mother**: ~4 × ~2 × ~2 = ~16 events
- **Um Yusuf**: ~4 × ~2 × ~2 = ~16 events
- **Umm Mariam**: ~4 × ~2 × ~2 = ~16 events
- **Bey**: ~5 × ~2.5 × ~2 = ~25 events
- **Factory owner**: ~5 × ~2.5 × ~2 = ~25 events
- **Stranger**: ~6 × ~2 × ~1 = ~12 events (strangers tend to be single-exchange)
- **Herself / God**: ~6 × ~1 (no real branching — self-talk is linear) = ~6 events
- **Ruler**: ~6 × ~3 × ~2 = ~36 events (most branched, most era-variant)

**Plus 10 interlocutor-level scenario pickers** (`cp_layla_vox.10, .20, .30...`).

**Plus ~10 fallback events** (`.19, .29, ...`) when an interlocutor's pool is exhausted.

**Total: ~220 events** at full scope. Not 500. (My earlier number was off; reality on a close re-count is tighter.)

**Localization keys:** each event has title + desc + flavor + 2–3 option names + sometimes 3–5 state-triggered desc variants. Call it ~10–15 keys per event. **~2500–3500 loc keys total.**

**Images:** one per interlocutor as a base palette (~10), plus ~20 situation-specific ones (Ahmed at war vs Ahmed at mill vs Ahmed dying, etc.). **~30 new DDS.** Many existing `cp_layla_conversation_*.dds` images are reusable; audit during migration.

**Writing budget (honest):** at 5–10 minutes per scenario event of quality Mahfouz-register prose × 220 events = **~30–40 hours of focused writing**. Plus wiring + loc + images. Call it **60–80 hours total for v0.4.0.**

Not one session. Not one week. This is the centerpiece of v0.4.

---

## 8. Writing voice — what must not drift

Everything in `cp_layla_vox.*` obeys the existing conversation register, clarified:

1. **Free indirect, not stream of consciousness.** The narrator is present. The narrator has an opinion. We slip into her interior without announcing — "She is aware of her own breath" — but we also pull back for a metaphor or an observation she wouldn't make of herself.

2. **Specificity outranks symbolism.** The bucket is a zinc bucket. The bread is kunafa-bread. The man wears a tarboosh, not "a hat." Real names of things.

3. **Subtext, not declaration.** Ahmed doesn't say "I love you." Ahmed hands her the bread and holds it two seconds longer than required and then pulls his hand away.

4. **Address the player as "you" if at all — but only as witness voice, never as character.** "You watch her fold the cloth." Not "You ask her about the mare." She does not answer the player.

5. **Land each scene on a concrete image.** Not "she felt sad." The wax is warm. The door is ajar. The mare had been her father's.

6. **No therapy-speak.** No "she felt empowered." No "she processed her grief." Describe the action; the feeling is in the action.

7. **No didactic politics.** The scene does not explain law_homesteading. The scene shows Umm Mariam across the wall, not holding paper.

8. **Short lines.** Characters speak like people, not like they're giving testimony. "Sold." "We will eat bread tonight." Not "The mare has unfortunately been sold, and I regret..."

9. **The Qur'an and folk idiom appear as texture, not as costume.** When she says "min fadlak" it is because the Bey is there. When she does not say it, that is the story.

10. **Every scene changes her by a little.** Even a neutral-seeming exchange shifts `cp_layla_recent_joy` or `recent_hardship` or `exhaustion`. The button is her growing. Not her rehearsing.

---

## 9. Build order

### Phase 1 — Kill and template (this session or next)

1. Write this plan. ✅ (you are here)
2. Create `mod/events/cp_layla_vox_events.txt` with the dispatcher + Ahmed's 6 scenarios + their branches. ~30 events.
3. Create `mod/localization/english/cp_layla_vox_l_english.yml` — Ahmed's ~100 loc keys.
4. Add `cp_layla_roll_interlocutor` scripted effect to `cp_layla_memory.txt`.
5. Rewire the conversation button to call `cp_layla_roll_interlocutor`.
6. Generate / reuse Ahmed's 4–5 scenario images.
7. Leave the old `cp_conversation.*` system in place but unreachable (button no longer routes to it).
8. **Playtest Ahmed.** Click the button 30 times in a playthrough. Does it feel right? Are the branches meaningful? Does the prose land?

If Ahmed works, the template is validated. If Ahmed doesn't work, we iterate on his tree alone before touching anyone else — changing the pattern is much cheaper with one interlocutor built.

### Phase 2 — Scale interlocutors, one per session

Each session: one interlocutor. ~20–30 events. ~200–300 loc keys. ~3–5 images.

Suggested order (easiest → hardest):

1. Ahmed (done in Phase 1)
2. Herself / God (linear, simplest)
3. Her mother (memory-only, no era-gating)
4. The stranger (single-exchange, no branching)
5. Um Yusuf (rural, no era-gating)
6. Umm Mariam (rural, uses owner/landless contrast)
7. Her daughter (moderate — gates on `cp_layla_children`, daughter's age)
8. The Bey (medium — era-gated, class-heavy)
9. The factory owner (harder — urban-only, wage politics)
10. The ruler (hardest — era-aware, branches on era, most scenarios)

### Phase 3 — Delete the old system

Once all 10 interlocutors are in:

1. Delete `mod/events/cp_layla_conversation_events.txt`.
2. Delete the loc for `cp_conversation.*` keys.
3. Audit `cp_layla_conversation_*.dds` images — retire unused, rename reused to `cp_layla_vox_*.dds`.
4. Update `documentation/characters/layla/` docs to reflect the new system.
5. Tag `v0.4.0`.

### Phase 4 — Iterate (the real work)

Content quality. Play through with each interlocutor. Identify scenarios that feel flat, rewrite. Add new scenarios organically as gaps emerge ("I never see her daughter past age 15 — write a scene"). Add optional late-additions (journalist, grown son, midwife, soldier, French agent).

---

## 10. Migration from `cp_conversation.*`

The old system is ~67 events. Not all dies.

**What survives (ported to new system):**
- The Land monologue opening ("My grandfather planted in this soil...") — this is the *strongest* single piece of prose in the old system. Port into the Ruler interlocutor's "homesteader meets Pasha" scenario.
- The Pasha's three response voices (dismissive / engaged / cruel) — port into the Ruler pool as state-gated branches.
- The "small thing" scenarios (she has nothing to say tonight) — port into the Stranger pool or the Herself-Alone pool.
- Specific beats: the closed door, the kneading, the return to the quern.

**What dies:**
- The palace frame itself. The long carpet. The invented ceiling.
- The topic menu.
- The requirement that she be eloquent on demand.
- The singular Pasha.

**During the build, each scenario event that ports something prose-carrying MUST cite the source** in a comment: `# Ported from cp_conversation.X`. This keeps lineage visible in git blame.

**Images:** existing `cp_layla_conversation_*.dds` are 17 files. Audit each:
- Reuseable in the new system → rename to `cp_layla_vox_<interlocutor>_<scene>.dds`
- Orphaned → delete
- New images needed → generate via Codex CLI following the existing prompt catalog

---

## 11. Debug + validation

### Debug events

Each interlocutor gets a cp_debug event that forces its scenario-picker to fire:

```
cp_debug.90 = {
    type = country_event
    hidden = yes
    orphan = yes
    immediate = { c:EGY ?= { trigger_event = { id = cp_layla_vox.10 popup = yes } } }
}
# Similarly .91, .92... for each interlocutor
```

These use `trigger_event popup = yes` but work from **button-thread context** (fired via scripted effect, not directly from console). Wait — console `event cp_debug.90` will still trigger the random-in-wrong-thread crash.

**Workaround:** add a *button* `cp_debug_conversation_button` to the JE that exposes these debug fires in the game thread. Visible only in debug builds or behind an always-`possible=no` guard that's toggled via a console flag.

Alternative: each debug fires a non-popup `cp_debug.X` that directly applies the scenario's outcomes (like cp_debug.5 now). Useful for testing state transitions but loses the prose test.

**Recommended:** do both. Hidden debug events for outcome-testing; JE debug button for prose-testing.

### QA checklist per scenario

Before marking a scenario done:
1. Localization renders in-game without raw keys.
2. Image loads (no pink placeholder).
3. Each choice branch fires the expected follow-up.
4. Weight variables shift by the intended amounts.
5. Seen-flag is set correctly.
6. The scenario doesn't crash when fired from a debug button.
7. All era-variants render correctly in their respective eras (test both 1836-Pasha and post-constitution-parliament).

### Regression testing

After each new interlocutor lands, playtest the button 15 times and confirm:
- Interlocutor distribution is reasonable (no single one dominating).
- State-gating works (factory owner doesn't fire when she's rural).
- Cooldown holds (no scenario fires twice within its seen-flag window).
- Each fire changes her by at least one weight.

---

## 12. Risks, tradeoffs, open questions

### Risks

**R1 — Scale overwhelms.** 220 events of Mahfouz-quality prose is 30–40 hours of focused writing. The temptation will be to mass-produce thinner content. We lose if we do. Preventative: one interlocutor per session, hard limit. No mass-writing sprints.

**R2 — The player doesn't notice the depth.** If the system has 10 interlocutors × 6 scenarios × state-variants × branching, and the player clicks 20 times across a 100-year playthrough, they see maybe 15 unique scene-paths out of thousands of possible. Most content is invisible per playthrough. Preventative: this is a feature, not a bug. The promise is that *every playthrough feels different*. Lean into it. Mention in release notes that one playthrough reveals ~5% of written content.

**R3 — State-gating bugs make whole interlocutors silent.** A typo in `has_variable = cp_layla_in_city` vs `cp_layla_in_cairo` can silently gate an entire pool out. Preventative: the debug button exposes all interlocutors regardless of gate for QA.

**R4 — Era-aware loc rots.** A line that references "the Pasha" hardcoded breaks in a 1910 game. Preventative: `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` and `[ROOT.GetCountry.GetRuler.GetFullName]` used everywhere in country events. No hardcoded ruler names.

**R5 — The Mahfouz register drifts under pressure.** After 150 events of similar-feeling scenes, the prose flattens into a monotone. Preventative: deliberately alternate tones. Some scenes humorous. Some warm. Some austere. Some cruel. Not every scene is sad.

**R6 — Scenarios feel same-y across interlocutors.** If Ahmed and the Bey both generate "she nods, he waits, they do not speak of the thing" scenes, the system feels like one big blur. Preventative: each interlocutor must have a *signature gesture vocabulary*. Ahmed clears his throat, touches the tobacco tin. The Bey adjusts his cuffs. Her mother's voice is a rhythm, not a body.

### Tradeoffs

**T1 — Random-picked interlocutor vs menu.** We picked random. Tradeoff: player can't seek Ahmed directly when he's the emotional draw. Accepted because the menu would have dominated the experience; scroll fatigue would set in. The random choice is the design's *promise* that the button is a window, not a remote.

**T2 — Player silent vs player-as-character.** We chose player-silent. Tradeoff: the player is observationally engaged but never diegetically present. They're reading, not conversing. Accepted because the alternative (player as Pasha / player as cousin / player as narrator-with-voice) collapses the reader distance that makes the prose work.

**T3 — Within-scene branching vs linear.** We chose branching. Tradeoff: 3× event count and loc count vs a linear scene. Accepted because replayability is the design driver; linear scenes are exhausted in one click each.

**T4 — Real-time era awareness vs frozen 1836 framing.** We chose dynamic. Tradeoff: complexity in every Ruler scene, plus testing across three or four eras. Accepted because a 1925 game with a 1836 Pasha fantasy is immersion-breaking.

### Open questions

**Q1 — Should scenes have option-level trigger gates?** If Layla's said the "I have come to ask you for a paper" line, should a *different* scenario open next time instead of the same one? We said yes via seen-flags. But should the gate be per-option too, within a scenario? (E.g. she can't pick the "persist" option if she's too exhausted.) Probably yes for some options. Decision: case-by-case during writing.

**Q2 — How many layers of branching deep?** Each scenario has 2–3 choice points. Do we allow a third choice in a follow-up? (Level 3 branching.) Probably yes for critical scenes (the ruler, the bey, Ahmed's final conversation). Level 3 for ~20% of scenarios; level 2 for most.

**Q3 — Do scenarios persist state beyond the scene?** We've said yes (seen-flags, weight shifts). But should they *also* set stronger flags that future scenes reference? "She once walked out of the Pasha's chamber" as a persistent flag the Ruler pool reads back? Yes — but maybe in v0.5, not v0.4. Would add another ~30% to content scope.

**Q4 — Can an interlocutor die?** Ahmed clearly can. The Bey can be replaced (Cairo sends a new one). Her mother is already dead — does that change the tone over time? Probably yes. Each interlocutor needs a "post-death" or "post-departure" mode. Out of scope for v0.4; handle in v0.5.

**Q5 — Is the button daily/weekly/seasonal from the player's point of view?** 90-day cooldown gives ~4 clicks per game-year. That's ~400 clicks per 100-year game. Too many. Consider raising cooldown to 180 days (2 clicks per game-year, ~200 clicks total). Decision: adjust during playtest.

---

## 13. What this plan is NOT

- It's **not** a story-map. Story-map is existing (`documentation/characters/layla/story-map.md`) and unchanged. This plan describes a *button system*, not the narrative arc of Layla's life.
- It's **not** a rewrite of ambient events. The ambient pool (`cp_roll_ambient_layla`) is unchanged and will keep firing small life beats between clicks.
- It's **not** a replacement of the Check-on-Layla button. Keep that. Two separate buttons with different promises:
  - **Check on Layla** → passive, a moment of her day. No choices. You read, you close.
  - **A word between** (conversation) → active, a scene with dialog. Choices steer the exchange. You participate.
- It's **not** v1.0 of the mod. This is the v0.4 centerpiece. The mod's v1.0 sets are the full 5-act story-map + every interlocutor at polish quality + Person 2 (the Bey) as his own registered character + 5 additional languages.

---

## 14. Starting point for the next session

When we begin implementing:

1. Read this plan first.
2. Create `mod/events/cp_layla_vox_events.txt` with header + the dispatcher (`cp_layla_vox.10`).
3. Write Ahmed's 6 scenarios as full V3 events. Prose first, engine wiring second.
4. Loc keys in `cp_layla_vox_l_english.yml` as we write.
5. Two images generated for Ahmed: one default ("at the door, bucket in hand") and one for "at war" scenarios. Other variants reuse.
6. Rewire button. Test. Tune. Write the next interlocutor.

The first playtestable increment is Ahmed. Target: end of one focused session.

---

*"She has an hour, perhaps. She has rehearsed this, kneading bread, a hundred times. Tonight she lets it happen."*
— the line that closed cp_conversation.1's root. We keep the spirit. We give the button to more voices.
