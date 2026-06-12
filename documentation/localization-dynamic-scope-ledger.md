# Dynamic Localization Scope Ledger

Generated from shipped English localization. Rebuild with:

```bash
python3 script/build-localization-dynamic-scope-ledger.py
python3 script/build-localization-dynamic-scope-ledger.py --check
python3 script/audit-localization-dynamic-scope.py
```

This ledger prevents the ruler-audience regression where unsupported dynamic loc rendered as `ERROR:[c:EGY.GetRuler...]` in game. New dynamic localization expressions must either match a reviewed safe pattern here or be deliberately added to the audit allow-list with a note.

## Contract

- Do not use direct tag scopes such as `[c:EGY...]` in player-facing localization.
- Do not use `GetRuler.GetTitle`; Victoria 3 1.13 uses `GetRuler.GetPrimaryRoleTitle`.
- Ruler references must use `[ROOT.GetCountry.GetRuler.GetFullName]` and `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` in country events.
- Legacy Layla journal variables use the proven `Country.MakeScope.Var(...)` form.
- Legacy Layla journal labels and prose fragments use `ROOT.GetCountry.GetCustom('cp_layla_*')`.
- Shared active journal slots use `ROOT.GetCountry.GetCustom('cp_common_people_active_body')` and `ROOT.GetCountry.GetCustom('cp_common_people_active_slot_<n>')`.
- Shared active person stats may render only age, SoL, hope, and literacy through reviewed `Country.MakeScope.Var('cp_<person>_<stat>')` expressions.

## Summary

- Dynamic expressions reviewed: 114
- Allowed categories: 9
- Issues: 0

## Category Counts

| Category | Count |
|---|---:|
| Layla SoL variable | 1 |
| Layla age variable | 1 |
| Layla hope variable | 1 |
| country ruler full name | 7 |
| country ruler role title | 7 |
| shared active-roster SoL variable | 15 |
| shared active-roster custom localization | 20 |
| shared active-roster home state pointer | 16 |
| shared active-roster integer variable | 46 |

## Dynamic Expressions

| File | Key | Expression | Category |
|---|---|---|---|
| `mod/localization/english/cp_layla_vox_l_english.yml:983` | `cp_layla_vox.101.flavor` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:983` | `cp_layla_vox.101.flavor` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_layla_vox_l_english.yml:990` | `cp_layla_vox.1011.flavor` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:990` | `cp_layla_vox.1011.flavor` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_layla_vox_l_english.yml:995` | `cp_layla_vox.1012.flavor` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:995` | `cp_layla_vox.1012.flavor` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_layla_vox_l_english.yml:1000` | `cp_layla_vox.1013.flavor` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:1000` | `cp_layla_vox.1013.flavor` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_layla_vox_l_english.yml:1005` | `cp_layla_vox.102.d.default` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:1005` | `cp_layla_vox.102.d.default` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_layla_vox_l_english.yml:1031` | `cp_layla_vox.103.flavor` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:1031` | `cp_layla_vox.103.flavor` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_layla_vox_l_english.yml:1100` | `cp_layla_vox.106.flavor` | `[ROOT.GetCountry.GetRuler.GetFullName]` | country ruler full name |
| `mod/localization/english/cp_layla_vox_l_english.yml:1100` | `cp_layla_vox.106.flavor` | `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | country ruler role title |
| `mod/localization/english/cp_shared_l_english.yml:13` | `cp_je_common_people_reason` | `[ROOT.GetCountry.GetCustom('cp_common_people_active_body')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:19` | `cp_common_people_active_body` | `[ROOT.GetCountry.GetCustom('cp_common_people_active_slot_1')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:19` | `cp_common_people_active_body` | `[ROOT.GetCountry.GetCustom('cp_common_people_active_slot_2')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:19` | `cp_common_people_active_body` | `[ROOT.GetCountry.GetCustom('cp_common_people_active_slot_3')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:23` | `cp_roster_layla_line_alive` | `[Country.MakeScope.Var('cp_layla_age').GetValue\|D]` | Layla age variable |
| `mod/localization/english/cp_shared_l_english.yml:23` | `cp_roster_layla_line_alive` | `[Country.MakeScope.Var('cp_layla_hope').GetValue\|D]` | Layla hope variable |
| `mod/localization/english/cp_shared_l_english.yml:23` | `cp_roster_layla_line_alive` | `[Country.MakeScope.Var('cp_layla_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:23` | `cp_roster_layla_line_alive` | `[Country.MakeScope.Var('cp_layla_sol').GetValue\|1]` | Layla SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:23` | `cp_roster_layla_line_alive` | `[Country.MakeScope.Var('cp_layla_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:23` | `cp_roster_layla_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_layla_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:24` | `cp_roster_nour_line_alive` | `[Country.MakeScope.Var('cp_nour_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:24` | `cp_roster_nour_line_alive` | `[Country.MakeScope.Var('cp_nour_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:24` | `cp_roster_nour_line_alive` | `[Country.MakeScope.Var('cp_nour_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:24` | `cp_roster_nour_line_alive` | `[Country.MakeScope.Var('cp_nour_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:24` | `cp_roster_nour_line_alive` | `[Country.MakeScope.Var('cp_nour_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:24` | `cp_roster_nour_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_nour_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:25` | `cp_roster_mina_line_alive` | `[Country.MakeScope.Var('cp_mina_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:25` | `cp_roster_mina_line_alive` | `[Country.MakeScope.Var('cp_mina_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:25` | `cp_roster_mina_line_alive` | `[Country.MakeScope.Var('cp_mina_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:25` | `cp_roster_mina_line_alive` | `[Country.MakeScope.Var('cp_mina_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:25` | `cp_roster_mina_line_alive` | `[Country.MakeScope.Var('cp_mina_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:25` | `cp_roster_mina_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_mina_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:26` | `cp_roster_zaynab_line_alive` | `[Country.MakeScope.Var('cp_zaynab_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:26` | `cp_roster_zaynab_line_alive` | `[Country.MakeScope.Var('cp_zaynab_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:26` | `cp_roster_zaynab_line_alive` | `[Country.MakeScope.Var('cp_zaynab_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:26` | `cp_roster_zaynab_line_alive` | `[Country.MakeScope.Var('cp_zaynab_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:26` | `cp_roster_zaynab_line_alive` | `[Country.MakeScope.Var('cp_zaynab_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:26` | `cp_roster_zaynab_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_zaynab_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:28` | `cp_roster_bey_line_alive` | `[Country.MakeScope.Var('cp_bey_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:28` | `cp_roster_bey_line_alive` | `[Country.MakeScope.Var('cp_bey_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:28` | `cp_roster_bey_line_alive` | `[Country.MakeScope.Var('cp_bey_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:28` | `cp_roster_bey_line_alive` | `[Country.MakeScope.Var('cp_bey_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:28` | `cp_roster_bey_line_alive` | `[Country.MakeScope.Var('cp_bey_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:28` | `cp_roster_bey_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_bey_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:29` | `cp_roster_nabil_line_alive` | `[Country.MakeScope.Var('cp_nabil_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:29` | `cp_roster_nabil_line_alive` | `[Country.MakeScope.Var('cp_nabil_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:29` | `cp_roster_nabil_line_alive` | `[Country.MakeScope.Var('cp_nabil_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:29` | `cp_roster_nabil_line_alive` | `[Country.MakeScope.Var('cp_nabil_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:29` | `cp_roster_nabil_line_alive` | `[Country.MakeScope.Var('cp_nabil_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:29` | `cp_roster_nabil_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_nabil_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:30` | `cp_roster_rashid_line_alive` | `[Country.MakeScope.Var('cp_rashid_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:30` | `cp_roster_rashid_line_alive` | `[Country.MakeScope.Var('cp_rashid_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:30` | `cp_roster_rashid_line_alive` | `[Country.MakeScope.Var('cp_rashid_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:30` | `cp_roster_rashid_line_alive` | `[Country.MakeScope.Var('cp_rashid_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:30` | `cp_roster_rashid_line_alive` | `[Country.MakeScope.Var('cp_rashid_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:30` | `cp_roster_rashid_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_rashid_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:31` | `cp_roster_salma_line_alive` | `[Country.MakeScope.Var('cp_salma_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:31` | `cp_roster_salma_line_alive` | `[Country.MakeScope.Var('cp_salma_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:31` | `cp_roster_salma_line_alive` | `[Country.MakeScope.Var('cp_salma_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:31` | `cp_roster_salma_line_alive` | `[Country.MakeScope.Var('cp_salma_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:31` | `cp_roster_salma_line_alive` | `[Country.MakeScope.Var('cp_salma_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:31` | `cp_roster_salma_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_salma_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:33` | `cp_roster_samier_line_alive` | `[Country.MakeScope.Var('cp_samier_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:33` | `cp_roster_samier_line_alive` | `[Country.MakeScope.Var('cp_samier_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:33` | `cp_roster_samier_line_alive` | `[Country.MakeScope.Var('cp_samier_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:33` | `cp_roster_samier_line_alive` | `[Country.MakeScope.Var('cp_samier_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:33` | `cp_roster_samier_line_alive` | `[Country.MakeScope.Var('cp_samier_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:33` | `cp_roster_samier_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_samier_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:34` | `cp_roster_tarek_line_alive` | `[Country.MakeScope.Var('cp_tarek_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:34` | `cp_roster_tarek_line_alive` | `[Country.MakeScope.Var('cp_tarek_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:34` | `cp_roster_tarek_line_alive` | `[Country.MakeScope.Var('cp_tarek_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:34` | `cp_roster_tarek_line_alive` | `[Country.MakeScope.Var('cp_tarek_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:34` | `cp_roster_tarek_line_alive` | `[Country.MakeScope.Var('cp_tarek_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:34` | `cp_roster_tarek_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_tarek_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:35` | `cp_roster_karim_line_alive` | `[Country.MakeScope.Var('cp_karim_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:35` | `cp_roster_karim_line_alive` | `[Country.MakeScope.Var('cp_karim_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:35` | `cp_roster_karim_line_alive` | `[Country.MakeScope.Var('cp_karim_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:35` | `cp_roster_karim_line_alive` | `[Country.MakeScope.Var('cp_karim_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:35` | `cp_roster_karim_line_alive` | `[Country.MakeScope.Var('cp_karim_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:35` | `cp_roster_karim_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_karim_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:36` | `cp_roster_mansur_line_alive` | `[Country.MakeScope.Var('cp_mansur_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:36` | `cp_roster_mansur_line_alive` | `[Country.MakeScope.Var('cp_mansur_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:36` | `cp_roster_mansur_line_alive` | `[Country.MakeScope.Var('cp_mansur_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:36` | `cp_roster_mansur_line_alive` | `[Country.MakeScope.Var('cp_mansur_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:36` | `cp_roster_mansur_line_alive` | `[Country.MakeScope.Var('cp_mansur_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:36` | `cp_roster_mansur_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_mansur_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:38` | `cp_roster_soldier_line_alive` | `[Country.MakeScope.Var('cp_soldier_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:38` | `cp_roster_soldier_line_alive` | `[Country.MakeScope.Var('cp_soldier_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:38` | `cp_roster_soldier_line_alive` | `[Country.MakeScope.Var('cp_soldier_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:38` | `cp_roster_soldier_line_alive` | `[Country.MakeScope.Var('cp_soldier_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:38` | `cp_roster_soldier_line_alive` | `[Country.MakeScope.Var('cp_soldier_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:38` | `cp_roster_soldier_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_soldier_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:39` | `cp_roster_farid_line_alive` | `[Country.MakeScope.Var('cp_farid_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:39` | `cp_roster_farid_line_alive` | `[Country.MakeScope.Var('cp_farid_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:39` | `cp_roster_farid_line_alive` | `[Country.MakeScope.Var('cp_farid_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:39` | `cp_roster_farid_line_alive` | `[Country.MakeScope.Var('cp_farid_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:39` | `cp_roster_farid_line_alive` | `[Country.MakeScope.Var('cp_farid_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:39` | `cp_roster_farid_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_farid_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:40` | `cp_roster_dawud_line_alive` | `[Country.MakeScope.Var('cp_dawud_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:40` | `cp_roster_dawud_line_alive` | `[Country.MakeScope.Var('cp_dawud_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:40` | `cp_roster_dawud_line_alive` | `[Country.MakeScope.Var('cp_dawud_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:40` | `cp_roster_dawud_line_alive` | `[Country.MakeScope.Var('cp_dawud_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:40` | `cp_roster_dawud_line_alive` | `[Country.MakeScope.Var('cp_dawud_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:40` | `cp_roster_dawud_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_dawud_current')]` | shared active-roster custom localization |
| `mod/localization/english/cp_shared_l_english.yml:41` | `cp_roster_huda_line_alive` | `[Country.MakeScope.Var('cp_huda_age').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:41` | `cp_roster_huda_line_alive` | `[Country.MakeScope.Var('cp_huda_hope').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:41` | `cp_roster_huda_line_alive` | `[Country.MakeScope.Var('cp_huda_literacy').GetValue\|D]` | shared active-roster integer variable |
| `mod/localization/english/cp_shared_l_english.yml:41` | `cp_roster_huda_line_alive` | `[Country.MakeScope.Var('cp_huda_sol').GetValue\|1]` | shared active-roster SoL variable |
| `mod/localization/english/cp_shared_l_english.yml:41` | `cp_roster_huda_line_alive` | `[Country.MakeScope.Var('cp_huda_state_pointer').GetState.GetStateRegion.GetName]` | shared active-roster home state pointer |
| `mod/localization/english/cp_shared_l_english.yml:41` | `cp_roster_huda_line_alive` | `[ROOT.GetCountry.GetCustom('cp_roster_huda_current')]` | shared active-roster custom localization |

## Checks

```bash
python3 script/audit-localization-dynamic-scope.py
python3 script/build-localization-dynamic-scope-ledger.py --check
script/audit-common-people.py
script/audit-production-debug-leaks.py
```
