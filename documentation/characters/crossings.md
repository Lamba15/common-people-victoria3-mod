# Character Crossings

Story trees are not isolated. Characters can meet in each other's events when they share a state, a class, or an enemy. Each crossing is checked when an event fires: "Is another Common People character in the same state with the right conditions?"

## Crossing Table

| If... | Then... |
|-------|---------|
| Tarek falls to laborer + Samier active in same state | They meet on the factory floor. Tarek tells Samier what owners really think. |
| Layla migrates to Cairo + Samier active | They share a neighborhood. Different worlds collide. |
| Tarek returns to farming + Layla is a farmer | They meet at the market. Bey's grandson buys seed from a former serf. |
| Al-Sayyid is alive + Tarek is active | Al-Sayyid hears about "the al-Rashidi boy who sold his land." Contempt or grudging respect. |
| Samier becomes Agitator + Tarek is factory owner | Samier organizes Tarek's workers. They are enemies. |
| Layla's husband conscripted + Soldier active | Ahmed might BE the soldier. Or they serve together. |

## Featured Crossing Scenes

### Tarek and Samier (factory floor)

Tarek has fallen. He works Samier's shift. Samier doesn't know Tarek's history. One night Tarek tells him.

> Samier stares. "You were one of THEM?"
> Tarek says: "I was. Now I'm one of you. And I'm telling you -- they don't think about us at all. Not with cruelty. They just don't think about us."

Mechanical: Samier's radicalism goes up or down depending on player choice in the conversation.

### Tarek and Layla (Fayoum market)

Tarek has returned to the land. Layla is a farmer. They meet at a market in Fayoum or on a road between villages. Neither knows the other's history. They haggle over the price of wheat.

Two people whose families were on opposite sides of history, now equal in the dirt.

### Layla and Samier (Cairo tenement)

Layla has migrated. Samier is already there, angry. They live in the same district.

> He talks about rights. She talks about the farm she lost. He doesn't understand why she'd want to go back to dirt. She doesn't understand why he'd want to fight the only people offering work. They disagree but they share bread.

No mechanical effect. Pure mutual confusion. This is what the mod is for.

### Al-Sayyid and Tarek (Cairo salon)

Al-Sayyid attends a dinner. Tarek is present, wearing a European suit. Al-Sayyid recognizes the family name -- al-Rashidi, the Fayoum branch. He remembers Tarek's father.

> "Your father was a good man. He held the land. You... you sold it."

Tarek does not defend himself. He just says: "Yes."

Al-Sayyid cannot decide if he hates Tarek or pities him. He leaves early.

### Samier and Ahmed (dead worker, dead soldier)

If Samier dies in a strike AND Ahmed (Layla's husband) dies at war in the same year, Layla gets a compound event. Two deaths in two different worlds, and she doesn't know either man well enough to grieve separately. She mourns an era.

## Implementation Notes

Crossings check:
1. Both characters are alive (`is_alive = yes`).
2. Both are in the same country, usually the same state.
3. Both have compatible pop types / branches for the meeting.
4. A crossing hasn't already fired between them (flag on one or both characters).

Crossings prefer to fire in the event of the character whose branch is more recent -- the newcomer sees the other, not vice versa.

```
# Pseudocode
trigger = {
    scope:tarek = {
        var:cp_branch = 2            # falling
        var:cp_sub_branch = 3        # factory floor
        is_in_same_state_as = scope:samier
        NOT = { has_character_flag = met_samier }
    }
}

effect = {
    scope:tarek = { set_character_flag = met_samier }
    scope:samier = { set_character_flag = met_tarek }
}
```
