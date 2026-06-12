# Event Firing Ledger

Generated from live Paradox script. Rebuild with `python3 script/build-event-firing-ledger.py`.

This ledger maps each visible non-debug event to its production route. Debug wrappers do not count as proof here.

## Summary

- Visible non-debug events: 356
- Events without production routes: 0
- Persons with visible events: 16

## Route Counts

- `ambient`: 84
- `button`: 84
- `first_contact`: 16
- `hidden_person_router`: 62
- `law_reaction`: 51
- `milestone`: 27
- `visible_chain`: 121
- `world_response`: 97

## Route Glossary

- `first_contact`: visible event selected by the startup first-contact roll.
- `ambient`: visible event selected by a person ambient pool through `cp_try_fire_ambient`.
- `law_reaction`: visible event selected by a law dispatcher through `cp_try_fire_law_reaction`.
- `world_response`: visible event selected by routine technology, building, conditional-entry, yearly, or public-order routing through `cp_try_fire_world_response`.
- `milestone`: visible event selected by a critical yearly, war, mortality, family, crossroads, revolution, or other life-event dispatcher through `cp_try_fire_milestone`.
- `button`: visible event selected by a player or QA button through `cp_button_fire`.
- `setup_first_appearance`: visible event opened by that person's hidden setup event after a conditional entry roll.
- `hidden_person_router`: visible event opened by a same-person hidden router, such as a conversation chooser.
- `visible_chain`: visible event opened by another visible event in the same beat.


## Person Event Counts

- `bey`: 6
- `dawud`: 6
- `farid`: 6
- `huda`: 6
- `karim`: 6
- `layla`: 266
- `mansur`: 6
- `mina`: 6
- `nabil`: 6
- `nour`: 6
- `rashid`: 6
- `salma`: 6
- `samier`: 6
- `soldier`: 6
- `tarek`: 6
- `zaynab`: 6

## Visible Event Routes

| Event | Person | Title | Routes | Production Sources | Definition |
|---|---|---|---|---|---|
| `cp_bey.10` | bey | The Master's Window | ambient, button, first_contact | `cp_roll_ambient_bey` (mod/common/scripted_effects/cp_bey_memory.txt:138)<br>`cp_shared_action_bey` (mod/common/scripted_effects/cp_shared_action_buttons.txt:48)<br>`cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_bey_events.txt:49` |
| `cp_bey.20` | bey | The Gate Opens | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:399) | `mod/events/cp_bey_events.txt:85` |
| `cp_bey.21` | bey | Order Restored | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:433) | `mod/events/cp_bey_events.txt:121` |
| `cp_bey.22` | bey | The Cotton Merchant | law_reaction | `cp_bey_dispatch_law_enacted` (mod/common/scripted_effects/cp_bey_memory.txt:41) | `mod/events/cp_bey_events.txt:157` |
| `cp_bey.30` | bey | Smoke at the Boundary | world_response=2 | `cp_bey_dispatch_tech` (mod/common/scripted_effects/cp_bey_memory.txt:59)<br>`cp_bey_dispatch_building` (mod/common/scripted_effects/cp_bey_memory.txt:75) | `mod/events/cp_bey_events.txt:193` |
| `cp_bey.40` | bey | The Visitor's Card | ambient, button | `cp_roll_ambient_bey` (mod/common/scripted_effects/cp_bey_memory.txt:145)<br>`cp_shared_action_bey` (mod/common/scripted_effects/cp_shared_action_buttons.txt:49) | `mod/events/cp_bey_events.txt:229` |
| `cp_dawud.10` | dawud | The Rope Burn | ambient, button, first_contact, world_response=2 | `cp_dawud_dispatch_building` (mod/common/scripted_effects/cp_dawud_memory.txt:130)<br>`cp_roll_ambient_dawud` (mod/common/scripted_effects/cp_dawud_memory.txt:206)<br>`cp_shared_action_dawud` (mod/common/scripted_effects/cp_shared_action_buttons.txt:121) | `mod/events/cp_dawud_events.txt:59` |
| `cp_dawud.20` | dawud | The Iron Hook | world_response=2 | `cp_dawud_dispatch_yearly` (mod/common/scripted_effects/cp_dawud_memory.txt:68)<br>`cp_dawud_dispatch_tech` (mod/common/scripted_effects/cp_dawud_memory.txt:113) | `mod/events/cp_dawud_events.txt:95` |
| `cp_dawud.30` | dawud | Smoke at the Quay | world_response | `cp_dawud_dispatch_tech` (mod/common/scripted_effects/cp_dawud_memory.txt:103) | `mod/events/cp_dawud_events.txt:131` |
| `cp_dawud.40` | dawud | Salt on the Floor | ambient, button | `cp_roll_ambient_dawud` (mod/common/scripted_effects/cp_dawud_memory.txt:213)<br>`cp_shared_action_dawud` (mod/common/scripted_effects/cp_shared_action_buttons.txt:122) | `mod/events/cp_dawud_events.txt:167` |
| `cp_dawud.50` | dawud | The Tariff Chalk | law_reaction | `cp_dawud_dispatch_law_enacted` (mod/common/scripted_effects/cp_dawud_memory.txt:85) | `mod/events/cp_dawud_events.txt:203` |
| `cp_dawud.60` | dawud | The Manifest Room | ambient, button, world_response | `cp_dawud_dispatch_building` (mod/common/scripted_effects/cp_dawud_memory.txt:150)<br>`cp_roll_ambient_dawud` (mod/common/scripted_effects/cp_dawud_memory.txt:220)<br>`cp_shared_action_dawud` (mod/common/scripted_effects/cp_shared_action_buttons.txt:123) | `mod/events/cp_dawud_events.txt:239` |
| `cp_farid.10` | farid | The Platform Boy | ambient, button, first_contact, world_response=2 | `cp_farid_dispatch_tech` (mod/common/scripted_effects/cp_farid_memory.txt:102)<br>`cp_roll_ambient_farid` (mod/common/scripted_effects/cp_farid_memory.txt:213)<br>`cp_shared_action_farid` (mod/common/scripted_effects/cp_shared_action_buttons.txt:112) | `mod/events/cp_farid_events.txt:60` |
| `cp_farid.20` | farid | The Blue Wire | world_response=2 | `cp_farid_dispatch_yearly` (mod/common/scripted_effects/cp_farid_memory.txt:64)<br>`cp_farid_dispatch_tech` (mod/common/scripted_effects/cp_farid_memory.txt:111) | `mod/events/cp_farid_events.txt:96` |
| `cp_farid.30` | farid | Stones for the Embankment | world_response | `cp_farid_dispatch_building` (mod/common/scripted_effects/cp_farid_memory.txt:138) | `mod/events/cp_farid_events.txt:132` |
| `cp_farid.40` | farid | The Night Lamp | ambient, button | `cp_roll_ambient_farid` (mod/common/scripted_effects/cp_farid_memory.txt:220)<br>`cp_shared_action_farid` (mod/common/scripted_effects/cp_shared_action_buttons.txt:113) | `mod/events/cp_farid_events.txt:168` |
| `cp_farid.50` | farid | The New Carriage | world_response=2 | `cp_farid_dispatch_yearly` (mod/common/scripted_effects/cp_farid_memory.txt:77)<br>`cp_farid_dispatch_tech` (mod/common/scripted_effects/cp_farid_memory.txt:121) | `mod/events/cp_farid_events.txt:204` |
| `cp_farid.60` | farid | The Parcel Bag | ambient, button, world_response | `cp_farid_dispatch_building` (mod/common/scripted_effects/cp_farid_memory.txt:155)<br>`cp_roll_ambient_farid` (mod/common/scripted_effects/cp_farid_memory.txt:227)<br>`cp_shared_action_farid` (mod/common/scripted_effects/cp_shared_action_buttons.txt:114) | `mod/events/cp_farid_events.txt:240` |
| `cp_huda.10` | huda | The Room Above the Alley | ambient, button, first_contact, world_response=2 | `cp_huda_dispatch_building` (mod/common/scripted_effects/cp_huda_memory.txt:164)<br>`cp_roll_ambient_huda` (mod/common/scripted_effects/cp_huda_memory.txt:255)<br>`cp_shared_action_huda` (mod/common/scripted_effects/cp_shared_action_buttons.txt:158) | `mod/events/cp_huda_events.txt:58` |
| `cp_huda.20` | huda | The Street Under Planks | world_response=2 | `cp_huda_dispatch_tech` (mod/common/scripted_effects/cp_huda_memory.txt:125)<br>`cp_huda_dispatch_building` (mod/common/scripted_effects/cp_huda_memory.txt:180) | `mod/events/cp_huda_events.txt:94` |
| `cp_huda.30` | huda | The Water Under Stone | ambient, button, world_response=2 | `cp_huda_dispatch_yearly` (mod/common/scripted_effects/cp_huda_memory.txt:76)<br>`cp_huda_dispatch_tech` (mod/common/scripted_effects/cp_huda_memory.txt:135)<br>`cp_roll_ambient_huda` (mod/common/scripted_effects/cp_huda_memory.txt:270) | `mod/events/cp_huda_events.txt:130` |
| `cp_huda.40` | huda | The Rent Book | ambient, button, world_response | `cp_huda_dispatch_yearly` (mod/common/scripted_effects/cp_huda_memory.txt:66)<br>`cp_roll_ambient_huda` (mod/common/scripted_effects/cp_huda_memory.txt:262)<br>`cp_shared_action_huda` (mod/common/scripted_effects/cp_shared_action_buttons.txt:159) | `mod/events/cp_huda_events.txt:166` |
| `cp_huda.50` | huda | The Roof Patch | ambient, button, world_response=2 | `cp_huda_dispatch_yearly` (mod/common/scripted_effects/cp_huda_memory.txt:87)<br>`cp_huda_dispatch_building` (mod/common/scripted_effects/cp_huda_memory.txt:198)<br>`cp_roll_ambient_huda` (mod/common/scripted_effects/cp_huda_memory.txt:277) | `mod/events/cp_huda_events.txt:202` |
| `cp_huda.60` | huda | The White Road | ambient, button, world_response=2 | `cp_huda_dispatch_yearly` (mod/common/scripted_effects/cp_huda_memory.txt:98)<br>`cp_huda_dispatch_tech` (mod/common/scripted_effects/cp_huda_memory.txt:143)<br>`cp_roll_ambient_huda` (mod/common/scripted_effects/cp_huda_memory.txt:285) | `mod/events/cp_huda_events.txt:239` |
| `cp_karim.10` | karim | The Iron Teeth | ambient, button, first_contact, world_response=2 | `cp_karim_dispatch_building` (mod/common/scripted_effects/cp_karim_memory.txt:141)<br>`cp_roll_ambient_karim` (mod/common/scripted_effects/cp_karim_memory.txt:247)<br>`cp_shared_action_karim` (mod/common/scripted_effects/cp_shared_action_buttons.txt:149) | `mod/events/cp_karim_events.txt:58` |
| `cp_karim.20` | karim | The Tool Bench | world_response=2 | `cp_karim_dispatch_tech` (mod/common/scripted_effects/cp_karim_memory.txt:109)<br>`cp_karim_dispatch_building` (mod/common/scripted_effects/cp_karim_memory.txt:157) | `mod/events/cp_karim_events.txt:94` |
| `cp_karim.30` | karim | The Broken Finger | ambient, button, world_response | `cp_karim_dispatch_yearly` (mod/common/scripted_effects/cp_karim_memory.txt:73)<br>`cp_roll_ambient_karim` (mod/common/scripted_effects/cp_karim_memory.txt:254)<br>`cp_shared_action_karim` (mod/common/scripted_effects/cp_shared_action_buttons.txt:150) | `mod/events/cp_karim_events.txt:130` |
| `cp_karim.40` | karim | The New Engine | world_response | `cp_karim_dispatch_tech` (mod/common/scripted_effects/cp_karim_memory.txt:120) | `mod/events/cp_karim_events.txt:166` |
| `cp_karim.50` | karim | The Steel Color | world_response | `cp_karim_dispatch_building` (mod/common/scripted_effects/cp_karim_memory.txt:172) | `mod/events/cp_karim_events.txt:202` |
| `cp_karim.60` | karim | The Night Gauge | ambient, button, world_response=2 | `cp_karim_dispatch_yearly` (mod/common/scripted_effects/cp_karim_memory.txt:84)<br>`cp_karim_dispatch_building` (mod/common/scripted_effects/cp_karim_memory.txt:190)<br>`cp_roll_ambient_karim` (mod/common/scripted_effects/cp_karim_memory.txt:261) | `mod/events/cp_karim_events.txt:239` |
| `cp_layla.1` | layla | The Farmer's Daughter | first_contact | `cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_layla_events.txt:28` |
| `cp_layla.10` | layla | The Letter That Has Not Come | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:1997)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:11) | `mod/events/cp_layla_events.txt:310` |
| `cp_layla.100` | layla | A School in the Next Village | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:500) | `mod/events/cp_layla_events.txt:2270` |
| `cp_layla.101` | layla | They Will Be Taken to the School | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:561) | `mod/events/cp_layla_events.txt:2331` |
| `cp_layla.102` | layla | The Daughter Reads | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2029)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:28) | `mod/events/cp_layla_events.txt:2408` |
| `cp_layla.103` | layla | The Chains Are Cut | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:574) | `mod/events/cp_layla_events.txt:2453` |
| `cp_layla.104` | layla | The Compound on the Edge of the Village | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2032)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:29) | `mod/events/cp_layla_events.txt:2510` |
| `cp_layla.105` | layla | Every Man, They Say | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:584) | `mod/events/cp_layla_events.txt:3017` |
| `cp_layla.106` | layla | The Poster on the Wall | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:592) | `mod/events/cp_layla_events.txt:3079` |
| `cp_layla.107` | layla | The Coptic Neighbour Exhales | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:602) | `mod/events/cp_layla_events.txt:3129` |
| `cp_layla.108` | layla | The Doctor at the Mosque | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:612) | `mod/events/cp_layla_events.txt:3186` |
| `cp_layla.109` | layla | The Man with the Bag | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:620) | `mod/events/cp_layla_events.txt:3228` |
| `cp_layla.11` | layla | Walking the Field She Owns | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2001)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:12) | `mod/events/cp_layla_events.txt:344` |
| `cp_layla.110` | layla | The Doctor in the Next Village | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:523) | `mod/events/cp_layla_events.txt:3281` |
| `cp_layla.111` | layla | The Guard Has Been Installed | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:630) | `mod/events/cp_layla_events.txt:3325` |
| `cp_layla.112` | layla | The Meeting After Shift | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:640) | `mod/events/cp_layla_events.txt:3369` |
| `cp_layla.113` | layla | The Strike | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2047)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:38) | `mod/events/cp_layla_events.txt:3417` |
| `cp_layla.114` | layla | The Minaret's Silence | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:653) | `mod/events/cp_layla_events.txt:3550` |
| `cp_layla.115` | layla | The Procession Passes | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:661) | `mod/events/cp_layla_events.txt:3601` |
| `cp_layla.116` | layla | The Square Fills and Does Not Empty | law_reaction=2 | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:675)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:225) | `mod/events/cp_layla_events.txt:3649` |
| `cp_layla.117` | layla | The Letter That Should Not Have Been Written | law_reaction=2 | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:685)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:243) | `mod/events/cp_layla_events.txt:3850` |
| `cp_layla.118` | layla | The Children Leave the Floor | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:697) | `mod/events/cp_layla_events.txt:3700` |
| `cp_layla.119` | layla | The Station in the Lane | law_reaction=2 | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:710)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:261) | `mod/events/cp_layla_events.txt:3754` |
| `cp_layla.12` | layla | Under the Bey's Eye | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2005)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:13) | `mod/events/cp_layla_events.txt:378` |
| `cp_layla.120` | layla | Rifles in the Square | law_reaction=2 | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:720)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:279) | `mod/events/cp_layla_events.txt:3802` |
| `cp_layla.121` | layla | Strangers in the Lane | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:731) | `mod/events/cp_layla_events.txt:3909` |
| `cp_layla.122` | layla | The Gate Closes | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:739) | `mod/events/cp_layla_events.txt:3957` |
| `cp_layla.123` | layla | The Market Eats the Village | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:751) | `mod/events/cp_layla_events.txt:4005` |
| `cp_layla.124` | layla | The Ministry Comes for the Stall | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:759) | `mod/events/cp_layla_events.txt:4058` |
| `cp_layla.125` | layla | The District Office | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:485) | `mod/events/cp_layla_events.txt:4172` |
| `cp_layla.126` | layla | The Imam's Visit | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2050)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:39) | `mod/events/cp_layla_events.txt:4232` |
| `cp_layla.127` | layla | The Small Victory | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2051)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:40) | `mod/events/cp_layla_events.txt:4288` |
| `cp_layla.128` | layla | Mariam Writes from Cairo | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2052)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:41) | `mod/events/cp_layla_events.txt:4349` |
| `cp_layla.13` | layla | A Day With No Wind | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2009)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:14) | `mod/events/cp_layla_events.txt:412` |
| `cp_layla.14` | layla | The Neighbour's Boy in the Lane | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2010)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:15) | `mod/events/cp_layla_events.txt:446` |
| `cp_layla.15` | layla | Her Mother's Left Hand | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2011)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:16) | `mod/events/cp_layla_events.txt:480` |
| `cp_layla.16` | layla | The Hen That Will Not Lay | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2012)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:17) | `mod/events/cp_layla_events.txt:524` |
| `cp_layla.17` | layla | The Merchant's Scale | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2013)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:18) | `mod/events/cp_layla_events.txt:558` |
| `cp_layla.18` | layla | Friday, the River Low | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2014)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:19) | `mod/events/cp_layla_events.txt:592` |
| `cp_layla.19` | layla | The Old Woman Who Sees Through Walls | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2015)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:20) | `mod/events/cp_layla_events.txt:626` |
| `cp_layla.2` | layla | The Deed | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:392) | `mod/events/cp_layla_events.txt:66` |
| `cp_layla.20` | layla | The Bread That Did Not Rise | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2016)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:21) | `mod/events/cp_layla_events.txt:660` |
| `cp_layla.21` | layla | Dust on the Water | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2017)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:22) | `mod/events/cp_layla_events.txt:694` |
| `cp_layla.22` | layla | The Younger Brother's Letter | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2018)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:23) | `mod/events/cp_layla_events.txt:728` |
| `cp_layla.23` | layla | The Mule That Will Not Move | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2019)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:24) | `mod/events/cp_layla_events.txt:762` |
| `cp_layla.24` | layla | Election Day | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2022)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:25) | `mod/events/cp_layla_events.txt:2197` |
| `cp_layla.25` | layla | The First Day of Ramadan | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2035)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:30) | `mod/events/cp_layla_events.txt:2581` |
| `cp_layla.26` | layla | The Nile Rises | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2036)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:31) | `mod/events/cp_layla_events.txt:2618` |
| `cp_layla.27` | layla | The Hajj Returnees | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2037)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:32) | `mod/events/cp_layla_events.txt:2672` |
| `cp_layla.28` | layla | The Midwife's Lamp | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2038)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:33) | `mod/events/cp_layla_events.txt:2710` |
| `cp_layla.29` | layla | The Date Harvest | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2039)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:34) | `mod/events/cp_layla_events.txt:2746` |
| `cp_layla.3` | layla | The Bey Returns | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:426) | `mod/events/cp_layla_events.txt:101` |
| `cp_layla.30` | layla | The Iron Horse | world_response | `cp_layla_dispatch_tech` (mod/common/scripted_effects/cp_layla_memory.txt:835) | `mod/events/cp_layla_events.txt:805` |
| `cp_layla.31` | layla | A Word From Beyond | world_response | `cp_layla_dispatch_tech` (mod/common/scripted_effects/cp_layla_memory.txt:843) | `mod/events/cp_layla_events.txt:843` |
| `cp_layla.32` | layla | Voices in the Air | world_response | `cp_layla_dispatch_tech` (mod/common/scripted_effects/cp_layla_memory.txt:851) | `mod/events/cp_layla_events.txt:881` |
| `cp_layla.33` | layla | The Cup of Coffee | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2042)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:35) | `mod/events/cp_layla_events.txt:2792` |
| `cp_layla.34` | layla | The White Sugar | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2043)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:36) | `mod/events/cp_layla_events.txt:2833` |
| `cp_layla.35` | layla | The Cloth from the Port | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2044)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:37) | `mod/events/cp_layla_events.txt:2873` |
| `cp_layla.4` | layla | He Marches | milestone | `cp_layla_dispatch_war_started` (mod/common/scripted_effects/cp_layla_memory.txt:779) | `mod/events/cp_layla_events.txt:135` |
| `cp_layla.40` | layla | The Column Returns | milestone=3 | `cp_layla_dispatch_war_end` (mod/common/scripted_effects/cp_layla_memory.txt:801)<br>`cp_layla_dispatch_war_end` (mod/common/scripted_effects/cp_layla_memory.txt:808)<br>`cp_layla_dispatch_war_end` (mod/common/scripted_effects/cp_layla_memory.txt:816) | `mod/events/cp_layla_events.txt:929` |
| `cp_layla.41` | layla | The Clerk's Letter | milestone=3 | `cp_layla_dispatch_war_end` (mod/common/scripted_effects/cp_layla_memory.txt:802)<br>`cp_layla_dispatch_war_end` (mod/common/scripted_effects/cp_layla_memory.txt:809)<br>`cp_layla_dispatch_war_end` (mod/common/scripted_effects/cp_layla_memory.txt:817) | `mod/events/cp_layla_events.txt:966` |
| `cp_layla.5` | layla | The First Cry | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:186) | `mod/events/cp_layla_events.txt:265` |
| `cp_layla.50` | layla | The Smoke Above the Palm | world_response | `cp_layla_dispatch_building` (mod/common/scripted_effects/cp_layla_memory.txt:875) | `mod/events/cp_layla_events.txt:1009` |
| `cp_layla.60` | layla | The Shutters Close | milestone | `cp_layla_dispatch_revolution` (mod/common/scripted_effects/cp_layla_memory.txt:892) | `mod/events/cp_layla_events.txt:1056` |
| `cp_layla.7` | layla | The Tax Collector | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:156) | `mod/events/cp_layla_events.txt:173` |
| `cp_layla.70` | layla | Cairo Is Calling | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:207) | `mod/events/cp_layla_events.txt:1523` |
| `cp_layla.71` | layla | The Small Concern | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:361) | `mod/events/cp_layla_events.txt:1431` |
| `cp_layla.72` | layla | The Suitor | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:438) | `mod/events/cp_layla_events.txt:2922` |
| `cp_layla.73` | layla | The Mill Closes | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:461) | `mod/events/cp_layla_events.txt:3477` |
| `cp_layla.8` | layla | The Price of the Loaf | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:166) | `mod/events/cp_layla_events.txt:221` |
| `cp_layla.80` | layla | The Last Morning | milestone=3 | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:273)<br>`cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:280)<br>`cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:286) | `mod/events/cp_layla_events.txt:1115` |
| `cp_layla.81` | layla | The Foreman's Runner | milestone=2 | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:306)<br>`cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:312) | `mod/events/cp_layla_events.txt:1159` |
| `cp_layla.82` | layla | The Child | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:329) | `mod/events/cp_layla_events.txt:1395` |
| `cp_layla.83` | layla | The Forty Days | visible_chain | `cp_layla.80` (mod/events/cp_layla_events.txt:1115) | `mod/events/cp_layla_events.txt:4129` |
| `cp_layla.90` | layla | The First Envelope | milestone | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:252) | `mod/events/cp_layla_events.txt:1200` |
| `cp_layla.91` | layla | The New Law | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:518) | `mod/events/cp_layla_events.txt:1271` |
| `cp_layla.92` | layla | They Have Taken It Back | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:523) | `mod/events/cp_layla_events.txt:1336` |
| `cp_layla.93` | layla | The Law Catches Up to Us | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:537) | `mod/events/cp_layla_events.txt:1600` |
| `cp_layla.94` | layla | A Paper with My Name | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:474) | `mod/events/cp_layla_events.txt:1672` |
| `cp_layla.95` | layla | They Are Hiring Women Now | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:545) | `mod/events/cp_layla_events.txt:1748` |
| `cp_layla.96` | layla | I Am on the Rolls | law_reaction | `cp_layla_dispatch_law_enacted` (mod/common/scripted_effects/cp_layla_memory.txt:553) | `mod/events/cp_layla_events.txt:1822` |
| `cp_layla.97` | layla | Her Own Stall | milestone=2 | `cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:400)<br>`cp_layla_dispatch_yearly` (mod/common/scripted_effects/cp_layla_memory.txt:419) | `mod/events/cp_layla_events.txt:1910` |
| `cp_layla.98` | layla | The Month Without | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2025)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:26) | `mod/events/cp_layla_events.txt:2040` |
| `cp_layla.99` | layla | Her Name Is Not on the Deed | ambient, button | `cp_roll_ambient_layla` (mod/common/scripted_effects/cp_layla_memory.txt:2026)<br>`cp_shared_action_layla` (mod/common/scripted_effects/cp_shared_action_buttons.txt:27) | `mod/events/cp_layla_events.txt:2115` |
| `cp_layla_vox.101` | layla | The Room She Has Built | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:3769` |
| `cp_layla_vox.1011` | layla | The Carpet's End | visible_chain | `cp_layla_vox.101` (mod/events/cp_layla_vox_events.txt:3769) | `mod/events/cp_layla_vox_events.txt:3821` |
| `cp_layla_vox.1012` | layla | She Walks | visible_chain | `cp_layla_vox.101` (mod/events/cp_layla_vox_events.txt:3769) | `mod/events/cp_layla_vox_events.txt:3839` |
| `cp_layla_vox.1013` | layla | Her Name | visible_chain | `cp_layla_vox.101` (mod/events/cp_layla_vox_events.txt:3769) | `mod/events/cp_layla_vox_events.txt:3857` |
| `cp_layla_vox.102` | layla | The Land | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:3876` |
| `cp_layla_vox.1021` | layla | He Does Not Look Up | visible_chain | `cp_layla_vox.102` (mod/events/cp_layla_vox_events.txt:3876) | `mod/events/cp_layla_vox_events.txt:3917` |
| `cp_layla_vox.1022` | layla | He Is Listening | visible_chain | `cp_layla_vox.102` (mod/events/cp_layla_vox_events.txt:3876) | `mod/events/cp_layla_vox_events.txt:3936` |
| `cp_layla_vox.1023` | layla | He Is Cruel | visible_chain | `cp_layla_vox.102` (mod/events/cp_layla_vox_events.txt:3876) | `mod/events/cp_layla_vox_events.txt:3955` |
| `cp_layla_vox.103` | layla | She Has Come with the Paper | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:3975` |
| `cp_layla_vox.1031` | layla | Only Thanks | visible_chain | `cp_layla_vox.103` (mod/events/cp_layla_vox_events.txt:3975) | `mod/events/cp_layla_vox_events.txt:3996` |
| `cp_layla_vox.1032` | layla | The Water | visible_chain | `cp_layla_vox.103` (mod/events/cp_layla_vox_events.txt:3975) | `mod/events/cp_layla_vox_events.txt:4014` |
| `cp_layla_vox.1033` | layla | Withdraw | visible_chain | `cp_layla_vox.103` (mod/events/cp_layla_vox_events.txt:3975) | `mod/events/cp_layla_vox_events.txt:4032` |
| `cp_layla_vox.104` | layla | The War | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:4051` |
| `cp_layla_vox.1041` | layla | She Does Not Wait for an Answer | visible_chain | `cp_layla_vox.104` (mod/events/cp_layla_vox_events.txt:4051) | `mod/events/cp_layla_vox_events.txt:4072` |
| `cp_layla_vox.1042` | layla | The Smaller Thing | visible_chain | `cp_layla_vox.104` (mod/events/cp_layla_vox_events.txt:4051) | `mod/events/cp_layla_vox_events.txt:4090` |
| `cp_layla_vox.1043` | layla | Why Does This War Need Him | visible_chain | `cp_layla_vox.104` (mod/events/cp_layla_vox_events.txt:4051) | `mod/events/cp_layla_vox_events.txt:4108` |
| `cp_layla_vox.105` | layla | The Vote She Is Given | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:4127` |
| `cp_layla_vox.1051` | layla | She Will Take It | visible_chain | `cp_layla_vox.105` (mod/events/cp_layla_vox_events.txt:4127) | `mod/events/cp_layla_vox_events.txt:4148` |
| `cp_layla_vox.1052` | layla | She Refuses | visible_chain | `cp_layla_vox.105` (mod/events/cp_layla_vox_events.txt:4127) | `mod/events/cp_layla_vox_events.txt:4166` |
| `cp_layla_vox.1053` | layla | An Honest Number | visible_chain | `cp_layla_vox.105` (mod/events/cp_layla_vox_events.txt:4127) | `mod/events/cp_layla_vox_events.txt:4184` |
| `cp_layla_vox.106` | layla | The Old Ruler, Remembered | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:4203` |
| `cp_layla_vox.1061` | layla | Bitterly | visible_chain | `cp_layla_vox.106` (mod/events/cp_layla_vox_events.txt:4203) | `mod/events/cp_layla_vox_events.txt:4224` |
| `cp_layla_vox.1062` | layla | Hopefully | visible_chain | `cp_layla_vox.106` (mod/events/cp_layla_vox_events.txt:4203) | `mod/events/cp_layla_vox_events.txt:4242` |
| `cp_layla_vox.1063` | layla | Tired | visible_chain | `cp_layla_vox.106` (mod/events/cp_layla_vox_events.txt:4203) | `mod/events/cp_layla_vox_events.txt:4260` |
| `cp_layla_vox.109` | layla | The Room Is Empty Tonight | hidden_person_router | `cp_layla_vox.100` (mod/events/cp_layla_vox_events.txt:3711) | `mod/events/cp_layla_vox_events.txt:4279` |
| `cp_layla_vox.11` | layla | The Letter That Has Not Come | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:115` |
| `cp_layla_vox.1101` | layla | The Silence That Is Prayer | visible_chain | `cp_layla_vox.11` (mod/events/cp_layla_vox_events.txt:115) | `mod/events/cp_layla_vox_events.txt:150` |
| `cp_layla_vox.1102` | layla | Um Hassan Has Had No Letter Either | visible_chain | `cp_layla_vox.11` (mod/events/cp_layla_vox_events.txt:115) | `mod/events/cp_layla_vox_events.txt:173` |
| `cp_layla_vox.1103` | layla | A Letter in the Head | visible_chain | `cp_layla_vox.11` (mod/events/cp_layla_vox_events.txt:115) | `mod/events/cp_layla_vox_events.txt:195` |
| `cp_layla_vox.12` | layla | The First Year | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:223` |
| `cp_layla_vox.1201` | layla | The Second Too Long | visible_chain | `cp_layla_vox.12` (mod/events/cp_layla_vox_events.txt:223) | `mod/events/cp_layla_vox_events.txt:258` |
| `cp_layla_vox.1202` | layla | The Way He Said Layla | visible_chain | `cp_layla_vox.12` (mod/events/cp_layla_vox_events.txt:223) | `mod/events/cp_layla_vox_events.txt:281` |
| `cp_layla_vox.1203` | layla | The Bread Burned a Second Time | visible_chain | `cp_layla_vox.12` (mod/events/cp_layla_vox_events.txt:223) | `mod/events/cp_layla_vox_events.txt:303` |
| `cp_layla_vox.13` | layla | Salt on His Neck | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:330` |
| `cp_layla_vox.1301` | layla | The Step, Shared | visible_chain | `cp_layla_vox.13` (mod/events/cp_layla_vox_events.txt:330) | `mod/events/cp_layla_vox_events.txt:365` |
| `cp_layla_vox.1302` | layla | How Much, How Good | visible_chain | `cp_layla_vox.13` (mod/events/cp_layla_vox_events.txt:330) | `mod/events/cp_layla_vox_events.txt:387` |
| `cp_layla_vox.1303` | layla | The Bread, Brought Out | visible_chain | `cp_layla_vox.13` (mod/events/cp_layla_vox_events.txt:330) | `mod/events/cp_layla_vox_events.txt:409` |
| `cp_layla_vox.14` | layla | Oil on His Shirt | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:436` |
| `cp_layla_vox.1401` | layla | The Child at the Gate | visible_chain | `cp_layla_vox.14` (mod/events/cp_layla_vox_events.txt:436) | `mod/events/cp_layla_vox_events.txt:471` |
| `cp_layla_vox.1402` | layla | The Coat on the Peg | visible_chain | `cp_layla_vox.14` (mod/events/cp_layla_vox_events.txt:436) | `mod/events/cp_layla_vox_events.txt:493` |
| `cp_layla_vox.1403` | layla | The Tin, Beside the Plate | visible_chain | `cp_layla_vox.14` (mod/events/cp_layla_vox_events.txt:436) | `mod/events/cp_layla_vox_events.txt:515` |
| `cp_layla_vox.15` | layla | The Room, Dark | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:542` |
| `cp_layla_vox.1501` | layla | Her Hand, Behind Her | visible_chain | `cp_layla_vox.15` (mod/events/cp_layla_vox_events.txt:542) | `mod/events/cp_layla_vox_events.txt:577` |
| `cp_layla_vox.1502` | layla | The Slow Falling | visible_chain | `cp_layla_vox.15` (mod/events/cp_layla_vox_events.txt:542) | `mod/events/cp_layla_vox_events.txt:599` |
| `cp_layla_vox.1503` | layla | The Door, Ajar | visible_chain | `cp_layla_vox.15` (mod/events/cp_layla_vox_events.txt:542) | `mod/events/cp_layla_vox_events.txt:621` |
| `cp_layla_vox.16` | layla | His Knees on the Mat | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:648` |
| `cp_layla_vox.1601` | layla | The Cup, as Always | visible_chain | `cp_layla_vox.16` (mod/events/cp_layla_vox_events.txt:648) | `mod/events/cp_layla_vox_events.txt:683` |
| `cp_layla_vox.1602` | layla | Her Grandfather's Knees | visible_chain | `cp_layla_vox.16` (mod/events/cp_layla_vox_events.txt:648) | `mod/events/cp_layla_vox_events.txt:705` |
| `cp_layla_vox.1603` | layla | Stillness Beside Him | visible_chain | `cp_layla_vox.16` (mod/events/cp_layla_vox_events.txt:648) | `mod/events/cp_layla_vox_events.txt:727` |
| `cp_layla_vox.19` | layla | Tonight He Is Only Ahmed | hidden_person_router | `cp_layla_vox.10` (mod/events/cp_layla_vox_events.txt:47) | `mod/events/cp_layla_vox_events.txt:754` |
| `cp_layla_vox.21` | layla | Why Does the Bey Come | hidden_person_router | `cp_layla_vox.20` (mod/events/cp_layla_vox_events.txt:785) | `mod/events/cp_layla_vox_events.txt:830` |
| `cp_layla_vox.2101` | layla | The Field Is Ours | visible_chain | `cp_layla_vox.21` (mod/events/cp_layla_vox_events.txt:830) | `mod/events/cp_layla_vox_events.txt:851` |
| `cp_layla_vox.2102` | layla | Do Not Ask | visible_chain | `cp_layla_vox.21` (mod/events/cp_layla_vox_events.txt:830) | `mod/events/cp_layla_vox_events.txt:873` |
| `cp_layla_vox.2103` | layla | The Heron and the Fisherman | visible_chain | `cp_layla_vox.21` (mod/events/cp_layla_vox_events.txt:830) | `mod/events/cp_layla_vox_events.txt:895` |
| `cp_layla_vox.22` | layla | The First Loaf | hidden_person_router | `cp_layla_vox.20` (mod/events/cp_layla_vox_events.txt:785) | `mod/events/cp_layla_vox_events.txt:918` |
| `cp_layla_vox.2201` | layla | It Is Becoming Bread | visible_chain | `cp_layla_vox.22` (mod/events/cp_layla_vox_events.txt:918) | `mod/events/cp_layla_vox_events.txt:939` |
| `cp_layla_vox.2202` | layla | Again | visible_chain | `cp_layla_vox.22` (mod/events/cp_layla_vox_events.txt:918) | `mod/events/cp_layla_vox_events.txt:962` |
| `cp_layla_vox.2203` | layla | Add Water to Her Own | visible_chain | `cp_layla_vox.22` (mod/events/cp_layla_vox_events.txt:918) | `mod/events/cp_layla_vox_events.txt:984` |
| `cp_layla_vox.23` | layla | She Reads to Me | hidden_person_router | `cp_layla_vox.20` (mod/events/cp_layla_vox_events.txt:785) | `mod/events/cp_layla_vox_events.txt:1007` |
| `cp_layla_vox.2301` | layla | The Nodding | visible_chain | `cp_layla_vox.23` (mod/events/cp_layla_vox_events.txt:1007) | `mod/events/cp_layla_vox_events.txt:1028` |
| `cp_layla_vox.2302` | layla | Again, Slowly | visible_chain | `cp_layla_vox.23` (mod/events/cp_layla_vox_events.txt:1007) | `mod/events/cp_layla_vox_events.txt:1050` |
| `cp_layla_vox.2303` | layla | I Am Proud | visible_chain | `cp_layla_vox.23` (mod/events/cp_layla_vox_events.txt:1007) | `mod/events/cp_layla_vox_events.txt:1072` |
| `cp_layla_vox.24` | layla | The Bag at the Door | hidden_person_router | `cp_layla_vox.20` (mod/events/cp_layla_vox_events.txt:785) | `mod/events/cp_layla_vox_events.txt:1096` |
| `cp_layla_vox.2401` | layla | Let Her Go | visible_chain | `cp_layla_vox.24` (mod/events/cp_layla_vox_events.txt:1096) | `mod/events/cp_layla_vox_events.txt:1117` |
| `cp_layla_vox.2402` | layla | One More Night | visible_chain | `cp_layla_vox.24` (mod/events/cp_layla_vox_events.txt:1096) | `mod/events/cp_layla_vox_events.txt:1140` |
| `cp_layla_vox.2403` | layla | The Mother's Shawl | visible_chain | `cp_layla_vox.24` (mod/events/cp_layla_vox_events.txt:1096) | `mod/events/cp_layla_vox_events.txt:1162` |
| `cp_layla_vox.25` | layla | She Does Not Want the Match | hidden_person_router | `cp_layla_vox.20` (mod/events/cp_layla_vox_events.txt:785) | `mod/events/cp_layla_vox_events.txt:1185` |
| `cp_layla_vox.2501` | layla | A Good Boy Is a Good Boy | visible_chain | `cp_layla_vox.25` (mod/events/cp_layla_vox_events.txt:1185) | `mod/events/cp_layla_vox_events.txt:1206` |
| `cp_layla_vox.2502` | layla | Not in Front of the Child | visible_chain | `cp_layla_vox.25` (mod/events/cp_layla_vox_events.txt:1185) | `mod/events/cp_layla_vox_events.txt:1229` |
| `cp_layla_vox.2503` | layla | Quietly | visible_chain | `cp_layla_vox.25` (mod/events/cp_layla_vox_events.txt:1185) | `mod/events/cp_layla_vox_events.txt:1251` |
| `cp_layla_vox.29` | layla | The Child Asleep | hidden_person_router | `cp_layla_vox.20` (mod/events/cp_layla_vox_events.txt:785) | `mod/events/cp_layla_vox_events.txt:1274` |
| `cp_layla_vox.31` | layla | The Rhythm of Her Mother's Hands | hidden_person_router | `cp_layla_vox.30` (mod/events/cp_layla_vox_events.txt:1302) | `mod/events/cp_layla_vox_events.txt:1347` |
| `cp_layla_vox.3101` | layla | The Small Grief | visible_chain | `cp_layla_vox.31` (mod/events/cp_layla_vox_events.txt:1347) | `mod/events/cp_layla_vox_events.txt:1368` |
| `cp_layla_vox.3102` | layla | Her Mother's Words | visible_chain | `cp_layla_vox.31` (mod/events/cp_layla_vox_events.txt:1347) | `mod/events/cp_layla_vox_events.txt:1390` |
| `cp_layla_vox.3103` | layla | The Attempt to Change | visible_chain | `cp_layla_vox.31` (mod/events/cp_layla_vox_events.txt:1347) | `mod/events/cp_layla_vox_events.txt:1412` |
| `cp_layla_vox.32` | layla | A Dream | hidden_person_router | `cp_layla_vox.30` (mod/events/cp_layla_vox_events.txt:1302) | `mod/events/cp_layla_vox_events.txt:1435` |
| `cp_layla_vox.3201` | layla | She Does Not Chase | visible_chain | `cp_layla_vox.32` (mod/events/cp_layla_vox_events.txt:1435) | `mod/events/cp_layla_vox_events.txt:1456` |
| `cp_layla_vox.3202` | layla | Trying to Go Back | visible_chain | `cp_layla_vox.32` (mod/events/cp_layla_vox_events.txt:1435) | `mod/events/cp_layla_vox_events.txt:1474` |
| `cp_layla_vox.3203` | layla | She Walks Past | visible_chain | `cp_layla_vox.32` (mod/events/cp_layla_vox_events.txt:1435) | `mod/events/cp_layla_vox_events.txt:1492` |
| `cp_layla_vox.33` | layla | The Stone at the Edge | hidden_person_router | `cp_layla_vox.30` (mod/events/cp_layla_vox_events.txt:1302) | `mod/events/cp_layla_vox_events.txt:1511` |
| `cp_layla_vox.3301` | layla | The Small Stone | visible_chain | `cp_layla_vox.33` (mod/events/cp_layla_vox_events.txt:1511) | `mod/events/cp_layla_vox_events.txt:1532` |
| `cp_layla_vox.3302` | layla | She Says Nothing | visible_chain | `cp_layla_vox.33` (mod/events/cp_layla_vox_events.txt:1511) | `mod/events/cp_layla_vox_events.txt:1550` |
| `cp_layla_vox.3303` | layla | The Short Fatiha | visible_chain | `cp_layla_vox.33` (mod/events/cp_layla_vox_events.txt:1511) | `mod/events/cp_layla_vox_events.txt:1568` |
| `cp_layla_vox.34` | layla | What Her Mother Would Say | hidden_person_router | `cp_layla_vox.30` (mod/events/cp_layla_vox_events.txt:1302) | `mod/events/cp_layla_vox_events.txt:1587` |
| `cp_layla_vox.3401` | layla | The Way of the World | visible_chain | `cp_layla_vox.34` (mod/events/cp_layla_vox_events.txt:1587) | `mod/events/cp_layla_vox_events.txt:1608` |
| `cp_layla_vox.3402` | layla | They Will Take More | visible_chain | `cp_layla_vox.34` (mod/events/cp_layla_vox_events.txt:1587) | `mod/events/cp_layla_vox_events.txt:1626` |
| `cp_layla_vox.3403` | layla | The Long Look | visible_chain | `cp_layla_vox.34` (mod/events/cp_layla_vox_events.txt:1587) | `mod/events/cp_layla_vox_events.txt:1644` |
| `cp_layla_vox.35` | layla | The One We Lost | hidden_person_router | `cp_layla_vox.30` (mod/events/cp_layla_vox_events.txt:1302) | `mod/events/cp_layla_vox_events.txt:1666` |
| `cp_layla_vox.3501` | layla | The Comforting Sentence | visible_chain | `cp_layla_vox.35` (mod/events/cp_layla_vox_events.txt:1666) | `mod/events/cp_layla_vox_events.txt:1687` |
| `cp_layla_vox.3502` | layla | The Silence | visible_chain | `cp_layla_vox.35` (mod/events/cp_layla_vox_events.txt:1666) | `mod/events/cp_layla_vox_events.txt:1706` |
| `cp_layla_vox.3503` | layla | Her Mother's Own | visible_chain | `cp_layla_vox.35` (mod/events/cp_layla_vox_events.txt:1666) | `mod/events/cp_layla_vox_events.txt:1725` |
| `cp_layla_vox.39` | layla | A Rhythm She Cannot Place | hidden_person_router | `cp_layla_vox.30` (mod/events/cp_layla_vox_events.txt:1302) | `mod/events/cp_layla_vox_events.txt:1745` |
| `cp_layla_vox.41` | layla | Over the Wall | hidden_person_router | `cp_layla_vox.40` (mod/events/cp_layla_vox_events.txt:1770) | `mod/events/cp_layla_vox_events.txt:1797` |
| `cp_layla_vox.4101` | layla | Small Gossip | visible_chain | `cp_layla_vox.41` (mod/events/cp_layla_vox_events.txt:1797) | `mod/events/cp_layla_vox_events.txt:1818` |
| `cp_layla_vox.4102` | layla | The Silence at the Wall | visible_chain | `cp_layla_vox.41` (mod/events/cp_layla_vox_events.txt:1797) | `mod/events/cp_layla_vox_events.txt:1836` |
| `cp_layla_vox.4103` | layla | Three Eggs in Cloth | visible_chain | `cp_layla_vox.41` (mod/events/cp_layla_vox_events.txt:1797) | `mod/events/cp_layla_vox_events.txt:1854` |
| `cp_layla_vox.42` | layla | The Priest's Son | hidden_person_router | `cp_layla_vox.40` (mod/events/cp_layla_vox_events.txt:1770) | `mod/events/cp_layla_vox_events.txt:1873` |
| `cp_layla_vox.4201` | layla | Sympathy, Plain | visible_chain | `cp_layla_vox.42` (mod/events/cp_layla_vox_events.txt:1873) | `mod/events/cp_layla_vox_events.txt:1894` |
| `cp_layla_vox.4202` | layla | They Are Young, They Burn | visible_chain | `cp_layla_vox.42` (mod/events/cp_layla_vox_events.txt:1873) | `mod/events/cp_layla_vox_events.txt:1912` |
| `cp_layla_vox.4203` | layla | Change the Subject | visible_chain | `cp_layla_vox.42` (mod/events/cp_layla_vox_events.txt:1873) | `mod/events/cp_layla_vox_events.txt:1930` |
| `cp_layla_vox.43` | layla | Her Feast, Not Yours | hidden_person_router | `cp_layla_vox.40` (mod/events/cp_layla_vox_events.txt:1770) | `mod/events/cp_layla_vox_events.txt:1949` |
| `cp_layla_vox.4301` | layla | The Bowl of Honey | visible_chain | `cp_layla_vox.43` (mod/events/cp_layla_vox_events.txt:1949) | `mod/events/cp_layla_vox_events.txt:1970` |
| `cp_layla_vox.4302` | layla | She Stays on Her Side | visible_chain | `cp_layla_vox.43` (mod/events/cp_layla_vox_events.txt:1949) | `mod/events/cp_layla_vox_events.txt:1988` |
| `cp_layla_vox.4303` | layla | What Are You Baking | visible_chain | `cp_layla_vox.43` (mod/events/cp_layla_vox_events.txt:1949) | `mod/events/cp_layla_vox_events.txt:2006` |
| `cp_layla_vox.44` | layla | The House Is Dark at Midday | hidden_person_router | `cp_layla_vox.40` (mod/events/cp_layla_vox_events.txt:1770) | `mod/events/cp_layla_vox_events.txt:2025` |
| `cp_layla_vox.4401` | layla | Sitting, Nothing More | visible_chain | `cp_layla_vox.44` (mod/events/cp_layla_vox_events.txt:2025) | `mod/events/cp_layla_vox_events.txt:2046` |
| `cp_layla_vox.4402` | layla | The Daughter with the Dish | visible_chain | `cp_layla_vox.44` (mod/events/cp_layla_vox_events.txt:2025) | `mod/events/cp_layla_vox_events.txt:2064` |
| `cp_layla_vox.4403` | layla | Wait Until Tomorrow | visible_chain | `cp_layla_vox.44` (mod/events/cp_layla_vox_events.txt:2025) | `mod/events/cp_layla_vox_events.txt:2082` |
| `cp_layla_vox.49` | layla | The Wall, Quiet Today | hidden_person_router | `cp_layla_vox.40` (mod/events/cp_layla_vox_events.txt:1770) | `mod/events/cp_layla_vox_events.txt:2101` |
| `cp_layla_vox.51` | layla | She Is at the Edge of the Field | hidden_person_router | `cp_layla_vox.50` (mod/events/cp_layla_vox_events.txt:2128) | `mod/events/cp_layla_vox_events.txt:2155` |
| `cp_layla_vox.5101` | layla | Pay Her More | visible_chain | `cp_layla_vox.51` (mod/events/cp_layla_vox_events.txt:2155) | `mod/events/cp_layla_vox_events.txt:2176` |
| `cp_layla_vox.5102` | layla | The Share, Exact | visible_chain | `cp_layla_vox.51` (mod/events/cp_layla_vox_events.txt:2155) | `mod/events/cp_layla_vox_events.txt:2194` |
| `cp_layla_vox.5103` | layla | A Small Accident | visible_chain | `cp_layla_vox.51` (mod/events/cp_layla_vox_events.txt:2155) | `mod/events/cp_layla_vox_events.txt:2212` |
| `cp_layla_vox.52` | layla | She Asks About the Paper | hidden_person_router | `cp_layla_vox.50` (mod/events/cp_layla_vox_events.txt:2128) | `mod/events/cp_layla_vox_events.txt:2231` |
| `cp_layla_vox.5201` | layla | Plain Speech | visible_chain | `cp_layla_vox.52` (mod/events/cp_layla_vox_events.txt:2231) | `mod/events/cp_layla_vox_events.txt:2252` |
| `cp_layla_vox.5202` | layla | Deflection | visible_chain | `cp_layla_vox.52` (mod/events/cp_layla_vox_events.txt:2231) | `mod/events/cp_layla_vox_events.txt:2270` |
| `cp_layla_vox.5203` | layla | A Small Lie | visible_chain | `cp_layla_vox.52` (mod/events/cp_layla_vox_events.txt:2231) | `mod/events/cp_layla_vox_events.txt:2288` |
| `cp_layla_vox.53` | layla | Two Boys in the Lane | hidden_person_router | `cp_layla_vox.50` (mod/events/cp_layla_vox_events.txt:2128) | `mod/events/cp_layla_vox_events.txt:2307` |
| `cp_layla_vox.5301` | layla | The Shirt, Casual | visible_chain | `cp_layla_vox.53` (mod/events/cp_layla_vox_events.txt:2307) | `mod/events/cp_layla_vox_events.txt:2328` |
| `cp_layla_vox.5302` | layla | In the Chest It Stays | visible_chain | `cp_layla_vox.53` (mod/events/cp_layla_vox_events.txt:2307) | `mod/events/cp_layla_vox_events.txt:2346` |
| `cp_layla_vox.5303` | layla | Both Boys for Bread | visible_chain | `cp_layla_vox.53` (mod/events/cp_layla_vox_events.txt:2307) | `mod/events/cp_layla_vox_events.txt:2364` |
| `cp_layla_vox.54` | layla | She Has Refused the Jar | hidden_person_router | `cp_layla_vox.50` (mod/events/cp_layla_vox_events.txt:2128) | `mod/events/cp_layla_vox_events.txt:2383` |
| `cp_layla_vox.5401` | layla | She Goes Around | visible_chain | `cp_layla_vox.54` (mod/events/cp_layla_vox_events.txt:2383) | `mod/events/cp_layla_vox_events.txt:2404` |
| `cp_layla_vox.5402` | layla | She Takes It Home | visible_chain | `cp_layla_vox.54` (mod/events/cp_layla_vox_events.txt:2383) | `mod/events/cp_layla_vox_events.txt:2422` |
| `cp_layla_vox.5403` | layla | A Different Pretext | visible_chain | `cp_layla_vox.54` (mod/events/cp_layla_vox_events.txt:2383) | `mod/events/cp_layla_vox_events.txt:2440` |
| `cp_layla_vox.59` | layla | Umm Mariam Does Not Appear | hidden_person_router | `cp_layla_vox.50` (mod/events/cp_layla_vox_events.txt:2128) | `mod/events/cp_layla_vox_events.txt:2459` |
| `cp_layla_vox.61` | layla | The Mare on the Canal Road | hidden_person_router | `cp_layla_vox.60` (mod/events/cp_layla_vox_events.txt:2483) | `mod/events/cp_layla_vox_events.txt:2523` |
| `cp_layla_vox.6101` | layla | Stand and Face | visible_chain | `cp_layla_vox.61` (mod/events/cp_layla_vox_events.txt:2523) | `mod/events/cp_layla_vox_events.txt:2544` |
| `cp_layla_vox.6102` | layla | The Old Gesture | visible_chain | `cp_layla_vox.61` (mod/events/cp_layla_vox_events.txt:2523) | `mod/events/cp_layla_vox_events.txt:2562` |
| `cp_layla_vox.6103` | layla | She Keeps Working | visible_chain | `cp_layla_vox.61` (mod/events/cp_layla_vox_events.txt:2523) | `mod/events/cp_layla_vox_events.txt:2580` |
| `cp_layla_vox.62` | layla | He Asks After Ahmed | hidden_person_router | `cp_layla_vox.60` (mod/events/cp_layla_vox_events.txt:2483) | `mod/events/cp_layla_vox_events.txt:2599` |
| `cp_layla_vox.6201` | layla | He Is Well | visible_chain | `cp_layla_vox.62` (mod/events/cp_layla_vox_events.txt:2599) | `mod/events/cp_layla_vox_events.txt:2620` |
| `cp_layla_vox.6202` | layla | The Truth | visible_chain | `cp_layla_vox.62` (mod/events/cp_layla_vox_events.txt:2599) | `mod/events/cp_layla_vox_events.txt:2638` |
| `cp_layla_vox.6203` | layla | Silence, Lowered Eyes | visible_chain | `cp_layla_vox.62` (mod/events/cp_layla_vox_events.txt:2599) | `mod/events/cp_layla_vox_events.txt:2656` |
| `cp_layla_vox.63` | layla | The Ledger at the Planting | hidden_person_router | `cp_layla_vox.60` (mod/events/cp_layla_vox_events.txt:2483) | `mod/events/cp_layla_vox_events.txt:2675` |
| `cp_layla_vox.6301` | layla | She Nods | visible_chain | `cp_layla_vox.63` (mod/events/cp_layla_vox_events.txt:2675) | `mod/events/cp_layla_vox_events.txt:2696` |
| `cp_layla_vox.6302` | layla | The Wheat | visible_chain | `cp_layla_vox.63` (mod/events/cp_layla_vox_events.txt:2675) | `mod/events/cp_layla_vox_events.txt:2714` |
| `cp_layla_vox.6303` | layla | A Compromise | visible_chain | `cp_layla_vox.63` (mod/events/cp_layla_vox_events.txt:2675) | `mod/events/cp_layla_vox_events.txt:2732` |
| `cp_layla_vox.64` | layla | He Comes Less, Now | hidden_person_router | `cp_layla_vox.60` (mod/events/cp_layla_vox_events.txt:2483) | `mod/events/cp_layla_vox_events.txt:2751` |
| `cp_layla_vox.6401` | layla | Tea, Formal | visible_chain | `cp_layla_vox.64` (mod/events/cp_layla_vox_events.txt:2751) | `mod/events/cp_layla_vox_events.txt:2772` |
| `cp_layla_vox.6402` | layla | He May Speak to Ahmed | visible_chain | `cp_layla_vox.64` (mod/events/cp_layla_vox_events.txt:2751) | `mod/events/cp_layla_vox_events.txt:2790` |
| `cp_layla_vox.6403` | layla | Her Silence, His First Word | visible_chain | `cp_layla_vox.64` (mod/events/cp_layla_vox_events.txt:2751) | `mod/events/cp_layla_vox_events.txt:2808` |
| `cp_layla_vox.65` | layla | News of His Son | hidden_person_router | `cp_layla_vox.60` (mod/events/cp_layla_vox_events.txt:2483) | `mod/events/cp_layla_vox_events.txt:2827` |
| `cp_layla_vox.6501` | layla | The Old Bey's Weight | visible_chain | `cp_layla_vox.65` (mod/events/cp_layla_vox_events.txt:2827) | `mod/events/cp_layla_vox_events.txt:2848` |
| `cp_layla_vox.6502` | layla | The Son Will Win | visible_chain | `cp_layla_vox.65` (mod/events/cp_layla_vox_events.txt:2827) | `mod/events/cp_layla_vox_events.txt:2866` |
| `cp_layla_vox.6503` | layla | Not Her Business | visible_chain | `cp_layla_vox.65` (mod/events/cp_layla_vox_events.txt:2827) | `mod/events/cp_layla_vox_events.txt:2884` |
| `cp_layla_vox.69` | layla | No Mare Today | hidden_person_router | `cp_layla_vox.60` (mod/events/cp_layla_vox_events.txt:2483) | `mod/events/cp_layla_vox_events.txt:2903` |
| `cp_layla_vox.71` | layla | At the Gate Before Shift | hidden_person_router | `cp_layla_vox.70` (mod/events/cp_layla_vox_events.txt:2927) | `mod/events/cp_layla_vox_events.txt:2965` |
| `cp_layla_vox.7101` | layla | Head Down | visible_chain | `cp_layla_vox.71` (mod/events/cp_layla_vox_events.txt:2965) | `mod/events/cp_layla_vox_events.txt:2986` |
| `cp_layla_vox.7102` | layla | She Looks | visible_chain | `cp_layla_vox.71` (mod/events/cp_layla_vox_events.txt:2965) | `mod/events/cp_layla_vox_events.txt:3004` |
| `cp_layla_vox.7103` | layla | He Is a Pillar | visible_chain | `cp_layla_vox.71` (mod/events/cp_layla_vox_events.txt:2965) | `mod/events/cp_layla_vox_events.txt:3022` |
| `cp_layla_vox.72` | layla | A Line in the Ledger | hidden_person_router | `cp_layla_vox.70` (mod/events/cp_layla_vox_events.txt:2927) | `mod/events/cp_layla_vox_events.txt:3041` |
| `cp_layla_vox.7201` | layla | She Asks | visible_chain | `cp_layla_vox.72` (mod/events/cp_layla_vox_events.txt:3041) | `mod/events/cp_layla_vox_events.txt:3062` |
| `cp_layla_vox.7202` | layla | Trust the Number | visible_chain | `cp_layla_vox.72` (mod/events/cp_layla_vox_events.txt:3041) | `mod/events/cp_layla_vox_events.txt:3080` |
| `cp_layla_vox.7203` | layla | The Foreman, Quietly | visible_chain | `cp_layla_vox.72` (mod/events/cp_layla_vox_events.txt:3041) | `mod/events/cp_layla_vox_events.txt:3098` |
| `cp_layla_vox.73` | layla | A Hand Caught in the Loom | hidden_person_router | `cp_layla_vox.70` (mod/events/cp_layla_vox_events.txt:2927) | `mod/events/cp_layla_vox_events.txt:3117` |
| `cp_layla_vox.7301` | layla | Report | visible_chain | `cp_layla_vox.73` (mod/events/cp_layla_vox_events.txt:3117) | `mod/events/cp_layla_vox_events.txt:3138` |
| `cp_layla_vox.7302` | layla | Silence | visible_chain | `cp_layla_vox.73` (mod/events/cp_layla_vox_events.txt:3117) | `mod/events/cp_layla_vox_events.txt:3156` |
| `cp_layla_vox.7303` | layla | She Cannot Go | visible_chain | `cp_layla_vox.73` (mod/events/cp_layla_vox_events.txt:3117) | `mod/events/cp_layla_vox_events.txt:3174` |
| `cp_layla_vox.74` | layla | He Knows My Name | hidden_person_router | `cp_layla_vox.70` (mod/events/cp_layla_vox_events.txt:2927) | `mod/events/cp_layla_vox_events.txt:3193` |
| `cp_layla_vox.7401` | layla | She Corrects Him | visible_chain | `cp_layla_vox.74` (mod/events/cp_layla_vox_events.txt:3193) | `mod/events/cp_layla_vox_events.txt:3214` |
| `cp_layla_vox.7402` | layla | She Accepts | visible_chain | `cp_layla_vox.74` (mod/events/cp_layla_vox_events.txt:3193) | `mod/events/cp_layla_vox_events.txt:3232` |
| `cp_layla_vox.7403` | layla | Ask for Transfer | visible_chain | `cp_layla_vox.74` (mod/events/cp_layla_vox_events.txt:3193) | `mod/events/cp_layla_vox_events.txt:3250` |
| `cp_layla_vox.75` | layla | The Gate, This Morning | hidden_person_router | `cp_layla_vox.70` (mod/events/cp_layla_vox_events.txt:2927) | `mod/events/cp_layla_vox_events.txt:3269` |
| `cp_layla_vox.7501` | layla | She Walks Through | visible_chain | `cp_layla_vox.75` (mod/events/cp_layla_vox_events.txt:3269) | `mod/events/cp_layla_vox_events.txt:3290` |
| `cp_layla_vox.7502` | layla | She Stands | visible_chain | `cp_layla_vox.75` (mod/events/cp_layla_vox_events.txt:3269) | `mod/events/cp_layla_vox_events.txt:3308` |
| `cp_layla_vox.7503` | layla | Home | visible_chain | `cp_layla_vox.75` (mod/events/cp_layla_vox_events.txt:3269) | `mod/events/cp_layla_vox_events.txt:3326` |
| `cp_layla_vox.79` | layla | The Owner Did Not Come to the Floor | hidden_person_router | `cp_layla_vox.70` (mod/events/cp_layla_vox_events.txt:2927) | `mod/events/cp_layla_vox_events.txt:3345` |
| `cp_layla_vox.81` | layla | The Man at the Well | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3406` |
| `cp_layla_vox.82` | layla | A Traveler with News | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3426` |
| `cp_layla_vox.83` | layla | A Beggar at the Door | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3446` |
| `cp_layla_vox.84` | layla | A Woman Sitting on the Canal Stone | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3467` |
| `cp_layla_vox.85` | layla | A Child at the Crossroads | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3487` |
| `cp_layla_vox.86` | layla | A Man with a Clipboard | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3507` |
| `cp_layla_vox.89` | layla | The Road, Empty Today | hidden_person_router | `cp_layla_vox.80` (mod/events/cp_layla_vox_events.txt:3371) | `mod/events/cp_layla_vox_events.txt:3528` |
| `cp_layla_vox.91` | layla | The Book on the Shelf | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3570` |
| `cp_layla_vox.92` | layla | The Candle, Alone | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3589` |
| `cp_layla_vox.93` | layla | A Line, Aloud | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3608` |
| `cp_layla_vox.94` | layla | Her Face in the Surface of the Water | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3627` |
| `cp_layla_vox.95` | layla | Walking Home Alone | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3646` |
| `cp_layla_vox.96` | layla | The Quiet After Everything | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3665` |
| `cp_layla_vox.99` | layla | Nothing Tonight | hidden_person_router | `cp_layla_vox.90` (mod/events/cp_layla_vox_events.txt:3553) | `mod/events/cp_layla_vox_events.txt:3684` |
| `cp_mansur.10` | mansur | The Mat Beside the Looms | ambient, button, first_contact, world_response=2 | `cp_mansur_dispatch_building` (mod/common/scripted_effects/cp_mansur_memory.txt:163)<br>`cp_roll_ambient_mansur` (mod/common/scripted_effects/cp_mansur_memory.txt:269)<br>`cp_shared_action_mansur` (mod/common/scripted_effects/cp_shared_action_buttons.txt:179) | `mod/events/cp_mansur_events.txt:57` |
| `cp_mansur.20` | mansur | The First Wage Token | ambient, button, world_response=3 | `cp_mansur_dispatch_yearly` (mod/common/scripted_effects/cp_mansur_memory.txt:66)<br>`cp_mansur_dispatch_tech` (mod/common/scripted_effects/cp_mansur_memory.txt:133)<br>`cp_mansur_dispatch_building` (mod/common/scripted_effects/cp_mansur_memory.txt:180) | `mod/events/cp_mansur_events.txt:93` |
| `cp_mansur.30` | mansur | The Belt Does Not Stop | ambient, button, world_response=2 | `cp_mansur_dispatch_yearly` (mod/common/scripted_effects/cp_mansur_memory.txt:77)<br>`cp_mansur_dispatch_tech` (mod/common/scripted_effects/cp_mansur_memory.txt:146)<br>`cp_roll_ambient_mansur` (mod/common/scripted_effects/cp_mansur_memory.txt:284) | `mod/events/cp_mansur_events.txt:129` |
| `cp_mansur.40` | mansur | Money Sent Home | ambient, button, world_response | `cp_mansur_dispatch_yearly` (mod/common/scripted_effects/cp_mansur_memory.txt:87)<br>`cp_roll_ambient_mansur` (mod/common/scripted_effects/cp_mansur_memory.txt:291)<br>`cp_shared_action_mansur` (mod/common/scripted_effects/cp_shared_action_buttons.txt:182) | `mod/events/cp_mansur_events.txt:165` |
| `cp_mansur.50` | mansur | The Bed Rent | ambient, button, world_response=2 | `cp_mansur_dispatch_yearly` (mod/common/scripted_effects/cp_mansur_memory.txt:98)<br>`cp_mansur_dispatch_building` (mod/common/scripted_effects/cp_mansur_memory.txt:195)<br>`cp_roll_ambient_mansur` (mod/common/scripted_effects/cp_mansur_memory.txt:298) | `mod/events/cp_mansur_events.txt:201` |
| `cp_mansur.60` | mansur | The Meal Tin | ambient, button, world_response=2 | `cp_mansur_dispatch_yearly` (mod/common/scripted_effects/cp_mansur_memory.txt:108)<br>`cp_mansur_dispatch_building` (mod/common/scripted_effects/cp_mansur_memory.txt:210)<br>`cp_roll_ambient_mansur` (mod/common/scripted_effects/cp_mansur_memory.txt:305) | `mod/events/cp_mansur_events.txt:238` |
| `cp_mina.10` | mina | The Letters Set in Lead | ambient, button, first_contact | `cp_roll_ambient_mina` (mod/common/scripted_effects/cp_mina_memory.txt:133)<br>`cp_shared_action_mina` (mod/common/scripted_effects/cp_shared_action_buttons.txt:74)<br>`cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_mina_events.txt:48` |
| `cp_mina.20` | mina | The Primer Leaves the Press | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:507) | `mod/events/cp_mina_events.txt:84` |
| `cp_mina.30` | mina | The Notice Sheet | world_response | `cp_mina_dispatch_tech` (mod/common/scripted_effects/cp_mina_memory.txt:53) | `mod/events/cp_mina_events.txt:120` |
| `cp_mina.40` | mina | The Night Proof | ambient, button | `cp_roll_ambient_mina` (mod/common/scripted_effects/cp_mina_memory.txt:140)<br>`cp_shared_action_mina` (mod/common/scripted_effects/cp_shared_action_buttons.txt:75) | `mod/events/cp_mina_events.txt:156` |
| `cp_mina.50` | mina | The Catalogue Room | world_response | `cp_mina_dispatch_building` (mod/common/scripted_effects/cp_mina_memory.txt:72) | `mod/events/cp_mina_events.txt:192` |
| `cp_mina.60` | mina | The Courtyard Sheet | ambient, button | `cp_roll_ambient_mina` (mod/common/scripted_effects/cp_mina_memory.txt:147)<br>`cp_shared_action_mina` (mod/common/scripted_effects/cp_shared_action_buttons.txt:76) | `mod/events/cp_mina_events.txt:228` |
| `cp_nabil.10` | nabil | The Lamp at the Corner | ambient, button, first_contact, world_response | `cp_roll_ambient_nabil` (mod/common/scripted_effects/cp_nabil_memory.txt:198)<br>`cp_shared_action_nabil` (mod/common/scripted_effects/cp_shared_action_buttons.txt:169)<br>`cp_nabil.1` (mod/events/cp_nabil_events.txt:12) | `mod/events/cp_nabil_events.txt:59` |
| `cp_nabil.20` | nabil | The New Station | law_reaction=2 | `cp_nabil_dispatch_law_enacted` (mod/common/scripted_effects/cp_nabil_memory.txt:93)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:270) | `mod/events/cp_nabil_events.txt:95` |
| `cp_nabil.30` | nabil | Rifles by the Bakery | law_reaction=3 | `cp_nabil_dispatch_law_enacted` (mod/common/scripted_effects/cp_nabil_memory.txt:105)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:252)<br>`cp_roll_public_order_law_reaction` (mod/common/scripted_effects/cp_shared_firing.txt:288) | `mod/events/cp_nabil_events.txt:131` |
| `cp_nabil.40` | nabil | The Square Afterwards | ambient, button, law_reaction=2, world_response=2 | `cp_nabil_dispatch_yearly` (mod/common/scripted_effects/cp_nabil_memory.txt:65)<br>`cp_nabil_dispatch_law_enacted` (mod/common/scripted_effects/cp_nabil_memory.txt:115)<br>`cp_nabil_dispatch_revolution` (mod/common/scripted_effects/cp_nabil_memory.txt:146) | `mod/events/cp_nabil_events.txt:167` |
| `cp_nabil.50` | nabil | The Lost Boy | ambient, button | `cp_roll_ambient_nabil` (mod/common/scripted_effects/cp_nabil_memory.txt:213)<br>`cp_shared_action_nabil` (mod/common/scripted_effects/cp_shared_action_buttons.txt:171) | `mod/events/cp_nabil_events.txt:203` |
| `cp_nabil.60` | nabil | The Complaint Bench | ambient, button, world_response | `cp_nabil_dispatch_yearly` (mod/common/scripted_effects/cp_nabil_memory.txt:79)<br>`cp_roll_ambient_nabil` (mod/common/scripted_effects/cp_nabil_memory.txt:224)<br>`cp_shared_action_nabil` (mod/common/scripted_effects/cp_shared_action_buttons.txt:172) | `mod/events/cp_nabil_events.txt:240` |
| `cp_nour.10` | nour | The Cedar Chest | ambient, button, first_contact | `cp_roll_ambient_nour` (mod/common/scripted_effects/cp_nour_memory.txt:134)<br>`cp_shared_action_nour` (mod/common/scripted_effects/cp_shared_action_buttons.txt:65)<br>`cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_nour_events.txt:48` |
| `cp_nour.20` | nour | Her Name on the Paper | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:481) | `mod/events/cp_nour_events.txt:84` |
| `cp_nour.30` | nour | The Rent Receipt | world_response | `cp_nour_dispatch_yearly` (mod/common/scripted_effects/cp_nour_memory.txt:38) | `mod/events/cp_nour_events.txt:120` |
| `cp_nour.40` | nour | The Key Under the Pillow | ambient, button | `cp_roll_ambient_nour` (mod/common/scripted_effects/cp_nour_memory.txt:141)<br>`cp_shared_action_nour` (mod/common/scripted_effects/cp_shared_action_buttons.txt:66) | `mod/events/cp_nour_events.txt:156` |
| `cp_nour.50` | nour | The Register Shelf | world_response=2 | `cp_nour_dispatch_tech` (mod/common/scripted_effects/cp_nour_memory.txt:60)<br>`cp_nour_dispatch_building` (mod/common/scripted_effects/cp_nour_memory.txt:76) | `mod/events/cp_nour_events.txt:192` |
| `cp_nour.60` | nour | The Morning Account | ambient, button | `cp_roll_ambient_nour` (mod/common/scripted_effects/cp_nour_memory.txt:148)<br>`cp_shared_action_nour` (mod/common/scripted_effects/cp_shared_action_buttons.txt:67) | `mod/events/cp_nour_events.txt:228` |
| `cp_rashid.10` | rashid | The Counter Window | ambient, button, first_contact, world_response=2 | `cp_rashid_dispatch_building` (mod/common/scripted_effects/cp_rashid_memory.txt:122)<br>`cp_roll_ambient_rashid` (mod/common/scripted_effects/cp_rashid_memory.txt:195)<br>`cp_shared_action_rashid` (mod/common/scripted_effects/cp_shared_action_buttons.txt:130) | `mod/events/cp_rashid_events.txt:58` |
| `cp_rashid.20` | rashid | The Archive Lamp | world_response=2 | `cp_rashid_dispatch_yearly` (mod/common/scripted_effects/cp_rashid_memory.txt:64)<br>`cp_rashid_dispatch_tech` (mod/common/scripted_effects/cp_rashid_memory.txt:98) | `mod/events/cp_rashid_events.txt:94` |
| `cp_rashid.30` | rashid | The Paper Name | world_response | `cp_rashid_dispatch_tech` (mod/common/scripted_effects/cp_rashid_memory.txt:105) | `mod/events/cp_rashid_events.txt:130` |
| `cp_rashid.40` | rashid | Dust in the Ink | ambient, button | `cp_roll_ambient_rashid` (mod/common/scripted_effects/cp_rashid_memory.txt:202)<br>`cp_shared_action_rashid` (mod/common/scripted_effects/cp_shared_action_buttons.txt:131) | `mod/events/cp_rashid_events.txt:166` |
| `cp_rashid.50` | rashid | The New Seal | law_reaction | `cp_rashid_dispatch_law_enacted` (mod/common/scripted_effects/cp_rashid_memory.txt:80) | `mod/events/cp_rashid_events.txt:202` |
| `cp_rashid.60` | rashid | The Numbered Drawer | ambient, button, world_response | `cp_rashid_dispatch_building` (mod/common/scripted_effects/cp_rashid_memory.txt:139)<br>`cp_roll_ambient_rashid` (mod/common/scripted_effects/cp_rashid_memory.txt:209)<br>`cp_shared_action_rashid` (mod/common/scripted_effects/cp_shared_action_buttons.txt:132) | `mod/events/cp_rashid_events.txt:238` |
| `cp_salma.10` | salma | The Switchboard | ambient, button, first_contact, world_response=3 | `cp_salma_dispatch_tech` (mod/common/scripted_effects/cp_salma_memory.txt:110)<br>`cp_salma_dispatch_building` (mod/common/scripted_effects/cp_salma_memory.txt:160)<br>`cp_roll_ambient_salma` (mod/common/scripted_effects/cp_salma_memory.txt:251) | `mod/events/cp_salma_events.txt:58` |
| `cp_salma.20` | salma | The First Light | world_response=2 | `cp_salma_dispatch_yearly` (mod/common/scripted_effects/cp_salma_memory.txt:64)<br>`cp_salma_dispatch_tech` (mod/common/scripted_effects/cp_salma_memory.txt:117) | `mod/events/cp_salma_events.txt:94` |
| `cp_salma.30` | salma | Voices in the Wall | world_response | `cp_salma_dispatch_tech` (mod/common/scripted_effects/cp_salma_memory.txt:124) | `mod/events/cp_salma_events.txt:130` |
| `cp_salma.40` | salma | The Night Bell | ambient, button | `cp_roll_ambient_salma` (mod/common/scripted_effects/cp_salma_memory.txt:258)<br>`cp_shared_action_salma` (mod/common/scripted_effects/cp_shared_action_buttons.txt:140) | `mod/events/cp_salma_events.txt:166` |
| `cp_salma.50` | salma | The Burned Fuse | ambient, button, world_response=3 | `cp_salma_dispatch_yearly` (mod/common/scripted_effects/cp_salma_memory.txt:75)<br>`cp_salma_dispatch_tech` (mod/common/scripted_effects/cp_salma_memory.txt:132)<br>`cp_salma_dispatch_building` (mod/common/scripted_effects/cp_salma_memory.txt:180) | `mod/events/cp_salma_events.txt:202` |
| `cp_salma.60` | salma | The Crossed Line | ambient, button, world_response=3 | `cp_salma_dispatch_yearly` (mod/common/scripted_effects/cp_salma_memory.txt:86)<br>`cp_salma_dispatch_tech` (mod/common/scripted_effects/cp_salma_memory.txt:140)<br>`cp_salma_dispatch_building` (mod/common/scripted_effects/cp_salma_memory.txt:195) | `mod/events/cp_salma_events.txt:239` |
| `cp_samier.10` | samier | The Gate of Smoke | ambient, button, first_contact, world_response | `cp_roll_ambient_samier` (mod/common/scripted_effects/cp_samier_memory.txt:212)<br>`cp_shared_action_samier` (mod/common/scripted_effects/cp_shared_action_buttons.txt:92)<br>`cp_samier.1` (mod/events/cp_samier_events.txt:12) | `mod/events/cp_samier_events.txt:58` |
| `cp_samier.20` | samier | Words on the Board | law_reaction | `cp_samier_dispatch_law_enacted` (mod/common/scripted_effects/cp_samier_memory.txt:94) | `mod/events/cp_samier_events.txt:94` |
| `cp_samier.30` | samier | The Red Thread | world_response=2 | `cp_samier_dispatch_tech` (mod/common/scripted_effects/cp_samier_memory.txt:113)<br>`cp_samier_dispatch_building` (mod/common/scripted_effects/cp_samier_memory.txt:129) | `mod/events/cp_samier_events.txt:130` |
| `cp_samier.40` | samier | Bread at the Gate | ambient, button | `cp_roll_ambient_samier` (mod/common/scripted_effects/cp_samier_memory.txt:219)<br>`cp_shared_action_samier` (mod/common/scripted_effects/cp_shared_action_buttons.txt:93) | `mod/events/cp_samier_events.txt:166` |
| `cp_samier.50` | samier | The False Quarter Hour | ambient, button, world_response=2 | `cp_samier_dispatch_yearly` (mod/common/scripted_effects/cp_samier_memory.txt:68)<br>`cp_samier_dispatch_building` (mod/common/scripted_effects/cp_samier_memory.txt:144)<br>`cp_roll_ambient_samier` (mod/common/scripted_effects/cp_samier_memory.txt:227) | `mod/events/cp_samier_events.txt:202` |
| `cp_samier.60` | samier | Letters After the Bell | ambient, button, world_response | `cp_samier_dispatch_yearly` (mod/common/scripted_effects/cp_samier_memory.txt:79)<br>`cp_roll_ambient_samier` (mod/common/scripted_effects/cp_samier_memory.txt:235)<br>`cp_shared_action_samier` (mod/common/scripted_effects/cp_shared_action_buttons.txt:95) | `mod/events/cp_samier_events.txt:240` |
| `cp_soldier.10` | soldier | The Strap | ambient, button, first_contact | `cp_shared_action_soldier` (mod/common/scripted_effects/cp_shared_action_buttons.txt:56)<br>`cp_roll_ambient_soldier` (mod/common/scripted_effects/cp_soldier_memory.txt:170)<br>`cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_soldier_events.txt:47` |
| `cp_soldier.20` | soldier | The Notice | milestone | `cp_soldier_dispatch_war_started` (mod/common/scripted_effects/cp_soldier_memory.txt:56) | `mod/events/cp_soldier_events.txt:84` |
| `cp_soldier.21` | soldier | The Road Back | milestone | `cp_soldier_dispatch_war_end` (mod/common/scripted_effects/cp_soldier_memory.txt:66) | `mod/events/cp_soldier_events.txt:121` |
| `cp_soldier.30` | soldier | The Arsenal Gate | world_response=2 | `cp_soldier_dispatch_tech` (mod/common/scripted_effects/cp_soldier_memory.txt:80)<br>`cp_soldier_dispatch_building` (mod/common/scripted_effects/cp_soldier_memory.txt:100) | `mod/events/cp_soldier_events.txt:158` |
| `cp_soldier.40` | soldier | Beans at Dusk | ambient, button | `cp_shared_action_soldier` (mod/common/scripted_effects/cp_shared_action_buttons.txt:57)<br>`cp_roll_ambient_soldier` (mod/common/scripted_effects/cp_soldier_memory.txt:178) | `mod/events/cp_soldier_events.txt:194` |
| `cp_soldier.50` | soldier | The Letter Folded Twice | ambient, button, world_response | `cp_shared_action_soldier` (mod/common/scripted_effects/cp_shared_action_buttons.txt:58)<br>`cp_soldier_dispatch_yearly` (mod/common/scripted_effects/cp_soldier_memory.txt:40)<br>`cp_roll_ambient_soldier` (mod/common/scripted_effects/cp_soldier_memory.txt:186) | `mod/events/cp_soldier_events.txt:232` |
| `cp_tarek.10` | tarek | The Mill Ledger | ambient, button, first_contact, world_response | `cp_shared_action_tarek` (mod/common/scripted_effects/cp_shared_action_buttons.txt:102)<br>`cp_roll_ambient_tarek` (mod/common/scripted_effects/cp_tarek_memory.txt:211)<br>`cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_tarek_events.txt:59` |
| `cp_tarek.20` | tarek | The New Arithmetic | law_reaction | `cp_tarek_dispatch_law_enacted` (mod/common/scripted_effects/cp_tarek_memory.txt:94) | `mod/events/cp_tarek_events.txt:95` |
| `cp_tarek.30` | tarek | The New Boiler | world_response=2 | `cp_tarek_dispatch_tech` (mod/common/scripted_effects/cp_tarek_memory.txt:112)<br>`cp_tarek_dispatch_building` (mod/common/scripted_effects/cp_tarek_memory.txt:127) | `mod/events/cp_tarek_events.txt:131` |
| `cp_tarek.40` | tarek | The Account Book | ambient, button | `cp_shared_action_tarek` (mod/common/scripted_effects/cp_shared_action_buttons.txt:103)<br>`cp_roll_ambient_tarek` (mod/common/scripted_effects/cp_tarek_memory.txt:218) | `mod/events/cp_tarek_events.txt:167` |
| `cp_tarek.50` | tarek | The Second Chimney | ambient, button, world_response=2 | `cp_shared_action_tarek` (mod/common/scripted_effects/cp_shared_action_buttons.txt:104)<br>`cp_tarek_dispatch_yearly` (mod/common/scripted_effects/cp_tarek_memory.txt:68)<br>`cp_tarek_dispatch_building` (mod/common/scripted_effects/cp_tarek_memory.txt:141) | `mod/events/cp_tarek_events.txt:203` |
| `cp_tarek.60` | tarek | The Locked Gate | ambient, button, world_response | `cp_shared_action_tarek` (mod/common/scripted_effects/cp_shared_action_buttons.txt:105)<br>`cp_tarek_dispatch_yearly` (mod/common/scripted_effects/cp_tarek_memory.txt:79)<br>`cp_roll_ambient_tarek` (mod/common/scripted_effects/cp_tarek_memory.txt:234) | `mod/events/cp_tarek_events.txt:241` |
| `cp_zaynab.10` | zaynab | The Brass Basin | ambient, button, first_contact | `cp_shared_action_zaynab` (mod/common/scripted_effects/cp_shared_action_buttons.txt:83)<br>`cp_roll_ambient_zaynab` (mod/common/scripted_effects/cp_zaynab_memory.txt:143)<br>`cp_shared_startup.2` (mod/events/cp_shared_startup_events.txt:201) | `mod/events/cp_zaynab_events.txt:48` |
| `cp_zaynab.20` | zaynab | The Doctor Waits Outside | law_reaction | `cp_on_law_enacted` (mod/common/on_actions/cp_on_actions.txt:530) | `mod/events/cp_zaynab_events.txt:84` |
| `cp_zaynab.30` | zaynab | The Fever Bowl | world_response | `cp_zaynab_dispatch_yearly` (mod/common/scripted_effects/cp_zaynab_memory.txt:38) | `mod/events/cp_zaynab_events.txt:120` |
| `cp_zaynab.40` | zaynab | The Long Night | ambient, button | `cp_shared_action_zaynab` (mod/common/scripted_effects/cp_shared_action_buttons.txt:84)<br>`cp_roll_ambient_zaynab` (mod/common/scripted_effects/cp_zaynab_memory.txt:150) | `mod/events/cp_zaynab_events.txt:156` |
| `cp_zaynab.50` | zaynab | The Lime Bucket | world_response=2 | `cp_zaynab_dispatch_tech` (mod/common/scripted_effects/cp_zaynab_memory.txt:64)<br>`cp_zaynab_dispatch_building` (mod/common/scripted_effects/cp_zaynab_memory.txt:83) | `mod/events/cp_zaynab_events.txt:192` |
| `cp_zaynab.60` | zaynab | Thread Around the Wrist | ambient, button | `cp_shared_action_zaynab` (mod/common/scripted_effects/cp_shared_action_buttons.txt:85)<br>`cp_roll_ambient_zaynab` (mod/common/scripted_effects/cp_zaynab_memory.txt:157) | `mod/events/cp_zaynab_events.txt:228` |
