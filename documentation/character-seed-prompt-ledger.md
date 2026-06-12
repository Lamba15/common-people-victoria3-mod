# Character Seed Prompt Ledger

Generated from character seed prompt docs. Rebuild with:

```bash
python3 script/build-character-seed-prompt-ledger.py --version v0.1
python3 script/build-character-seed-prompt-ledger.py --version v0.1 --check
python3 script/export-character-seed-prompts.py --version v0.1 --check
```

This ledger is the review surface for the first non-Layla character art pass. The exported prompt files and JSONL manifests are generation-ready inputs for `gpt-image-2`; promoted event art still has to pass the event image and provenance audits.

## Summary

- Requested version: `v0.1`
- Versions found: `v0.1`
- Registered persons: 16
- Persons with prompts: 16
- Registered-person coverage: 16/16
- Prompt files: 16
- Prompt exports: 48
- Issues: 0

## Batch Manifests

- `image/generated/character-seeds/v0.1/gpt-image-2-seed-batch.jsonl`

## Prompt Types

- `portrait`: 16
- `scene`: 32

## Person Counts

| Person | Prompt Files | Prompts |
|---|---:|---:|
| `bey` | 1 | 3 |
| `dawud` | 1 | 3 |
| `farid` | 1 | 3 |
| `huda` | 1 | 3 |
| `karim` | 1 | 3 |
| `layla` | 1 | 3 |
| `mansur` | 1 | 3 |
| `mina` | 1 | 3 |
| `nabil` | 1 | 3 |
| `nour` | 1 | 3 |
| `rashid` | 1 | 3 |
| `salma` | 1 | 3 |
| `samier` | 1 | 3 |
| `soldier` | 1 | 3 |
| `tarek` | 1 | 3 |
| `zaynab` | 1 | 3 |

## Seed Prompts

| Person | Prompt | Kind | Source | Export | Target PNG |
|---|---|---|---|---|---|
| `bey` | Canonical Portrait | portrait | `documentation/characters/al-sayyid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/bey_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/bey_01_canonical_portrait.png` |
| `bey` | `cp_bey.10` - The House Counts the Doors | scene | `documentation/characters/al-sayyid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/bey_02_cp_bey_10_the_house_counts_the_doors.prompt.txt` | `image/generated/character-seeds/v0.1/bey_02_cp_bey_10_the_house_counts_the_doors.png` |
| `bey` | `cp_bey.20` - The Gate Opens | scene | `documentation/characters/al-sayyid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/bey_03_cp_bey_20_the_gate_opens.prompt.txt` | `image/generated/character-seeds/v0.1/bey_03_cp_bey_20_the_gate_opens.png` |
| `dawud` | Canonical Portrait | portrait | `documentation/characters/dawud/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/dawud_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/dawud_01_canonical_portrait.png` |
| `dawud` | `cp_dawud.10` - The Rope Burn | scene | `documentation/characters/dawud/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/dawud_02_cp_dawud_10_the_rope_burn.prompt.txt` | `image/generated/character-seeds/v0.1/dawud_02_cp_dawud_10_the_rope_burn.png` |
| `dawud` | `cp_dawud.20` - The Iron Hook | scene | `documentation/characters/dawud/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/dawud_03_cp_dawud_20_the_iron_hook.prompt.txt` | `image/generated/character-seeds/v0.1/dawud_03_cp_dawud_20_the_iron_hook.png` |
| `farid` | Canonical Portrait | portrait | `documentation/characters/farid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/farid_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/farid_01_canonical_portrait.png` |
| `farid` | `cp_farid.10` - The Platform Boy | scene | `documentation/characters/farid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/farid_02_cp_farid_10_the_platform_boy.prompt.txt` | `image/generated/character-seeds/v0.1/farid_02_cp_farid_10_the_platform_boy.png` |
| `farid` | `cp_farid.20` - The Blue Wire | scene | `documentation/characters/farid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/farid_03_cp_farid_20_the_blue_wire.prompt.txt` | `image/generated/character-seeds/v0.1/farid_03_cp_farid_20_the_blue_wire.png` |
| `huda` | Canonical Portrait | portrait | `documentation/characters/huda/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/huda_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/huda_01_canonical_portrait.png` |
| `huda` | `cp_huda.10` - The Room Above the Alley | scene | `documentation/characters/huda/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/huda_02_cp_huda_10_the_room_above_the_alley.prompt.txt` | `image/generated/character-seeds/v0.1/huda_02_cp_huda_10_the_room_above_the_alley.png` |
| `huda` | `cp_huda.40` - The Rent Book | scene | `documentation/characters/huda/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/huda_03_cp_huda_40_the_rent_book.prompt.txt` | `image/generated/character-seeds/v0.1/huda_03_cp_huda_40_the_rent_book.png` |
| `karim` | Canonical Portrait | portrait | `documentation/characters/karim/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/karim_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/karim_01_canonical_portrait.png` |
| `karim` | `cp_karim.10` - The Iron Teeth | scene | `documentation/characters/karim/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/karim_02_cp_karim_10_the_iron_teeth.prompt.txt` | `image/generated/character-seeds/v0.1/karim_02_cp_karim_10_the_iron_teeth.png` |
| `karim` | `cp_karim.30` - The Broken Finger | scene | `documentation/characters/karim/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/karim_03_cp_karim_30_the_broken_finger.prompt.txt` | `image/generated/character-seeds/v0.1/karim_03_cp_karim_30_the_broken_finger.png` |
| `layla` | Canonical Portrait | portrait | `documentation/characters/layla/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/layla_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/layla_01_canonical_portrait.png` |
| `layla` | `cp_layla.1` - The Farmer's Daughter | scene | `documentation/characters/layla/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/layla_02_cp_layla_1_the_farmer_s_daughter.prompt.txt` | `image/generated/character-seeds/v0.1/layla_02_cp_layla_1_the_farmer_s_daughter.png` |
| `layla` | `cp_layla.2` - The Deed | scene | `documentation/characters/layla/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/layla_03_cp_layla_2_the_deed.prompt.txt` | `image/generated/character-seeds/v0.1/layla_03_cp_layla_2_the_deed.png` |
| `mansur` | Canonical Portrait | portrait | `documentation/characters/mansur/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/mansur_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/mansur_01_canonical_portrait.png` |
| `mansur` | `cp_mansur.10` - The Mat Beside the Looms | scene | `documentation/characters/mansur/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/mansur_02_cp_mansur_10_the_mat_beside_the_looms.prompt.txt` | `image/generated/character-seeds/v0.1/mansur_02_cp_mansur_10_the_mat_beside_the_looms.png` |
| `mansur` | `cp_mansur.20` - The First Wage Token | scene | `documentation/characters/mansur/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/mansur_03_cp_mansur_20_the_first_wage_token.prompt.txt` | `image/generated/character-seeds/v0.1/mansur_03_cp_mansur_20_the_first_wage_token.png` |
| `mina` | Canonical Portrait | portrait | `documentation/characters/mina/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/mina_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/mina_01_canonical_portrait.png` |
| `mina` | `cp_mina.10` - The First Line | scene | `documentation/characters/mina/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/mina_02_cp_mina_10_the_first_line.prompt.txt` | `image/generated/character-seeds/v0.1/mina_02_cp_mina_10_the_first_line.png` |
| `mina` | `cp_mina.20` - Letters for the Schools | scene | `documentation/characters/mina/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/mina_03_cp_mina_20_letters_for_the_schools.prompt.txt` | `image/generated/character-seeds/v0.1/mina_03_cp_mina_20_letters_for_the_schools.png` |
| `nabil` | Canonical Portrait | portrait | `documentation/characters/nabil/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/nabil_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/nabil_01_canonical_portrait.png` |
| `nabil` | `cp_nabil.10` - The Lamp at the Corner | scene | `documentation/characters/nabil/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/nabil_02_cp_nabil_10_the_lamp_at_the_corner.prompt.txt` | `image/generated/character-seeds/v0.1/nabil_02_cp_nabil_10_the_lamp_at_the_corner.png` |
| `nabil` | `cp_nabil.30` - Rifles by the Bakery | scene | `documentation/characters/nabil/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/nabil_03_cp_nabil_30_rifles_by_the_bakery.prompt.txt` | `image/generated/character-seeds/v0.1/nabil_03_cp_nabil_30_rifles_by_the_bakery.png` |
| `nour` | Canonical Portrait | portrait | `documentation/characters/nour/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/nour_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/nour_01_canonical_portrait.png` |
| `nour` | `cp_nour.10` - The Cedar Chest | scene | `documentation/characters/nour/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/nour_02_cp_nour_10_the_cedar_chest.prompt.txt` | `image/generated/character-seeds/v0.1/nour_02_cp_nour_10_the_cedar_chest.png` |
| `nour` | `cp_nour.20` - Her Name on the Paper | scene | `documentation/characters/nour/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/nour_03_cp_nour_20_her_name_on_the_paper.prompt.txt` | `image/generated/character-seeds/v0.1/nour_03_cp_nour_20_her_name_on_the_paper.png` |
| `rashid` | Canonical Portrait | portrait | `documentation/characters/rashid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/rashid_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/rashid_01_canonical_portrait.png` |
| `rashid` | `cp_rashid.10` - The Counter Window | scene | `documentation/characters/rashid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/rashid_02_cp_rashid_10_the_counter_window.prompt.txt` | `image/generated/character-seeds/v0.1/rashid_02_cp_rashid_10_the_counter_window.png` |
| `rashid` | `cp_rashid.30` - The Paper Name | scene | `documentation/characters/rashid/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/rashid_03_cp_rashid_30_the_paper_name.prompt.txt` | `image/generated/character-seeds/v0.1/rashid_03_cp_rashid_30_the_paper_name.png` |
| `salma` | Canonical Portrait | portrait | `documentation/characters/salma/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/salma_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/salma_01_canonical_portrait.png` |
| `salma` | `cp_salma.10` - The Switchboard | scene | `documentation/characters/salma/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/salma_02_cp_salma_10_the_switchboard.prompt.txt` | `image/generated/character-seeds/v0.1/salma_02_cp_salma_10_the_switchboard.png` |
| `salma` | `cp_salma.20` - The First Light | scene | `documentation/characters/salma/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/salma_03_cp_salma_20_the_first_light.prompt.txt` | `image/generated/character-seeds/v0.1/salma_03_cp_salma_20_the_first_light.png` |
| `samier` | Canonical Portrait | portrait | `documentation/characters/samier/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/samier_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/samier_01_canonical_portrait.png` |
| `samier` | `cp_samier.10` - The Gate of Smoke | scene | `documentation/characters/samier/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/samier_02_cp_samier_10_the_gate_of_smoke.prompt.txt` | `image/generated/character-seeds/v0.1/samier_02_cp_samier_10_the_gate_of_smoke.png` |
| `samier` | Future accident/radicalization beat | scene | `documentation/characters/samier/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/samier_03_future_accident_radicalization_beat.prompt.txt` | `image/generated/character-seeds/v0.1/samier_03_future_accident_radicalization_beat.png` |
| `soldier` | Canonical Portrait | portrait | `documentation/characters/the-soldier/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/soldier_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/soldier_01_canonical_portrait.png` |
| `soldier` | `cp_soldier.10` - The Notice | scene | `documentation/characters/the-soldier/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/soldier_02_cp_soldier_10_the_notice.prompt.txt` | `image/generated/character-seeds/v0.1/soldier_02_cp_soldier_10_the_notice.png` |
| `soldier` | `cp_soldier.21` - The Return | scene | `documentation/characters/the-soldier/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/soldier_03_cp_soldier_21_the_return.prompt.txt` | `image/generated/character-seeds/v0.1/soldier_03_cp_soldier_21_the_return.png` |
| `tarek` | Canonical Portrait | portrait | `documentation/characters/tarek/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/tarek_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/tarek_01_canonical_portrait.png` |
| `tarek` | `cp_tarek.10` - The Mill Ledger | scene | `documentation/characters/tarek/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/tarek_02_cp_tarek_10_the_mill_ledger.prompt.txt` | `image/generated/character-seeds/v0.1/tarek_02_cp_tarek_10_the_mill_ledger.png` |
| `tarek` | Future Samier crossover beat | scene | `documentation/characters/tarek/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/tarek_03_future_samier_crossover_beat.prompt.txt` | `image/generated/character-seeds/v0.1/tarek_03_future_samier_crossover_beat.png` |
| `zaynab` | Canonical Portrait | portrait | `documentation/characters/zaynab/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/zaynab_01_canonical_portrait.prompt.txt` | `image/generated/character-seeds/v0.1/zaynab_01_canonical_portrait.png` |
| `zaynab` | `cp_zaynab.10` - The Midwife's Lamp | scene | `documentation/characters/zaynab/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/zaynab_02_cp_zaynab_10_the_midwife_s_lamp.prompt.txt` | `image/generated/character-seeds/v0.1/zaynab_02_cp_zaynab_10_the_midwife_s_lamp.png` |
| `zaynab` | `cp_zaynab.20` - Names on the Health List | scene | `documentation/characters/zaynab/prompts/seed-v0.1.md` | `image/generated/character-seeds/v0.1/prompts/zaynab_03_cp_zaynab_20_names_on_the_health_list.prompt.txt` | `image/generated/character-seeds/v0.1/zaynab_03_cp_zaynab_20_names_on_the_health_list.png` |

## Rules

- Seed prompt docs live at `documentation/characters/<person>/prompts/seed-v*.md`.
- Versioned seed batches must cover every registered person and include one canonical portrait prompt per person.
- Each prompt must be exported through `script/export-character-seed-prompts.py` before image generation.
- Generated source PNGs should stay under `image/generated/character-seeds/<version>/` until a reviewed DDS or BK2 promotion path exists.
- New character art should preserve the person token, scene purpose, and 3:2 event-window crop contract.

## Checks

```bash
python3 script/audit-character-art-contract.py
python3 script/build-character-seed-prompt-ledger.py --version v0.1 --check
python3 script/export-character-seed-prompts.py --version v0.1 --check
```
