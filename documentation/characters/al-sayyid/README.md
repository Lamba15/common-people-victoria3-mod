# Hassan Bey al-Sayyid (Egypt)

## Implementation Status

First scaffold landed in the v0.5 rebuild:

- Name token: `bey`
- Script files: `mod/events/cp_bey_events.txt`, `mod/common/scripted_effects/cp_bey_memory.txt`, `mod/localization/english/cp_bey_l_english.yml`
- Shared wiring: `cp_shared_startup.1` registers him death-safely, `cp_roll_for_event` gives him a 7-weight ambient branch, and `cp_on_law_enacted` uses a weighted shared Homesteading resolver between Layla and the Bey.
- Images: all six visible Bey events now use mod-owned generated DDS art, with source/archive files under `image/generated/al-sayyid/v0.1/`, `image/generated/al-sayyid/v0.2/`, and `image/generated/al-sayyid/v0.3/`. The v0.3 batch replaces the final generic factory and officialdom motion plates.
- Current content: two ambient beats (`cp_bey.10`, `cp_bey.40`), three land-reform reactions (`cp_bey.20` Homesteading, `cp_bey.21` Serfdom Restored, `cp_bey.22` Commercialized Agriculture), and one industrialization world-response (`cp_bey.30`). No JE, button, conversation tree, death event, or Landowners clout ladder yet.

## Profile

- **Pop type**: Aristocrat
- **Culture**: Misri | **Religion**: Sunni | **Age**: 52 | **Traits**: Arrogant
- **Home state**: `STATE_LOWER_EGYPT`, stored through the shared `cp_bey_lives_here` residence marker and journal state pointer.
- **Workplace profile**: estate landholder / manufacturing-boundary observer, so factory reactions only matter when industrial buildings touch his home-state world.
- **Full name**: Hassan Bey al-Sayyid. His farmers call him "al-Sayyid" -- The Master. Only his wife calls him Hassan. The day someone calls him just "Hassan" to his face is the day his world has ended.
- **Interest group**: Landowners (ig_landowners)
- **Personality**: Paternalistic, traditionalist, monarchist. Genuinely believes he cares for "his" peasants. Does not see the cruelty because the cruelty IS the system and the system is all he knows.

## Personality Weights

| Interest | Weight | Why |
|----------|--------|-----|
| Land reform | 10 | His entire world depends on serfdom staying |
| Industrialization | 9 | Factories steal his laborers and threaten his monopoly |
| Landowners IG clout | 10 | When they lose clout, he loses power |
| Monarchy/governance | 8 | Democracy makes his voice one among millions |
| Education | 7 | Literate peasants question the order |
| Religion | 8 | The mosque validates the hierarchy |
| Economy | 9 | Watches GDP shift from agriculture to industry with dread |
| Women's rights | 6 | Disrupts the family structure he controls |
| France/diplomacy | 4 | French ideas are revolutionary poison |
| War | 3 | Not his concern unless his estate is threatened |

## Historical Context

The Bey class in 19th century Egypt were Ottoman-era landowners who controlled vast agricultural estates. Under the corvee system, peasants were bound to their land. The Bey's authority was absolute in his domain -- local judge, employer, landlord, and patriarch in one person. Muhammad Ali's reforms began eroding their power, and the shift toward private land ownership threatened their entire existence.

## What Makes Him Interesting

He is NOT a cartoon villain. He is a man born at the top of a system he didn't create, watching that system collapse under him. He is paternalistic -- he genuinely believes he feeds and protects "his" people. When serfdom is abolished, he doesn't understand why they would want to leave. "I gave them everything." He gave them everything except freedom, and he cannot see the difference.

**His story mirrors Layla's in reverse.** She rises as he falls. Same events, opposite perspectives. When Layla holds a deed, al-Sayyid watches his estate emptied. The player sees both sides of the same history.

## Key V3 Hooks

```
# Track Landowners IG clout
ig:ig_landowners = {
    ig_clout >= 0.20              # Powerful -- al-Sayyid is confident
    ig_clout < 0.04               # Marginalized -- al-Sayyid is irrelevant
    is_in_government = yes        # Landowners in government -- his allies rule
}

# Track industrialization eating his world
any_scope_building = {
    is_building_group = bg_manufacturing    # Factories exist
}

# Aristocrat pops shrinking
any_scope_pop = {
    pop_type = aristocrats        # His class is disappearing
}
```

Mirror every Layla land-reform event with an al-Sayyid counterpart on the same `on_law_enactment_pass` hook.

## Life Events

*When Serfdom is active (al-Sayyid is powerful):*
He hosts a feast at his estate. Rides through his fields. His overseer reports on the harvest. He gives alms at the mosque and the imam praises his generosity. He believes the world is as God intended. The player sees a man at peace inside a system of bondage.

*Serfdom -> Tenant Farmers (first crack):*
"They say the fellahin can leave now. Where would they go? They need me. They'll stay." He sounds confident but there's a tremor. His best worker's son has already gone to the city.

*Tenant Farmers -> Homesteading (his world shatters):*
The same morning Layla holds her deed, al-Sayyid stands at his window watching government officials distribute HIS land. His overseer packs his things. Farmers walk past his gate without bowing. A young man -- Layla's husband -- looks him in the eye for the first time. Al-Sayyid does not understand. "I fed them. I built the irrigation canal. I settled their disputes. And they take my land?"

*Homesteading -> Commercialized Agriculture (a different loss):*
A man from Cairo in a European suit offers to buy al-Sayyid's remaining estate. The Bey refuses. The man shrugs and buys the neighboring estates instead. Al-Sayyid watches his former peers sell everything. "They have no honor. They sell their grandfather's land to merchants." But the merchants are getting richer and al-Sayyid is getting poorer.

*Landowners IG loses clout:*
"The parliament is full of shopkeepers and factory men now. They have money but no blood. They don't understand what this country IS. They think you can buy what my family built over centuries."

*Landowners IG becomes marginalized:*
"Nobody comes to my estate anymore. The governor doesn't return my letters. My son says I should sell the house and invest in railways. Railways." He sits alone in a room that was full of guests ten years ago.

*Industrialization advances (factories built):*
Implemented as `cp_bey.30`, "Smoke at the Boundary": they build a factory where the estate road used to turn, and the old boundary stone suddenly looks like a relic nobody has agreed to preserve. The world-response uses the shared visible-story cooldown, so modernization can make Al-Sayyid visible without increasing the routine event budget.

*New administrative middle class:*
Implemented as ambient `cp_bey.40`, "The Visitor's Card": a new official leaves a printed card and speaks in the language of committees and valuations. This gives Al-Sayyid a quiet life beat after the intro, with the same ambient cooldown protections as every other person.

*Serfdom RE-ENACTED (if the player goes backwards):*
"Order is restored." Al-Sayyid rides through the village again. The fellahin lower their eyes. The young man who looked him in the eye works his field again. Al-Sayyid should feel triumph. Instead he feels something he cannot name. The village is quieter than before. There is no feast this time.

*Education laws passed:*
"They opened a school in the village. A school! What does a farmer need with reading? Next they'll want to vote."

*Al-Sayyid dies:*
His son sold the estate to a cotton merchant. The house became a grain warehouse. The overseer's stick hangs on a wall nobody looks at. In the village, Layla's granddaughter plays in a field that used to be his. Nobody tells her who al-Sayyid was. Nobody remembers.

## Narrative Tone

Tragic, uncomfortable. The player should feel conflicted. Al-Sayyid is wrong about everything -- but he is also a human being losing everything he was born into. The mod doesn't ask the player to sympathize with him. It asks the player to see him. That is enough.
