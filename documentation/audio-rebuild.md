# Common People audio rebuild

Date: 2026-05-26

This is the working audio contract for the v0.5 rebuild. The immediate goal is that visible events are no longer silent or generic: each event should open with a deliberate cue that matches its narrative weight.

## Implemented now

- All 356 visible non-debug Common People events keep the vanilla notification cue on creation:
  - `event:/SFX/UI/Alerts/event_appear`
- Visible events now use validated Victoria 3 music stingers on open:
  - `event:/MUSIC/Stingers/events/tranquil`
  - `event:/MUSIC/Stingers/events/civil`
  - `event:/MUSIC/Stingers/events/political`
  - `event:/MUSIC/Stingers/events/dramatic`
  - `event:/MUSIC/Stingers/events/sadness`
  - `event:/MUSIC/Stingers/events/spiritual`
  - `event:/MUSIC/Stingers/events/enthusiastic`
- The local static audit validates these paths against the installed game's `sound/GUIDs.txt` when available.
- The focused audio audit requires every visible event to use one of the seven reviewed Victoria 3 event music stingers on open. Room/crowd/banner SFX can still be added later as secondary sound design only after a proven script pattern exists; they must not replace the music stinger.

Current palette count:

```text
26  civil
34  dramatic
27  enthusiastic
22  political
42  sadness
10  spiritual
195 tranquil
```

The large tranquil count is intentional for the conversation system. Most dialogue responses are private, small, and low-pressure; the stronger stingers are reserved for war, death, law shock, protest, spiritual ritual, genuine breakthroughs, and ruler-audience scenes whose stakes are political rather than reflective.

## Victoria 3 audio boundary

Victoria 3 event windows expose `on_created_soundeffect` and `on_opened_soundeffect`. The installed game GUI plays the latter through `Event.GetOnOpenedSoundEvent`.

The installed 1.13.8 game also has a separate music system under `game/music/`. Local evidence:

- `game/gui/eventwindow.gui` contains `soundeffect = "[Event.GetOnOpenedSoundEvent]"` in the event-window opening state.
- `game/sound/GUIDs.txt` contains the seven event stingers used by Common People under `event:/MUSIC/Stingers/events/`.
- `game/music/music.md` documents long-form tracks with `music = "event:/..."`, `mood = yes/no`, cooldowns, and validity triggers.
- `game/music/music.txt` and `game/music/main_themes/music.txt` define mood tracks and main themes. These are not event block fields.

That means Common People can safely attach short music stingers directly to events today. A full custom score is a separate music-bank/FMOD pipeline: it needs shipped audio banks plus GUID paths before script can reference new `event:/MUSIC/...` entries.

The mod must not invent `music = ...` fields inside event blocks unless vanilla proves such syntax exists.

For now, "audio with events" means event-open music stingers. A later full-score pass can add custom mood tracks, secondary SFX, or FMOD banks only after the asset pipeline is proven in-game.

## Audit rule

`script/audit-common-people.py` now checks:

- every visible non-debug event has `on_opened_soundeffect`
- every event audio path exists in the local Victoria 3 `sound/GUIDs.txt`, when the file can be found

`script/audit-event-audio.py` is the focused audio proof. It checks every visible non-debug event for:

- exactly one `on_created_soundeffect`
- `event:/SFX/UI/Alerts/event_appear` as the creation cue
- exactly one `on_opened_soundeffect`
- a reviewed Victoria 3 music stinger under `event:/MUSIC/Stingers/events/`
- GUID validity against the installed game when `sound/GUIDs.txt` is available

`script/build-audio-cue-ledger.py` is the review ledger generator. It records every visible non-debug event id, localized title, selected cue, and source line in `documentation/audio-cue-ledger.md`, so cue choices can be reviewed as content rather than hidden in event script.

```bash
script/build-audio-cue-ledger.py
script/build-audio-cue-ledger.py --check
```

`script/audit-audio-palette.py` is the variety guard. It keeps the rebuild from sliding back into "everything tranquil" by checking that all seven event stingers are used, tranquil remains below 70% of visible cues, at least 25% of cues are non-tranquil, and non-Layla people with multiple scenes have more than one cue type. `script/build-audio-palette-ledger.py` writes the summary to `documentation/audio-palette-ledger.md`.

```bash
python3 script/audit-audio-palette.py
python3 script/build-audio-palette-ledger.py --check
```

Set `CP_V3_GAME_DIR` to point at a different installed Victoria 3 `game/` directory if needed:

```bash
CP_V3_GAME_DIR="/path/to/Victoria 3/game" script/audit-common-people.py
```

Current focused audit:

```text
Common People event audio audit
Visible non-debug events: 356
Game dir: /media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game
Audio GUID validation: enabled: /media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game/sound/GUIDs.txt
Event window opened hook: enabled
Music definition files: 3
Created sounds:
  356  event:/SFX/UI/Alerts/event_appear
Opened cues:
   26  civil
   34  dramatic
   27  enthusiastic
   22  political
   42  sadness
   10  spiritual
  195  tranquil
Issues: 0
```

Current palette audit:

```text
Common People audio palette audit
Visible non-debug events: 356
Music cue categories used: 7/7
Tranquil share: 195/356 (54.8%)
Non-tranquil share: 161/356 (45.2%)
Issues: 0
```

## In-game QA

Listen specifically to:

- `cp_layla.1` intro: tranquil
- `cp_layla.2` homesteading deed: political
- `cp_layla.3` serfdom restored: dramatic
- `cp_layla.4` Ahmed conscripted: dramatic
- `cp_layla.41` Ahmed death letter: sadness
- `cp_layla.80` Layla death: sadness
- `cp_layla_vox.102` land petition: political
- `cp_layla_vox.1021` ruler dismisses the land petition: sadness
- `cp_layla_vox.1023` ruler's cruel reply: dramatic
- one `cp_layla_vox.*` conversation opener and one follow-up response
- `cp_bey.20` Homesteading from the landlord side: dramatic
- `cp_soldier.20` war notice: dramatic
- `cp_soldier.21` return from war: sadness
- `cp_samier.10` factory arrival: tranquil
- `cp_samier.20` worker protections: political
- `cp_tarek.10` mill ledger: tranquil
- `cp_tarek.20` worker protections from the owner's office: political
- `cp_nour.10` cedar chest: tranquil
- `cp_nour.20` name on the paper: political
- `cp_mina.10` printer's workshop: tranquil
- `cp_mina.20` public-school primer: enthusiastic
- `cp_zaynab.10` brass basin: spiritual
- `cp_zaynab.20` public-health doctor: civil
- `cp_farid.10` railway platform: enthusiastic
- `cp_farid.20` telegraph wire: civil
- `cp_dawud.20` cargo crane: dramatic
- `cp_dawud.30` steamship quay: enthusiastic
- `cp_rashid.30` identity paper: political
- `cp_salma.20` first electric light: enthusiastic
- `cp_salma.30` radio/telephone voices: political
- `cp_karim.10` machine teeth: civil
- `cp_karim.30` factory injury: dramatic
- `cp_huda.10` rented room: civil
- `cp_huda.40` rent book: dramatic
- `cp_mansur.20` first wage token: enthusiastic
- `cp_nabil.30` rifles by the bakery: dramatic
- `cp_nabil.40` square afterwards: political

If a stinger feels too loud, too grand, or too repetitive, retune that event id directly rather than changing the whole category.
