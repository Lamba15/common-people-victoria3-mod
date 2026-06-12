# Common People

**A Victoria 3 narrative mod.** Personal, novelistic stories about ordinary citizens of the nations you govern. When you pass a law, a specific person in the roster finds out about it — and you find out about them.

---

## What this is

Victoria 3 tells you abolishing serfdom shifted your GDP by 3.2%. Common People tells you about a roster of ordinary people who feel the policy in their hands: Layla with a land deed, Hassan Bey losing tenants, Yusuf going to war, Salma at the switchboard, Karim by the machine teeth, Huda counting rent above a growing street, Mansur sending factory wages home, Nabil keeping the corner lamp lit.

- Events are hand-written as paragraphs of a novel. Tone reference: Naguib Mahfouz's *Cairo Trilogy*. Specific, sensory, subtext — not narration.
- The shared Common People journal tracks up to three active lives: the people whose stories most recently surfaced through an event, law reaction, world response, milestone, or direct check-in. It is not Layla-owned and it is not a full catalogue.
- Every active event image is custom generated, reviewed, converted to DDS, and audited at 600x400. No visible event now relies on a generic vanilla video placeholder.
- No new buildings, laws, or map changes. This is not a mechanics mod. It sits on top of the base game and adds what the base game can't: ordinary lives, observed closely, while you play empires.

A sample of the monthly journal, the month her husband Ahmed is at the front:

> She is thinking about the shaving-water he left in its clay jar. It has gone green. She has not emptied it.
>
> She is sweeping a floor that is already swept, because sitting still is the worst of the hours.
>
> She is hoping, in the quietest part of her, only to know. Either way. Only to know.

---

## Status

**v0.4 — rebuild/playtest phase.** Not on the Steam Workshop yet.

- Layla is Person 1 of N, not a special infrastructure lane. She is playable end-to-end: intro event, life events tied to your laws and wars, her husband's conscription, possible widowhood. Fifteen additional people now have audited first-pass scaffolds.
- Egypt-first because that's where the author lives and can get the specifics right. The framework is nation-agnostic.
- Target game version: Victoria 3 **1.13.x**. Metadata currently supports `1.13.*`; static validation detects the installed local build as `release/1.13.8`. Runtime proof uses `script/audit-victoria3-logs.py --require-current-build`, which rejects logs from older game builds or logs older than the shipped mod files.
- Multi-person roster scaffolding is checked with `script/audit-person-roster.py`; the current scaffold has 16 registered persons, including ten conditional entrants, and counts person-owned subnamespaces such as `cp_layla_vox.*`. `documentation/person-selection-ledger.md` records the current first-contact, monthly, and conditional-entry weights; `documentation/person-contract-ledger.md` proves every person has the same setup, hook, yearly, ambient, audio/art, and generated QA surfaces; `documentation/event-firing-ledger.md` maps every visible event to a production route; `documentation/world-response-ledger.md` maps visible events to startup, monthly, law, technology, building, war, revolution, yearly/date, and chain hooks; and `documentation/motion-art-ledger.md` proves there are currently no moving event plates or vanilla video placeholders left. Generated Layla and non-Layla debug queues keep visible-event QA coverage complete without console-thread popups.
- Routine event pacing is an audited contract, not per-character luck. `script/audit-event-pacing.py` targets 1-2 automatic Common People beats per year across the whole roster, never per person, with a hard cap of two. Ambient, startup first-contact, law-reaction, and routine world-response popups share that same cooldown lane so rapid reform, technology, and building years stay quiet. `documentation/event-pacing-ledger.md` records the current proof.
- Player-facing localization is guarded against the broken ruler-audience pattern seen in early tests: `script/audit-localization-dynamic-scope.py` and `documentation/localization-dynamic-scope-ledger.md` reject direct tag scopes such as `[c:EGY...]`, unsupported `GetRuler.GetTitle`, and unreviewed dynamic localization expressions.
- Event audio is audited beyond mere presence: `script/audit-event-audio.py` proves every visible event has a valid opened cue, while `script/audit-audio-palette.py` and `documentation/audio-palette-ledger.md` keep the seven-stinger palette varied across the roster.
- Character art direction is also audited: `script/audit-character-art-contract.py` requires every registered person to have a reusable historical-scene prompt contract, `documentation/character-seed-prompt-ledger.md` records the roster-wide 48-prompt seed batch, and `script/export-character-seed-prompts.py` turns the per-person seed prompts into a generation-ready `gpt-image-2` manifest so future stills and portraits do not fall back into one-off, Layla-only art habits.
- Development readiness is checked with `script/audit-release-readiness.py --mode dev`; strict script/art/runtime dry-runs use `script/audit-release-readiness.py --mode release --skip-egypt-save`; full release readiness requires `script/audit-release-readiness.py --mode release --egypt-save <tested-save>.v3`. Runtime/release proof needs both current-build logs and a real Egypt gameplay save. For user-driven live testing, `script/audit-live-test-state.sh` watches the current process/log/save state without launching or closing the game.
- Adding more characters is purely additive by design — see `documentation/characters/_shared/adding-a-new-person.md`.

---

## Install

The mod is not on Workshop. You clone the repo, then link the `mod/` subfolder (not the repo root) into your Victoria 3 mods directory.

### Windows

Open a terminal and run:

```
mklink /j "%USERPROFILE%\Documents\Paradox Interactive\Victoria 3\mod\common-people" "X:\path\to\common-people-victoria3-mod\mod"
```

Replace `X:\path\to\common-people-victoria3-mod` with wherever you cloned the repo.

### Linux

```
ln -s "/path/to/common-people-victoria3-mod/mod" "$HOME/.local/share/Paradox Interactive/Victoria 3/mod/common-people"
```

### macOS

```
ln -s "/path/to/common-people-victoria3-mod/mod" "$HOME/Library/Application Support/Paradox Interactive/Victoria 3/mod/common-people"
```

### Enable and launch

1. Open the Paradox launcher.
2. Under **Mods**, Common People should appear. Add it to a playset.
3. Launch Victoria 3. Start a new game as **Egypt**.
4. On game start, Common People makes one first-contact roll. It may introduce any always-on starting person, or any conditional person whose world gates are already true for that start date/save state, or it may stay quiet and let the monthly ambient router introduce the roster later. If no Common People events ever appear, see **Troubleshooting** below.

---

## How to play

Start as Egypt. Play the game normally. The mod reacts to your decisions:

- Pass **homesteading** — the change can belong to Layla's deed or the Bey's opened gate.
- Restore **serfdom** (or fail to abolish it) — the old land order returns to the room.
- Go to **war** — Yusuf may be called up, and Layla's household may be pulled into the front.
- Pass **property, school, health, worker-protection, or welfare laws** — the shared dispatcher picks whose life the reform touches this time.
- Advance **technology** or build modern infrastructure — railways, ports, records, electricity, telephones, machine tools, and engines can introduce new people.

Open the Common People journal entry from the left-side panel to see up to three currently active lives and their check-in buttons while playtesting. Most of the mod's content is event windows; the shared router decides whose life rises to the surface.

---

## What playtesters can help with

If you try the mod in its current state, the most useful feedback is:

1. **Does the prose land?** Read an event and tell me whether it hit or felt overwritten. Honest is useful; polite isn't.
2. **Who should get the next deep arc?** Specific pitches win. *"A Silesian weaver watching the mechanical looms arrive in 1848"* is actionable; *"a Polish character"* is not.
3. **Bug reports.** If an event doesn't fire, a variable shows garbled text, or the journal breaks — open a GitHub issue with a screenshot and, if possible, the last few lines of `error.log` from your V3 logs folder.

---

## Known limitations

Being honest up front, so you know what you're getting:

- **Some ambient events may re-fire after their seen cooldowns** on long playthroughs. The global pacing audit still keeps routine automatic Common People popups at the 1-2/year target with a hard cap of two across the full roster.
- **Named-neighbour integration is half-complete.** About half the events reference the named village census (Umm Mariam, Hajj Rashid, Badr, Sheikh Abdallah). The other half still say "the neighbour" or "the baker." Being woven in progressively.
- **Layla is still the only mature arc.** Fifteen more people now have initial scaffolds, but their stories are not Layla-depth yet.
- **One-shot crossroads lock permanently.** If you send Layla to Cairo, she goes. No reverse.
- **Not yet multi-language.** Localization exists in English. The `script/generate-localization.sh` script copies English into the other language folders as a fallback, but no real translation has been done.

## Troubleshooting

**No Common People event appeared.**
- Confirm you started as Egypt (tag `EGY`).
- Confirm the mod is enabled in your playset and the launcher shows it loaded.
- Check `~/Documents/Paradox Interactive/Victoria 3/logs/error.log` (Windows) or the equivalent on your OS for errors mentioning `cp_*`.
- Open an issue with the log excerpt.

**The game crashes on load.**
- Almost always a mod conflict with another mod that touches `on_actions` or startup. Try loading Common People alone first.
- If it still crashes alone, that's a bug — please report it with the crash dump.

**The localization shows placeholder text like `cp_layla.1.d`.**
- The `.yml` file is not being loaded. Most common cause: the file lost its BOM (byte-order mark) during transfer. Check with `xxd mod/localization/english/cp_layla_l_english.yml | head -1` — the first three bytes must be `ef bb bf`. If they're not, the file is corrupted.

---

## Design doc, architecture, contributing

- **Design doc:** `documentation/the-holy-grail.md`. The full pitch and a modding guide for anyone curious how it's built or wanting to extend it.
- **Adding a character:** `documentation/characters/_shared/adding-a-new-person.md`. The 7-step recipe for Person 2+.
- **Architecture overview:** `CLAUDE.md`. The top-level conventions: file prefixes, variable naming, firing gatekeepers, event budget.
- **Audit of the current state:** `documentation/audit-v0.5-rebuild.md`.

Pull requests welcome. Prose edits especially welcome — if a line doesn't read right to you, open a PR with a better one. The voice should be consistent, but it doesn't have to be mine.

---

## Credits

- Built from the [common-people Victoria 3 mod template](https://github.com/common-people).
- Tone and voice owe an unpayable debt to Naguib Mahfouz's *Cairo Trilogy*.
- Event imagery: Victoria 3 base-game assets and hand-curated additions (see `image/`).
- Author: see commit history.

## License

Mod code is released under the same terms as the parent template. Prose content is authored by the mod author — attribution appreciated if reused.
