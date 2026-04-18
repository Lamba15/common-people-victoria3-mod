# Layla MVP -- 30 Events

The first playable slice. Goal: prove every mechanism end-to-end with Layla-only content, then scale up to full 100+ event pool and add other characters.

## Event catalog (30)

Events are numbered `cp_layla.N` for story/branch events and `cp_layla_life.N` for pulse life events.

### Bootstrap and intro (2)

| # | ID | Type | When fires | What happens |
|---|----|----|-----------|--------------|
| 1 | `cp_startup.1` | hidden country_event | `on_game_started` on EGY | Creates Layla, sets weights, saves scope, fires intro |
| 2 | `cp_layla.intro` | character_event | immediately after startup | "The Farmer's Daughter" -- she rises before dawn; meet her |

### Land reform forward (4)

Firing: `on_law_enacted`, root = EGY, new law is the one in the row.

| # | ID | Trigger law | Mood |
|---|----|------------|------|
| 3 | `cp_layla.tenant_farmers` | `law_tenant_farmers` | Half-free. She can leave, but where? Stays. |
| 4 | `cp_layla.homesteading` | `law_homesteading` | **The Deed.** Loyalist spike. The great moment. |
| 5 | `cp_layla.commercialized` | `law_commercialized_agriculture` | A company owns the field. Same work, a wage now. |
| 6 | `cp_layla.collectivized` | `law_collectivized_agriculture` | The committee. Community or loss of ownership? |

### Land reform backward (2)

| # | ID | Trigger | Mood |
|---|----|---------|------|
| 7 | `cp_layla.serfdom_restored` | any law -> `law_serfdom` | **The darkest event.** Radical spike. The bey rides through the village again. |
| 8 | `cp_layla.tenant_rollback` | `law_homesteading` -> `law_tenant_farmers` | She tasted ownership. Now she pays rent. |

### Monthly life pulse (8)

10% monthly fire (~1.2 events per year). The pool chosen contextually by current state.

| # | ID | Bucket | When weighted up |
|---|----|--------|------------------|
| 9 | `cp_layla_life.flooding_nile` | Harvest/seasons | No drought + summer |
| 10 | `cp_layla_life.locust_sighting` | Harvest/seasons | Any year, slight risk |
| 11 | `cp_layla_life.drought_panic` | Harvest/seasons | State has drought harvest condition |
| 12 | `cp_layla_life.fajr_in_the_dark` | Faith | Any year; she is tired |
| 13 | `cp_layla_life.neighbor_funeral` | Community | Any year, small weight |
| 14 | `cp_layla_life.mariam_letter` | World beyond | She hears foreign news + FRA is at peace |
| 15 | `cp_layla_life.tax_collector` | Community | Country has extractive laws |
| 16 | `cp_layla_life.ahmed_tender` | Family | Low-stakes quiet happiness |

### Family and mortality (4)

| # | ID | Trigger | What happens |
|---|----|---------|--------------|
| 17 | `cp_layla.pregnancy` | random, married, under 35 | She is pregnant. Sets `cp_pregnant = 1`. |
| 18 | `cp_layla.childbirth` | `cp_pregnant = 1` + 1 year passed | Child born OR mother dies (era-dependent roll) |
| 19 | `cp_layla.ahmed_conscripted` | `on_war_started`, EGY involved | Terror. Ahmed marches away. |
| 20 | `cp_layla.ahmed_dies` | war ends with casualties + roll | Funeral. `cp_widow = 1`. |

### Opinions and information (3)

| # | ID | Trigger | What happens |
|---|----|---------|--------------|
| 21 | `cp_layla.hears_of_industry` | first time `cp_hears_about_industrialization` fires | She hears there are factories in Cairo. Confusion or wonder. |
| 22 | `cp_layla.failed_reform_hope` | any land reform law proposed and failed | News reaches her: they tried. Small `cp_hope` gain. |
| 23 | `cp_layla.independence_day` | Muhammad Ali independence event fires | Massive `cp_opinion_egy` shift. Pride and fear. |

### Mirror/Reaction events (4)

Templated reactions gated by personality weight.

| # | ID | Hook | When |
|---|----|------|------|
| 24 | `cp_layla.reform_failed` | `on_law_proposed_failed` (if exists) | Devastated. "They promised." |
| 25 | `cp_layla.revolution_starts` | `on_revolution_start` | Hides. "I told you." |
| 26 | `cp_layla.cholera_hits` | state gets `disease_outbreak` | Child could die. Possibly her death roll. |
| 27 | `cp_layla.press_crackdown` | `law_free_press` -> censored | Silent. She wouldn't even notice -- which is the point. Small `cp_hope` bleed. |

### Closure (3)

| # | ID | Trigger | What happens |
|---|----|---------|--------------|
| 28 | `cp_layla.natural_death` | age >= 60 + yearly roll | Her death. A final event. |
| 29 | `cp_layla.legacy_prosperity` | she died + `cp_social_class = "farmer"` + SoL rose | Grandchild plays in her field. |
| 30 | `cp_layla.legacy_hardship` | she died + she migrated to city | She died a domestic servant in Cairo. The land a memory. |

## What this slice proves

- [ ] Character creation and persistent scope (`cp_layla`)
- [ ] Variables on character persist through save/reload
- [ ] Yearly pulse with contextual weighting
- [ ] `on_law_enacted` router dispatching to character events
- [ ] Forward AND backward law transitions handled
- [ ] Information-flow gate (`cp_hears_foreign_news`) works
- [ ] Silent drift accumulates over years
- [ ] War hooks pull Ahmed into the story
- [ ] Death, and a successor narrative
- [ ] Journal entry as National Cast stand-in shows Layla exists

If these 30 events ship clean, everything else is content.

## Build order (vertical slices)

Each step is playable and produces a visible result before moving to the next.

1. **Template init** -- replace `ABBREVIATION_PLACEHOLDER` -> `cp`, `MODNAME_PLACEHOLDER` -> `Common People`. Metadata updated. Verify launcher sees mod.
2. **Hollow on_action** -- log "CP loaded" on game start. Verify in `debug.log`.
3. **Character creation + intro** -- events 1 and 2. Verify face shows, option clickable, save/reload persists her scope.
4. **Land reform forward** -- events 3-6. Verify `on_law_enacted` routes correctly. Use console `set_law` to test each.
5. **Land reform backward** -- events 7-8. Test rollback detection.
6. **Pulse framework + 3 life events** -- events 9, 10, 12. Verify 10% monthly fire.
7. **Remaining life events** -- 11, 13-16.
8. **Information-flow trigger library** -- scripted triggers (`cp_hears_foreign_news`, `cp_hears_about_industrialization`, game-rule guards).
9. **Opinion/info events** -- 21, 22, 23.
10. **Family and mortality** -- 17-20, 28-30.
11. **Mirror events** -- 24-27.
12. **Journal entry** as National Cast stand-in, minimal text.
13. **Polish, bug sweep, image prompts for all events.**

## Image prompt format

Per-event, self-contained, one prompt per file in `prompts/`. Each prompt includes:
- V3 art style block (same preamble every prompt)
- Character reference instruction ("use attached image as the person, a Misri peasant woman in her twenties named Layla, see `/home/aboelsoud/Pictures/common-people-mod-images/Layla -- Farming/` for her look")
- Specific scene description for this event

User supplies the reference image alongside the prompt when generating.

Files: `prompts/cp_layla.intro.md`, `prompts/cp_layla.homesteading.md`, etc. One prompt file per event that needs imagery. Life-pulse events can share an image across variants where appropriate.

## What we defer to post-MVP

- Actual historical accuracy scripted-trigger library beyond `cp_hears_*`. Grow as events demand.
- Full silent-drift per-year ticks. Start with event-driven drift; add silent only once stable.
- Character successor spawning (Layla's daughter Fatima). After Layla's death, for now just ends her arc.
- 1.13 migration. Write 1.12 cleanly and commented so migration is mechanical.
- Other characters (al-Sayyid, Tarek, Samier, Soldier). Zero work until Layla is shippable.
- Other countries. Zero.
