# Layla's Reactions

> Reactions fire on game-state triggers and change her state. Some set branch letters (H1/H2/H3 hinges). Some move her anchor. Some tweak weights, opinions, or flags. All of them are narrated in Mahfouz register -- interior, sensory, specific. No real-history names or dates; the V3 save decides who the foreign fleet belongs to.
>
> The state model is in [anchors.md](anchors.md). The pulse pool is in [pulse.md](pulse.md). This file catalogs the reactions.

---

## Table of contents

- [H1 resolutions -- The Land](#h1-resolutions--the-land) (R1-R5)
- [H1 rollbacks](#h1-rollbacks) (R6-R7)
- [H2 resolutions -- The Throne](#h2-resolutions--the-throne) (R8-R11)
- [H3 resolutions -- The World](#h3-resolutions--the-world) (R12-R14)
- [Anchor-moving personal](#anchor-moving-personal) (R15-R20)
- [Migration](#migration) (R21-R23)
- [War and conscription](#war-and-conscription) (R24-R29)
- [Epidemic and disaster](#epidemic-and-disaster) (R30-R34)
- [Governance (non-hinge)](#governance-non-hinge) (R35-R39)
- [Diplomacy and foreign](#diplomacy-and-foreign) (R40-R43)
- [Family and Mariam](#family-and-mariam) (R44-R46)
- [Economy](#economy) (R47-R48)
- [Closure](#closure) (R49-R50)

---

## H1 resolutions -- The Land

The five reactions that set `cp_h1` (and `cp_h1_sub` where applicable). Between them, they exhaust the H1 possibilities -- no game-state can leave H1 unresolved past her middle age.

### R1. cp_layla.h1_tenant_farmers

**Trigger:** `on_law_enactment_pass` for EGY, new law = `law_tenant_farmers`, Layla alive, `cp_h1` unset.
**Fires:** once.

**State change:**
- `cp_resolve_h1 = { letter=A sub=T }`
- `cp_set_land_anchor = tenant_wife`
- `cp_shift_weight = { name=cp_w_land_reform delta=+1 }`
- `cp_mark_joy` if she was in `serf_wife` (partial relief); otherwise no joy mark.
- `cp_shift_opinion = { tag=egy delta=+5 }` if `cp_is_sovereign_egypt`; else `+3`.

**Prose variants:**

- *Default.* A clerk reads a paper aloud in the courtyard. The word she catches is *tenant*. Ahmed does not know what it means. The imam explains after Friday prayer: the bey is not your master any more, but the rent still is. She nods slowly. It is the first time in her life she has had a number to owe.
- *Branch `α` (still Ottoman).* The paper bears two seals -- the Cairo pasha's and, stamped below, the Sultan's. Ahmed looks at the Sultan's seal for a long time before he rolls the paper up. As if to say: at least one of the two who owns us now owns us a little less.

### R2. cp_layla.h1_homesteading

**Trigger:** `on_law_enactment_pass` for EGY, new law = `law_homesteading`, Layla alive, `cp_h1` unset.
**Fires:** once.

**State change:**
- `cp_resolve_h1 = { letter=A sub=H }`
- `cp_set_land_anchor = landowner_wife`
- `cp_shift_weight = { name=cp_w_land_reform delta=+2 cp_hope delta=+2 }`
- `cp_mark_joy`
- `cp_shift_opinion = { tag=egy delta=+10 }`
- loyalist spike (mechanical -- sets a flag the eventify pass reads to trigger a `increase_loyalists` effect on farmers in her state).

**Prose variants:**

- *Default.* The clerk's hand on the paper. Ahmed's face when he reads his own name aloud, slowly, as if hearing it for the first time. The bey's cousin in the doorway, watching with his hands folded. The paper feels lighter than she expected. She thinks of her mother, who died on land that was not hers and never could have been.
- *Branch `α`.* The imam signs below the Sultan's seal and beneath that below the Cairo pasha's, and beneath that a space for Ahmed's mark. Three authorities on one page to say this one thing is *his*. She does not understand the politics. She understands the weight of ink.
- *Branch `β`.* There is only one seal. It is new and green and does not include the Caliph's calligraphy that every other document of her life has borne. Ahmed traces it with his thumb, uncertain. The land is his now, by an authority he is still learning to name.

### R3. cp_layla.h1_commercialized

**Trigger:** `on_law_enactment_pass` for EGY, new law = `law_commercialized_agriculture`, Layla alive, `cp_h1` unset.
**Fires:** once.

**State change:**
- `cp_resolve_h1 = { letter=A sub=C }`
- `cp_set_land_anchor = wage_laborer_wife`
- `cp_shift_weight = { name=cp_w_economy delta=+2 cp_w_land_reform delta=+1 }`
- `cp_shift_opinion = { tag=egy delta=-2 }` (complicated: formally better, felt worse)
- `cp_mark_hardship` softly (wage uncertainty).

**Prose variants:**

- *Default.* A company has bought the field. Not a man; a name on a paper, with offices in the capital. Ahmed works the same furrow he worked yesterday and is paid a coin at dusk for it. It is more than the bey ever gave him. It is less than he thought being paid would feel like.

### R4. cp_layla.h1_collectivized

**Trigger:** `on_law_enactment_pass` for EGY, new law = `law_collectivized_agriculture`, Layla alive, `cp_h1` unset.
**Fires:** once.

**State change:**
- `cp_resolve_h1 = { letter=A sub=K }`
- `cp_set_land_anchor = collective_member`
- `cp_shift_weight = { name=cp_w_revolution delta=+1 cp_w_land_reform delta=+2 }`
- `cp_mark_joy` if `cp_had_hardship_recently`; else no mark -- the feeling is uncertainty, not joy.
- `cp_shift_opinion = { tag=egy delta=+3 }`

**Prose variants:**

- *Default.* Men with notebooks come to the village and call everyone to the mosque courtyard. They say: the field is ours now. All of ours. A committee will be chosen. Ahmed asks what that word means; the man with the notebook is patient. Layla watches her husband learning a word that was not in his father's mouth. She does not know yet whether to be afraid.

### R5. cp_layla.serfdom_endures

**Trigger:** Layla reaches age 40 (birth_date + 18 years after spawn) with `cp_h1` still unset and EGY still has `law_serfdom`. Automatic once-in-life check.
**Fires:** once.

**State change:**
- `cp_resolve_h1 = { letter=B }`
- `cp_set_land_anchor = serf_wife` (no-op if already there)
- `cp_shift_weight = { name=cp_hope delta=-2 cp_w_land_reform delta=+1 }` (she keeps caring; she stops expecting)
- no anchor-side move. The weight of the reaction is narrative.

**Prose variants:**

- *Default.* She is forty. Her mother was forty once too, and her mother's mother. None of them knew another way. She catches herself, mid-harvest, thinking the word *change* and being unable to fit it to anything she has seen. The bey's man rides past on the road. The dust settles.
- *Branch `α`.* The imam's sermon names the Sultan-Caliph as he did when she was a child. The coin in her palm bears the same script. The old order is not cruel today -- only heavy. Only exactly what it was.

---

## H1 rollbacks

### R6. cp_layla.serfdom_restored

**Trigger:** `on_law_enactment_pass` for EGY, new law = `law_serfdom`, Layla alive, `cp_h1 = "A"`.
**Fires:** once.

**State change:**
- `cp_resolve_h1 = { letter=B }`
- `cp_h1_rolled_back = 1`
- `cp_set_land_anchor = serf_wife`
- `cp_shift_weight = { name=cp_hope delta=-4 cp_w_revolution delta=+3 cp_w_land_reform delta=+2 }`
- `cp_mark_hardship` hard (flag set to 2 instead of 1, 18-month window)
- `cp_shift_opinion = { tag=egy delta=-20 }`
- **the darkest event.** Eventify pass may wire this to a state-wide radicals boost.

**Prose variants:**

- *Default.* The paper Ahmed kept in the chest is useless now. Not burned, not torn -- simply *useless*, the way a prayer becomes useless when no one remains to hear it. The bey's men ride through the village on their old route, smiling. Ahmed stops speaking for three days. When he speaks again, it is not about the land.
- *Branch `α.H` (was homestead, under Sultan).* They came with new seals pasted over the old. The Caliph's script remains; only the space for Ahmed's name is gone. The coin in her palm is the same. She is the one who is different now.

### R7. cp_layla.tenancy_rollback

**Trigger:** `on_law_enactment_pass` for EGY, new law = `law_tenant_farmers`, Layla alive, `cp_h1 = "A"`, `cp_h1_sub = "H"`.
**Fires:** once.

**State change:**
- `cp_h1_sub = "T"`
- `cp_set_land_anchor = tenant_wife`
- `cp_shift_weight = { name=cp_hope delta=-2 cp_w_land_reform delta=+2 }`
- `cp_mark_hardship`
- `cp_shift_opinion = { tag=egy delta=-8 }`

**Prose variants:**

- *Default.* The paper is still in the chest. It no longer says what it used to say. Someone has decided that a rent must now be paid on the land that was hers, to a person whose face she does not know. She tastes ownership in her mouth for a second longer and then it is gone.

---

## H2 resolutions -- The Throne

### R8. cp_layla.egypt_sovereign

**Trigger:** EGY's overlord changes from OTT to none (independence, any mechanism), Layla alive, `cp_h2` unset.
**Fires:** once.

**State change:**
- `cp_resolve_h2 = { letter=beta }`
- `cp_shift_weight = { name=cp_w_revolution delta=+1 cp_w_diplomacy delta=+1 }`
- `cp_shift_opinion = { tag=egy delta=+30 tag=ott delta=-10 }` -- the numbers are big here because this is the central political event of her era.
- `cp_mark_joy` if Ahmed alive; else no mark.
- eventify pass considers a loyalists boost for her state.

**Prose variants:**

- *Default.* On Friday the imam hesitates before he names the ruler in the khutba. The name that comes out of his mouth is new -- not the Sultan's -- and the men in the back row look at each other. She listens. She prays. At the evening meal Ahmed says the coin in his pocket is the old one still. *For now*, he says, and she hears the two words separately.
- *Variant -- Ahmed conscripted for the independence war.* The name in the khutba is new because her husband fought for it. He came home thinner and quieter and with a mark on his leg that will not heal. The name in the prayer is the weight of him walking.

### R9. cp_layla.egypt_vassalized_again

**Trigger:** EGY's overlord becomes OTT again after being sovereign, Layla alive, `cp_h2 = "beta"`.
**Fires:** once.

**State change:**
- `cp_resolve_h2 = { letter=alpha }`
- `cp_h2_rolled_back = 1`
- `cp_shift_weight = { name=cp_hope delta=-3 cp_w_revolution delta=+2 }`
- `cp_shift_opinion = { tag=egy delta=-10 tag=ott delta=-15 }` -- both resented, one as betrayer one as reimposed.
- `cp_mark_hardship`

**Prose variants:**

- *Default.* The imam names the Sultan again. He does it without apology, as if the last years had not happened. She listens and remembers the first Friday he had said the new name, when a generation had dared. She does not know what to pray for. She prays.

### R10. cp_layla.caliph_dies

**Trigger:** OTT ruler dies (any cause), Layla alive, `cp_is_sultanate` still true at fire time.
**Fires:** once per dynastic death.

**State change:**
- no branch move.
- `cp_shift_opinion = { tag=ott delta=-2 }` if new Sultan is a child/weak; `+2` if strong-seeming. (Eventify pass: check new OTT ruler's traits.)
- `cp_mark_hardship` softly.
- `cp_shift_weight = { name=cp_w_religion delta=+1 }`

**Prose variants:**

- *Default.* The imam's voice trembles in the khutba and she does not know why, until he names a new Sultan. The old name had been in the prayer since before she was born. A world closes. Another opens, with the same shape.
- *Branch `β` (Egypt sovereign).* The news arrives slower than it would have once, and the imam names the dead man in a commemorative prayer, as if naming an uncle. The new Sultan is not their Sultan. The distance between the two shores has a new weight.

### R11. cp_layla.khedive_crowned

**Trigger:** Sovereign-Egypt monarch/king declared (tag-event in V3 narratives). Layla alive, `cp_h2 = "beta"`.
**Fires:** once.

**State change:**
- no branch move.
- `cp_shift_opinion = { tag=egy delta=+10 }`
- `cp_shift_weight = { name=cp_w_diplomacy delta=+1 }`

**Prose variants:**

- *Default.* They say there is a king in Cairo now, with his own name in the prayer. Ahmed has seen the new coin; a man in the market showed him. She turns it over in her fingers at home, when the children are asleep. The face is unfamiliar. The hand that holds it is hers, and it is forty years old, and it has never held a coin that belonged to an *Egyptian* king before.

---

## H3 resolutions -- The World

### R12. cp_layla.industrial_threshold

**Trigger:** any EGY state crosses an urbanization / industry-law threshold. Layla alive, `cp_h3` unset. First time.
**Fires:** once.

**State change:**
- `cp_resolve_h3 = { letter=Y }`
- `cp_shift_weight = { name=cp_w_economy delta=+2 cp_w_labor_laws delta=+1 }`
- no anchor move unless she or her family migrates (separate reactions).

**Prose variants:**

- *Default.* A traveler from Alexandria sits on the mosque steps and tells stories of smoke, of a building as tall as a minaret where men go in at dawn and come out at dusk grey. The children listen. Layla listens. That night she dreams of a minaret that hums.

### R13. cp_layla.foreign_concession

**Trigger:** a foreign GP is granted a major economic concession or investment rights in EGY. Layla alive.
**Fires:** once per distinct foreign GP.

**State change:**
- if `cp_h3` unset: `cp_resolve_h3 = { letter=Y }`.
- `cp_shift_weight = { name=cp_w_diplomacy delta=+1 }`
- `cp_shift_opinion = { tag=<foreign GP> delta=-5 }` if she `cp_hears_foreign_news`; else no opinion move (she simply does not know).

**Prose variants:**

- *Default.* Foreign men arrived with papers stamped in a language no one reads here, and they bought something -- a harbor, a rail line, the right to dig. Ahmed explains what he has heard from the market. She listens and thinks of the bey, who at least had a face.

### R14. cp_layla.capitulations

**Trigger:** EGY signs a capitulations / extraterritoriality agreement. Layla alive.
**Fires:** once.

**State change:**
- if `cp_h3` unset: `cp_resolve_h3 = { letter=Y }`.
- `cp_shift_opinion = { tag=egy delta=-10 }` (to the capitulating state).
- `cp_shift_weight = { name=cp_w_revolution delta=+1 cp_hope delta=-1 }`

**Prose variants:**

- *Default.* A foreign man killed a porter in the port. The porter's brother is a cousin of their neighbor, and the story travels up the river in a week. The foreign man will not be tried. He answers to his own country's judge, and his own country's judge is a thousand miles away.

---

## Anchor-moving personal

### R15. cp_layla.first_pregnancy

**Trigger:** yearly check: `cp_anchor = "bride"`, age 22-35, `cp_barren_wife` unset, `cp_ahmed_at_war` = 0. Low probability per year; high after the second year.
**Fires:** once, or never (the barren-wife path).

**State change:**
- `cp_pregnant = 1`
- `cp_set_anchor = young_mother` after childbirth reaction, not here.

**Prose variants:**

- *Default.* She knows before Ahmed knows. She knows before her mother knows. For three days she tells no one. Then she tells Ahmed while she is kneading bread and he has come in from the field with his hands black. He sits on the stool by the door for a long time, saying nothing, watching her.

### R16. cp_layla.childbirth

**Trigger:** `cp_pregnant = 1` and 9 months elapsed. Outcome rolled against era-appropriate maternal mortality (higher early campaign, lower as `cp_world_came`).
**Fires:** each birth.

**State change (three outcomes):**

- **Live birth, mother lives:** `cp_pregnant = 0`, `cp_children_alive += 1`, `cp_set_anchor = young_mother` if first, `cp_mark_joy`.
- **Stillbirth / infant death:** `cp_pregnant = 0`, `cp_bereaved_mother += 1`, `cp_mark_hardship`, `cp_shift_weight = { cp_hope -1 cp_w_religion +1 }`. Anchor unchanged.
- **Mother dies in childbirth:** fires `R50 cp_layla.closure_childbirth`. Terminal.

**Prose variants:**

- *Default (live birth).* The midwife's hand on her forehead. Ahmed outside the door, pacing the courtyard. The cry that changes the geometry of a room. Later she holds the child and does not speak for an hour.
- *Variant (infant death).* The child drew breath and the midwife said it was weak and by dawn it was not breathing. They wash the body together. Ahmed digs the grave himself, in the old cemetery, where his father is.
- *Variant (mother dies).* — see R50.

### R17. cp_layla.child_dies

**Trigger:** per-child yearly roll, weighted against state disease conditions and SoL. Higher under `serf_wife` and `city_laborer`.
**Fires:** any number of times (per child).

**State change:**
- `cp_children_alive -= 1`, `cp_bereaved_mother += 1`
- `cp_shift_weight = { cp_hope -2 cp_w_religion +1 cp_w_revolution +1 }`
- `cp_mark_hardship`
- If all children now dead: `cp_shift_weight = { cp_hope -4 }` (cumulative).

**Prose variants:**

- *Default.* The fever went on through a night and a day and another night. In the morning she woke and the room was too quiet. Ahmed is kneeling by the bed. He is praying and weeping at the same time; she has never seen him do both at once.

### R18. cp_layla.ahmed_conscripted

**Trigger:** `on_diplo_play_war_start` involving EGY, Ahmed alive, `cp_ahmed_at_war = 0`, first event of this war.
**Fires:** once per war.

**State change:**
- `cp_ahmed_at_war = 1`
- `cp_prev_anchor = <current marital anchor>`; `cp_set_anchor = soldiers_wife`
- `cp_shift_weight = { cp_w_war +3 cp_w_revolution +1 }`
- `cp_mark_hardship`
- if the war's primary enemy is OTT: `cp_shift_opinion = { ott -5 }`.
- if the war is fought in OTT's cause (Egypt `α` and enemy is OTT's enemy): `cp_shift_opinion = { ott +2 }` (a conflicted loyalty).

**Prose variants:**

- *Default.* Three men come up the path with papers. Ahmed stands very still while they read. He does not look at her. When they leave he sits on the bench by the door and does not move for a long time. She brings him water. He forgets to drink it.
- *Branch `B.α` (serf, still Ottoman).* They carry the Sultan's seal and the bey's cousin has told them Ahmed's name before they arrived. There is no negotiating with a decree from two empires at once.
- *Branch `A.β` (sovereign Egypt, landowning / tenant).* The paper bears an Egyptian seal she does not recognize from any other document of her life. Ahmed runs his hand over it as if to verify it is real. A state that did not exist when he was born is calling him to die for it.
- *Variant -- soldiers_wife already once before.* This is the second time. She does not cry this time. She cooks as if he is not leaving, and only when he is truly gone, truly walking away down the road, does she sit against the wall and hold her knees.

### R19. cp_layla.ahmed_returns

**Trigger:** war ends with EGY as participant, Ahmed not killed, `cp_ahmed_at_war = 1`.
**Fires:** once per war.

**State change:**
- `cp_ahmed_at_war = 0`
- `cp_set_anchor = cp_prev_anchor` (and clear)
- `cp_shift_weight = { cp_w_war +1 }` (he brought some of the war home)
- `cp_mark_joy`

**Prose variants:**

- *Default.* He walks up the path in the afternoon. Thinner. He holds her for a long time in the doorway, where the neighbors can see, and she lets them see. That night he sleeps so deeply she checks his breath three times.
- *Variant -- Ahmed wounded.* He walks with a stick now. The wound is in his leg; he does not speak of it. The first day he spends sitting on the stool watching the field he could once cross in six strides.

### R20. cp_layla.ahmed_dies

**Trigger:** war ends with casualties roll for Ahmed, or disaster/disease kills him. Layla alive.
**Fires:** once (terminal for Ahmed).

**State change:**
- `cp_widow = 1`, `cp_set_anchor = widow`, `cp_ahmed_at_war = 0`.
- `cp_shift_weight = { cp_w_war +3 cp_w_revolution +2 cp_hope -4 cp_w_religion +1 }`
- `cp_shift_opinion = { ott -10 }` if he died fighting against OTT; `{ ott +5 }` if he died in OTT service ("he was a martyr").
- `cp_mark_hardship` (hard, 18 months).
- eventify: a letter-bearing messenger event, or a neighbor bringing the news, depending on war distance.

**Prose variants:**

- *Default.* A neighbor comes to the door in the evening. He does not say anything for a long time, and she already knows. The letter is in his hand. It is addressed to her, in a hand she does not know. Her name spelled in a stranger's ink.
- *Branch `α` (still under Sultan).* The letter bears two seals, the Caliph's and the pasha's. It names him martyr. The word is meant to comfort. It does not.
- *Branch `β` (sovereign Egypt).* The letter bears one seal, the new one she has still not gotten used to. The name at the bottom is Egyptian and she has never heard it. He died for someone whose name she does not know.

---

## Migration

### R21. cp_layla.family_migrates_to_city

**Trigger:** weighted probability when `cp_land_anchor = wage_laborer_wife` or `tenant_wife` with debt flag, AND `cp_h3 = "Y"`, AND state urbanization pulling.
**Fires:** once.

**State change:**
- `cp_set_land_anchor = city_laborer`, `cp_in_city = 1`
- move her home-state variable to a city (Cairo or Alexandria by weight)
- `cp_shift_weight = { cp_w_economy +2 cp_w_labor_laws +2 cp_w_land_reform -1 cp_hope -1 }`
- `cp_shift_opinion` unchanged.
- `cp_mark_hardship`

**Prose variants:**

- *Default.* They pack what fits in a cart. The rest is left -- the copper pot that was her mother's, the low stool, the prayer mat by the window. The walk to the river takes half a day; the boat takes a day and a half. She does not sleep on the boat. She watches the shore retreat, then the shore arrive.

### R22. cp_layla.children_migrate

**Trigger:** weighted probability when `cp_h3 = "Y"`, children 16+, and Layla is in a rural anchor (not city).
**Fires:** per child.

**State change:**
- `cp_shift_weight = { cp_w_economy +1 cp_hope -1 }`
- no anchor move.
- `cp_children_in_city += 1` (new counter if eventify wants).

**Prose variants:**

- *Default.* The eldest goes first. He had been restless; he had heard the stories. In the morning he kisses her hand and Ahmed's hand and walks to the road. She watches him until he is a figure, and then a speck, and then nothing. The youngest cries. She does not.

### R23. cp_layla.husband_migrates_alone

**Trigger:** harvest crisis + weighted probability, `cp_ahmed_at_war = 0`, `cp_in_city = 0`, `cp_h3 = "Y"`.
**Fires:** once.

**State change:**
- `cp_ahmed_in_city = 1`
- no anchor move on Layla; she stays rural.
- `cp_shift_weight = { cp_w_economy +1 cp_hope -1 cp_w_war +1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* He will be back by harvest. He says this three times, in three different rooms of the house, on the night before he leaves. She nods each time. The harvest passes and he is not back. The next one does. He sends coins wrapped in paper, in a hand Mariam helps him write.

---

## War and conscription

### R24. cp_layla.war_declared

**Trigger:** `on_diplo_play_war_start` involving EGY.
**Fires:** once per war.

**State change:**
- `cp_shift_weight = { cp_w_war +1 }`
- `cp_mark_hardship` if the war is against a bordering power or against OTT.
- opinion deltas applied based on declared enemy; see specific rules in R18 for OTT cases.

**Prose variants:**

- *Default.* News of a war comes before the soldiers do. A man on a horse at the market. The imam is grave in the khutba. Mothers hold their older sons closer that week. Nothing has happened yet. The waiting has started.

### R25. cp_layla.war_drags_on

**Trigger:** a war involving EGY continues into its third year.
**Fires:** once per long war.

**State change:**
- `cp_shift_weight = { cp_w_war +2 cp_w_revolution +1 cp_hope -1 }`

**Prose variants:**

- *Default.* The war is now older than her youngest. A child born the month the name arrived walks and speaks and asks for bread, and still the news in the market is of the same campaign, the same names, as if a great wheel had begun to turn and could not find ground to stop on.

### R26. cp_layla.egypt_wins_war

**Trigger:** war ends, EGY on victor side.
**Fires:** once per war.

**State change:**
- `cp_shift_weight = { cp_w_war +1 }`
- `cp_shift_opinion = { egy +5 }` if Ahmed alive; `-5` if Ahmed dead.
- `cp_mark_joy` if Ahmed alive; else no mark.

**Prose variants:**

- *Default.* They say the war is won. The imam offers a special prayer. Men embrace in the square. She cannot tell if the victory is as tall as the cost, because she does not know the cost yet -- not until the names of the dead come back, over weeks, in letters and in silences.
- *Branch `β` fighting for sovereign Egypt.* The new flag is hung above the mosque door. The children in the street say its name as if it were a game. Ahmed stares at it for a long time after the prayer.

### R27. cp_layla.egypt_loses_war

**Trigger:** war ends, EGY on loser side.
**Fires:** once per war.

**State change:**
- `cp_shift_weight = { cp_w_war +1 cp_w_revolution +2 cp_hope -2 }`
- `cp_shift_opinion = { egy -8 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* They say the war is lost. No one knows what that means until the next market day, when the prices are wrong and the men with certain accents from the winning country are here, buying. The imam prays for patience. Patience is not a thing she is short on. She is short on bread.

### R28. cp_layla.soldiers_billet

**Trigger:** military event places troops in her state during wartime.
**Fires:** up to once per war.

**State change:**
- `cp_shift_weight = { cp_w_war +1 }`
- if troops are friendly: `cp_mark_hardship` soft (they eat the grain).
- if troops are foreign (occupying): `cp_mark_hardship` hard, `cp_shift_opinion = { <foreign tag> -10 }`.

**Prose variants:**

- *Default (friendly).* A company of soldiers sleeps in the mosque courtyard for a week. They eat. They drill at dawn. One of them is a boy from her cousin's village. He eats at her table once; she gives him the larger piece of bread.
- *Branch `α` (Ottoman soldiers billeting).* The officer is Anatolian and does not speak more than ten words of Arabic. He is polite. He pays for what he takes. He gives her eldest a small coin with the Sultan's seal and tells the boy to keep it for luck. The boy keeps it.
- *Branch `β` + foreign occupation.* The officer speaks to her through an interpreter and the interpreter does not translate all of what he says. Her grain bin is emptied and she is given a paper in exchange that she cannot read. Ahmed burns the paper that night.

### R29. cp_layla.conscription_quota

**Trigger:** state-level conscription event firing in her state, a son is 16+, `cp_ahmed_at_war` = 1 or 0.
**Fires:** per son per war.

**State change:**
- `cp_son_conscripted` counter increments.
- `cp_shift_weight = { cp_w_war +3 cp_w_revolution +1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* Her son is sixteen. They take him at the market. She runs after the cart for a hundred paces and she is forty-two now, she is not fast, and someone -- a neighbor, kindly -- holds her back before she falls.

---

## Epidemic and disaster

### R30. cp_layla.cholera_outbreak

**Trigger:** her state gets `harvest_condition disease_outbreak` or equivalent epidemic event.
**Fires:** per outbreak.

**State change:**
- per-family-member death rolls (children, Ahmed, Layla herself).
- `cp_shift_weight = { cp_w_religion +1 cp_hope -2 }`
- `cp_mark_hardship` hard.
- if any death: fires follow-on reactions (R17 for child, R20 for Ahmed, R50 for Layla).

**Prose variants:**

- *Default.* The neighbor's youngest goes first. Then the house across the lane. They burn rosemary in the courtyards and the imam's voice is hoarse from reciting the prayer for the dead. She keeps her children inside for ten days. When she lets them out, one is coughing.

### R31. cp_layla.flood

**Trigger:** flood harvest condition in her state (not the ordinary Nile flood; a destructive one).
**Fires:** per major flood.

**State change:**
- `cp_shift_weight = { cp_w_religion +1 cp_hope -1 cp_w_economy -1 }`
- `cp_mark_hardship` if severe.
- partial harvest lost (narrative -- real SoL handled by V3 economy).

**Prose variants:**

- *Default.* The river came higher than the old men remembered. The floor of the house held water for four days. The grain in the lower bin is ruined; Ahmed stood in the courtyard looking at it and she could see him calculating, the way he does, silently, how long they would last.

### R32. cp_layla.drought

**Trigger:** drought harvest condition in her state.
**Fires:** per drought year.

**State change:**
- `cp_shift_weight = { cp_w_religion +1 cp_hope -1 cp_w_economy -1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* The sky is white for weeks. The cotton buds that had come early do not open. At the well the line is long and the talk is the same talk. The imam leads a prayer for rain on a Friday, and on the next Friday, and on the one after that.

### R33. cp_layla.locust_year

**Trigger:** locust harvest condition in her state.
**Fires:** per locust event.

**State change:**
- `cp_shift_weight = { cp_w_religion +1 cp_hope -1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* They come out of the east in a line like weather. The sound is the sound of a great fire being fed. The field that had been green is brown by evening. She stands at the edge of it with Ahmed, and neither of them says anything for a long time.

### R34. cp_layla.village_fire

**Trigger:** random low probability during dry seasons.
**Fires:** rarely -- at most once in her life.

**State change:**
- if roll catches her house: possessions lost, `cp_mark_hardship` hard, possibly a child death roll.
- else: a neighbor's house; `cp_mark_hardship` light.

**Prose variants:**

- *Default (neighbor's house).* The cry goes up at midnight. Men run with buckets. She holds the youngest and stands in the lane watching the flame climb a wall that is not hers. Afterwards they help the neighbor sift the ash.

---

## Governance (non-hinge)

### R35. cp_layla.law_proposed

**Trigger:** a law proposal begins for a law whose topic weights highly for her (`cp_w_land_reform > 5` or `cp_w_labor_laws > 5` etc., depending on law group).
**Fires:** per relevant proposal.

**State change:**
- `cp_shift_weight = { cp_hope +1 }`
- temporary flag `cp_law_hope_pending = 1` until the proposal resolves.

**Prose variants:**

- *Default.* Word reaches the village from the market: they are talking about the land law in the capital again. She has heard this before. Twice. She lets herself hope in the private way she has learned to hope, where she does not tell Ahmed, in case it comes to nothing.

### R36. cp_layla.law_failed

**Trigger:** the proposal in R35 fails (or a reform law she cared about is voted down).
**Fires:** per failure.

**State change:**
- `cp_shift_weight = { cp_hope -2 cp_w_revolution +1 cp_w_land_reform +1 }` (she keeps caring; she stops trusting)
- `cp_mark_hardship` soft.
- clear `cp_law_hope_pending`.

**Prose variants:**

- *Default.* The word comes back: they did not pass it. A faction refused. A count was off. The reasons are elaborate and she does not follow them. What she follows is that the paper she had begun to imagine is not going to arrive.

### R37. cp_layla.revolution_starts

**Trigger:** `on_revolution_start` for EGY.
**Fires:** once per revolution.

**State change:**
- `cp_shift_weight = { cp_w_revolution +2 cp_w_war +1 cp_hope -1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* There has been shouting on the road for two weeks. Now there is smoke in the direction of the next town. Ahmed brings the children inside before noon. They all eat together without speaking. After the meal, he puts the cookpot back on its shelf with a care that is unlike him. Something is ending. She does not know yet what.

### R38. cp_layla.revolution_crushed

**Trigger:** a revolution ends without success; EGY government holds.
**Fires:** per crushed revolution.

**State change:**
- `cp_shift_weight = { cp_hope -3 cp_w_revolution +2 }`
- `cp_mark_hardship`
- opinion on EGY drops by -5 to -15 depending on repression severity (eventify: can key off how many pops killed in crushing).

**Prose variants:**

- *Default.* The names of the hanged are in the market for a week. Then the market returns to its older rhythms, prices, haggling, the occasional call to prayer from the mosque, as if the names had never been named. She buys onions. She buys bread. She goes home.

### R39. cp_layla.press_crackdown

**Trigger:** EGY passes a restrictive censorship law.
**Fires:** per law.

**State change:**
- `cp_hears_foreign_news = 0` (until a later liberalizing law restores it)
- `cp_shift_weight = { cp_hope -1 }`
- no prose mark if she is illiterate and rural -- a silent loss.

**Prose variants:**

- *Default.* The traveler at the mosque steps is not there this month. Nor the next. Mariam's letters have begun to arrive opened and retied. None of this reaches Layla as *news*; she only notices, over a year, that she knows less than she used to.

---

## Diplomacy and foreign

### R40. cp_layla.foreign_fleet_shells_port

**Trigger:** an EGY port is bombarded / attacked by a foreign naval event.
**Fires:** per incident.

**State change:**
- `cp_shift_opinion = { <foreign tag> -25 }` -- this hits regardless of info-flow gate; it is her country.
- `cp_shift_weight = { cp_w_war +2 cp_w_revolution +1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* The news comes up the river the slow way: smoke at the port, some number of dead, a foreign flag on a warship that had no business in the harbor. The children ask what a *warship* is. Ahmed does not answer. In the evening prayer the imam's voice shakes.

### R41. cp_layla.foreign_famine_aid

**Trigger:** a foreign GP delivers famine aid to EGY during a hunger event.
**Fires:** per aid event.

**State change:**
- `cp_shift_opinion = { <foreign tag> +15 }` (gated by `cp_hears_foreign_news`; without it she eats the grain without knowing whose it was).
- `cp_shift_weight = { cp_w_diplomacy +1 }`

**Prose variants:**

- *Default.* The grain sacks come up on the boats. There is writing on them in a language she cannot read. A man at the distribution says the word for the country that sent them. She holds the grain and thinks: this grew in a place where snow falls. That is a thing she knows only because a cousin once told her.

### R42. cp_layla.ally_signed

**Trigger:** EGY signs a major alliance.
**Fires:** per alliance.

**State change:**
- if ally is OTT and `cp_is_sultanate`: `cp_shift_opinion = { ott +5 }` (a confirmation).
- if ally is a foreign non-Muslim power and `cp_hears_foreign_news`: `cp_shift_opinion = { <tag> +8 }` but `cp_shift_weight = { cp_w_religion +1 }` (conflicted).

**Prose variants:**

- *Default.* The imam names a new ally in the khutba, asks for blessings on their friendship. She tries to place the name on a map she has never seen. It is a sound, not a place. Ahmed shrugs when she asks him, later, where it is.

### R43. cp_layla.rival_declared

**Trigger:** EGY declares rivalry with a major power.
**Fires:** per rivalry.

**State change:**
- `cp_shift_opinion = { <tag> -10 }` if `cp_hears_foreign_news`.
- `cp_shift_weight = { cp_w_war +1 }`

**Prose variants:**

- *Default.* A name circulates in the market for a month as an enemy. By the second month it is simply part of speech -- *those people*, said as if everyone had always known. She accepts it the way she accepts the weather.

---

## Family and Mariam

### R44. cp_layla.mariam_goes_silent

**Trigger:** a long gap in letters from Alexandria (model as: no Mariam pulse event fired for 24 months, or a press-crackdown reaction, or Alexandria has a crisis event).
**Fires:** once per silence episode.

**State change:**
- `cp_shift_weight = { cp_hope -1 cp_w_france -1 }` (Mariam is her main thread to the wider world).
- `cp_mark_hardship` soft.

**Prose variants:**

- *Default.* Two years of no letters. She does not know if Mariam is dead or only quiet. She asks travelers at the market who have been to the port. None of them know a Mariam. She wonders if she is remembering her cousin correctly, if the face in her head is still the face.

### R45. cp_layla.mother_dies

**Trigger:** automatic, roughly 15-20 years after game start (Layla's mother would be ~60+); or earlier if epidemic hits her mother's village.
**Fires:** once.

**State change:**
- `cp_shift_weight = { cp_w_religion +1 cp_hope -1 }`
- `cp_mark_hardship`

**Prose variants:**

- *Default.* The message comes from her brother by a traveler. She walks the half day to her mother's village with Ahmed beside her. The body is washed by hands she remembers from her childhood. She helps. Her mother weighed so little.

### R46. cp_layla.ahmeds_uncle_dies

**Trigger:** narrative trigger, roughly 10-15 years in, OR the uncle was a minor character in prior pulse events and a war/famine kills him.
**Fires:** once.

**State change:**
- no branch move.
- `cp_shift_weight = { cp_w_war +1 cp_hope -1 }` (the uncle was the family's living link to the old Sultan's armies).
- `cp_mark_hardship` soft.

**Prose variants:**

- *Default.* The uncle had always been the one to speak of the Sultan's armies, in that voice men reserve for wars they fought before they had children. He dies in his sleep in the village he had returned to. Ahmed weeps at the grave without sound.
- *Branch `β` (sovereign Egypt).* The uncle's stories were Ottoman stories. They are harder to tell, now, in a country where the prayer names a different ruler. He dies unheard, in a room where no one is listening.

---

## Economy

### R47. cp_layla.cotton_bust

**Trigger:** EGY's cotton-export price crashes, or a trade-route disruption event fires.
**Fires:** per crash (usually once or twice per campaign).

**State change:**
- `cp_shift_weight = { cp_w_economy +2 cp_hope -1 }`
- `cp_mark_hardship`
- if `cp_land_anchor = wage_laborer_wife`: weight double (her wage depends directly).

**Prose variants:**

- *Default.* The price of cotton at the market is half what it was last season. Ahmed walks back from the gin with an expression she has learned to recognize. He does not say anything. He puts the coin on the shelf by the door. It is too light.

### R48. cp_layla.new_tax_assessment

**Trigger:** EGY enacts a new tax law or a new assessment cycle fires.
**Fires:** per assessment.

**State change:**
- `cp_shift_weight = { cp_hope -1 cp_w_economy +1 }`
- if the new tax is regressive: `cp_shift_opinion = { egy -5 }`.

**Prose variants:**

- *Default.* The tax collector has a new set of numbers. He writes them in a book and reads them aloud and Ahmed pays. He always pays on the first day. *Do not make them come back*, he says, the same sentence he has said since they were first married.

---

## Closure

### R49. cp_layla.closure_natural

**Trigger:** `cp_anchor = "elder"` (or `widow` + age band elder) and yearly death roll succeeds. Or age 78+ automatic.
**Fires:** once. Terminal.

**State change:**
- `cp_set_anchor = dying` at start, then fires the scene, then marks her dead.
- successor spawn: if eldest daughter alive, save her as `cp_fatima` and optionally promote to her own character in a later update; else no successor.
- fires a legacy mini-event 30 days later keyed off `(cp_h1, cp_h2, cp_h3, cp_land_anchor, cp_widow)` to determine *which* legacy scene: grandchild in her field / grandchild in a factory / grandchild a nationalist agitator / grandchild emigrated / land sold to a foreign company / an empty room.

**Prose variants:**

- *Default.* She is old. She knows the morning before the morning she does not wake. The light comes through the window the way it did when she was a bride. Ahmed is not here -- or he is here and she is here too, somewhere that is not this room. The call to prayer begins. She does not rise.
- *Branch `α.X` (still Ottoman, traditional village).* The Sultan's name is in the muezzin's voice as she hears it for the last time. It is the same name the imam named when she was eight years old and her mother had held her in the courtyard. The world ends as it began.
- *Branch `β.Y` (sovereign Egypt, industrial).* The muezzin's voice is pitched over the hum of something mechanical in the distance -- a factory, or a train, or a thing she has never had a word for. The name in the prayer is the new name. Her life has been a bridge between two languages of the same faith.
- *Branch `B.α` (serfdom endured, still Ottoman).* The bey's son rides past in the road that morning. The dust comes up as it has come up for all of her life. She turns her face away from it for the last time.
- *Branch `A.H.β.X` (held a deed, sovereign Egypt, world stayed simple).* The paper is still in the chest. Ahmed's name in her husband's hand. The deed is all that is happening, in the end. It is enough.

### R50. cp_layla.closure_childbirth

**Trigger:** childbirth roll fatal (see R16). Layla dies in childbirth.
**Fires:** once. Terminal (rare, early-campaign-weighted).

**State change:**
- marks her dead.
- no successor spawn (the child may or may not have survived; eventify decides).
- fires a legacy scene: the midwife's hands, Ahmed in the courtyard, the grave in the old cemetery.

**Prose variants:**

- *Default.* The labor was two days long. The midwife did everything she knew. Ahmed is outside the door and has been outside the door and will not come in when the midwife comes out with her hands washed. The child -- lives, or does not, the save will decide. Layla does not. The last thing she sees is the beam of the ceiling, and it is the one her father helped raise.

---

## Notes for the eventify pass

- Every state change above is a call to a scripted effect named in `anchors.md` §6. No reaction writes `set_variable` directly in its effect block -- it calls `cp_set_anchor`, `cp_resolve_h1`, `cp_shift_weight`, etc.
- Prose variants localize as separate keys (`cp_layla.ahmed_conscripted.default`, `cp_layla.ahmed_conscripted.B_alpha`, etc.) and the event's `option.name` / `desc` pick via a series of `triggered_desc` blocks.
- All reactions that could fire repeatedly (cholera, war, drought) must guard against firing more than once inside a short cooldown window. Cooldowns live in the eventify pass's scripted-effects library.
- Reactions that set branch letters must guard that `cp_h1` / `cp_h2` / `cp_h3` is unset, except rollback reactions which require it set.
- The closure reactions (R49, R50) need a 30-day follow-up event whose trigger reads the final state tuple and selects from ~8 legacy scenes. These follow-ups are not counted in the 50-reaction budget.

*Next: `pulse.md` -- the ~100 vignettes that fill each anchor pool.*
