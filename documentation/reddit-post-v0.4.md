# Reddit devlog post — Common People v0.4

Draft for r/victoria3 (primary). Cross-post r/paradoxplaza 24–48h later.

**Framing:** devlog + playtest invitation. Not a Workshop release.

---

## Title

> A Victoria 3 mod about the common people whose lives your choices change

For the r/paradoxplaza cross-post, the title reads the same — no edits needed.

### Alternates (if the primary underperforms on a later repost)

- *A Victoria 3 mod about the woman on the other end of your reign*
- *A Victoria 3 mod where you see your empire through the eyes of one of its common people*
- *A Victoria 3 mod that gives one of your pops a name, a home, and a life*
- *Ever wondered what one of your Victoria 3 pops is actually thinking? I'm making a mod where you can find out.*
- *I'm making a Victoria 3 mod where one of your pops becomes a person*
- *I'm making a Victoria 3 mod where abolishing serfdom means a woman named Layla holds a deed and can't stop her hands shaking* (the original literary-specific version — keep in reserve for a later "content-drop" post showing a specific event)

---

## Body

> **Devlog, not a release — the mod isn't on the Workshop yet. I'm sharing it now because I want your opinion on it before I keep building.**

Victoria 3 tells you abolishing serfdom shifted your GDP by 3.2%.

I'm making a mod that tells you about Layla.

She is twenty-two, from Mīt al-Nakhla, two days' walk from the river's eastern mouth. She has been awake before the muezzin every morning of her adult life. When you pass the homesteading law in Egypt, this is what happens to her:

> **The Deed**
>
> *She holds it. She has waited her whole life to hold it. Her grandmothers waited too.*
>
> The wax is still warm where the seal pressed it. The notary had not yet wiped his pen when he handed it over; the wax is the kind that stays warm in the hand for twenty minutes and then cools. It is the color of dried blood and it carries her name. Her name. Layla bint Mohamed al-Sharif, of Mīt al-Nakhla, on a paper that the law says cannot be taken from her. She stands in the middle of the field and her hands will not stop shaking and the field — green, hers, hers — keeps blurring at the edges. She does not weep. She has not wept for anything before, not the babies she has lost or the brother who never came back, and she will not weep now. But the field will not stop blurring. Somewhere, in a village she will never visit, a man with a name like hers walks past with a paper of his own, and he is also not weeping. Across the lane, she knows, Umm Mariam — who has worked the field next to theirs for thirty years — does not, today, have a paper. A clerk in Mansoura wrote her husband's name incorrectly in the ledger and no one, in the years since, has corrected it. The sun is high. The wax is warm. The earth is hers. The earth next door is not, today, Umm Mariam's.

**What the mod is**

- A V3 narrative mod that tracks individual peasants whose lives bend with your laws and wars. Not a stats mod. Not a map mod. Prose and a journal.
- Every event hand-written. Tone reference is Naguib Mahfouz's *Cairo Trilogy* — specific, sensory, subtext. No "you see a pop radicalize" telling.
- A journal entry tracks her in real time. Each month she gets three lines: what she's *thinking*, what she's *doing*, what she's *hoping*. The lines change with her circumstances — wartime, widowhood, serfdom restored, affluence.

Here's her journal the month her husband Ahmed is at the front and she's having a bad week:

> She is thinking about the shaving-water he left in its clay jar. It has gone green. She has not emptied it.
>
> She is sweeping a floor that is already swept, because sitting still is the worst of the hours.
>
> She is hoping, in the quietest part of her, only to know. Either way. Only to know.

**Where it is**

- v0.4 in active development. Layla is Person 1 of N, playable from her intro through widowhood.
- Not on the Workshop yet — I want feedback from a small first audience before polishing for public release.
- Egypt-first because it's where I live. The framework is nation-agnostic.
- No new buildings, laws, or map changes. Prose and a journal. That's the whole mod.

**Want to playtest?**

Clone the repo, symlink `mod/` into your V3 mods folder, start as Egypt. There's a README with exact steps for Windows / Linux / macOS. Takes about 2 minutes to install.

**What I'm asking for:**

1. **Does the prose land?** Read an event and tell me whether it hit or felt overwritten. Honest is useful; polite isn't.
2. **Who should Person 2 be?** Specific pitches win: *"a Silesian weaver watching the mechanical looms arrive in 1848"* beats *"a Polish character."*
3. **Bug reports.** This is pre-release. If an event doesn't fire, a variable shows garbled, or the journal breaks — tell me. Screenshot the log if you can.

**Known limitations (being honest up front):**

- Some ambient events can re-fire after ~180 days instead of being strictly one-shot. Not broken, just occasionally repetitive on long playthroughs. Patching next.
- About half the "named neighbour" census (Umm Mariam, Hajj Rashid, Badr) isn't woven into every event that mentions them yet. You'll sometimes see "the neighbour" where a name would be better.
- Layla is the only person right now. The framework supports more — I'm building toward them, not faking them.

I'll be in this thread for the next few hours. Ask anything.

---

## Pinned top comment

- **GitHub (clone here):** https://github.com/Lamba15/common-people-victoria3-mod
- **Install:** see README in the repo root — junction/symlink into your V3 mod folder, enable in launcher, start as Egypt, wait for the intro event on the first month.
- **Design doc:** `documentation/the-holy-grail.md` — the full pitch + modding architecture.
- **Report bugs:** GitHub issues, or reply here with a screenshot.
- **Who should Person 2 be?** Drop your pitch. The more specific, the more seriously I'll take it.

---

## Screenshots to prepare (in this order)

1. **Hero shot** — `cp_layla.1` "The Farmer's Daughter" intro event popup in-game, normal zoom. Top of the post.
2. **The distinctive shot** — the journal entry panel showing her status line ("She is thinking / doing / hoping"). Nothing else in V3 modding looks like this. Converts scrollers into clickers.
3. **The mechanics tie** — either `cp_layla.3` "The Bey Returns" (serfdom restored) or `cp_layla.4` "He Marches" (conscription). Readers need to see that the prose is load-bearing on real game state.

Capture at 1080p minimum. Close side panels for a clean UI. Upload directly to Reddit, not imgur (imgur links get downranked).

---

## Pre-post checklist

- [x] v0.4 bumped in `mod/.metadata/metadata.json`, `CLAUDE.md`, `README.md`
- [x] README rewritten with pitch + install steps + playtest instructions
- [x] First in-game test passed (per user confirmation)
- [ ] Three screenshots captured (see list above)
- [ ] Title chosen
- [ ] Post body pasted into Reddit, previewed for formatting
- [ ] Pinned comment ready to paste immediately after posting
- [ ] Set aside ~2 hours after posting to reply personally to early comments

## Timing

- **Primary window:** Saturday or Sunday, 10am–2pm US Eastern. r/victoria3 peaks here.
- **Secondary:** Tuesday evening US Eastern.
- **Avoid:** Thursdays (Paradox dev-diary day — you'll be drowned out), Friday nights (dead sub).

## Engagement discipline during the first hour

- Reply in the same literary register as the mod. One-word "thanks!" replies undercut the whole pitch.
- If someone asks whether the prose is AI-generated, answer clearly: no, it's hand-written, and offer to show drafts/cut scenes.
- Don't argue with lukewarm reactions. "Fair, I'll keep working on it" is usually the right reply.
- Pin the top comment as soon as it's posted.

## Cross-post plan

- **24–48 hours after r/victoria3 post settles:** cross-post to r/paradoxplaza using the literary-alternate title.
- Optional: r/CrusaderKings (narrative-mod readers), r/Egypt (framed as an Egyptian history piece).
- Do not cross-post before the primary post has had its own run.
