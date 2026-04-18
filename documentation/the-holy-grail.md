# The Holy Grail

## Common People -- Design Document & Modding Guide

*"History is not the story of heroes entirely. It is often the story of cruelty and injustice and shortsightedness. There are monsters, there is evil, there is betrayal. That's why people should read history -- so that they'll get angry enough to demand change."*

---

## Table of Contents

- [Part 1: Vision](#part-1-vision)
  - [What Victoria 3 Gets Right](#what-victoria-3-gets-right)
  - [What It Misses](#what-it-misses)
  - [The Common People Concept](#the-common-people-concept)
  - [Why Now: The National Cast](#why-now-the-national-cast)
  - [Design Principles](#design-principles)
- [Part 2: Victoria 3 for Modders](#part-2-victoria-3-for-modders)
  - [Pops: The Invisible Protagonists](#pops-the-invisible-protagonists)
  - [Laws: The Player's Lever](#laws-the-players-lever)
  - [Interest Groups and Political Movements](#interest-groups-and-political-movements)
  - [War and Its Human Cost](#war-and-its-human-cost)
  - [The National Cast System](#the-national-cast-system)
  - [What Characters Can and Cannot Do](#what-characters-can-and-cannot-do)
- [Part 3: Paradox Modding 101](#part-3-paradox-modding-101)
  - [File Structure](#file-structure)
  - [Paradox Script Syntax](#paradox-script-syntax)
  - [Scopes: The Most Important Concept](#scopes-the-most-important-concept)
  - [Events: The Core Building Block](#events-the-core-building-block)
  - [On Actions and Pulse Events](#on-actions-and-pulse-events)
  - [Journal Entries: Tracking Narratives](#journal-entries-tracking-narratives)
  - [Character Creation and Tracking](#character-creation-and-tracking)
  - [Variables and Flags](#variables-and-flags)
  - [Scripted Triggers and Effects](#scripted-triggers-and-effects)
  - [Localization](#localization)
  - [Images and Graphics](#images-and-graphics)
  - [Debug Mode and Development Tools](#debug-mode-and-development-tools)
- [Part 4: Mod Architecture](#part-4-mod-architecture)
  - [The Core Idea: A Living Cast](#the-core-idea-a-living-cast)
  - [Naming Conventions](#naming-conventions)
  - [Directory Structure](#directory-structure)
  - [The Character Pool and Activation System](#the-character-pool-and-activation-system)
  - [The Personality and Reaction System](#the-personality-and-reaction-system)
  - [The Trigger System](#the-trigger-system)
  - [Event Types](#event-types)
  - [Nation-Specific vs Generic Characters](#nation-specific-vs-generic-characters)
- [Part 5: Characters](#part-5-characters) -- (content lives in [`characters/`](characters/))
- [Part 6: Technical Implementation Plan](#part-6-technical-implementation-plan)
  - [Phase 0: Template Initialization](#phase-0-template-initialization)
  - [Phase 1: Proof of Concept](#phase-1-proof-of-concept)
  - [Phase 2: Journal Tracking](#phase-2-journal-tracking)
  - [Phase 3: Second Archetype](#phase-3-second-archetype)
  - [Phase 4: Generic Archetypes](#phase-4-generic-archetypes)
  - [Phase 5: Polish and Release](#phase-5-polish-and-release)
  - [Code Examples](#code-examples)
- [Part 7: What's Possible vs What's Hard](#part-7-whats-possible-vs-whats-hard)
  - [What Works Well](#what-works-well)
  - [What Needs Workarounds](#what-needs-workarounds)
  - [What Is Hard or Impossible](#what-is-hard-or-impossible)
  - [Performance Considerations](#performance-considerations)
- [Appendices](#appendices)
  - [A: Paradox Script Cheat Sheet](#a-paradox-script-cheat-sheet)
  - [B: Relevant V3 Law Types](#b-relevant-v3-law-types)
  - [C: Vanilla Event Image Paths](#c-vanilla-event-image-paths)
  - [D: Common Errors and Fixes](#d-common-errors-and-fixes)
  - [E: Resources and Links](#e-resources-and-links)

---

# Part 1: Vision

## What Victoria 3 Gets Right

Victoria 3 is arguably the most ambitious economic and political simulation ever made. It models the entire world from 1836 to 1936 -- a century of revolutions, industrialization, colonial empires, and world wars. Every nation has populations divided into "pops" that work, consume goods, pay taxes, join political movements, and fight wars. The game simulates supply chains, labor markets, literacy rates, standards of living, and political radicalism across thousands of interconnected systems.

When you, the player, decide to abolish serfdom in Russia, the game calculates the impact on millions of pops: their new freedom to migrate, their changing employment prospects, the shifting political power of landowners versus reformers, the economic disruption of an entire labor system being dismantled. It is a remarkable achievement.

## What It Misses

But here is what happens when you abolish serfdom in Victoria 3: a number changes. A law icon updates. A tooltip tells you that your GDP per capita shifted by some percentage. You see graphs move. You might notice that your Landowners interest group lost some clout.

What you never see is the freed serf.

You never meet the woman who worked land she did not own for twenty-two years and now holds a deed with her name on it. You never follow the young man who walks away from the fields into a factory in Cairo, only to find that freedom and exploitation can coexist. You never read a letter from the front, written by a conscripted farmer's son who had never left his village before the war.

Victoria 3 simulates populations. It does not tell their stories. This is the gap that "Common People" fills.

## The Common People Concept

Common People is a mod with a **growing pool of named characters** -- farmers, factory workers, soldiers, mothers, radicals, dreamers, cowards, poets -- each with a distinct personality, a set of things they care about, and things they don't.

Each playthrough, a random subset of these characters activates. The player does not choose them and does not know in advance who will appear. One game as Egypt, you might meet Layla -- a 22-year-old farmer in the Nile Delta who has never owned land and just wants peace. Next game, you get Fatima -- a teacher's daughter who devours French novels and has opinions about everything. Or Hassan, the dock worker who couldn't care less about politics but lights up when foreign ships arrive.

### You Are Not Governing a Country. You Are Governing People.

The core feeling this mod creates: **the player should imagine these common people as their own great-grandparents.** People just like them, living in this country, affected by every decision the ruler makes. The goal is empathy and connection -- not information, not flavor text, not a newspaper.

This works through three types of moments:

**1. You feel your people.** When you enact a policy, you don't just see numbers change. You see Layla's reaction. She's happy -- the land is hers now. Or she's worried -- the new taxes are eating her harvest. Your normal gameplay actions (laws, wars, economy) flow down to real people and you feel the impact. This is not a choice event. This is a mirror.

**2. You live their lives with them.** Common people have personal lives that are not about your governance at all. Layla argues with her landlord. Samier falls in love. A soldier misses his daughter's first steps. A child learns to read. These are life events -- the texture of ordinary existence in the era. They make you care about these people as people, not as policy outcomes.

**3. You make their life decisions.** Sometimes a common person faces a crossroads and you -- the player, the ruler, the god of this simulation -- decide for them. Layla doesn't know if she should leave the farm for a factory job in Cairo. The pay is better but people say city life is hard. You choose. And that choice CHANGES her. She moves pop types -- she was a farmer, now she's a laborer. Her home state changes. Her future events change. Her personality weights shift. She is a different person because of your choice, and she stays that different person for the rest of her life.

### Living Characters, Not Story Arcs

Common people don't have a "story arc" that ends. They have **lives**. They are born (or they appear when conditions are right), they live, they react, they face decisions, they change, they age, and eventually they die. When Layla dies -- of old age, of illness, in a famine, in a revolution -- her story is over. Maybe her daughter appears. Maybe not. The mod does not protect characters from death. They are mortal, like real people.

Characters change pop types when their life changes. Layla starts as a farmer. If she moves to Cairo, she becomes a laborer. Her events now reflect laborer conditions, not farmer conditions. If Samier gets educated and becomes a shopkeeper, his interests shift. Characters are not static archetypes -- they are living people who transform based on what happens to them and to their country.

### Complementing the Game

Victoria 3 simulates economics, politics, and war. It does not simulate the human experience of living through those things. Common People fills the gaps:

- The game has no events for what serfdom FEELS like. We add them.
- The game has no events for the daily life of a factory worker. We add them.
- The game doesn't show you what war does to the family left behind. We add it.
- The game doesn't model the specific historical experiences of nations like Egypt -- the corvee system, the cotton boom, the Suez Canal labor. We add nation-specific events that bring history alive through personal stories.

The result: **every playthrough tells different stories.** Different characters, different reactions, different lives. The player gets attached to whoever shows up. They start making policy decisions partly because they want to see how *their* people are living. They remember the characters across campaigns -- "Last time Samier died in a factory accident. This time I'm going to pass labor laws before it happens."

You are still playing a grand strategy game. But now you are governing people, not numbers.

## Why Now: The National Cast

This mod was not technically feasible until recently. Victoria 3's character system used to discard characters who lost their active role -- a general relieved of command, an interest group leader replaced -- they simply vanished from the game. You could not maintain persistent named characters who existed outside the political elite.

The **National Cast** system, introduced in version 1.8 (detailed in [Dev Diary #176](https://forum.paradoxplaza.com/forum/threads/victoria-3-dev-diary-176-martins-character-collection.1910270/)), changed this fundamentally. Characters now persist in a "character pool" even without active jobs. They wait, age, develop traits, and can be recalled or referenced. The system supports 8 distinct roles including Agitator (a character who supports political movements without holding office) -- a natural fit for common people who become politically active.

Combined with the existing event system, journal entries, and variable tracking, the National Cast gives us the tools to create persistent named characters whose stories span an entire campaign.

## Design Principles

1. **People, not numbers**: The player should feel they are governing human beings. Every policy decision should echo down to someone with a name and a face.

2. **Three types of moments**: (a) Mirror events -- your policies affect them, you feel it. (b) Life events -- their personal lives, independent of your governance, making you care about them. (c) Life decisions -- you choose their path at a crossroads, and it permanently changes who they are.

3. **Living characters, not story arcs**: Characters don't have a plot that ends. They live, change, age, and die. Layla can change pop types (farmer to laborer if she moves to Cairo). Her personality weights shift over time. She is not an archetype -- she is a person who transforms.

4. **Novelty every playthrough**: Large and ever-growing character pool, random subset active per game. The player never knows who will show up.

5. **Personality-driven reactions**: Characters don't react to everything. Each has weighted interests. Reactions are probabilistic. The mod has a mind of its own.

6. **Bound to pop types and home states**: Each character is tied to a real pop type and lives in a real state. Their events reflect actual simulation data. When they change, their binding changes too.

7. **Complement the game**: Fill gaps V3 doesn't cover -- the human experience of serfdom, factory life, war, migration, and nation-specific history (Egypt's corvee system, Russia's emancipation, etc.).

8. **Historical authenticity**: Characters and situations grounded in real conditions. Researched and faithfully represented.

9. **Minimal base-game conflict**: We add content; we override nothing. Compatible with other mods.

10. **Monthly life pulse**: A character's life rolls forward even when no political event happens. Most months are quiet; some bring a small moment -- a broken plow, a neighbor's funeral, a letter from a cousin. Big events layer on top of this quiet stream. The player should feel her life is *always going on*, not just when a law passes.

11. **Game-rule integrity**: Never break Victoria 3's internal rules. If `law_women_own_property` isn't enacted, no event shows Layla signing a deed. If the country hasn't researched literacy tech, no event has her reading a newspaper. Every event gates itself on the actual state of the world. Each such rule becomes a reusable scripted trigger: `cp_woman_can_own_property`, `cp_country_is_literate`, `cp_has_factories_in_state`, etc.

12. **Evolving characters**: Initial personality weights are a starting point, not a fingerprint. Ten years of hardship can shift her toward revolution. A loving family can blunt her politics. The player should feel she has *grown* -- not stayed the same since 1836. Weights drift both from big branch events and from the quiet accumulation of small ones.

13. **Opinions on the world**: Characters hold views of nations, events abroad, and policies they hear about. These opinions shift with exposure. A cousin emigrating to France raises Layla's opinion of France. A French warship shelling Alexandria drops it. Opinions are stored per character: `cp_opinion_fra`, `cp_opinion_gbr`, `cp_opinion_ott`. They affect which reactions fire and how.

14. **Mortal characters**: Characters die. Age rolls use V3 defaults (~60-75). Events roll era-appropriate deaths: war, cholera, childbirth, factory accidents, famine. When a character dies, a new one can inherit their context -- a daughter, a neighbor -- but they are a new person, not a reincarnation. The campaign has funerals.

15. **Novel-quality writing**: This is a novel threaded through a strategy game, not a text adventure. Every event is written like a paragraph in a book: specific details, sensory language, subtext. Avoid narration ("You see X happen") -- write what a witness would feel. Length per event is whatever the moment needs. Short beats for small moments, longer pieces for life decisions.

16. **Egypt-perfect first, then generalize**: We build one country all the way -- events, pop-type integrity, historical accuracy, dialect in translation, image art direction -- before attempting a second. A shallow global mod is worse than a deep Egyptian one. Egypt is the template; other countries inherit the pattern when ready.

17. **1.12 today, 1.13 ready**: Store everything we need on the character object itself (variables, flags). When 1.13 ships National Cast enhancements (April 28, 2026), our characters slot in cleanly and we drop the 1.12 workarounds. In 1.12, journal entries stand in for the National Cast tracker.

---

# Part 2: Victoria 3 for Modders

This section covers only the game systems you need to understand for building this mod. It is not a general game guide.

## Pops: The Invisible Protagonists

A "pop" in Victoria 3 is an aggregate -- a group of individuals who share the same culture, religion, profession, state of residence, and workplace. A single pop might represent anywhere from a handful to millions of people. Every combination of these five attributes in each state creates a distinct pop.

**Professions** (15 total, in 3 strata):
- **Lower strata** (lowest pay, no qualification requirements): Laborers, Farmers, Peasants, Machinists, Clerks, Servicemen, Slaves
- **Middle strata** (moderate pay, literacy-dependent): Academics, Bureaucrats, Clergymen, Engineers, Officers, Shopkeepers
- **Upper strata** (highest income): Aristocrats, Capitalists

**Standard of Living (SoL)** ranges from 1 to 99 and determines quality of life:
- 1-4: Starving (literal famine conditions)
- 5-9: Struggling (subsistence living)
- 10-14: Impoverished (basic needs barely met)
- 15-19: Middling (modest comfort)
- 20-29: Secure (comfortable living)
- 30+: Prosperous through Opulent

**Why SoL matters for us**: When SoL drops, pops become radical. When it rises, they become loyal. This is the emotional engine of our stories. Layla's life improves when her SoL rises; Samier becomes angry when his SoL stagnates while capitalists profit. We cannot directly tie a character to a pop's SoL (characters and pops are separate systems), but we can check state-level SoL for specific pop types and use it to drive narrative events.

**Radicalism and loyalty**: Individual pops (actually, individuals within pops) become radical when their standard of living falls, when they lose jobs due to production method changes, when their culture or religion is discriminated against, or when their interest group's political demands go unmet. Radical pops create Turmoil in states, reducing tax and building efficiency, and can fuel revolutionary movements. Loyalists provide stability and insulate against radicalism.

## Laws: The Player's Lever

Laws are the primary way the player shapes society, and they are **our primary event trigger**. When the player enacts a law, we check which stories to advance.

**Laws most relevant to Common People stories:**

| Law Group | Key Laws | Story Impact |
|-----------|----------|--------------|
| Land Reform | Serfdom, Tenant Farmers, Homesteading | Layla's entire arc |
| Labor Rights | No Workers' Rights through Workers' Protection | Samier's arc, child labor |
| Economic System | Traditionalism through Command Economy | Who benefits from growth |
| Rights of Women | No Women's Rights through Women's Suffrage | The Woman archetype |
| Slavery | Slave Trade through Abolition | The Slave archetype |
| Welfare | No Social Security through Old Age Pension | Safety net stories |
| Health System | No Health System through Public Health Insurance | Quality of life |
| Education System | No Schools through Public Schools | Literacy and opportunity |
| Conscription | No Conscription through Mass Conscription | Soldier archetype |

**How law enactment works**: A law is proposed, progresses toward passage (or failure) over time based on political support, and when it passes, the `on_law_enacted` on-action fires. This is where we hook in.

**Key interaction**: Serfdom prevents migration between states. Abolishing it opens mobility. Homesteading boosts farmer income and political power while reducing aristocrat influence. These mechanical changes correspond directly to narrative moments in our stories.

## Interest Groups and Political Movements

Interest Groups (IGs) are factions representing organized political interests: Landowners, Industrialists, Trade Unions, Rural Folk, Intelligentsia, Armed Forces, Devout, and Petit Bourgeoisie. Individual people within pops decide which IG to support based on their profession, wealth, and education.

**Why IGs matter for us**: When Samier becomes radicalized, he is narratively joining a political movement. In game terms, radical pops fuel Political Movements -- organized pushes for specific law changes. If radicalism gets high enough, revolutions can occur. Our stories can reflect this: Samier's personal anger mirrors the growing radicalism of factory workers across the nation.

## War and Its Human Cost

When a country goes to war, its military units (composed of conscripted and professional soldiers) fight battles that generate casualties. Not all casualties die -- some become **Dependents** of other pops, representing wounded veterans who cannot work. These dependents consume resources and reduce economic productivity.

Post-war periods often feature outsized Dependent-to-Workforce ratios, causing economic strain and potentially triggering further radicalism. War exhaustion also rises with casualties, reducing war support.

**For the Soldier archetype**: `on_war_declared` and `on_war_end` on-actions trigger the soldier's story. We can check casualty-related modifiers and devastation in states to flavor the narrative appropriately.

## The National Cast System

Introduced in V3 1.8 (Dev Diary #176), the National Cast is a character pool where all characters in your country reside, including those without active jobs.

**Character roles** (8 types):
1. **Ruler** -- Head of state
2. **Heir** -- Designated successor
3. **Leader** -- Interest Group leader
4. **General / Admiral** -- Military commanders
5. **Executive** -- Company leaders
6. **Politician** -- Political operatives
7. **Agitator** -- Activists supporting political movements
8. **Magnate** -- Wealthy landowners/businessmen

**Key attributes:**
- **Prominence**: Political entrenchment; determines leadership selection likelihood
- **Popularity**: Public favor (-100 to +100); affects different things depending on role
- **Traits**: Personality, skills, and conditions that modify behavior (e.g., Cruel, Ambitious, Innovative)
- **Interest Group affiliation**: Which faction the character supports

**For our mod**: The **Agitator** role is the most natural fit for common people who become politically active. An Agitator supports political movements aligned with their ideologies without holding formal office. Samier, if radicalized, can literally become an in-game Agitator character who affects your politics.

For characters who remain "ordinary" (Layla the farmer who just wants to live in peace), we create them as characters in the pool without assigning an active role. The National Cast system keeps them alive and trackable.

## What Characters Can and Cannot Do

This is the honest assessment. Understanding these boundaries is critical for designing stories that work.

**CAN do:**
- Create a named character with specific culture, religion, age, gender, and traits
- Display the character's portrait in events (generated from their culture/ethnicity data)
- Track the character across multiple events using saved scopes and variables
- Assign the character a role (Agitator, if they become politically active)
- Check if the character is alive, and trigger events on their death
- Give the character traits that change over time

**NEW IN UPDATE 1.13 (April 28, 2026) -- Game Changers:**
- **Custom character roles**: We can define a `common_person` role in `common/character_roles/`. Characters get a real role in the game system, with custom titles ("Farmer Layla", "Worker Samier"), auto-spawning to pool, and proper engine integration. Common People characters are a first-class game feature, not a hack.
- **`set_home_state` effect**: Characters officially have a home state that can be changed via script. Layla lives in Lower Egypt. When she migrates, we call `set_home_state` and she's in Cairo. No workaround needed.
- **`home_region` in character templates**: Can set home region directly when creating characters.
- **`is_noble` trigger**: Distinguish commoners from nobility in script.
- **`set_first_name` / `set_last_name` effects**: Can change character names dynamically.
- **Variable maps** (from EU5): Key-value pairings -- more powerful than variable lists for tracking complex personality data.

**CANNOT do:**
- Make a character literally be a farmer pop in the economic simulation (she won't appear in the pop browser)
- Generate character stories procedurally -- every event must be hand-written

**What we WILL do:**
- **Bind characters to pop types.** Layla is connected to the farmer pop type. Her story events trigger based on real farmer pop data in her state -- their Standard of Living, their radicalism, their employment. She is a narrative window into that pop group, not a disconnected fiction. When the player sees farmer SoL tick up after homesteading, Layla's next event confirms what that number *feels like* on the ground.
- **Bind characters to a home state.** Layla lives in a specific state (e.g., Lower Egypt), not "somewhere." Her checks target farmer pops in HER state. She notices migration into her state -- if Italian immigrants arrive, she might react (positively or xenophobically depending on her personality). She can also travel: if her story branches into hardship, she migrates to Cairo, and her home state variable updates. Now her events check Cairo's pop data instead.
- Same for Samier: bound to laborers/machinists in a specific industrial state. His radicalization tracks real radical pop percentages in that state.
- Variables on the character or country track personal story state (e.g., `cp_layla_chapter`, `cp_layla_home_state`, `cp_samier_radical_level`) alongside the real pop data.

---

# Part 3: Paradox Modding 101

This section teaches you how to actually build things in Victoria 3's modding system. If you have software development experience but have never modded a Paradox game, start here.

## File Structure

Victoria 3 mods mirror the base game's directory structure. Anything you place in your mod folder that matches a base game path will be loaded alongside (or instead of) the vanilla content.

```
mod/
  .metadata/
    metadata.json            # Mod identity (name, version, tags)
    thumbnail.png            # Launcher icon
  common/
    on_actions/              # Hooks into game events
    journal_entries/         # Persistent narrative trackers
    character_templates/     # Pre-defined character definitions
    scripted_triggers/       # Reusable condition checks
    scripted_effects/        # Reusable effect blocks
    decisions/               # Player-initiated actions
  events/                    # Event scripts (the heart of this mod)
  localization/
    english/                 # English text (UTF-8 BOM!)
      replace/               # Overrides for base game text
  gfx/
    event_pictures/          # Event images (DDS format)
  gui/                       # UI layout files (advanced)
```

**Key rule**: Files in `common/` subdirectories and `events/` are loaded automatically. You do not need to register them anywhere -- the game reads all `.txt` files in the correct directories.

## Paradox Script Syntax

This is not JSON, YAML, or any standard format. It is Paradox's own declarative scripting language, sometimes called "Clausewitz script" (after the engine).

```
# This is a comment

# Assignment uses = (no colons, no semicolons)
my_key = my_value

# Blocks use { }
my_block = {
    key_1 = value_1
    key_2 = value_2
    
    # Nested blocks
    inner_block = {
        nested_key = nested_value
    }
}

# Booleans are yes/no (not true/false)
is_active = yes
hidden = no

# Numbers are bare (no quotes)
weight = 100
threshold = 0.5

# Strings use quotes when they contain spaces
name = "John Smith"

# References to game objects use specific prefixes
# c: for countries, s: for states, cu: for cultures, etc.
country = c:EGY
culture = cu:misri
```

**Indentation**: Tabs are conventional but not enforced. Use tabs to match Paradox's own style.

**File encoding**: Event files and most script files use UTF-8. Localization files MUST use UTF-8 with BOM (byte order mark). This is the single most common source of bugs for new modders.

## Scopes: The Most Important Concept

A scope is the "current context" in which triggers and effects execute. Think of it like `this` in object-oriented programming -- it tells the engine what object you are operating on.

```
# This event fires in COUNTRY scope (root = the country)
my_events.1 = {
    type = country_event
    
    trigger = {
        # These triggers check the COUNTRY (root scope)
        has_law = law_type:law_serfdom
        gdp > 50000
    }
    
    option = {
        # This effect changes the COUNTRY
        set_variable = { name = my_var value = 1 }
        
        # Scope change: now we are inside a specific state
        random_scope_state = {
            limit = { state_region = s:STATE_LOWER_EGYPT }
            # Effects here operate on the STATE, not the country
            add_modifier = { name = my_modifier months = 12 }
        }
    }
}
```

**Common scope keywords:**
- `root` -- The base scope of the current event/effect (usually the country)
- `prev` -- The scope before the most recent scope change
- `scope:name` -- A named scope saved earlier with `save_scope_as`
- `c:TAG` -- A specific country (e.g., `c:EGY` for Egypt)
- `s:REGION` -- A specific state region

**Scope iterators** (loop over matching objects):
- `every_scope_state = { }` -- Every state in the current country
- `random_scope_state = { limit = { ... } }` -- A random state matching conditions
- `any_scope_character = { }` -- Any character in the current scope
- `ordered_interest_group = { }` -- Interest groups sorted by some criteria

**Saving scopes for later use:**
```
immediate = {
    random_scope_character = {
        limit = { has_variable = cp_is_layla }
        save_scope_as = layla
    }
}

option = {
    # Now we can reference her anywhere in this event
    scope:layla = {
        add_trait = ambitious
    }
}
```

## Events: The Core Building Block

Events are popup windows that show text, images, and present the player with choices. They are the primary way this mod delivers its narratives.

**Event types:**
- `country_event` -- Fires in country scope. The most common type. Shows the country's leader by default.
- `character_event` -- Fires in character scope. Centers on a specific character.
- `state_event` -- Fires in state scope. Relates to a specific territory.

**Anatomy of an event:**

```
namespace = cp_layla           # Groups events. ID = namespace.number

cp_layla.001 = {
    type = country_event
    
    # Visual presentation
    title = cp_layla.001.t     # Localization key for title
    desc = cp_layla.001.d      # Localization key for description
    flavor = cp_layla.001.f    # Optional italic flavor text
    
    event_image = {
        video = "gfx/event_pictures/africa_leader_speaking.bk2"
    }
    
    # left_icon shows a character portrait on the event window
    left_icon = scope:layla
    
    # GUI window type (determines layout)
    gui_window = event_window_1char_tabloid
    
    # When can this event fire?
    trigger = {
        country_tag = EGY
        has_variable = cp_layla_chapter
        var:cp_layla_chapter = 1
    }
    
    # Effects that run immediately when the event fires
    # (before the player sees anything)
    immediate = {
        random_scope_character = {
            limit = { has_variable = cp_is_layla }
            save_scope_as = layla
        }
    }
    
    # Player choices (at least one required for non-hidden events)
    option = {
        name = cp_layla.001.a              # "Her life will improve"
        default_option = yes               # Pre-selected option
        
        # Effects when this option is chosen
        change_variable = {
            name = cp_layla_chapter
            add = 1
        }
    }
    
    option = {
        name = cp_layla.001.b              # "Change is painful"
        
        set_variable = {
            name = cp_layla_pessimist_path
            value = yes
        }
        change_variable = {
            name = cp_layla_chapter
            add = 1
        }
    }
}
```

**Hidden events** (no UI, used for background logic):
```
cp_router.001 = {
    type = country_event
    hidden = yes             # Player never sees this
    
    trigger = { ... }
    
    immediate = {
        # Do logic here: spawn characters, set variables, fire visible events
        trigger_event = { id = cp_layla.001 }
    }
}
```

**Critical rule**: Events never trigger on their own. They must always be fired by something else: an on_action, another event's effect, a journal entry, or a decision.

## On Actions and Pulse Events

On actions are hooks into game events. When something happens in the game (a law passes, a war starts, a month ticks), the engine runs the on_action for that event, which can fire your events.

```
# mod/common/on_actions/cp_on_actions.txt

# Hook into law enactment (fires for every country when they enact any law)
on_law_enacted = {
    on_actions = {
        cp_on_law_enacted
    }
}

# Our custom on_action that dispatches to story events
cp_on_law_enacted = {
    effect = {
        # Check if Layla's story should advance
        if = {
            limit = {
                country_tag = EGY
                has_variable = cp_layla_spawned
                NOT = { has_variable = cp_layla_complete }
            }
            trigger_event = { id = cp_layla_check.001 }
        }
    }
}
```

**Key on_actions for this mod:**

| On Action | When It Fires | Use For |
|-----------|---------------|---------|
| `on_game_started` | Game begins | Initialize mod, set global variables |
| `on_law_enacted` | Any law passes | Primary story trigger |
| `on_monthly_pulse_country` | Every month per country | Periodic story advancement checks |
| `on_yearly_pulse_country` | Every year per country | Slower story progression |
| `on_war_declared` | War begins | Soldier archetype start |
| `on_war_end` | War concludes | Soldier aftermath events |
| `on_character_death` | Character dies | Handle character death in stories |
| `on_revolution_start` | Revolution begins | Radicalization climax events |

**Weighted random events** (used in pulse on_actions):
```
on_yearly_pulse_country = {
    random_events = {
        100 = 0                    # 100/(100+5+5) = ~91% chance nothing happens
        5 = cp_layla_check.002     # ~4.5% chance
        5 = cp_samier_check.002    # ~4.5% chance
    }
}
```

The numbers are weights, not percentages. The probability of each event is its weight divided by the total of all weights (including the 0 entry, which means "nothing happens").

## Journal Entries: Tracking Narratives

Journal entries are persistent UI elements that appear in the player's journal panel. They track ongoing objectives with progress bars and status text. For our mod, each character's storyline gets a journal entry so the player can see where the story stands.

```
# mod/common/journal_entries/cp_journal_entries.txt

je_cp_layla_story = {
    icon = "gfx/interface/icons/event_icons/event_portrait.dds"
    
    # When should this journal entry be visible?
    is_shown_when_inactive = {
        country_tag = EGY
        has_variable = cp_layla_spawned
    }
    
    # When is it actively tracking?
    possible = {
        has_variable = cp_layla_spawned
        NOT = { has_variable = cp_layla_complete }
    }
    
    # What completes it?
    complete = {
        has_variable = cp_layla_complete
    }
    
    on_complete = {
        # Effects when the story finishes
    }
    
    # Dynamic status text that changes with the story
    status_desc = {
        first_valid = {
            triggered_desc = {
                trigger = { var:cp_layla_chapter = 1 }
                desc = je_cp_layla_ch1_desc
            }
            triggered_desc = {
                trigger = { var:cp_layla_chapter = 2 }
                desc = je_cp_layla_ch2_desc
            }
            triggered_desc = {
                trigger = { var:cp_layla_chapter >= 3 }
                desc = je_cp_layla_ch3_desc
            }
        }
    }
    
    # Progress bar
    progressbar = yes
    current_value = {
        value = var:cp_layla_chapter
    }
    goal_add_value = {
        value = 7
    }
    
    weight = 100
}
```

The player sees a journal entry like "Layla's Journey" with a progress bar showing chapter 3/7 and a description that updates as the story advances. This gives the player visibility into ongoing storylines and makes the mod feel integrated with the base game's UI.

## Character Creation and Tracking

The `create_character` effect spawns a new character. Combined with `save_scope_as`, we can reference them across events.

```
# Create Layla
create_character = {
    first_name = "Layla"
    culture = cu:misri          # Egyptian culture
    religion = rel:sunni        # Sunni Muslim
    female = yes
    age = 22
    traits = { persistent }
    save_scope_as = cp_layla
}

# Mark her on the character for later identification
scope:cp_layla = {
    set_variable = {
        name = cp_is_layla
        value = yes
    }
}
```

**Finding a character later** (in a subsequent event):
```
immediate = {
    random_scope_character = {
        limit = { has_variable = cp_is_layla }
        save_scope_as = layla
    }
}
```

**Checking if alive:**
```
trigger = {
    any_scope_character = {
        has_variable = cp_is_layla
        is_alive = yes
    }
}
```

**Giving a character a role** (e.g., Samier becomes an Agitator):
```
scope:samier = {
    set_character_as_agitator = yes
}
```

**Character traits** modify behavior and can be added/removed:
```
scope:layla = {
    add_trait = ambitious       # Layla gains ambition after land reform
    remove_trait = persistent   # Her stubbornness fades
}
```

## Variables and Flags

Variables store numeric or boolean state. They are scoped to the object they are set on (country, character, state, or global).

**Setting variables:**
```
# On the country (accessible in country scope)
set_variable = { name = cp_layla_chapter value = 1 }

# Incrementing
change_variable = { name = cp_layla_chapter add = 1 }

# On a character
scope:layla = {
    set_variable = { name = cp_personal_sol value = 12 }
}

# Global (accessible from anywhere)
set_global_variable = { name = cp_is_loaded value = yes }
```

**Checking variables:**
```
trigger = {
    has_variable = cp_layla_chapter           # Variable exists
    var:cp_layla_chapter >= 3                 # Value check
    NOT = { has_variable = cp_layla_complete } # Variable does NOT exist
}
```

**Country flags** (simpler boolean markers):
```
# Set a flag
set_country_flag = cp_layla_chose_optimism

# Check a flag
has_country_flag = cp_layla_chose_optimism
```

**Use variables for**: chapter tracking, branching state, numeric conditions.
**Use flags for**: simple yes/no story branching ("did the player choose option A?").

## Scripted Triggers and Effects

Scripted triggers and effects are reusable code blocks -- the Paradox equivalent of functions. They keep your code DRY (Don't Repeat Yourself).

**Scripted trigger** (reusable condition):
```
# mod/common/scripted_triggers/cp_triggers.txt

cp_is_egypt_with_serfdom = {
    country_tag = EGY
    has_law = law_type:law_serfdom
}

cp_layla_story_active = {
    has_variable = cp_layla_spawned
    NOT = { has_variable = cp_layla_complete }
    any_scope_character = {
        has_variable = cp_is_layla
        is_alive = yes
    }
}
```

**Usage:**
```
trigger = {
    cp_layla_story_active = yes
}
```

**Scripted effect** (reusable action):
```
# mod/common/scripted_effects/cp_effects.txt

cp_spawn_layla = {
    create_character = {
        first_name = "Layla"
        culture = cu:misri
        religion = rel:sunni
        female = yes
        age = 22
        traits = { persistent }
        save_scope_as = cp_layla
    }
    scope:cp_layla = {
        set_variable = { name = cp_is_layla value = yes }
    }
    set_variable = { name = cp_layla_spawned value = yes }
    set_variable = { name = cp_layla_chapter value = 0 }
}
```

**Usage:**
```
immediate = {
    cp_spawn_layla = yes
}
```

## Localization

Localization files contain all player-visible text. They are YAML-like but with important quirks.

**Critical**: Localization files MUST be saved as **UTF-8 with BOM** (byte order mark: the invisible bytes `EF BB BF` at the start of the file). Without BOM, the game silently ignores the entire file. This is the #1 modding mistake. Most code editors can be configured to save with BOM -- in VS Code, look at the bottom-right encoding indicator and select "UTF-8 with BOM".

**File naming**: Files must end with `_l_<language>.yml` (e.g., `cp_layla_l_english.yml`).

**Format:**
```yaml
l_english:
 cp_layla.001.t:0 "The Farmer's Daughter"
 cp_layla.001.d:0 "In a small village along the Nile Delta, a young woman named Layla rises before dawn, as she has every day of her twenty-two years. The land she works is not hers -- it belongs to the local bey, as it belonged to his father, as it has always belonged to someone else.\n\nBut today, word has come from Cairo. The laws are changing."
 cp_layla.001.f:0 "The earth does not care who owns the deed. It yields to the one who tends it."
 cp_layla.001.a:0 "Her life will change for the better."
 cp_layla.001.b:0 "Change brings its own hardships."
 je_cp_layla_ch1_desc:0 "Layla's story has just begun."
```

**Key conventions:**
- First line is always `l_english:` (or `l_french:`, etc.)
- Keys use the pattern `namespace.eventid.element:version "text"`
- The `:0` is a version number (always use 0 for mod content)
- `\n` creates a newline in displayed text
- `#bold text#!` for bold, `#italic text#!` for italics
- `[scope.GetName]` inserts a dynamic value (e.g., `[ROOT.GetName]` for country name)
- `$other_key$` references another localization key inline

## Images and Graphics

Event images appear at the top of event popups. Victoria 3 uses two formats:

- **BK2** (Bink Video): Animated, used by base game. Requires special tools to create. Skip for initial development.
- **DDS** (DirectDraw Surface): Static images. Can be created with GIMP (export as DDS with DXT5 compression) or ImageMagick.

**For initial development**: Reuse base game event images. They are referenced by path:
```
event_image = {
    video = "gfx/event_pictures/africa_leader_speaking.bk2"
}
```

See [Appendix C](#c-vanilla-event-image-paths) for a list of reusable vanilla paths.

**Custom images** (when ready): Place DDS files in `mod/gfx/event_pictures/` and reference them the same way. Typical dimensions are approximately 620x400 pixels, but check base game files for exact sizes.

## Debug Mode and Development Tools

**Launching in debug mode**: Add `-debug_mode` to your Victoria 3 launch options in Steam (right-click game > Properties > Launch Options).

Debug mode enables:
- The console (press `~` to open)
- Detailed error logging
- Hot reloading of script files

**Essential console commands:**

| Command | What It Does |
|---------|-------------|
| `event cp_layla.001` | Fire a specific event immediately |
| `yesmen` | All law proposals pass instantly (speeds up testing) |
| `observe` | Detach from a country to watch the simulation |
| `reload events` | Reload all event files without restarting |
| `tag EGY` | Switch to playing as Egypt |

**Error log**: Located at `Documents/Paradox Interactive/Victoria 3/logs/error.log`. Check this after every game launch. Common errors include missing localization keys, invalid scope references, and syntax errors in script files.

**Script documentation export**: Run `script_docs` in the console to export comprehensive documentation of all available triggers, effects, modifiers, and scopes to `Documents/Paradox Interactive/Victoria 3/docs/`. This is the definitive reference for what you can do in scripting.

---

# Part 4: Mod Architecture

## The Core Idea: A Living Cast

The mod maintains a **pool of character definitions** that grows with every release. At game start (and periodically throughout the game), the mod randomly selects a subset of characters to activate for this playthrough. Each active character:

- Is bound to a **pop type** (farmer, laborer, machinist, etc.)
- Has a **personality** -- a set of weighted interests that determine what they react to
- Has a **main story arc** -- a multi-chapter chain tied to their primary concern (land reform for a farmer, labor conditions for a worker)
- Has **reaction potential** -- probabilistic responses to game events outside their main arc

The player never sees the pool. They only see the characters who show up. Different game, different people, different stories.

## Naming Conventions

Everything uses the `cp_` prefix (Common People):

| Element | Convention | Example |
|---------|-----------|---------|
| Files | `cp_<system>.txt` | `cp_on_actions.txt` |
| Event namespaces | `cp_<character>` or `cp_react_<system>` | `cp_layla`, `cp_react_law` |
| Variables | `cp_<character>_<property>` | `cp_layla_chapter` |
| Personality flags | `cp_<char>_cares_<topic>` | `cp_layla_cares_france` |
| Localization keys | `cp_<namespace>.<id>.<element>` | `cp_layla.001.t` |
| Journal entries | `je_cp_<name>` | `je_cp_layla_story` |

## Directory Structure

```
mod/
  common/
    on_actions/
      cp_on_actions.txt              # Master on-action hooks (all game systems)
    journal_entries/
      cp_journal_entries.txt         # Story tracking journals
    scripted_triggers/
      cp_triggers.txt                # Reusable conditions
      cp_personality_triggers.txt    # "Does this character care about X?"
    scripted_effects/
      cp_effects.txt                 # Character spawning, personality assignment
      cp_reaction_effects.txt        # Shared reaction-firing logic
    character_templates/
      cp_characters.txt              # Character definitions (grows over time)
  events/
    cp_init_events.txt               # Mod initialization + character pool activation
    cp_router_events.txt             # Hidden dispatch events (per game system)
    cp_layla_events.txt              # Layla's main arc + personal reactions
    cp_samier_events.txt             # Samier's main arc + personal reactions
    cp_react_law_events.txt          # Shared reaction events: law enacted/failed
    cp_react_war_events.txt          # Shared reaction events: war
    cp_react_diplomacy_events.txt    # Shared reaction events: diplomacy
    cp_react_economy_events.txt      # Shared reaction events: economic shifts
    cp_react_politics_events.txt     # Shared reaction events: IG changes, revolutions
    ... (one per character with a deep arc, plus shared reaction files)
  localization/
    english/
      cp_layla_l_english.yml
      cp_samier_l_english.yml
      cp_reactions_l_english.yml     # Shared reaction event text
      cp_ui_l_english.yml            # Journal entries, shared UI
  gfx/
    event_pictures/
      cp_farming.dds
      cp_factory.dds
      cp_warfront.dds
```

## The Character Pool and Activation System

### Character Definitions

Each character is defined as a data block with:

```
# Personality data (stored as variables on the character after spawning)
cp_layla:
  name: Layla
  culture: misri
  religion: sunni
  female: yes
  age: 22
  pop_type: farmer            # Bound to farmer pop data
  traits: [persistent]
  nation: EGY                 # Nation-specific (or "any" for generic)
  
  # Personality: what does she care about? (weights 0-10)
  interest_land_reform: 10    # Core concern
  interest_labor: 2           # Vaguely aware
  interest_war: 7             # Fears war (husband could be conscripted)
  interest_diplomacy: 1       # Doesn't care
  interest_france: 4          # Cousin works at the port
  interest_education: 3       # Wants children to read
  interest_womens_rights: 5   # Affects her directly but she doesn't organize
  interest_religion: 6        # Traditional, cares about religious laws
  interest_revolution: 8      # Terrified of instability
  interest_economy: 5         # Feels economic shifts through harvests
```

In practice, these personality weights are stored as variables on the character after spawning:
```
scope:cp_layla = {
    set_variable = { name = cp_interest_land_reform value = 10 }
    set_variable = { name = cp_interest_war value = 7 }
    set_variable = { name = cp_interest_france value = 4 }
    # ... etc
}
```

### Activation at Game Start

At game start, the mod:
1. Checks which characters are eligible for this country (nation-specific + generic pool)
2. Randomly selects 3-5 characters to activate immediately
3. Sets up a yearly pulse to potentially activate 1-2 more as the game progresses (new people enter your awareness as society changes)

```
# Hidden initialization event
cp_init.001 = {
    type = country_event
    hidden = yes
    
    immediate = {
        # Activate random characters from the eligible pool
        # Using weighted random: characters whose conditions are met
        # get a chance to spawn
        
        random_list = {
            10 = { # 10% weight for each eligible character
                trigger = { country_tag = EGY }
                cp_spawn_layla = yes
            }
            10 = {
                trigger = { country_tag = EGY }
                cp_spawn_samier = yes
            }
            10 = {
                trigger = {
                    any_scope_state = {
                        has_building = building_textile_mills
                    }
                }
                cp_spawn_fatima = yes
            }
            # ... etc for all characters in the pool
        }
    }
}
```

The player starts the game and within the first year, 3-5 characters introduce themselves through events. The player doesn't know who they'll get.

### Activation Over Time

New characters can activate mid-game when conditions change:
- Industrialization begins -> factory worker characters become eligible
- War declared -> soldier characters activate
- Women's rights law passed -> women's stories unlock
- Immigration wave -> immigrant characters appear

This means the cast evolves with the game state. Early game might be farmers and traditional characters. Late game adds factory workers, soldiers, political activists.

## The Personality and Reaction System

### How Reactions Work

When a game event fires (law enacted, war declared, etc.), the router:

1. Iterates over all active characters
2. For each character, checks their interest weight for this event type
3. Rolls against the weight to decide if they react
4. If they react, fires a reaction event flavored by their personality

```
# Pseudocode for the reaction system
on_law_enacted:
  for each active character:
    interest = character's interest weight for this law category
    roll = random 1-10
    if roll <= interest:
      fire reaction event for this character about this law
    else:
      character doesn't care this time -- silence
```

In Paradox script, this looks like:
```
# Router: check if Layla reacts to a law change
cp_router_law.001 = {
    type = country_event
    hidden = yes
    
    immediate = {
        # Check each active character
        every_scope_character = {
            limit = { has_variable = cp_is_common_person }
            save_scope_as = cp_current_char
            
            # Roll against their interest weight
            random = {
                chance = {
                    value = 0
                    add = scope:cp_current_char.var:cp_interest_land_reform
                    multiply = 10   # Convert 0-10 weight to 0-100% chance
                }
                # They care! Fire their reaction
                root = {
                    trigger_event = { id = cp_react_law.001 }
                }
            }
        }
    }
}
```

### Reaction Events: Templated, Not Unique

The key architectural insight: **reaction events are templates**, not unique per character. A "reaction to law failure" event adapts based on which character is reacting:

```
cp_react_law.001 = {
    type = country_event
    
    title = cp_react_law.001.t
    
    # Description changes based on who is reacting
    desc = {
        first_valid = {
            triggered_desc = {
                trigger = {
                    scope:cp_current_char = { has_variable = cp_is_layla }
                }
                desc = cp_react_law.001.d_layla  # Layla's personal reaction
            }
            triggered_desc = {
                trigger = {
                    scope:cp_current_char = { has_variable = cp_is_samier }
                }
                desc = cp_react_law.001.d_samier  # Samier's personal reaction
            }
            triggered_desc = {
                desc = cp_react_law.001.d_generic  # Fallback for characters
                                                    # without a unique reaction
            }
        }
    }
    
    left_icon = scope:cp_current_char
    ...
}
```

This means:
The architecture scales linearly:
- **Each character** requires 1 spawn effect + personality data
- **Deep story arcs** (6-8 chapter chains) are written for "main" characters -- not all of them
- **Reaction events** are shared templates with per-character localization variants where it matters, and generic fallback text where it doesn't
- A character can have a unique reaction to something they deeply care about, and a generic "I noticed" reaction to things they vaguely register

Adding a new character means: one spawn effect, personality weights, optionally a deep arc, and localization entries for their unique reactions. Nothing else in the mod needs to change. The pool can grow indefinitely -- 50 in v1, hundreds over time.

## The Trigger System

The mod hooks into every major game system:

```
Game Event
  -> on_action hook (cp_on_actions.txt)
    -> System-specific router (cp_router_events.txt)
      -> For each active character:
        -> Roll against personality weight
          -> If hit: fire reaction event (templated, flavored by character)
      -> For main arc characters:
        -> Check chapter + conditions -> advance story
```

**All hooked on-actions:**

| On Action | What It Catches | Character Interest Variable |
|-----------|----------------|---------------------------|
| `on_law_enacted` | Law passes | `cp_interest_<law_category>` |
| `on_law_enactment_failed` | Law fails | Same as above |
| `on_law_enactment_started` | Law proposed | Same as above |
| `on_war_declared` | War starts | `cp_interest_war` |
| `on_war_end` | War ends | `cp_interest_war` |
| `on_battle_won` / `on_battle_lost` | Battle result | `cp_interest_war` |
| `on_revolution_start` | Revolution | `cp_interest_revolution` |
| `on_new_ruler` | New leader | `cp_interest_politics` |
| `on_government_reformed` | Government changes | `cp_interest_politics` |
| `on_character_death` | Someone dies | Handle death of story characters |
| `on_yearly_pulse_country` | Annual check | Life events, harvest reactions, aging |
| `on_monthly_pulse_state` | Monthly per state | State condition checks |
| `on_yearly_pulse_character` | Annual per character | Personal life events |
| Diplomatic actions | Treaties, relations | `cp_interest_diplomacy`, `cp_interest_<country>` |
| IG enters/leaves government | Political shift | `cp_interest_politics` |
| Technology researched | New tech | `cp_interest_<tech_category>` |

**State conditions checked on pulse events:**

In addition to on-actions, the mod checks **state-level conditions** in a character's home state during pulse events. These are not on-actions (the game doesn't fire a hook for "drought started") -- instead we check them periodically and react when they change.

| State Condition | What It Is | Trigger | Example Reaction |
|----------------|-----------|---------|-----------------|
| Harvest conditions (bad) | Drought, flood, frost, locust swarm, hailstorm, wildfire, heatwave, disease outbreak, earthquake, torrential rain, extreme wind | `any_harvest_condition = { }` on home state | "The rains didn't come. Layla watches the soil crack." |
| Harvest conditions (good) | Moderate rainfall, optimal sunlight, pollinator surge | `any_harvest_condition = { }` on home state | "The Nile was generous. Layla bought cloth for a new dress -- the first in three years." |
| Devastation | War damage in a state | `devastation >= X` on home state | "Soldiers came through. The eastern fields are ruined." |
| Pollution | Industrial pollution | `pollution >= X` on home state | "The river water tastes wrong since they built the factory." |
| Turmoil | Radical pops causing unrest | `turmoil >= X` on home state | "There was shouting in the market today." |
| Food security | Can pops afford food? | SoL thresholds for pop type | "Bread costs twice what it did last year." |
| Disease outbreak | Epidemic via harvest condition | `any_harvest_condition = { type = disease_outbreak }` | "Three families are sick. Layla keeps the children inside." |
| Infrastructure change | New railways, roads | `infrastructure >= X` or building checks | "They're building a rail line through the valley." |
| Urbanization | City growth | Pop count or building density | "Cairo grows every year. More people, more noise." |
| Pop type presence | New cultures, immigrants | `any_scope_pop = { culture = cu:X }` | "Strange people from the north arrived. They speak differently." |

These state conditions are the source of **life events** -- personal moments that happen to characters because of where they live, not because of what the player decided. A drought is not the player's fault. But the player's response to it (or lack of response) will shape the character's future.

## Event Types

### 1. Mirror Events
Your policy decisions reflected through the eyes of a character. You enacted homesteading -- Layla holds a deed for the first time. You ignored labor laws -- Samier's friend lost an arm. These fire from on-actions (law enacted, war declared, etc.) and their mechanical effects ripple back into the country (loyalists, radicals, modifiers).

### 2. Life Events
Personal moments independent of governance. Layla's harvest is good. Samier falls in love. A drought hits. A child is born. A character falls ill. These fire from pulse events checking state conditions (harvest, pollution, devastation, SoL) and from random yearly rolls. They make you care about characters as people, not as policy outcomes.

### 3. Life Decision Events
Crossroads moments where the player chooses a character's path. Layla doesn't know if she should move to Cairo for factory work -- better pay but hard life. The player decides. This PERMANENTLY changes the character: pop type switches (farmer -> laborer), home state changes, personality weights shift, future events change. These are the moments where the player feels they are shaping a human life, not just governing a country.

### 4. Reaction Events (Templated)
Shared event templates that adapt to whichever character is reacting, driven by personality weights. A law fails -- Layla's variant is disappointed, Samier's is furious, the fisherman doesn't notice. Per-character localization where it matters, generic fallback otherwise.

## Living Systems

These systems make a character feel alive between the big events. They are the background radiation of a life.

### The Monthly Life Pulse

A hidden per-character pulse event rolls **once per game month** with a **10% fire chance**. Most months silent; on average ~1.2 pulse events per year. When it fires, the event chosen is *contextual* -- weighted heavily by current state conditions (bad harvest, war, the character's age, etc.), not purely random.

The pulse is one of several event sources; the richer stream of events comes from world hooks (law changes, wars, tech, harvest conditions, IG movements, diplomatic shifts). The pulse fills the quiet months where the player isn't doing anything dramatic but life is still happening.

```
cp_layla_life_pulse (hidden, character_event, on monthly_pulse_country)
  trigger = { exists = scope:cp_layla }
  immediate = {
    scope:cp_layla = {
      random = {
        chance = 10                # 10% any given month something small happens
        random_list = {
          # Family-and-home beats
          10 = { fire_event = cp_layla_life.child_fever }
          10 = { fire_event = cp_layla_life.ahmed_comes_home_tired }
           8 = { trigger = { has_character_flag = married }
                 fire_event = cp_layla_life.new_pregnancy }
          # Harvest beats
          15 = { trigger = { scope:cp_layla.var:cp_home_state = {
                               any_harvest_condition = { type = drought } } }
                 fire_event = cp_layla_life.dry_earth }
          # Faith beats
           5 = { fire_event = cp_layla_life.fajr_in_the_dark }
          # Community beats
           8 = { fire_event = cp_layla_life.neighbor_funeral }
          # ...etc
        }
      }
    }
  }
```

Life pulse events are **short**. A paragraph. They rarely affect the simulation mechanically -- maybe a tiny variable tick (`cp_exhaustion + 1`, `cp_faith + 1`). They build texture. Over a 90-year campaign, Layla's timeline is dense with these small moments, punctuated by the rare big one.

### Game-Rule Integrity

Events must gate themselves on the actual state of the world. Never show content that V3's rules say shouldn't exist. The check is a scripted trigger that any event can reuse.

```
# common/scripted_triggers/cp_rule_triggers.txt
cp_woman_can_work_factory = {
    # In V3, women-in-workforce is tied to labor rights laws
    root.has_law = law_type:law_women_in_the_workplace
    # ... or whatever the actual law is in 1.12
}

cp_country_is_literate = {
    has_technology_researched = pedagogy
    has_law = law_type:law_public_schools    # or whatever grants mass literacy
}

cp_has_factories_in_state = {
    scope:cp_layla.var:cp_home_state = {
        any_scope_building = { is_building_group = bg_manufacturing }
    }
}

cp_newspapers_exist = {
    has_technology_researched = mass_communication
}
```

Every event's `trigger` block composes these. Layla does not read a newspaper in 1837. She does not work in a factory before women are legally in workplaces. The overseer does not "arrest her for union activity" before trade unions are legal. We NEVER write content that breaks the game's model of the world.

Write these triggers as we hit each rule. Treat the trigger file as our lore-integrity contract.

### Evolving Personality

Initial weights are the starting point. A character's interests shift over time from:

**Branch events** (big shifts): Layla chooses to move to Cairo -> `interest_land_reform` drops from 10 to 4, `interest_labor` rises from 2 to 8.

**Drift from life pulse** (small shifts): every bad harvest nudges `interest_revolution` up by a tiny amount. Every good year nudges it down. Bounded 0-10.

**Silent background drift** (the long slow burn): each year under certain conditions nudges weights invisibly. No event fires. The player doesn't see it. But 20 years of serfdom under a censored press slowly bleeds hope. Documented in code but not surfaced to the player. This is what lets a country stay feudal for decades and still feel alive -- the pressure builds without fireworks.

**Drift from major country changes**: when a war drags into a third year, `interest_war` increases for everyone. When literacy becomes widespread, `interest_education` rises for characters with children. When a failed reform bill is proposed (even without passing), `cp_hope` rises a small amount -- the news of the attempt leaks through information channels and tells the fellahin that change is *thinkable*.

**Balance constraint**: silent drift must never swing a mechanic hard enough to notice in a normal play session. We are painting texture, not tuning the game. If a weight changes by 0.1/year that's fine; 1.0/year is too much. The cumulative effect over 30 years should still feel subtle. If playtesters say "my country flipped because of this mod," we've over-drifted.

Implementation: in each event's `effect`, include a small weight update where relevant. In the life pulse, include an `immediate` that applies slow drift based on state conditions.

```
# Inside an event's option that involves Layla losing the harvest
scope:cp_layla = {
    change_variable = { name = cp_interest_revolution add = 1 }
    change_variable = { name = cp_hope subtract = 1 }
    clamp_variable = { name = cp_interest_revolution min = 0 max = 10 }
    clamp_variable = { name = cp_hope min = 0 max = 10 }
}
```

Document every weight-affecting line in the character's README so we can audit drift.

### Opinions on Other Nations

Each character holds a per-nation opinion stored as a variable: `cp_opinion_<TAG>`, scaled -100 to +100, default 0 (indifferent/unaware). Opinions are formed by:

- **Exposure events**: a cousin in Alexandria (FRA opinion), a pilgrim returning from Istanbul (OTT opinion), a British engineer building a rail line (GBR opinion).
- **War/diplomacy**: a war with France drops Layla's FRA opinion sharply; a favorable treaty nudges it up.
- **Famine aid**: a foreign country sending grain during famine raises that country's opinion significantly.

Opinions gate future events. Layla only gets a "worried about the French" event if her FRA opinion is non-zero (she has heard of them). This keeps the story grounded -- a fellaha in 1836 doesn't spontaneously have thoughts about Austria.

### Information Flow (the most important layer)

A serf in an isolated, censored country doesn't know what's happening in the world. A serf in a port city with a literate cousin does. Opinions and reactions are **gated by what could plausibly reach her**. This is the mod's most powerful subtlety -- and the reason a country can have serfs for decades without revolution.

Each character has information channels. Each channel is a scripted trigger that checks whether a piece of news could reach her:

```
# common/scripted_triggers/cp_info_triggers.txt

cp_hears_foreign_news = {
    OR = {
        # Personal connection: a relative in the port
        scope:cp_layla = { has_character_flag = cousin_in_alexandria }
        # Media: literate + press exists + not censored
        AND = {
            scope:cp_layla = { var:cp_literate = 1 }
            root.has_technology_researched = mass_communication
            root.has_law = law_type:law_free_press       # or protected
        }
        # Travel: she's in a port or trade hub
        scope:cp_layla.var:cp_home_state = {
            OR = {
                is_sea_adjacent = yes
                any_scope_building = { is_building_group = bg_trade }
            }
        }
    }
}

cp_hears_domestic_news = {
    # Rural + censored + illiterate = almost no info
    # The country's literacy rate, press laws, urbanization all matter
    OR = {
        scope:cp_layla = { var:cp_literate = 1 }
        scope:cp_layla.var:cp_home_state = {
            state_population >= 500000       # a city-ish state
        }
        root.has_law = law_type:law_free_press
    }
}

cp_hears_about_industrialization = {
    # The domestic contradiction: peasants hear about factories if...
    OR = {
        scope:cp_layla.var:cp_home_state = {
            any_scope_building = { is_building_group = bg_manufacturing }
        }
        # Or someone from her village went to the factory
        scope:cp_layla = { has_character_flag = knew_someone_who_went_to_city }
    }
}
```

**This gates everything.** A foreign war, a failed reform attempt, a factory being built in a neighboring state -- none of it reaches Layla unless information flows. The mod should feel claustrophobic for isolated characters and cosmopolitan for characters with access. When a player censors the press, their serfs *literally stop reacting to the outside world*.

**The "serfs for 200 years" dynamic**: a country can remain feudal indefinitely if its characters never hear that a different life is possible. The player's information policies -- press laws, education, urbanization, travel rights -- become *narrative* decisions, not just statistical ones. Abolishing press freedom is now something that quiets your peasants' imaginations, not just a POP modifier.

**Hope leaks**: even a FAILED reform attempt can transmit hope. If a land reform bill is proposed and fails in parliament, the news that reform was even *attempted* reaches the fellahin through their information channels and slightly raises `cp_hope`. A government that never proposes reform gets no hope leak. A government that proposes and fails repeatedly gets a frustrated population. These subtleties are the mod's heart.

### The Domestic Contradiction

Separate from foreign information: a peasant in an industrializing country can see factories being built, people leaving for the city, and new money circulating -- while they themselves remain serfs. This *internal* information flow is its own trigger (`cp_hears_about_industrialization` above). When it fires, it generates *rage-or-hope* events specific to the contradiction: the farmer's children leaving for Cairo, a bey building a factory on his former estate, a returning laborer telling stories.

The severity of the rage/hope depends on the character's personality weights and the gap between their condition and the new wealth. Layla's interest_revolution doesn't rise because the game decided -- it rises because she watched her cousin come home with a wristwatch.

### Death and Succession

Characters die. Sources of death, each checked on an appropriate pulse:

| Cause | Check | Probability |
|-------|-------|-------------|
| Natural (age) | `age >= 60` + yearly roll | V3 default, ~15%/year past 60 |
| War | Husband/son is soldier + battle lost + roll | High during wars |
| Cholera/disease | `any_harvest_condition = disease_outbreak` + roll | Episodic |
| Childbirth | Women + `has_character_flag = pregnant` + era | Higher pre-1860s |
| Factory accident | Laborer + weak workers' rights + roll | Situational |
| Famine | Home state SoL crashes + roll | During cotton bust, etc. |

On death: a final event plays (funeral, burial, "Ahmed came home to an empty house"). Then a *successor* may spawn -- Layla's daughter, Samier's brother -- with a *related* but not identical personality. The campaign has continuity without reincarnation.

### 1.12 Workaround: Journal Entries as National Cast

Until 1.13's National Cast enhancements ship (April 28, 2026), we use a hidden per-country journal entry `je_cp_common_people` as our character tracker:

- The JE lives as long as the country does. It holds aggregate variables (total active characters, generations passed, etc.).
- Each character's own variables live on their character object (forward-compatible with 1.13).
- The JE's `status_desc` can summarize active characters as a dev-visible inspector.
- When 1.13 ships, we migrate inspection to the proper National Cast UI and keep character variables unchanged.

This keeps us from painting ourselves into a 1.12-only corner.

## Nation-Specific vs Generic Characters

**Nation-specific** characters (e.g., Layla for Egypt, a Decembrist's wife for Russia) have:
- Hardcoded name, culture, religion
- Deep story arcs tied to that nation's historical context
- Eligibility: `country_tag = EGY`

**Generic** characters (e.g., "a factory worker," "a conscripted soldier") have:
- Culture-generated names (the game picks culturally appropriate names)
- Story arcs that work for any qualifying nation
- Eligibility: condition-based (has factories, is at war, etc.)
- Dynamic localization: `[ROOT.GetName]` for country, `[scope:cp_current_char.GetName]` for character

The pool should mix both: nation-specific characters spread across major playable nations, and generic characters available to any qualifying country. As the pool grows, every nation gets richer coverage.

---

# Part 5: Characters

The character pool -- profiles, personality weights, interests, life events, story trees, crossings, event text, image prompts, and artwork -- lives in [`characters/`](characters/). See [`characters/README.md`](characters/README.md) for the index.

Each anchor character has its own folder with:
- `README.md` -- profile, weights, V3 hooks, life events, story tree
- `events/` -- event text drafts (one file per event)
- `prompts/` -- image-generation prompts
- `images/` -- rendered portraits and scenes

Anchor characters (deep arcs): [Layla](characters/layla/), [al-Sayyid](characters/al-sayyid/), [Tarek](characters/tarek/), [Samier](characters/samier/), [the Soldier](characters/the-soldier/). Lightweight "reaction-only" characters live in [`characters/sketches.md`](characters/sketches.md). How trees intersect lives in [`characters/crossings.md`](characters/crossings.md).

This file holds the *theory* (what a character is, how personality weights work, how events fire). The characters folder holds the *content* (who they are, what happens to them).

# Part 6: Technical Implementation Plan

## Phase 0: Template Initialization

Before any mod development, replace the template placeholders:

**Option A -- GitHub Actions** (recommended):
1. Go to repository Settings > Actions > General > Workflow permissions > Read and write
2. Run the "Initialize Mod Template" workflow with:
   - ABBREVIATION: `cp`
   - MOD_NAME: `Common People`
   - MOD_DESCRIPTION: `Personal stories of ordinary people whose lives change through your policy decisions`
   - MOD_TAGS: `Events,Gameplay`

**Option B -- Manual**:
```bash
# From repository root
find . -type f -not -path './.git/*' -not -path './.github/*' \
  -exec sed -i 's/ABBREVIATION_PLACEHOLDER/cp/g' {} +
find . -type f -not -path './.git/*' -not -path './.github/*' \
  -exec sed -i 's/MODNAME_PLACEHOLDER/Common People/g' {} +
# Rename files
mv mod/events/ABBREVIATION_PLACEHOLDER_events.txt mod/events/cp_events.txt
mv mod/common/on_actions/ABBREVIATION_PLACEHOLDER_on_actions.txt mod/common/on_actions/cp_on_actions.txt
```

Update `mod/.metadata/metadata.json` with:
```json
{
  "name": "Common People",
  "id": "com.github.aboelsoud.common-people-victoria3-mod",
  "version": "0.1.0",
  "game_id": "victoria3",
  "picture": "thumbnail.png",
  "supported_game_version": "1.13.*",
  "short_description": "Personal stories of ordinary people whose lives change through your policy decisions",
  "tags": ["Events", "Gameplay"],
  "relationships": [],
  "game_custom_data": {
    "multiplayer_synchronized": true
  }
}
```

## Phase 1: Proof of Concept -- Layla + Personality System

**Goal**: Prove two things work: (1) a deep story arc triggered by game systems, and (2) the personality-weighted reaction system.

**What we build:**
- Layla with her full personality weights
- Her first 3 main arc chapters (land reform)
- 2-3 reaction events (war declared, law failed, IG shift)
- The router + personality roll system
- A journal entry tracking her story

**Files to create:**
- `mod/common/on_actions/cp_on_actions.txt` -- hooks into game start, law enacted, law failed, war declared
- `mod/common/scripted_effects/cp_effects.txt` -- `cp_spawn_layla` with personality weights
- `mod/common/scripted_triggers/cp_triggers.txt` -- condition checks
- `mod/events/cp_init_events.txt` -- initialization + random activation
- `mod/events/cp_router_events.txt` -- hidden dispatch with personality rolls
- `mod/events/cp_layla_events.txt` -- Layla's arc chapters 1-3
- `mod/events/cp_react_law_events.txt` -- shared law reaction template
- `mod/events/cp_react_war_events.txt` -- shared war reaction template
- `mod/common/journal_entries/cp_journal_entries.txt`
- `mod/localization/english/cp_layla_l_english.yml`
- `mod/localization/english/cp_reactions_l_english.yml`
- `mod/localization/english/cp_ui_l_english.yml`

**Testing**: Debug mode, play as Egypt, verify: (1) Layla spawns, (2) main arc events fire on law change, (3) reaction events fire probabilistically on other game events, (4) journal entry tracks progress.

## Phase 2: Second Character + Pool System

**Goal**: Add Samier. Validate that two characters coexist, react to different events with different personalities, and the pool activation system works.

**Key test**: Same game event fires -> Layla reacts one way (or not at all), Samier reacts differently (or not at all). The personality system produces distinct behaviors.

## Phase 3: Scale to 10 Characters

**Goal**: Prove the architecture handles 10 active characters without performance issues.

- Add 8 more characters (mix of nation-specific and generic)
- Build the random activation system (3-5 active at game start)
- Build the mid-game activation system (new characters unlock as conditions change)
- Add reaction templates for: diplomacy, revolution, IG shifts, technology, economy
- Test late-game performance

## Phase 4: Content Expansion

**Goal**: Grow the character pool. Define personalities and spawn effects for as many characters as we can. Write deep arcs for main characters. Complete reaction templates for all game systems.

This is the content phase -- mostly writing event text and localization, using the proven architecture from Phases 1-3. The pool grows with every release. There is no finish line -- just more people to meet.

## Phase 5: Polish and Release

- Custom DDS event images
- Playtest across multiple campaigns and countries
- Balance reaction frequency (not too many events, not too few)
- Steam Workshop upload

## Code Examples

### Complete On-Actions File

```
# mod/common/on_actions/cp_on_actions.txt

on_game_started = {
    on_actions = {
        on_cp_start
    }
}

on_cp_start = {
    effect = {
        set_global_variable = {
            name = cp_is_loaded
            value = yes
        }
        # Activate random characters from the pool
        trigger_event = { id = cp_init.001 }
    }
}

on_law_enacted = {
    on_actions = {
        cp_on_law_enacted
    }
}

on_law_enactment_failed = {
    on_actions = {
        cp_on_law_failed
    }
}

cp_on_law_enacted = {
    trigger = {
        exists = global_var:cp_is_loaded
    }
    events = {
        cp_router.001     # Main arc advancement
        cp_router.010     # Personality-based reactions
    }
}

cp_on_law_failed = {
    trigger = {
        exists = global_var:cp_is_loaded
    }
    events = {
        cp_router.011     # Personality-based reactions to failure
    }
}

on_war_declared = {
    on_actions = {
        cp_on_war_start
    }
}

cp_on_war_start = {
    trigger = {
        exists = global_var:cp_is_loaded
    }
    events = {
        cp_router.002     # Soldier main arc activation
        cp_router.020     # Personality-based war reactions
    }
}
```

### Personality-Based Router (The Core Innovation)

```
# mod/events/cp_router_events.txt
namespace = cp_router

# React to law enacted: check each active character's interest
cp_router.010 = {
    type = country_event
    hidden = yes

    trigger = {
        exists = global_var:cp_is_loaded
    }

    immediate = {
        # For each active Common People character...
        every_scope_character = {
            limit = { has_variable = cp_is_common_person }
            save_scope_as = cp_reacting_char

            # Roll against their interest in this law category
            # Example: land reform law enacted
            if = {
                limit = {
                    root = {
                        OR = {
                            has_law = law_type:law_tenant_farmers
                            has_law = law_type:law_homesteading
                        }
                    }
                }
                random = {
                    chance = {
                        value = 0
                        add = var:cp_interest_land_reform
                        multiply = 10    # 0-10 weight -> 0-100% chance
                    }
                    # They care! Fire reaction
                    root = {
                        trigger_event = { id = cp_react_law.001 }
                    }
                }
            }

            # Same check for labor laws
            if = {
                limit = {
                    root = {
                        OR = {
                            has_law = law_type:law_regulatory_bodies
                            has_law = law_type:law_workers_protection
                        }
                    }
                }
                random = {
                    chance = {
                        value = 0
                        add = var:cp_interest_labor
                        multiply = 10
                    }
                    root = {
                        trigger_event = { id = cp_react_law.002 }
                    }
                }
            }
        }
    }
}

# Main arc router: advance deep stories when conditions met
cp_router.001 = {
    type = country_event
    hidden = yes

    trigger = {
        exists = global_var:cp_is_loaded
    }

    immediate = {
        # Spawn Layla if eligible and randomly selected
        if = {
            limit = {
                country_tag = EGY
                NOT = { has_variable = cp_layla_spawned }
                OR = {
                    has_law = law_type:law_tenant_farmers
                    has_law = law_type:law_homesteading
                }
            }
            cp_spawn_layla = yes
            trigger_event = { id = cp_layla.001 }
        }

        # Advance Layla's story if active
        if = {
            limit = {
                cp_layla_story_active = yes
                var:cp_layla_chapter >= 1
            }
            trigger_event = { id = cp_layla.002 }
        }
    }
}
```

### Character Spawn with Personality Weights

```
# mod/common/scripted_effects/cp_effects.txt

cp_spawn_layla = {
    create_character = {
        first_name = "Layla"
        culture = cu:misri
        religion = rel:sunni
        female = yes
        age = 22
        traits = { persistent }
        save_scope_as = cp_layla_char
    }
    scope:cp_layla_char = {
        # Identity markers
        set_variable = { name = cp_is_common_person value = yes }
        set_variable = { name = cp_is_layla value = yes }
        set_variable = { name = cp_pop_type value = 1 }  # 1 = farmer

        # Personality weights (0-10 scale)
        set_variable = { name = cp_interest_land_reform value = 10 }
        set_variable = { name = cp_interest_war value = 7 }
        set_variable = { name = cp_interest_revolution value = 8 }
        set_variable = { name = cp_interest_religion value = 6 }
        set_variable = { name = cp_interest_womens_rights value = 5 }
        set_variable = { name = cp_interest_economy value = 5 }
        set_variable = { name = cp_interest_france value = 4 }
        set_variable = { name = cp_interest_education value = 3 }
        set_variable = { name = cp_interest_labor value = 2 }
        set_variable = { name = cp_interest_diplomacy value = 1 }
    }
    set_variable = { name = cp_layla_spawned value = yes }
    set_variable = { name = cp_layla_chapter value = 0 }
}

cp_spawn_samier = {
    create_character = {
        first_name = "Samier"
        culture = cu:misri
        religion = rel:sunni
        female = no
        age = 19
        traits = { ambitious }
        save_scope_as = cp_samier_char
    }
    scope:cp_samier_char = {
        set_variable = { name = cp_is_common_person value = yes }
        set_variable = { name = cp_is_samier value = yes }
        set_variable = { name = cp_pop_type value = 2 }  # 2 = laborer

        # Samier's personality: cares about labor, revolution, economy
        set_variable = { name = cp_interest_labor value = 10 }
        set_variable = { name = cp_interest_revolution value = 8 }
        set_variable = { name = cp_interest_economy value = 8 }
        set_variable = { name = cp_interest_education value = 6 }
        set_variable = { name = cp_interest_war value = 4 }
        set_variable = { name = cp_interest_land_reform value = 3 }
        set_variable = { name = cp_interest_religion value = 3 }
        set_variable = { name = cp_interest_womens_rights value = 2 }
        set_variable = { name = cp_interest_france value = 1 }
        set_variable = { name = cp_interest_diplomacy value = 1 }
    }
    set_variable = { name = cp_samier_spawned value = yes }
    set_variable = { name = cp_samier_chapter value = 0 }
}
```

### Complete First Story Event

```
# mod/events/cp_layla_events.txt
namespace = cp_layla

cp_layla.001 = {
    type = country_event
    placement = root

    title = cp_layla.001.t
    desc = cp_layla.001.d
    flavor = cp_layla.001.f

    event_image = {
        video = "gfx/event_pictures/africa_leader_speaking.bk2"
    }

    gui_window = event_window_1char_tabloid

    left_icon = scope:layla

    trigger = {
        has_variable = cp_layla_spawned
    }

    immediate = {
        random_scope_character = {
            limit = { has_variable = cp_is_layla }
            save_scope_as = layla
        }
    }

    option = {
        name = cp_layla.001.a
        default_option = yes
        set_country_flag = cp_layla_optimist
        change_variable = {
            name = cp_layla_chapter
            add = 1
        }
    }

    option = {
        name = cp_layla.001.b
        set_country_flag = cp_layla_realist
        change_variable = {
            name = cp_layla_chapter
            add = 1
        }
    }
}
```

### Complete Localization File

```yaml
# mod/localization/english/cp_layla_l_english.yml
# IMPORTANT: This file MUST be saved with UTF-8 BOM encoding
l_english:
 cp_layla.001.t:0 "The Farmer's Daughter"
 cp_layla.001.d:0 "In a small village along the Nile Delta, a young woman named Layla rises before dawn, as she has every day of her twenty-two years.\n\nThe land she works is not hers. It belongs to the local bey, as it belonged to his father, and his father before him. Layla does not question this. She questions very little about the order of things. She wants what her mother wanted: a family, a roof, enough bread, and the sound of her children laughing in the evening.\n\nHer husband, Ahmed, works beside her in the fields. They were married at seventeen. There is talk of a child.\n\nLayla does not follow politics. She does not know who governs in Cairo, nor does she care. But even in this village, far from the ministries and the parliaments, the winds of change carry whispers.\n\nThe laws, they say, are changing. The land may soon belong to those who work it."
 cp_layla.001.f:0 "The earth does not care who holds the deed. It yields to the hands that tend it."
 cp_layla.001.a:0 "Her life will change for the better."
 cp_layla.001.b:0 "Change brings its own hardships."
```

### Complete Journal Entry

```
# mod/common/journal_entries/cp_journal_entries.txt

je_cp_layla_story = {
    icon = "gfx/interface/icons/event_icons/event_portrait.dds"

    is_shown_when_inactive = {
        country_tag = EGY
    }

    possible = {
        has_variable = cp_layla_spawned
        NOT = { has_variable = cp_layla_complete }
    }

    complete = {
        has_variable = cp_layla_complete
    }

    on_complete = {
    }

    status_desc = {
        first_valid = {
            triggered_desc = {
                trigger = { var:cp_layla_chapter <= 1 }
                desc = je_cp_layla_ch1
            }
            triggered_desc = {
                trigger = { var:cp_layla_chapter = 2 }
                desc = je_cp_layla_ch2
            }
            triggered_desc = {
                trigger = { var:cp_layla_chapter = 3 }
                desc = je_cp_layla_ch3
            }
            triggered_desc = {
                trigger = { var:cp_layla_chapter >= 4 }
                desc = je_cp_layla_ch4
            }
        }
    }

    current_value = {
        value = var:cp_layla_chapter
    }

    goal_add_value = {
        value = 7
    }

    progressbar = yes
    weight = 100
}
```

---

# Part 7: What's Possible vs What's Hard

## What Works Well

- **Event chains**: Fully supported, well-understood. The bread and butter of V3 modding.
- **Named persistent characters**: The National Cast keeps them alive in the pool indefinitely.
- **Multi-system hooks**: `on_law_enacted`, `on_law_enactment_failed`, `on_war_declared`, `on_war_end`, and many more -- we can hook into nearly every major game event.
- **Weighted random**: The `random` effect with `chance` blocks gives us the personality roll system. Characters with high interest weights react more often -- exactly what we need.
- **Pop-type binding**: We can check SoL, radicalism, and employment for specific pop types in specific states. Characters' stories reflect real simulation data.
- **Journal entry tracking**: Built-in UI with progress bars and dynamic text.
- **Rich localization with triggered_desc**: Event text can branch based on which character is reacting, making shared templates feel personal.
- **Modular architecture**: Adding the next character doesn't touch any existing ones.

## What Needs Workarounds

**Characters bound to pop types and home states**: Layla won't appear in the pop browser -- she's a character object, not a pop. But she has a real home state (via `set_home_state`, new in 1.13) and her story events are driven by real pop data in that state. We check farmer SoL, farmer radicalism, and farmer employment in her home state to determine what happens in her narrative. Example:
```
trigger = {
    any_scope_state = {
        state_region = s:STATE_LOWER_EGYPT
        any_scope_pop = {
            pop_type = farmer
            standard_of_living >= 15
        }
    }
}
```
This means Layla's story is never disconnected from gameplay -- it directly reflects what the simulation is doing to her pop type.

**Commoner portraits**: V3 generates character portraits based on culture and ethnicity, which looks great. However, the event UI frames characters with the same visual treatment as political elites. The player needs to understand through narrative context that these are ordinary people, not politicians. The Agitator role is the exception -- if Samier becomes an Agitator, he IS a political figure.

**Character aging and death**: Characters age and can die naturally. If Layla's story spans 30 years, she will age in the portrait. This is actually a feature -- seeing her grow old across the story is powerful. But we must handle the edge case where she dies of natural causes before the story completes (use `on_character_death` to trigger a premature ending event).

## What Is Hard or Impossible

**Characters in the pop browser**: Cannot be done. The pop browser shows aggregate pop data, not individual characters. Layla will never appear there.

**Physical character movement**: Characters do not have a "current state" location in the way pops do. We cannot mechanically move Layla from a rural state to Cairo. We describe it in text.

**Procedural story generation**: Every event must be hand-written. We cannot generate "a random story about a random person." The mod's content scales linearly with authoring effort.

**Multiplayer determinism**: Events that fire differently for different players can cause desynchronization. All Common People events must trigger deterministically from game state (law changes, war state), not from random rolls that might differ between players. Use `random_events` weights carefully.

**Save compatibility across versions**: Adding new events is safe. Changing existing event IDs or variable names will break saves that have active storylines. Choose naming conventions carefully and commit to them.

## Performance Considerations

- **Event-driven, not pulse-driven**: The personality roll system fires from on-actions (`on_law_enacted`, `on_war_declared`) -- these only fire when something happens. The `every_scope_character` iteration only loops over active CP characters (3-8 at a time), not all characters in the game. This is lightweight.
- **Limit active characters**: Cap simultaneously active characters at 5-8. More than that risks event spam (imagine 10 characters all reacting to one law change). The player would be overwhelmed with popups, not just the engine.
- **Yearly pulse for gradual stories only**: Use `on_yearly_pulse_country` sparingly -- only for checking slow story progression (e.g., Layla's harvest chapter needs SoL check). Keep the trigger block lightweight.
- **Clean up completed characters**: When a story arc completes, remove the `cp_is_common_person` variable so the character stops being iterated in router events. The character persists in the National Cast but the mod stops checking them.
- **Test at scale**: Phase 3 specifically tests 10 characters to validate performance. The pool can be hundreds of definitions -- only 5-8 are active at once, so pool size doesn't affect runtime performance.
- **Reaction cooldowns**: After a character reacts to an event, set a short cooldown variable (e.g., 30-day flag) to prevent them from reacting to every single event in quick succession. Space out the personal moments.

---

# Appendices

## A: Paradox Script Cheat Sheet

### Logical Operators
```
AND = { trigger_a trigger_b }      # Both must be true (implicit in blocks)
OR = { trigger_a trigger_b }       # At least one must be true
NOT = { trigger }                  # Must be false
NAND = { trigger_a trigger_b }     # At least one must be false
NOR = { trigger_a trigger_b }      # Both must be false
```

### Conditional Effects
```
if = {
    limit = { condition }
    # effects if true
}
else_if = {
    limit = { other_condition }
    # effects if this is true
}
else = {
    # effects if nothing matched
}
```

### Common Trigger Patterns
```
has_law = law_type:law_serfdom             # Country has this law
has_variable = my_var                       # Variable exists
var:my_var >= 5                             # Variable value check
country_tag = EGY                           # Is this country
is_at_war = yes                             # Currently at war
any_scope_state = { has_building = X }      # Any state has building
any_scope_character = { has_trait = X }     # Any character has trait
year >= 1860                                # Game year check
has_country_flag = my_flag                  # Flag is set
```

### Common Effect Patterns
```
set_variable = { name = X value = Y }      # Set variable
change_variable = { name = X add = Y }     # Increment variable
set_country_flag = my_flag                  # Set flag
trigger_event = { id = ns.001 }            # Fire event immediately
trigger_event = { id = ns.001 days = 30 }  # Fire event after 30 days
create_character = { ... }                  # Spawn character
save_scope_as = my_scope                    # Save current scope
add_modifier = { name = X months = 12 }    # Apply temporary modifier
```

## B: Relevant V3 Law Types

These are the law type references used in triggers and checks:

**Land Reform:**
- `law_type:law_serfdom`
- `law_type:law_tenant_farmers`
- `law_type:law_homesteading`
- `law_type:law_collectivized_agriculture`

**Labor:**
- `law_type:law_no_workers_rights`
- `law_type:law_regulatory_bodies`
- `law_type:law_workers_protection`

**Economic System:**
- `law_type:law_traditionalism`
- `law_type:law_interventionism`
- `law_type:law_laissez_faire`
- `law_type:law_command_economy`
- `law_type:law_cooperative_ownership`

**Rights of Women:**
- `law_type:law_no_womens_rights`
- `law_type:law_women_own_property`
- `law_type:law_women_in_the_workplace`
- `law_type:law_womens_suffrage`

**Slavery:**
- `law_type:law_slave_trade`
- `law_type:law_legacy_slavery`
- `law_type:law_slavery_banned`

**Welfare:**
- `law_type:law_no_social_security`
- `law_type:law_poor_laws`
- `law_type:law_wage_subsidies`
- `law_type:law_old_age_pension`

**Education:**
- `law_type:law_no_schools`
- `law_type:law_religious_schools`
- `law_type:law_private_schools`
- `law_type:law_public_schools`

**Health:**
- `law_type:law_no_health_system`
- `law_type:law_private_health_insurance`
- `law_type:law_public_health_insurance`

**Conscription:**
- `law_type:law_no_conscription`
- `law_type:law_conscription`
- `law_type:law_mass_conscription`

## C: Vanilla Event Image Paths

These base game event images can be referenced in your events during development before creating custom art:

```
# African/Middle Eastern settings
gfx/event_pictures/africa_leader_speaking.bk2
gfx/event_pictures/africa_diplomacy.bk2
gfx/event_pictures/africa_marketplace.bk2

# Agricultural/Rural
gfx/event_pictures/unspecific_farm.bk2
gfx/event_pictures/unspecific_ruler_speaking_to_people.bk2
gfx/event_pictures/unspecific_harvest.bk2

# Industrial/Urban
gfx/event_pictures/unspecific_factory.bk2
gfx/event_pictures/unspecific_city_streets.bk2
gfx/event_pictures/unspecific_workers.bk2
gfx/event_pictures/unspecific_industrial_district.bk2

# Military/War
gfx/event_pictures/unspecific_military_parade.bk2
gfx/event_pictures/unspecific_battlefield.bk2
gfx/event_pictures/unspecific_naval_battle.bk2

# Political/Social
gfx/event_pictures/unspecific_politicians_arguing.bk2
gfx/event_pictures/unspecific_newspaper.bk2
gfx/event_pictures/unspecific_protest.bk2
gfx/event_pictures/unspecific_courtroom.bk2
gfx/event_pictures/europenorthamerica_springtime_of_nations.bk2
```

**Note**: These paths are based on common patterns in vanilla V3. Verify exact paths by examining the base game's `gfx/event_pictures/` directory in `Victoria 3/game/`. File names may vary between game versions. Use debug mode -- if a path is wrong, the error log will tell you.

## D: Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Localization keys showing as raw keys (e.g., `cp_layla.001.t`) | File missing UTF-8 BOM | Re-save with BOM encoding |
| `Event namespace not found` | Missing `namespace = ` declaration at top of file | Add namespace declaration |
| `Unexpected token` | Syntax error (missing `=`, unmatched `{}`) | Check bracket matching |
| `Invalid scope` | Using a trigger/effect in the wrong scope | Check what scope you are in |
| `Variable does not exist` | Checking a variable before it was set | Add `has_variable` check first |
| Event never fires | Not hooked into any on_action | Add to on_actions file |
| Event fires but shows blank | Localization file not loaded | Check BOM, file naming (`_l_english.yml`) |
| Character not found in later events | Not saved with `save_scope_as` | Use variable marker + `random_scope_character` pattern |

## E: Resources and Links

**Official:**
- [Victoria 3 Modding Wiki](https://vic3.paradoxwikis.com/Modding)
- [Event Modding](https://vic3.paradoxwikis.com/Event_modding)
- [Journal Modding](https://vic3.paradoxwikis.com/Journal_modding)
- [Character Modding](https://vic3.paradoxwikis.com/Character_modding)
- [Scopes](https://vic3.paradoxwikis.com/Scopes)
- [Localization](https://vic3.paradoxwikis.com/Localization)
- [Effects](https://vic3.paradoxwikis.com/Effects)
- [Triggers](https://vic3.paradoxwikis.com/Triggers)

**Dev Diaries:**
- [Dev Diary #176 -- Martin's Character Collection (National Cast)](https://forum.paradoxplaza.com/forum/threads/victoria-3-dev-diary-176-martins-character-collection.1910270/)
- [Dev Diary #60 -- Modding Introduction](https://www.paradoxinteractive.com/games/victoria-3/news/victoria-3-dev-diary-60-modding)
- [Dev Diary #120 -- Modding Features in 1.7](https://forum.paradoxplaza.com/forum/threads/victoria-3-dev-diary-120-modding-features-in-1-7.1685347/)

**Community:**
- [Victoria 3 Modding Co-op Discord](https://discord.com/invite/uUbuMTQjA7)
- [Community Mod Framework (GitHub)](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework)
- [Mod Template (GitHub)](https://github.com/Victoria-3-Modding-Co-op/Mod-Template)
- [Paradox Forums -- Victoria 3 User Mods](https://forum.paradoxplaza.com/forum/forums/victoria-3-user-mods.1115/)
- [Steam Workshop -- Victoria 3](https://steamcommunity.com/app/529340/workshop/)

**Reference Mods (study their source for techniques):**
- [Victorian Flavor Mod (GitHub)](https://github.com/Radsterman/Victorian-Flavor-Mod)
- [Historical Flavor Expansion (GitHub)](https://github.com/Nightingale1997/Historical-Flavor-Expansion)
- [More Flavor Events (Steam)](https://steamcommunity.com/sharedfiles/filedetails/?id=2924315345)

**Tools:**
- [GIMP](https://www.gimp.org/) -- Free image editor with DDS export plugin (for event images)
- [VS Code](https://code.visualstudio.com/) + CWTools extension -- Syntax highlighting for Paradox scripts
- [Sublime Text](https://www.sublimetext.com/) + Victoria3Tools plugin -- Autocomplete for V3 scripting
