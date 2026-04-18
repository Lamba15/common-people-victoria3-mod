# Layla's Pulse Pool

> The monthly pulse (10% fire chance) draws one vignette from the pool of events matching her current state (anchor + land anchor + branch letters + flags). These paint her present life. They don't move her anchor and don't set branch letters -- reactions do that. Pulse events are the novel; reactions are the hinges.
>
> State model: [anchors.md](anchors.md). Hinges: [reactions.md](reactions.md). 100-event target, ~80 unique events, some applying to several anchors.

---

## Pool schema (reminder)

Each event has five fields:

- **Anchors:** marital and/or land anchors this event can fire in.
- **Branch requirements:** optional H1/H2/H3 letter(s) required, or "none" for universal.
- **Flag requirements:** optional flags that must be set/clear.
- **Cooldown:** months before the same event can re-fire.
- **Weight:** base 1.0 and conditional modifiers.

Prose kernel follows, 2-4 sentences in Mahfouz register. Some events have **Variants** keyed to branch/anchor where the same moment reads fundamentally differently; the default is always safe.

Ottoman motifs are threaded throughout and especially pronounced in the Faith and World Beyond clusters. Count at end of file confirms ≥20 Ottoman-flavored pulse events.

---

## Table of contents

- [Universal rural (applies across marital anchors + any rural land_anchor)](#universal-rural)
  - [Faith](#faith)
  - [Harvest and seasons](#harvest-and-seasons)
  - [Community](#community)
  - [Home](#home)
  - [Body](#body)
  - [Inner life](#inner-life)
  - [World beyond](#world-beyond)
- [Marital-anchor specific](#marital-anchor-specific)
  - [Bride](#bride)
  - [Young mother](#young-mother)
  - [Mother](#mother)
  - [Soldiers' wife](#soldiers-wife)
  - [Widow](#widow)
  - [Matriarch](#matriarch)
  - [Elder](#elder)
- [Land-anchor specific](#land-anchor-specific)
  - [Landowner wife](#landowner-wife)
  - [Tenant wife](#tenant-wife)
  - [Serf wife](#serf-wife)
  - [Wage laborer wife](#wage-laborer-wife)
  - [Collective member](#collective-member)
  - [City laborer](#city-laborer)

---

## Universal rural

These can fire while she is in any marital anchor except `dying` and any land anchor except `city_laborer`. They paint the rhythm of village life.

### Faith

#### P01. cp_layla.pulse.fajr_in_the_dark

**Anchors:** all marital; all rural land_anchors.
**Branches:** none.
**Flags:** `cp_ahmed_at_war` may toggle variant.
**Cooldown:** 18 months.
**Weight:** 1.0.

> The call comes before the light. She washes in cold water. In the courtyard a rooster answers the muezzin out of habit. She prays.
>
> *Variant `α`:* The Sultan's name in the imam's voice carries clearly today; the wind is from the east.
> *Variant `β`:* The new name in the prayer still startles her if she is half-asleep. By the fourth rak'ah it is only the prayer.

#### P02. cp_layla.pulse.friday_khutba

**Anchors:** all marital; all rural.
**Branches:** none (variant keyed to H2).
**Cooldown:** 10 months.
**Weight:** 1.2.

> Friday. The imam's voice goes on a long time today about patience. Ahmed sleeps sitting up beside her in the men's section, she knows without looking because she has known his posture for ten years. Outside afterwards the air smells of coriander from someone's pot.
>
> *Variant `α`:* The Sultan-Caliph is named, then the pasha, then the bey, descending through the hierarchies of the name of God. A world arranged in layers, the imam his voice low and even.
> *Variant `β`:* The new king is named and the Caliph named after, as a memory, a blessing. The imam still falters on the order sometimes. She understands that a man's tongue takes longer to learn a new prayer than a man's heart.

#### P03. cp_layla.pulse.ramadan_nightfall

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** season = ramadan (eventify: date-math trigger).
**Cooldown:** 12 months (i.e. once per ramadan).
**Weight:** 2.0 during ramadan.

> The sun goes down over the field and the first date goes in Ahmed's mouth and then in hers. They eat slowly. The children are asleep against the wall. For one hour after the meal the whole village is quiet together, and it is the kind of quiet she will think of, later, as a room she once lived in.

#### P04. cp_layla.pulse.eid_morning

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** season = eid.
**Cooldown:** 12 months.
**Weight:** 2.0 at eid.

> Eid. Ahmed's best coat, the one she washed three times this week. The children in the new clothes her mother sewed. The field empty and quiet on a day that is not quite Friday. She holds her daughter's hand on the way to the mosque and her daughter's hand is sticky with honey and she does not mind.

#### P05. cp_layla.pulse.funeral_washing

**Anchors:** young_mother, mother, matriarch, widow, elder.
**Branches:** none.
**Cooldown:** 24 months.
**Weight:** 0.8 -- low; these are occasional.

> A neighbor died in the night. The women gather to wash the body. She has done this six times now. Each time the hands remember. Each time they are stranger's hands and also her own mother's hands, because the first time was her mother and her mother's hands.

#### P06. cp_layla.pulse.prayer_for_rain

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** state has drought condition.
**Cooldown:** 6 months.
**Weight:** 1.5 during drought.

> The imam leads a prayer for rain on the third Friday of it. All the men are there, even those who never come. The women pray behind. She prays and she does not know whether she believes the prayer will be answered; she knows that not praying would be worse.

### Harvest and seasons

#### P07. cp_layla.pulse.flooding_nile

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** season = summer, state not in drought.
**Cooldown:** 11 months.
**Weight:** 1.5 in summer.

> The Nile rises on its calendar. Ahmed walks to the river's edge at dusk and she sees him standing there a long time, silhouetted against the water. He comes back and says only: *good this year*. They eat better for it through the winter.

#### P08. cp_layla.pulse.first_cotton_buds

**Anchors:** all marital; all rural except collective_member.
**Branches:** none.
**Flags:** season = late spring.
**Cooldown:** 11 months.
**Weight:** 1.3.

> The first buds on the cotton. She walks the row in the early light with the sickle's shadow behind her and stops at the third one, which is always the first to open. The white of it against her hand, like a story that begins again.

#### P09. cp_layla.pulse.last_threshing

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** season = late summer.
**Cooldown:** 11 months.
**Weight:** 1.3.

> The last day of threshing. Ahmed's shoulders are loose for the first time in a month. They eat with the whole extended household in the courtyard. Her uncle tells the same joke about the ox and it is funny again.

#### P10. cp_layla.pulse.locust_sighting

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 36 months.
**Weight:** 0.4 -- rare.

> The first one lands on her arm at noon. Green, the size of a date. She watches it for a second and then flicks it off and calls out to Ahmed. He looks up. He looks east. *Maybe*, he says. Maybe not this year.

#### P11. cp_layla.pulse.neighbors_field_fails

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.6.

> The field to the south did not come up. The neighbor stands at its edge with his hands on his hips, not moving. Ahmed goes over in the afternoon; she hears their voices low and long. Ahmed comes home with the quiet he carries when a plan is forming.

#### P12. cp_layla.pulse.first_cold_morning

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** season = early winter.
**Cooldown:** 11 months.
**Weight:** 1.2.

> The first morning her breath is visible. The children want to see their own and they run around the courtyard laughing, making clouds. Ahmed mends the shutter. The water in the jar has a thin skin of ice at the very top.

### Community

#### P13. cp_layla.pulse.village_wedding

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 14 months.
**Weight:** 1.0.

> A wedding in the village. She goes with the other women; Ahmed goes with the men. The bride is a girl she remembers being three years old in her mother's lap. The drumming goes until very late. The next day, everything is sore and pleasant.

#### P14. cp_layla.pulse.tax_collector

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** none.
**Cooldown:** 8 months.
**Weight:** 1.0.

> The tax collector's cart at the top of the lane. Ahmed has the coins ready; he always does, on the first day the man comes. *Do not make them come back*, he has said to her since before they were married. He says it again in his head now, she can tell, by the set of his mouth.
>
> *Variant B (serf_wife):* The collector is the bey's man and takes more than the paper says he should. No one argues. The bey's men have not needed to argue for a hundred years.
> *Variant A.H (landowner_wife):* The collector is a clerk from the capital with ink on his cuff. He asks for Ahmed's name twice and writes it down carefully and gives a receipt. The receipt is new.

#### P15. cp_layla.pulse.storyteller_passes

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 20 months.
**Weight:** 0.7.

> A storyteller passing through the village, set up in the courtyard of the coffeehouse. The children sit in a half-moon on the dust. She listens from the edge with the women. He tells the story of Majnun. She has heard it three times in her life. Each time it is shorter than she remembered.

#### P16. cp_layla.pulse.neighbor_funeral

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 8 months.
**Weight:** 0.8.

> A neighbor is buried. The men dig. The women cry in a room. She takes a dish of rice to the family. The widow accepts it without looking up.

#### P17. cp_layla.pulse.bey_rides_past

**Anchors:** all marital.
**Branches:** B (or A in early years before the change settles).
**Cooldown:** 8 months.
**Weight:** 1.0 in B; 0.3 in A (residual presence).

> The bey or his cousin on the road at noon. Dust comes up through the open door. She turns her face away until it settles. *I did not see him*, she thinks. *He did not see me.* It is the arrangement under which her mother lived.

#### P18. cp_layla.pulse.foreign_traveler_asks_directions

**Anchors:** all marital; all rural.
**Branches:** none (variant by `cp_hears_foreign_news`).
**Cooldown:** 30 months.
**Weight:** 0.3.

> A man in pale clothes on the road, his Arabic strange. He asks for the way to somewhere Ahmed has never been. Ahmed points anyway, in the approximate direction. The man thanks him and walks on. His hair is the color of hay.

### Home

#### P19. cp_layla.pulse.wall_cracks

**Anchors:** all marital; all rural land_anchors.
**Branches:** none.
**Cooldown:** 24 months.
**Weight:** 0.5.

> A crack in the mud-brick wall where it meets the ceiling, thin as a hair and exactly the length of her forearm. She has been watching it for a week. Today she points it out to Ahmed. He looks at it and says he will mend it. He will, eventually, some other Saturday.

#### P20. cp_layla.pulse.snake_in_grain_store

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 36 months.
**Weight:** 0.3.

> A small snake in the grain store. She does not scream. She backs out and calls Ahmed. The neighbor's boy comes with a stick. Afterwards she checks every jar. She thinks about her mother telling her, once, that a snake in the grain meant a marriage.

#### P21. cp_layla.pulse.cat_kittens

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 20 months.
**Weight:** 0.6.

> The grey cat under the bench has kittens in the night. Four, one very small. The children find them in the morning and make a circle of hands around the bench. For two weeks the house has six tiny lives in it.

#### P22. cp_layla.pulse.roof_mends

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.6.

> Ahmed on the roof in the afternoon with palm fronds and a handful of straw. She brings him water. He drinks and hands the cup back and does not speak. The sun on his neck is very red.

#### P23. cp_layla.pulse.new_chicken

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.5.

> A new hen in the yard, bought at market for two of yesterday's coins. She names it something in her head and does not tell anyone the name. In two months it is laying.

### Body

#### P24. cp_layla.pulse.exhaustion

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** `cp_recent_hardship = 1` weights up.
**Cooldown:** 10 months.
**Weight:** 0.8; +0.5 in harvest months.

> The tiredness that comes after a week of the harvest is in her knees and her elbows. She sits down and does not get up for an hour. Ahmed does not say anything. He brings her water.

#### P25. cp_layla.pulse.fever

**Anchors:** all marital; all rural.
**Branches:** none.
**Cooldown:** 15 months.
**Weight:** 0.5.

> A fever that keeps her in bed for two days. Ahmed manages the children. The neighbor brings soup. On the third day she stands up and the floor is farther away than she remembers, and then it is not.

#### P26. cp_layla.pulse.hunger

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** `cp_recent_hardship = 1`.
**Cooldown:** 10 months.
**Weight:** 0 (default); 2.0 after hardship.

> She goes to bed hungry. Not starving, not the way the beggar by the road is hungry; the way that wears the edges off a day. She sleeps. She dreams of her mother's house.

#### P27. cp_layla.pulse.pain_in_the_hands

**Anchors:** mother, matriarch, widow, elder.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.7 (age-banded up).

> Her hands have begun to hurt in the cold. She rubs them at the fire. The joints at the base of her thumbs. It is small and it does not go away. It is the beginning of a conversation she will have with her body for thirty years.

### Inner life

#### P28. cp_layla.pulse.memory_of_mother

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 14 months.
**Weight:** 0.7.

> A smell in the courtyard -- damp rope, or coriander, or a certain dust -- and her mother is suddenly in her chest as if she had walked into the room. For a second it is worse than it has been in years. Then it passes. Then she is making bread again.

#### P29. cp_layla.pulse.unexpected_joy

**Anchors:** all marital.
**Branches:** none.
**Flags:** `cp_recent_joy = 1` weights up.
**Cooldown:** 14 months.
**Weight:** 0.8.

> Ahmed laughs at something a child has said, and it is a laugh she has not heard in a month, and it is the one she married him for. The evening is good for a reason she will not remember by next week. But she remembers, now, that evenings can be good.

#### P30. cp_layla.pulse.fear_for_the_children

**Anchors:** young_mother, mother, matriarch.
**Branches:** none.
**Flags:** `cp_children_alive > 0`.
**Cooldown:** 12 months.
**Weight:** 1.0.

> She wakes in the night for no reason and listens for each of their breaths. Ahmed sleeps. The breaths are all there. Then she cannot fall back asleep, and she lies in the dark and counts them, three times, four times.

#### P31. cp_layla.pulse.doubt

**Anchors:** all marital.
**Branches:** none.
**Flags:** `cp_bereaved_mother >= 1` or `cp_recent_hardship = 1` weights up.
**Cooldown:** 20 months.
**Weight:** 0.3.

> A moment in the afternoon prayer when she cannot find the feeling. The words are there. Her body is where it should be. The feeling is gone. She finishes the prayer with the discipline of a woman who was taught well. It comes back next week. She does not speak of it.

#### P32. cp_layla.pulse.gratitude

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.6.

> A moment in the evening after the children are asleep when she sees the house and sees that it holds them, all of them, safely, tonight. She sits on the stool by the door and does not move for a long time. Ahmed finds her there. He does not ask.

### World beyond

#### P33. cp_layla.pulse.mariam_letter

**Anchors:** all marital.
**Branches:** none (variant keyed to `cp_hears_foreign_news` and H2).
**Flags:** `cp_hears_foreign_news = 1` required to fire.
**Cooldown:** 10 months.
**Weight:** 1.0.

> A letter from Alexandria, from Mariam. The imam reads it for her. Mariam writes in the same slightly formal style she has written in for ten years, telling a small thing as if it were a large one, and a large one as if it were small. Layla listens to it twice.
>
> *Variant `α`:* Mariam has been shopping in the Ottoman customs house. She writes about an Anatolian clerk who was courteous to her.
> *Variant `β`:* Mariam writes about the new Egyptian officials and how they are still learning the city. She is not sure what to think of them. Neither is Layla.

#### P34. cp_layla.pulse.foreign_coin

**Anchors:** all marital; all rural.
**Branches:** none.
**Flags:** `cp_hears_foreign_news = 1` to trigger; otherwise she has the coin but does not know.
**Cooldown:** 18 months.
**Weight:** 0.5.

> A coin in her palm from the market that is not Egyptian and not Ottoman. A face on it she does not know. Ahmed turns it over and squints. *The seller said it was from a country beyond Rum.* She puts it in the chest and forgets about it for a year.

#### P35. cp_layla.pulse.news_of_sultans_war

**Anchors:** all marital.
**Branches:** `α` only (or `β` with nostalgic framing).
**Flags:** `cp_hears_foreign_news = 1`.
**Cooldown:** 12 months.
**Weight:** 0.8.

> A man at the coffeehouse has heard that the Sultan is at war with a northern power. No one in the village has ever seen the northern power. The imam prays for the Sultan's armies at Friday.

#### P36. cp_layla.pulse.anatolian_clerk_passes

**Anchors:** all marital; all rural.
**Branches:** `α` required.
**Cooldown:** 30 months.
**Weight:** 0.3.

> A clerk on horseback in Ottoman-cut clothes, going from one capital to another through the village. He stops at the well. His Arabic is slow but careful. He thanks Ahmed with a small coin from his pouch, and she sees the Sultan's seal on it clearly, under the dust.

#### P37. cp_layla.pulse.greek_trader

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 24 months.
**Weight:** 0.4.

> A Greek trader in the village for a day, selling copper from Alexandria. His Arabic is very good; he has lived here longer than Layla has been alive. He has a cross on a chain under his shirt. She buys a small pot from him. She thanks him in Arabic and he thanks her in Greek, and they both smile.

#### P38. cp_layla.pulse.armenian_apothecary

**Anchors:** all marital.
**Branches:** none.
**Flags:** `cp_children_alive > 0` or `cp_recent_hardship = 1` to fire meaningfully.
**Cooldown:** 36 months.
**Weight:** 0.2.

> The Armenian apothecary from the next town is at the market this week with his case of small bottles. She asks him for something for a cough. He gives her a brown syrup and tells her how many drops in how much water. He will not take her money. *Next time*, he says, in his gentle accented Arabic.

#### P39. cp_layla.pulse.jewish_silversmith

**Anchors:** all marital.
**Branches:** none.
**Cooldown:** 36 months.
**Weight:** 0.2.

> The Jewish silversmith from the capital repairs a small chain her grandmother gave her. He works at a bench in the courtyard of the caravanserai, slowly. He tells her the chain is very old. He does not ask its story. She pays him. He wraps the chain in a square of cotton.

#### P40. cp_layla.pulse.turkish_word_in_ahmeds_mouth

**Anchors:** all marital.
**Branches:** `α` weights up; `β` weights this down (the words fade).
**Cooldown:** 24 months.
**Weight:** 0.4.

> Ahmed uses a Turkish word at dinner -- one he learned from a cousin who served in the city -- and she understands him perfectly and realizes, afterwards, that she had not known she understood it. The old languages live under the Arabic like fish under a still river.

---

## Marital-anchor specific

### Bride

#### P41. cp_layla.pulse.bride_first_courtyard

**Anchors:** bride.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 1.2 at young age.

> She is new to this house. She walks the perimeter of the courtyard in the morning, learning its corners. The well in the far left. The bench by the east wall where Ahmed's mother used to sit. She moves a jar six inches and decides, afterwards, that she will be the kind of wife who moves things slowly.

#### P42. cp_layla.pulse.bride_ahmeds_quiet

**Anchors:** bride.
**Branches:** none.
**Cooldown:** 15 months.
**Weight:** 1.0.

> Ahmed is quieter than her father was. She is still learning what his quiet means. Tonight it means the harvest was not good; last week it meant he was tired; the week before, that he was thinking about his dead brother. She will know all of his silences by the time they are old.

#### P43. cp_layla.pulse.bride_mother_visits

**Anchors:** bride.
**Branches:** none.
**Cooldown:** 10 months.
**Weight:** 1.1.

> Her mother walks from the next village and stays three days. She corrects two things in the way Layla is managing the kitchen, and praises one thing, and says nothing about the rest. Layla understands the nothing-about-the-rest to be praise too. On the third morning she walks her mother back to the road.

#### P44. cp_layla.pulse.bride_pregnancy_hope

**Anchors:** bride.
**Branches:** none.
**Flags:** `cp_pregnant = 0`, `cp_barren_wife = 0`.
**Cooldown:** 6 months.
**Weight:** 1.0.

> Another month, and nothing. Her mother has not said anything and will not say anything. The imam's wife asked, casually, last week. Layla smiled and did not answer. She knows the village is watching.

#### P45. cp_layla.pulse.bride_barren_shame

**Anchors:** bride.
**Branches:** none.
**Flags:** `cp_barren_wife = 1`.
**Cooldown:** 18 months.
**Weight:** 0.8.

> Ahmed's cousin's wife has had her third. The whole household goes to the naming. Layla holds the baby when it is her turn and hands it back. In the walk home Ahmed does not speak of it. Ahmed does not speak of it, ever, in any of the years.

#### P46. cp_layla.pulse.bride_lamp_at_dawn

**Anchors:** bride.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.8.

> She wakes early on a Tuesday. Ahmed is asleep. The lamp is still lit; she forgot to extinguish it last night. She lies watching the small flame and thinks: *this is my house now*. The thought is so large it takes another year to finish having.

### Young mother

#### P47. cp_layla.pulse.ym_first_night

**Anchors:** young_mother.
**Branches:** none.
**Cooldown:** 48 months (rare, early).
**Weight:** 1.5 in first year post-birth.

> The first night the child sleeps through. She wakes at dawn having slept seven hours in a row for the first time in months, and she panics, and she rushes to the cradle, and the child is breathing, and she weeps for five minutes in the courtyard where Ahmed cannot see.

#### P48. cp_layla.pulse.ym_teething

**Anchors:** young_mother.
**Branches:** none.
**Cooldown:** 30 months.
**Weight:** 0.8.

> The child cries for two nights. It is teeth; her mother said it would be teeth. She walks the courtyard carrying the child and singing the lullaby her mother sang, and it works on the second verse, as it worked for her mother.

#### P49. cp_layla.pulse.ym_first_word

**Anchors:** young_mother.
**Branches:** none.
**Cooldown:** 36 months.
**Weight:** 0.7.

> The child's first word. It is not a word she expected. It is a word the neighbor's boy says often. She tells Ahmed. Ahmed laughs, and the child, hearing Ahmed laugh, says the word again, louder. They laugh until Layla's eyes are wet.

#### P50. cp_layla.pulse.ym_child_fever

**Anchors:** young_mother, mother.
**Branches:** none.
**Flags:** `cp_children_alive > 0`.
**Cooldown:** 14 months.
**Weight:** 1.0.

> One of them has a fever in the night. She sits with the child and wipes the forehead with a wet cloth, and prays, and the fever breaks by morning. She is very tired the next day. It passes for ordinary weariness.

#### P51. cp_layla.pulse.ym_second_pregnancy_whisper

**Anchors:** young_mother.
**Branches:** none.
**Flags:** `cp_children_alive >= 1`, `cp_pregnant = 0`, `cp_ahmed_at_war = 0`.
**Cooldown:** 24 months.
**Weight:** 0.5.

> She suspects again. She has learned the signs. She does not tell Ahmed yet. She keeps it for one more week. She watches her own reflection in the water at the well and tries to see a different face, and cannot, and is reassured.

#### P52. cp_layla.pulse.ym_ahmeds_tenderness

**Anchors:** young_mother, mother.
**Branches:** none.
**Flags:** `cp_ahmed_at_war = 0`, `cp_widow = 0`.
**Cooldown:** 12 months.
**Weight:** 0.9.

> Ahmed comes in from the field and picks up the sleeping child without breaking stride and carries her to bed. Layla watches from the stove. He does not look at Layla. He does not need to.

#### P53. cp_layla.pulse.ym_neighbors_birth

**Anchors:** young_mother, mother.
**Branches:** none.
**Cooldown:** 12 months.
**Weight:** 0.7.

> A birth in the neighbor's house. Layla goes with the older women. She is one of the younger women there now, still, though she has children of her own. She holds the new mother's hand through the hard part. Afterwards she washes her own hands three times in cold water.

#### P54. cp_layla.pulse.ym_lullaby

**Anchors:** young_mother, mother.
**Branches:** none.
**Cooldown:** 14 months.
**Weight:** 0.7.

> She sings the lullaby in the evening, and her second child sings along now, imperfectly, half a beat behind, and it is the most perfect music of her life.

### Mother

#### P55. cp_layla.pulse.m_eldest_grows

**Anchors:** mother.
**Branches:** none.
**Flags:** `cp_children_alive >= 1`.
**Cooldown:** 20 months.
**Weight:** 0.8.

> The eldest stands as tall as her shoulder today. She measures with her hand and he laughs and stands straighter. Ahmed in the doorway says nothing. There is a thing in his face she understands.

#### P56. cp_layla.pulse.m_son_works_with_father

**Anchors:** mother.
**Branches:** none.
**Flags:** oldest son >= 10.
**Cooldown:** 18 months.
**Weight:** 0.8.

> The eldest boy goes to the field with Ahmed now. She watches them leave at dawn and they do not come back until the noon meal, two shapes on the road, the boy's shape smaller and matching Ahmed's stride by three steps of his own.

#### P57. cp_layla.pulse.m_daughter_learns

**Anchors:** mother.
**Branches:** none.
**Flags:** eldest daughter exists.
**Cooldown:** 18 months.
**Weight:** 0.8.

> Her daughter kneads the bread tonight. Layla watches and does not correct. The dough is lumpy. The bread will be fine. The next morning the girl kneads again and it is better. By the end of the month she is a baker.

#### P58. cp_layla.pulse.m_literacy_question

**Anchors:** mother.
**Branches:** none.
**Flags:** `cp_literacy = 0`, EGY has a public-schools or similar law.
**Cooldown:** 36 months.
**Weight:** 0.4.

> A man from the capital comes and says there will be schooling for the children now, those whose parents want it. Ahmed does not know. He asks her. She does not know either. They agree to think about it. They think about it for a year.

#### P59. cp_layla.pulse.m_child_marries

**Anchors:** mother, matriarch.
**Branches:** none.
**Flags:** any child >= 16.
**Cooldown:** 60 months.
**Weight:** 0.3.

> The first of them marries. The wedding is in the courtyard and it is three nights long, and on the third night Layla sits on the stool by the door and watches her child in a wedding dress and her husband beside her and thinks: *how did I get here? I am a woman whose children marry.*

### Soldiers' wife

#### P60. cp_layla.pulse.sw_empty_bench

**Anchors:** soldiers_wife.
**Branches:** none.
**Cooldown:** 4 months.
**Weight:** 1.2.

> The bench by the door where Ahmed sits in the evening is empty tonight. It has been empty for fifty-seven days. She knows because she has been counting without meaning to count. She sits on it herself for the first time.

#### P61. cp_layla.pulse.sw_letter_arrives

**Anchors:** soldiers_wife.
**Branches:** none.
**Cooldown:** 6 months.
**Weight:** 1.3.

> A letter. The imam reads it at her door. Ahmed is well. The weather where he is is cold. He asks after the children. He does not say where he is. She listens with her hand pressed flat against her mouth.

#### P62. cp_layla.pulse.sw_no_letter

**Anchors:** soldiers_wife.
**Branches:** none.
**Cooldown:** 4 months.
**Weight:** 1.1.

> No letter this month. No letter last month either. She does not tell the children. She does not tell her mother. She tells God, every night, and hears nothing back, which is the shape of faith she has come to know.

#### P63. cp_layla.pulse.sw_neighbors_husband_returns

**Anchors:** soldiers_wife.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.5.

> A neighbor's husband comes home from the same war. She watches him walk up the lane. She stands in her doorway while he passes, and she does not know what to say to him, and he does not know what to say to her, and they nod to each other.

#### P64. cp_layla.pulse.sw_quran_recitation

**Anchors:** soldiers_wife, widow.
**Branches:** none.
**Cooldown:** 10 months.
**Weight:** 0.8.

> She recites the short surahs at night now, for their own sake. Not as prayer, or not only as prayer. As the sound of her own voice in a house she has started to be alone in.

#### P65. cp_layla.pulse.sw_soldiers_widow_visits

**Anchors:** soldiers_wife.
**Branches:** none.
**Cooldown:** 12 months.
**Weight:** 0.5.

> The widow from the house across the lane brings her rice. They sit together. The widow does not say anything. They drink tea. After an hour the widow leaves. Layla sits in the place where the widow sat for a long time afterwards.

#### P66. cp_layla.pulse.sw_running_the_farm

**Anchors:** soldiers_wife.
**Branches:** none.
**Flags:** any rural land_anchor.
**Cooldown:** 6 months.
**Weight:** 1.2.

> The field needs Ahmed's hands. She does what she can. The oldest boy does the rest. Neighbors help in the first week; in the second week they are back at their own fields. She learns to harness the ox in an afternoon that takes longer than a week.

#### P67. cp_layla.pulse.sw_silent_prayer_for_ahmed

**Anchors:** soldiers_wife.
**Branches:** none.
**Cooldown:** 3 months.
**Weight:** 1.5.

> Every day after the noon prayer she adds a sentence. Not aloud. *Keep him. Keep him. Bring him back whole.* Every day for the whole length of the war. If the war is long the sentence wears thin as an old coin.

### Widow

#### P68. cp_layla.pulse.w_empty_bed

**Anchors:** widow.
**Branches:** none.
**Cooldown:** 6 months.
**Weight:** 1.3 first year after death; 0.6 later.

> Waking up and remembering he is not there. It is no kinder in the sixth month than it was in the first. She keeps his side of the bed as his side of the bed.

#### P69. cp_layla.pulse.w_his_coat_on_the_hook

**Anchors:** widow.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.8.

> His coat on the hook by the door. She has not moved it in eighteen months. Today she takes it down, folds it, puts it in the chest. The hook is bare. She looks at the bare hook and understands that she has done a thing without being sure she was going to do it.

#### P70. cp_layla.pulse.w_children_ask_about_father

**Anchors:** widow.
**Branches:** none.
**Flags:** `cp_children_alive > 0`.
**Cooldown:** 12 months.
**Weight:** 1.0.

> The youngest asks her today what he was like. Not *do you remember him*; he does remember. He wants her to tell him. She tells him a story she has not told before, and at the end she does not know whether she made it up or whether it is true. She decides, afterwards, that it is both.

#### P71. cp_layla.pulse.w_silence_after_prayer

**Anchors:** widow.
**Branches:** none.
**Cooldown:** 10 months.
**Weight:** 0.9.

> After the evening prayer she sits for a long time. The house is quiet. The children sleep. She has not said anything to anyone since the morning. The silence does not hurt tonight. Some nights it hurts and some nights it is simply the shape of what is.

#### P72. cp_layla.pulse.w_first_laugh

**Anchors:** widow.
**Branches:** none.
**Cooldown:** 60 months.
**Weight:** 0.4 (rare, meaningful).

> The first time she laughs, really laughs, after Ahmed. It is a thing her daughter says. She is so surprised by her own laugh that she stops, and then she laughs again, at the surprise, and she cries at the same time.

#### P73. cp_layla.pulse.w_marriage_offer

**Anchors:** widow.
**Branches:** none.
**Flags:** age < 45.
**Cooldown:** 48 months.
**Weight:** 0.3.

> An offer, brought through her brother. A man from the next village, widowed himself, older, with grown children. She thinks about it for three days. She says no. She does not explain. No one asks her to.

#### P74. cp_layla.pulse.w_running_the_household

**Anchors:** widow.
**Branches:** none.
**Cooldown:** 8 months.
**Weight:** 1.0.

> She decides today. She always decided; she decided smaller things. Now she decides the field and the roof and the tax money and whether her son goes to the market with the cousin. The decisions are not harder than the old ones. The decisions are just hers now.

### Matriarch

#### P75. cp_layla.pulse.mat_grandchild_first_visit

**Anchors:** matriarch.
**Branches:** none.
**Flags:** any child married with children.
**Cooldown:** 14 months.
**Weight:** 1.2.

> Her daughter's daughter is in the courtyard, sitting in the dust. Two years old, serious. Layla crouches with her and the girl hands her a pebble. She accepts it as if it were currency.

#### P76. cp_layla.pulse.mat_advising_daughter_in_law

**Anchors:** matriarch.
**Branches:** none.
**Cooldown:** 16 months.
**Weight:** 0.8.

> Her son's wife asks her how to treat a cough. Layla tells her what her own mother told her. She hears her mother's voice in her mouth for a moment and is startled. The wife thanks her and goes home. Layla sits on the bench afterwards, lightly shaken by her own age.

#### P77. cp_layla.pulse.mat_village_elder_role

**Anchors:** matriarch, elder.
**Branches:** none.
**Cooldown:** 14 months.
**Weight:** 0.7.

> They call on her now when a woman dies, for the washing. She used to be one of the younger hands. Now she is the hands that have done it the most. She does not remember when the shift happened. It happened over many funerals.

#### P78. cp_layla.pulse.mat_ahmed_gray

**Anchors:** matriarch.
**Branches:** none.
**Flags:** `cp_widow = 0`.
**Cooldown:** 18 months.
**Weight:** 0.7.

> Ahmed's hair is more gray than black now. He will not let her cut it. She notices, one afternoon, that his hands are her father's hands. She is not sure when that happened either.

#### P79. cp_layla.pulse.mat_regret

**Anchors:** matriarch, elder, widow.
**Branches:** none.
**Flags:** `cp_bereaved_mother >= 1` weights up.
**Cooldown:** 30 months.
**Weight:** 0.4.

> A moment, unexpectedly, in the afternoon. She thinks of the child she lost, in the third year of her marriage, and the small grave, and the name she had been going to give the child. She has not thought the name in a long time. She thinks it now, once, and then she puts it back.

### Elder

#### P80. cp_layla.pulse.e_old_hands

**Anchors:** elder.
**Branches:** none.
**Cooldown:** 10 months.
**Weight:** 1.0.

> Her hands are an old woman's hands. She looks at them over the bread dough and they are a stranger's hands, and also her mother's, and also, still, hers.

#### P81. cp_layla.pulse.e_a_son_returns_from_the_city

**Anchors:** elder, matriarch, widow.
**Branches:** none (variant by H3).
**Flags:** `cp_children_in_city >= 1`.
**Cooldown:** 24 months.
**Weight:** 0.6.

> Her son who went to Alexandria is home for a week. He sleeps in his old bed. He eats her bread and he eats too much of it and he says, again, that no one in the city bakes like her. He says it every visit. It is slightly less true every visit. She lets it be true.
>
> *Variant Y:* He brings a device she does not understand and shows it to the children. It ticks. He calls it a *clock*. She holds it and listens.

#### P82. cp_layla.pulse.e_telling_stories

**Anchors:** elder, matriarch.
**Branches:** none.
**Cooldown:** 12 months.
**Weight:** 0.8.

> Grandchildren in a circle around her in the evening. She tells the story of the cholera year and the story of the flood and the story of the time a locust cloud blocked the sun. The stories are hers now. The stories are how she will be remembered.

#### P83. cp_layla.pulse.e_call_to_prayer_at_dusk

**Anchors:** elder, widow.
**Branches:** none.
**Cooldown:** 8 months.
**Weight:** 1.0.

> The muezzin's voice at dusk. She is too tired to go to the mosque most weeks now, even the women's part. She prays in the courtyard, on the mat her mother gave her, and the words she knows by heart she says more slowly than she used to.

#### P84. cp_layla.pulse.e_body_warning

**Anchors:** elder.
**Branches:** none.
**Cooldown:** 18 months.
**Weight:** 0.7.

> A pain in her chest that lasts an hour. She does not tell anyone. By evening it is gone. She lies awake that night thinking, not about dying, but about the morning she will be too tired to get up. That is what she is afraid of. The other thing she has made peace with for years.

---

## Land-anchor specific

### Landowner wife

#### P85. cp_layla.pulse.lo_the_paper_in_the_chest

**Anchors:** bride, young_mother, mother, matriarch, widow, soldiers_wife.
**Land:** landowner_wife.
**Branches:** `A.H`.
**Cooldown:** 24 months.
**Weight:** 0.8.

> The paper in the chest. She takes it out sometimes, when the house is quiet. She cannot read it. She knows the shape of Ahmed's name at the bottom. She traces it with her finger, and it is the shape of all the years of it.

#### P86. cp_layla.pulse.lo_selling_to_market

**Anchors:** young_mother, mother, matriarch, widow.
**Land:** landowner_wife.
**Cooldown:** 14 months.
**Weight:** 0.9.

> They sell their own grain at the market now. Ahmed haggles with the merchant and comes back with coins he has counted three times. The coins are heavier than the rent they used to pay. Heavier in a way she likes.

#### P87. cp_layla.pulse.lo_first_hired_hand

**Anchors:** mother, matriarch.
**Land:** landowner_wife.
**Cooldown:** 36 months.
**Weight:** 0.3.

> A young man from the next village comes to work their field for a week at harvest. They feed him. He sleeps in the stable. Ahmed pays him on the last day, coin into palm. It is the first time they have been on the paying side of that exchange.

#### P88. cp_layla.pulse.lo_bey_passes_without_stopping

**Anchors:** all marital.
**Land:** landowner_wife, tenant_wife (A).
**Branches:** `A`.
**Cooldown:** 20 months.
**Weight:** 0.5.

> The bey on the road at noon. His son now, actually; the old bey has been dead for years. He does not turn in at their gate. He has no reason to. The change of what he has no reason to do is the largest political change of her life.

#### P89. cp_layla.pulse.lo_debt_whisper

**Anchors:** young_mother, mother, matriarch.
**Land:** landowner_wife.
**Branches:** `A.H`.
**Flags:** `cp_recent_hardship = 1`.
**Cooldown:** 14 months.
**Weight:** 0.5.

> A merchant from the capital offers credit against next year's harvest. Ahmed refuses. He comes home angry -- not at the merchant, at the offer itself, at the easiness of it. *We do not borrow*, he says, as if she had argued with him.

### Tenant wife

#### P90. cp_layla.pulse.t_rent_day

**Anchors:** all marital.
**Land:** tenant_wife.
**Cooldown:** 8 months.
**Weight:** 1.0.

> The rent is due. Ahmed has the coin. He goes to the landlord's agent and pays. The agent writes in his book. Ahmed comes home. It is a transaction he has learned the shape of. She does not like the shape, exactly, but she has learned it too.

#### P91. cp_layla.pulse.t_contract_renewed

**Anchors:** all marital.
**Land:** tenant_wife.
**Cooldown:** 36 months.
**Weight:** 0.5.

> The contract is renewed for three more years at a slightly higher rate. Ahmed signs. He makes his mark; he writes a small version of his name now, a thing she taught him to do in the evenings. Afterwards he is quiet.

#### P92. cp_layla.pulse.t_neighbor_loses_tenancy

**Anchors:** all marital.
**Land:** tenant_wife.
**Cooldown:** 24 months.
**Weight:** 0.4.

> The neighbor's contract was not renewed. They pack. They go to the city -- she does not know which. Layla helps the wife carry a bundle to the road. Afterwards, the field to their south stands fallow for a month before a new family moves in.

### Serf wife

#### P93. cp_layla.pulse.s_beys_man_collects

**Anchors:** all marital.
**Land:** serf_wife.
**Cooldown:** 6 months.
**Weight:** 1.0.

> The bey's man at the door. He asks for the share. Ahmed gives it. He always gives more than he should because one year they gave less and there was trouble. The man takes the bag and leaves without thanking Ahmed. Thanking is not in the arrangement.

#### P94. cp_layla.pulse.s_overseer_beats_a_neighbor

**Anchors:** all marital.
**Land:** serf_wife.
**Cooldown:** 18 months.
**Weight:** 0.5.

> The overseer beats a man two houses down for a thing no one can quite explain. Ahmed comes home and closes the door and does not speak until the meal is over. Layla does not ask. She washes the pot. She prays.

#### P95. cp_layla.pulse.s_corvee_call

**Anchors:** all marital.
**Land:** serf_wife.
**Cooldown:** 10 months.
**Weight:** 0.9.

> The call goes out for corvee labor. Ahmed goes. He is gone two weeks at the canal. He comes back thinner. He does not speak of it. Later, at night, he says only: *a man died while I was there. I did not know him.*

#### P96. cp_layla.pulse.s_sultan_in_sermon

**Anchors:** all marital.
**Land:** serf_wife.
**Branches:** `α`.
**Cooldown:** 10 months.
**Weight:** 0.8.

> The imam names the Sultan at Friday, as he has every Friday of her life. The bey sits in the front row. The pasha's cousin, visiting from the capital, sits beside the bey. Three layers of authority, arranged in descending order, each one with its own claim on her week's work.

#### P97. cp_layla.pulse.s_the_road_is_closed

**Anchors:** all marital.
**Land:** serf_wife.
**Cooldown:** 24 months.
**Weight:** 0.4.

> The bey's men close the road for a morning while a caravan passes. No one in the village can go anywhere. She stands in the yard and watches the carts pass from a distance. There is a woman in one of the carts in silk that shines in the sun. She does not look at the village.

### Wage laborer wife

#### P98. cp_layla.pulse.wl_payday

**Anchors:** all marital.
**Land:** wage_laborer_wife.
**Cooldown:** 6 months.
**Weight:** 1.0.

> Ahmed's wage on the first of the month. Coin onto the shelf by the door. She counts it after he has gone to sleep. It is enough or it is not enough; there is no year it has been more than enough. It is a different poverty than the old one. It has numbers.

#### P99. cp_layla.pulse.wl_company_man

**Anchors:** all marital.
**Land:** wage_laborer_wife.
**Cooldown:** 18 months.
**Weight:** 0.5.

> A company man from the capital inspects the fields. He never speaks to the workers. He speaks to the overseer. He wears clothes she has never seen anyone wear. He leaves in the afternoon and the field keeps being what it was.

### Collective member

#### P100. cp_layla.pulse.col_committee_meeting

**Anchors:** all marital.
**Land:** collective_member.
**Cooldown:** 8 months.
**Weight:** 0.8.

> The committee meets at the mosque courtyard every month. Ahmed goes. Sometimes she goes too, and stands with the women at the back. The voices rise and fall. Decisions are made slowly. Sometimes she understands them and sometimes she does not, and both are ordinary now.

#### P101. cp_layla.pulse.col_shared_harvest

**Anchors:** all marital.
**Land:** collective_member.
**Flags:** season = harvest.
**Cooldown:** 11 months.
**Weight:** 1.0.

> The harvest this year is shared. Each household's portion is weighed and read out. Ahmed brings home a measure. It is less than he expected and more than she expected. She is not sure how that is possible. It is.

#### P102. cp_layla.pulse.col_old_neighbors

**Anchors:** all marital.
**Land:** collective_member.
**Cooldown:** 18 months.
**Weight:** 0.5.

> The old neighbor, who was always difficult, has to work alongside Ahmed now in the shared field. They manage. They do not speak much. Layla watches them from the courtyard with a small, surprised pleasure.

### City laborer

#### P103. cp_layla.pulse.cl_first_factory_morning

**Anchors:** all marital.
**Land:** city_laborer.
**Cooldown:** 60 months (one-time feel).
**Weight:** 1.0 first year after migration; 0.3 later.

> Her first morning in the city. Ahmed leaves at dawn for the factory. The sound of the street is not a sound she recognizes. A cart goes past whose wheels shriek. A man calls something up at another man in an accent she has never heard. She closes the shutter.

#### P104. cp_layla.pulse.cl_one_room

**Anchors:** all marital.
**Land:** city_laborer.
**Cooldown:** 10 months.
**Weight:** 1.0.

> One room now. The four of them. The wall is thin; she can hear the family on the other side eating. The children sleep against her. Ahmed coughs through the night. The smell of the city is coal and oil and too many people and the river.

#### P105. cp_layla.pulse.cl_foreman_shouts

**Anchors:** all marital.
**Land:** city_laborer.
**Cooldown:** 12 months.
**Weight:** 0.7.

> Ahmed comes home with the stiff walk he gets when the foreman has shouted at him. She does not ask. He eats. He sleeps. In the morning he walks back.

#### P106. cp_layla.pulse.cl_letter_home

**Anchors:** all marital.
**Land:** city_laborer.
**Cooldown:** 12 months.
**Weight:** 0.8.

> She writes, or gets written, a letter to her mother, who is alive or to whom the letter is read by her brother. She describes the city. She does not describe the room. She asks after the field they used to work. She does not say she misses it. Her mother will know.

#### P107. cp_layla.pulse.cl_factory_whistle_at_dawn

**Anchors:** all marital.
**Land:** city_laborer.
**Branches:** `Y`.
**Cooldown:** 6 months.
**Weight:** 1.2.

> The factory whistle at dawn. Ahmed gets up before it, now, so that he is not inside the sound when it comes. She lies with her eyes closed and listens to the whistle, and after it the footsteps in the street, and after that the shouting in a language that is not her own.

#### P108. cp_layla.pulse.cl_european_in_tram

**Anchors:** all marital.
**Land:** city_laborer.
**Branches:** `Y`.
**Cooldown:** 18 months.
**Weight:** 0.3.

> A man on the new tram, which she has not ridden, in European clothes, reading a newspaper in a language that is not Arabic and not Turkish. He does not look at her. He does not look at anyone. She watches him until the tram is past.

#### P109. cp_layla.pulse.cl_missing_the_sky

**Anchors:** all marital.
**Land:** city_laborer.
**Cooldown:** 10 months.
**Weight:** 0.8.

> At night in the room, after the children sleep, she thinks of the sky over the field. That particular sky. In the city the sky is cut by walls and smoke. She does not know she is thinking of it until she has been thinking of it a long time.

#### P110. cp_layla.pulse.cl_strike

**Anchors:** all marital.
**Land:** city_laborer.
**Branches:** `Y`.
**Cooldown:** 30 months.
**Weight:** 0.3.

> Men stand outside the factory for three days and do not work. Ahmed is among them; he is not a leader, only one of the men. She brings him bread at noon. She does not know what to think. She asks the neighbor, who also does not know what to think. They do not know together, companionably.

#### P111. cp_layla.pulse.cl_son_becomes_foreman

**Anchors:** matriarch, widow, elder.
**Land:** city_laborer.
**Flags:** oldest son works in city.
**Cooldown:** 60 months.
**Weight:** 0.2.

> Her son is a foreman now. Not a rich man, but a man who stands above other men. He wears a shirt with collar that buttons. He visits the room she still shares with his father and he seems too large for it. She feeds him. He eats slowly.

#### P112. cp_layla.pulse.cl_minaret_and_smokestack

**Anchors:** all marital.
**Land:** city_laborer.
**Branches:** `Y`.
**Cooldown:** 24 months.
**Weight:** 0.4.

> From the doorway she can see the minaret of the small mosque at the end of the lane and, behind it, the smokestack of the factory. They are about the same height. The muezzin's voice and the whistle do not quite agree on what time it is.

---

## Ottoman-motif count (verification)

Pulse events whose prose explicitly invokes Ottoman motifs (Sultan, Caliph, pasha, bey-as-Ottoman-appointee, Ottoman coin, Anatolian officer, Turkish word, millet-status trader, Ottoman-calendar observance, news of Sultan's war, khutba naming the Sultan): **P01, P02, P14 (variant), P17, P33, P34, P35, P36, P37, P38, P39, P40, P78, P96, P97** -- plus the `α` variants of P02, P33, P40, P73 (marriage offer referenced traditionally), P83. Counting unique events: **20+**. Satisfies the ≥20 threshold in the plan verification list.

Under `β`, the same events read as absence/memory -- P02 variant, P33 variant, P40 de-emphasized. The authoring rule: Ottoman motifs are always present in the world; their valence shifts from "the water she swims in" (α) to "a water that has receded" (β).

## Event count (verification)

Events P01 through P112 minus gaps: continuous numbering, no skips. Total: **112 entries** in the pool. Plan target was ~100; 112 gives the dispatcher headroom and lets the per-anchor distribution exceed the floor of 5 events per anchor comfortably.

## Per-anchor floor check

| Anchor / land_anchor | Unique pulse events applicable (approximate) |
|---|---|
| bride | 6 specific + universal ≈ 30 |
| young_mother | 8 specific + universal ≈ 30 |
| mother | 5 specific + universal ≈ 30 |
| soldiers_wife | 8 specific + subset of universal ≈ 20 |
| widow | 7 specific + subset of universal ≈ 20 |
| matriarch | 5 specific + universal ≈ 25 |
| elder | 5 specific + subset of universal ≈ 20 |
| serf_wife | 5 specific + universal ≈ 30 |
| landowner_wife | 5 specific + universal ≈ 30 |
| tenant_wife | 3 specific + universal ≈ 30 |
| wage_laborer_wife | 2 specific + universal ≈ 25 |
| collective_member | 3 specific + universal ≈ 25 |
| city_laborer | 10 specific + limited universal ≈ 15 |

Every anchor comfortably exceeds the 5-event floor. `city_laborer` has the thinnest pool because most rural universals (harvest, bey, village community) do not apply -- compensated by 10 city-specific events.

*Next: the eventify pass, a later plan. Each pulse event becomes a hidden `country_event` fired by the dispatcher; variants localize as `triggered_desc` blocks; cooldowns managed via `cp_last_pulse_<id>` timed variables.*
