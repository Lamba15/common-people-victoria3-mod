# Common People art review - v0.5 candidates

Date: 2026-05-26

This is the visual QA ledger for generated event-image candidates. It is intentionally stricter than the missing-file audit: an image can load correctly and still fail the desired direction.

## Review sheets

Run:

```bash
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-art-provenance.py
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/promote-art-batch.py --all
```

Current sheets:

- `image/generated/layla/v0.5/contact-sheet.png`
- `image/generated/layla/v0.6/contact-sheet.png`
- `image/generated/al-sayyid/v0.1/contact-sheet.png`
- `image/generated/al-sayyid/v0.2/contact-sheet.png`
- `image/generated/soldier/v0.1/contact-sheet.png`
- `image/generated/soldier/v0.2/contact-sheet.png`
- `image/generated/samier/v0.1/contact-sheet.png`
- `image/generated/tarek/v0.1/contact-sheet.png`
- `image/generated/nour/v0.1/contact-sheet.png`
- `image/generated/mina/v0.1/contact-sheet.png`
- `image/generated/zaynab/v0.1/contact-sheet.png`

## Next Replacement Batches

The next high-impact Layla batches are defined in:

```text
documentation/characters/layla/prompts/replacement-batch-v0.7.md
documentation/characters/layla/prompts/replacement-batch-v0.8.md
documentation/characters/layla/prompts/replacement-batch-v0.9.md
documentation/characters/layla/prompts/replacement-batch-v0.10.md
documentation/characters/layla/prompts/replacement-batch-v0.11.md
documentation/characters/layla/prompts/replacement-batch-v0.12.md
```

They target the highest-use legacy/no-source assets from:

```bash
script/audit-art-provenance.py --rank-missing --limit 30
script/audit-art-batch-plan.py --all
```

v0.7 priority targets are `cp_layla_bey_eye`, `cp_layla_coptic_neighbour`, `cp_layla_mothers_hand`, `cp_layla_not_on_deed`, `cp_layla_conversation_ahmed`, `cp_layla_conversation_children`, `cp_layla_conversation_mill`, `cp_layla_letter_not_come`, `cp_layla_mill_closed`, `cp_layla_strike`, and `cp_layla_conversation_land`.

v0.8 priority targets are `cp_layla_children_leave`, `cp_layla_election_day`, `cp_layla_foreman_runner`, `cp_layla_rifles`, `cp_layla_strangers`, `cp_layla_conversation_country`, `cp_layla_conversation_lost_child`, `cp_layla_conversation_paper`, `cp_layla_conversation_rolls`, `cp_layla_conversation_room`, and `cp_layla_daughter_reads`.

v0.9 priority targets are `cp_layla_moment`, `cp_layla_neighbours_boy`, `cp_layla_no_wind`, `cp_layla_bread_not_rise`, `cp_layla_brothers_letter`, `cp_layla_burning_letters`, `cp_layla_cairo_calling`, `cp_layla_chains`, `cp_layla_child_fever`, `cp_layla_childbirth`, and `cp_layla_children_school`.

v0.10 priority targets are `cp_layla_cloth`, `cp_layla_coffee`, `cp_layla_column_returns`, `cp_layla_compound`, `cp_layla_conversation_distance`, `cp_layla_conversation_envelope`, `cp_layla_conversation_kitchen`, `cp_layla_conversation_nile`, `cp_layla_conversation_school`, `cp_layla_conversation_small`, and `cp_layla_conversation_stall`.

v0.11 priority targets are `cp_layla_dates`, `cp_layla_district_office`, `cp_layla_dust_on_water`, `cp_layla_every_man`, `cp_layla_factory_field`, `cp_layla_first_envelope`, `cp_layla_forty_days`, `cp_layla_guard`, `cp_layla_hajj`, `cp_layla_hen`, and `cp_layla_imam_visit`.

v0.12 priority targets are `cp_layla_insurance_man`, `cp_layla_law_new`, `cp_layla_letter_folded`, `cp_layla_loaf`, `cp_layla_mariam_letter`, `cp_layla_meeting`, `cp_layla_merchants_scale`, `cp_layla_midwife_lamp`, `cp_layla_mill_smoke`, `cp_layla_minaret_silence`, and `cp_layla_ministry`.

`script/export-art-batch-prompts.py --all` exports auditable prompt text files plus one `gpt-image-2-batch.jsonl` manifest per active versioned batch under `image/generated/layla/<version>/`. The v0.7-v0.12 manifests have been dry-run validated against the image generation CLI, with each job targeting `gpt-image-2`, `1536x1024`, high-quality PNG output, and an explicit `<asset>.dds.png` filename under its versioned `image/generated/layla/<version>/` directory.

`script/build-art-acceptance-ledger.py` writes `documentation/art-acceptance-ledger.md`, the current production queue for planned replacements. It reports all 66 v0.7-v0.12 targets as `waiting-gpt-image-2`, with 228 legacy event-window references queued.

`script/promote-art-batch.py --all` reports the exact source/DDS/reference state for all active ledgers and refuses `--apply` until the generated PNG and shipped DDS are present. At the current checkpoint all 66 targets are still waiting; the tool sees 228 legacy event-window references queued for replacement.

## Review rubric

Every event image must pass all five checks before release:

- **Narrative object**: a deed, letter, ledger, rifle, gate, bed, hand, or other concrete story anchor is legible at 600x400.
- **Human scale**: the image feels witnessed, not staged as a hero poster or a generic strategy-game backdrop.
- **Period fit**: clothes, interiors, tools, machines, and paper feel plausible for 19th-century Egypt and the event's decade.
- **Character continuity**: repeat appearances look like the same person aging or changing, not a different cast member.
- **No empty atmosphere**: beautiful scenery without a specific action fails.

## First-pass findings

### Layla v0.5 prototype

- `cp_layla_homesteading_v05` is the strongest proof of direction: the deed is readable, the face carries the event, and the field context is clear.
- `cp_layla_last_morning_v05` works for late-life continuity and restraint.
- `cp_layla_intro_v05` was readable and quiet, but the scene was more mood-setting than event-specific.
- `cp_layla_intro_v06` replaces the v0.5 first-meeting proof. The patched reed roof, visible drip, clay jar, doorway hand, and field view now establish Layla's material life before the politics arrive.
- `cp_layla_ahmed_conscripted_v05` risked making Layla the only clear subject.
- `cp_layla_ahmed_conscripted_v06` replaces the v0.5 departure proof. Ahmed now reads as the departing husband, his backward glance and bundle carry the beat, and Layla remains a restrained witness.
- `cp_layla_clerks_letter_v05` had a useful witness/crowd structure, but the paper/letter action was weaker than the title wanted.
- `cp_layla_clerks_letter_v06` replaces the v0.5 grief proof. The open ledger is now the clear visual hinge, and Layla's doorway grip makes the withheld grief legible without melodrama.
- `cp_layla_conversation_audience_v05` is visually good but does not yet prove the conversation system's "audience" language; it reads more like solitary waiting.
- `cp_layla_conversation_audience_v06` replaces the v0.5 conversation proof. The empty chair, lamp, and papers now make the absent audience readable at event-window size.

### Hassan Bey al-Sayyid

- The set is coherent and recognizable across four scenes.
- `cp_bey_homesteading` and `cp_bey_serfdom_restored` clearly show class power in public space.
- `cp_bey_commercialized` and `cp_bey_intro` risk feeling too similar because both are desk/interior scenes. Future Bey images need stronger object variation: seal, account book, crop sample, eviction notice, broken lease, or rail prospectus.
- `cp_bey_commercialized_v02` replaces the v0.1 commercialized-agriculture image. The cotton bolls, sealed contract, exterior arch, and refusal gesture now distinguish the beat from the intro-room image.

### Yusuf ibn Mahmud

- `cp_soldier_notice` is the clearest narrative beat: officer, paper, family threshold, and road all read.
- `cp_soldier_intro` establishes Yusuf but is quiet enough that it may feel like a portrait rather than an event.
- `cp_soldier_return` has strong mood, but the lone back-facing figure may be too ambiguous in-game; a family threshold, bandage, or returned rifle would make the beat harder to miss.
- `cp_soldier_return_v02` replaces the v0.1 return image. Yusuf is now front-readable, and the bandage, rifle, threshold, and mother figure make the homecoming specific.

### Samier

- `cp_samier_intro` gives the strongest industrial-labor transition in the current set.
- `cp_samier_labor_law` reads as a factory notice-board moment and is mechanically on-target.
- Future Samier scenes should keep the factory specific but avoid generic European mill language when the event is meant to stay Egyptian and human-scale.

### Tarek al-Rashidi

- `cp_tarek_intro` establishes the owner-side factory view and the ledger object clearly.
- `cp_tarek_labor_law` communicates pressure and calculation.
- Both images lean into a polished late-19th-century European suit/interior language. That can fit Tarek's class aspiration, but future prompts should add stronger Egyptian/Fayoum markers so he does not become a generic industrialist.

## Immediate art decisions

- Keep the current generated sets wired for smoke testing; they are loadable and coherent enough to validate event flow, audio, and UI.
- Do not promote the legacy Layla prototype DDS files back into active use.
- Six first-pass weak proof points now have stronger replacements wired: Layla intro v0.6, Layla Ahmed conscripted v0.6, Layla clerk's letter v0.6, Layla conversation audience v0.6, Yusuf return v0.2, and Bey commercialized agriculture v0.2.
- Use contact sheets after every generation batch before DDS conversion or event wiring.
- Keep `documentation/art-acceptance-ledger.md` current after every generation, DDS conversion, or promotion step. It is the handoff ledger between GPT image generation, human review, conversion, and event rewiring.
- Treat `script/audit-art-provenance.py` as the active replacement meter. It currently reports 23 generated/source-covered active images and 95 legacy/no-source active images; all remaining no-source images are Layla-owned. v0.7-v0.12 now queue 66 of those legacy images for replacement. Use `--rank-missing` to choose each following generation batch by active event-window impact.
