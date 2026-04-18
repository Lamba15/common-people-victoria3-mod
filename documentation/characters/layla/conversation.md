# Imagined Audience with the Pasha

A verb on Layla's journal entry labelled **"Imagine an audience with the Pasha."** Where Check-on-Layla is a moment observed, Audience is a fantasy: she is standing in an enormous room she has never seen, in Cairo, before Muhammad Ali Pasha, ruler of Egypt. She is wearing clothes she does not own. She has been granted an hour. She has rehearsed this a hundred times over the quern-stone and over the oven and in the dark before sleep. Tonight she lets it happen.

This is the mental mode of every powerless person who has ever imagined walking into the office of the minister, the president, the king, the boss — the practice-speech that will never be given, the rehearsed argument that dissolves the moment the imagined audience ends.

**The player is Muhammad Ali Pasha, in her imagination.** The player chooses the topic she brings before him, and then — at every turn — the player chooses what the Pasha says back. The player plays the role of the ruler she has invented. She speaks her monologue; the player as Pasha replies; she reacts to the reply; the player as Pasha replies again; the back-and-forth continues until the audience closes.

This is roleplay with asymmetric authorship: **she is fixed, he is player-directed**. Her voice is written; his voice is yours. You choose whether the Pasha she imagines tonight is dismissive, indulgent, cruel, curious, or (most dangerously) understanding. Her reactions branch accordingly — her voice hardens or breaks or persists, depending on the Pasha you chose to be.

---

## Frame

**Who is the Pasha?** Muhammad Ali Pasha (Wāli of Egypt 1805–1848; viceroy under the Ottoman Sultan). In 1836 he is at the height of his power: he has reformed land ownership, modernised the army by conscripting peasants like Ahmed, built textile mills and arsenals, and fought Ottoman wars that killed uncounted Egyptian men. He has never visited Layla's village. He will never know she existed.

**Why he is who she imagines.** She has heard his name all her life. He is the ultimate authority in her world — not God, not the bey, but the man whose orders the bey ultimately obeys. She has seen his image only in vague report. When she imagines the face of power, she imagines him. The way an Egyptian peasant woman in 2026 might imagine addressing the president.

**What the fantasy feels like.** Grandiose, shameful, necessary. She knows it is fantasy. She lets it happen because she needs to hear her own voice speaking the things she cannot say aloud. After the audience ends she returns to the oven and does not speak of it.

**What she calls him.** "Effendim," "Sidi," "my lord in Cairo," "Pasha," "you" (the most daring form). She rarely uses his name. When she does — Muhammad Ali — it is an act.

---

## Structure

A conversation is a branching tree. Each event is one turn in the dialogue. Odd-numbered layers are HER monologue (flavor text, fixed writing); even-numbered layers are the PASHA (options — player picks what he says).

### Layer 1 — Root (narrator setup + topic select)
`cp_conversation.1` — the narrator tells us she has decided to go to Cairo in her mind. Options = topics. The player picks the subject she brings.

### Layer 2 — Her opening speech
One event per topic. The flavor is her opening monologue — 300–500 words of her laying out the case before him. Options = what the Pasha says in reply. Three moods typically: **dismissive**, **engaged**, **cruel**. You choose which Pasha she faces tonight.

### Layer 3 — Her reaction to his reply
One event per Pasha-mood branch. The flavor is how she receives his reply and what she says next. Options = the Pasha's second response.

### Layer 4 — Her second reaction
One event per branch. The flavor closes her case, or pushes harder, or retreats. Options = the Pasha's final gesture (or the audience simply ending).

### Layer 5 — Closer
Shared by all branches: the fantasy dissolves. She is back at the quern or the oven. The kitchen is quiet. The button cooldown starts.

A rich topic has ~10 events in total (1 opener + 3 reaction branches × 2-3 turns each + 1 closer). Simpler topics have fewer.

---

## Topics (Phase 1 implementation)

Five topics. Each gated on what's knowable to her. Each deeply written. Each sets a permanent flag on completion so future pulses can reference "she has rehearsed this before."

### T10 — The Land
She tells him the field is hers. She tells him what her grandfathers did. She asks for a paper with her name on it that the bey cannot tear up. Available whenever she is rural (peasant, farmer, or homesteader, or under serfdom).

### T20 — Ahmed
She asks for him back, or she asks for him never to be taken, or she tells the Pasha that the war has a price and she is paying it in her one husband. Branch varies by Ahmed's state (at war / home / conscripted recently / long gone).

### T30 — The Bey
She tells the Pasha, quietly, what his bailiff actually does at harvest. She is not asking for revenge. She is asking to be believed. Gated on `has_variable = cp_under_serfdom` OR any time she is tenant under a bey.

### T40 — The Water
She tells him the sluice at the head of her village canal has been broken since before she was a bride. She tells him the cost of a broken sluice in loaves. Always available.

### T50 — Herself
The hardest. She tells him she is a woman and she has a voice and she is here. She does not ask for anything. Always available. Gated on `cp_last_conversation_topic != 50` so it cannot be the first audience.

---

## Cooldown and persistence

- `cp_audience_cooldown` — timed flag, 90 days. Set on button click. Prevents a second audience in that window.
- `cp_seen_audience_T<N>` — timed flag, 18 months, per topic. A topic rests between hearings so she does not repeat the same speech twice in a season.
- `cp_has_stood_before_pasha` — permanent, set the first time any audience completes. Pulse events may reference: *"The woman who, in her mind, has stood before the Pasha."*
- `cp_has_spoken_of_<topic>` — permanent per topic. Unlocks later deepening events or referenced by future conversations.

---

## Writing rules

1. **Never let him speak in his own voice.** He is her projection. What she "hears" from him is her imagination of him. The narrator, when describing his reactions, uses "she imagines him..." or "she sees him..."
2. **Specific Egypt 1836.** Mud-brick, date palms, the Nile, the muezzin, the dust on the Cairo road, the gold thread on an imagined robe, the brass ink-pot on an imagined desk.
3. **Long paragraphs.** The monologues breathe. They do not skip. A real speech does not fit in three sentences.
4. **Her voice, not a poem.** She uses the vocabulary of a Delta peasant woman. She would not say "sovereignty." She would say "the paper that says the field is mine."
5. **Surprising turns.** Halfway through a speech she says something the player did not expect — a defence of the bey's wife, an admission she prayed for a French soldier, an argument she half-disbelieves even as she delivers it.
6. **End on a concrete object.** The last image of every monologue is a thing in the world: the gold thread on his sleeve, the brass ink-pot, the red carpet, her own hand.

---

## Images

Phase 1 reuses existing DDS files:
- Root: `cp_layla_intro.dds` (her face, before the fantasy begins)
- T10 Land: `cp_layla_homesteading.dds` (the field)
- T20 Ahmed: `cp_layla_ahmed_conscripted.dds` (the soldier)
- T30 Bey: `cp_layla_serfdom_restored.dds` (authority on horseback)
- T40 Water: `cp_layla_no_wind.dds` (still canal)
- T50 Herself: `cp_layla_mothers_hand.dds` (interiority)

Phase 2 will generate purpose-built images: *Layla in an imagined throne-room, Layla seen in profile with the gold-threaded Pasha out of focus, Layla walking back down an imagined palace corridor.*

---

## Phase map

- **Phase 1 (this build):** button + root + **The Land** topic fully written (10 events, 5 layers). Proves the pattern, establishes the Pasha-mood branching, exercises the roleplay.
- **Phase 2:** **Ahmed**, **The Bey**, **The Water** topics (~10 events each). Richer branching; some topics should give the Pasha a fourth mood ("understanding") as a rare, destabilising option.
- **Phase 3:** **Herself**, **The Children**, **The Boys**, **The Law** — the harder ones. She risks saying things she has never said.
- **Phase 4:** reactive topics — "The French," "The Railway," "The Newspaper" — gated on tech / law / world events having crossed her awareness.
- **Phase 5:** she imagines addressing not the Pasha but God, or her mother, or the version of herself at sixteen. The same structure redirected inward. Hardest to write; do last.
