# Person Selection Ledger

Generated from live Paradox script. Rebuild with `python3 script/build-person-selection-ledger.py`.

## First Contact

All-candidate roll: 16 visible candidates, visible weight 166, silent weight 14, top share `bey` at 8.9%.
Always-on baseline if no conditional startup scan succeeds: 6 visible candidates, visible weight 86, silent weight 14, top share `bey` at 16.0%.

| Person | Event | Weight | Share | Gate |
|---|---|---:|---:|---|
| layla | `cp_layla.1` | 14 | 7.8% | not has_variable = cp_layla_met_player |
| bey | `cp_bey.10` | 16 | 8.9% | not has_variable = cp_bey_seen_intro |
| soldier | `cp_soldier.10` | 14 | 7.8% | not has_variable = cp_soldier_seen_intro |
| nour | `cp_nour.10` | 14 | 7.8% | not has_variable = cp_nour_seen_intro |
| mina | `cp_mina.10` | 14 | 7.8% | not has_variable = cp_mina_seen_intro |
| zaynab | `cp_zaynab.10` | 14 | 7.8% | not has_variable = cp_zaynab_seen_intro |
| samier | `cp_samier.10` | 8 | 4.4% | not has_variable = cp_samier_seen_intro |
| tarek | `cp_tarek.10` | 8 | 4.4% | not has_variable = cp_tarek_seen_intro |
| farid | `cp_farid.10` | 8 | 4.4% | not has_variable = cp_farid_seen_intro |
| dawud | `cp_dawud.10` | 8 | 4.4% | not has_variable = cp_dawud_seen_intro |
| rashid | `cp_rashid.10` | 8 | 4.4% | not has_variable = cp_rashid_seen_intro |
| salma | `cp_salma.10` | 8 | 4.4% | not has_variable = cp_salma_seen_intro |
| karim | `cp_karim.10` | 8 | 4.4% | not has_variable = cp_karim_seen_intro |
| huda | `cp_huda.10` | 8 | 4.4% | not has_variable = cp_huda_seen_intro |
| nabil | `cp_nabil.10` | 8 | 4.4% | not has_variable = cp_nabil_seen_intro |
| mansur | `cp_mansur.10` | 8 | 4.4% | not has_variable = cp_mansur_seen_intro |
| silent | - | 14 | 7.8% | no visible first contact |

## Monthly Ambient Router

These weights pick whose ambient pool gets a chance each month. The actual event still passes through the shared ambient cooldowns, so most eligible months remain quiet.

| Person | Weight | Conditions | Pool |
|---|---:|---|---|
| layla | 9 | before 1850 | `cp_roll_ambient_layla` |
| layla | 7 | 1850-1880 | `cp_roll_ambient_layla` |
| layla | 5 | after 1880 | `cp_roll_ambient_layla` |
| bey | 10 | old land order; game_date < 1860.1.1 | `cp_roll_ambient_bey` |
| bey | 6 | old land order; game_date >= 1860.1.1 | `cp_roll_ambient_bey` |
| bey | 3 | not old land order | `cp_roll_ambient_bey` |
| soldier | 10 | has_variable = cp_soldier_at_war | `cp_roll_ambient_soldier` |
| soldier | 5 | not has_variable = cp_soldier_at_war | `cp_roll_ambient_soldier` |
| mansur | 8 | cp_person_home_has_manufacturing = { person = mansur } | `cp_roll_ambient_mansur` |
| mansur | 3 | not cp_person_home_has_manufacturing = { person = mansur | `cp_roll_ambient_mansur` |
| samier | 10 | cp_person_home_has_manufacturing = { person = samier }; workers unprotected | `cp_roll_ambient_samier` |
| samier | 6 | cp_person_home_has_manufacturing = { person = samier }; not workers unprotected | `cp_roll_ambient_samier` |
| samier | 3 | not cp_person_home_has_manufacturing = { person = samier | `cp_roll_ambient_samier` |
| tarek | 8 | cp_person_home_has_manufacturing = { person = tarek }; not old land order | `cp_roll_ambient_tarek` |
| tarek | 5 | any of: not cp_person_home_has_manufacturing = { person = tarek; old land order | `cp_roll_ambient_tarek` |
| karim | 8 | cp_person_home_has_machine_industry = { person = karim } | `cp_roll_ambient_karim` |
| karim | 4 | not cp_person_home_has_machine_industry = { person = karim | `cp_roll_ambient_karim` |
| farid | 9 | any of: cp_person_home_has_rail_infrastructure = { person = farid }; telegraph exists | `cp_roll_ambient_farid` |
| farid | 5 | not any of: cp_person_home_has_rail_infrastructure = { person = farid }; telegraph exists | `cp_roll_ambient_farid` |
| dawud | 8 | any of: cp_person_home_has_port = { person = dawud }; steam trade exists | `cp_roll_ambient_dawud` |
| dawud | 4 | not any of: cp_person_home_has_port = { person = dawud }; steam trade exists | `cp_roll_ambient_dawud` |
| rashid | 8 | any of: cp_person_home_has_government_office = { person = rashid }; modern records exist | `cp_roll_ambient_rashid` |
| rashid | 4 | not any of: cp_person_home_has_government_office = { person = rashid }; modern records exist | `cp_roll_ambient_rashid` |
| salma | 8 | any of: cp_person_home_has_electric_service = { person = salma }; cp_person_home_has_telephone_network = { person = salma }; after 1880 | `cp_roll_ambient_salma` |
| salma | 3 | not any of: cp_person_home_has_electric_service = { person = salma }; cp_person_home_has_telephone_network = { person = salma }; after 1880 | `cp_roll_ambient_salma` |
| huda | 8 | cp_person_home_has_urban_growth = { person = huda } | `cp_roll_ambient_huda` |
| huda | 3 | not cp_person_home_has_urban_growth = { person = huda | `cp_roll_ambient_huda` |
| nabil | 8 | public-order pressure | `cp_roll_ambient_nabil` |
| nabil | 3 | not public-order pressure | `cp_roll_ambient_nabil` |
| nour | 8 | women have property rights | `cp_roll_ambient_nour` |
| nour | 5 | not women have property rights | `cp_roll_ambient_nour` |
| mina | 8 | any of: public schools; 1850-1880; after 1880 | `cp_roll_ambient_mina` |
| mina | 5 | before 1850; not public schools | `cp_roll_ambient_mina` |
| zaynab | 9 | not public health | `cp_roll_ambient_zaynab` |
| zaynab | 5 | public health | `cp_roll_ambient_zaynab` |
| silent | 32 | always | no event |

## Conditional Entrants

Conditional people are not always present in 1836. Their spawn effects are called from the startup scan and later hooks below, and their hidden setup events randomize whether a visible first appearance fires immediately or stays silent.

| Person | Hooks | Setup Event | First Appearance Weight | Silent Weight | Immediate Visible Chance | Targets |
|---|---|---|---:|---:|---:|---|
| dawud | startup, yearly, tech, building | `cp_dawud.1` (mod/events/cp_dawud_events.txt:12) | 55 | 45 | 55.0% | `cp_dawud.10` |
| farid | startup, yearly, tech, building | `cp_farid.1` (mod/events/cp_farid_events.txt:13) | 60 | 40 | 60.0% | `cp_farid.10` |
| huda | startup, yearly, tech, building | `cp_huda.1` (mod/events/cp_huda_events.txt:12) | 50 | 50 | 50.0% | `cp_huda.10` |
| karim | startup, yearly, tech, building | `cp_karim.1` (mod/events/cp_karim_events.txt:12) | 55 | 45 | 55.0% | `cp_karim.10` |
| mansur | startup, yearly, tech, building | `cp_mansur.1` (mod/events/cp_mansur_events.txt:12) | 55 | 45 | 55.0% | `cp_mansur.10` |
| nabil | startup, yearly, law_enacted, revolution | `cp_nabil.1` (mod/events/cp_nabil_events.txt:12) | 50 | 50 | 50.0% | `cp_nabil.10` |
| rashid | startup, yearly, tech, building | `cp_rashid.1` (mod/events/cp_rashid_events.txt:12) | 50 | 50 | 50.0% | `cp_rashid.10` |
| salma | startup, yearly, tech, building | `cp_salma.1` (mod/events/cp_salma_events.txt:12) | 55 | 45 | 55.0% | `cp_salma.10` |
| samier | startup, yearly, tech, building | `cp_samier.1` (mod/events/cp_samier_events.txt:12) | 65 | 35 | 65.0% | `cp_samier.10` |
| tarek | startup, yearly, tech, building | `cp_tarek.1` (mod/events/cp_tarek_events.txt:12) | 55 | 45 | 55.0% | `cp_tarek.10` |
