# Audio Palette Ledger

Generated from visible non-debug event audio hooks. Rebuild with:

```bash
python3 script/build-audio-palette-ledger.py
python3 script/build-audio-palette-ledger.py --check
python3 script/audit-audio-palette.py
```

This ledger is the review surface for whether Common People's event music still feels deliberate as the roster expands. `documentation/audio-cue-ledger.md` records every individual event cue; this file summarizes palette balance and per-person variety.

## Contract

- Every visible event already has one creation cue and one opened cue, enforced by `script/audit-event-audio.py`.
- The seven reviewed Victoria 3 event stingers should all remain in use: civil, dramatic, enthusiastic, political, sadness, spiritual, tranquil.
- Tranquil can dominate quiet conversation scenes, but it must not exceed 70% of visible event cues overall.
- At least 25% of visible events should use a non-tranquil cue so laws, war, death, reforms, protest, spirituality, and breakthroughs do not feel flat.
- Non-Layla people with two or more visible events need at least two cue types; non-Layla people with four or more visible events need at least three cue types.

## Summary

- Visible non-debug events: 356
- Music cue categories used: 7/7
- Tranquil share: 195/356 (54.8%)
- Non-tranquil share: 161/356 (45.2%)
- Issues: 0

## Palette Counts

| Cue | Events | Share |
|---|---:|---:|
| `civil` | 26 | 7.3% |
| `dramatic` | 34 | 9.6% |
| `enthusiastic` | 27 | 7.6% |
| `political` | 22 | 6.2% |
| `sadness` | 42 | 11.8% |
| `spiritual` | 10 | 2.8% |
| `tranquil` | 195 | 54.8% |

## Person Variety

| Person | Events | Cue Types | Cue Mix |
|---|---:|---:|---|
| `bey` | 6 | 5 | `civil` 1, `dramatic` 2, `political` 1, `sadness` 1, `tranquil` 1 |
| `dawud` | 6 | 6 | `civil` 1, `dramatic` 1, `enthusiastic` 1, `political` 1, `sadness` 1, `tranquil` 1 |
| `farid` | 6 | 5 | `civil` 1, `dramatic` 1, `enthusiastic` 2, `sadness` 1, `tranquil` 1 |
| `huda` | 6 | 5 | `civil` 1, `dramatic` 2, `enthusiastic` 1, `sadness` 1, `tranquil` 1 |
| `karim` | 6 | 3 | `civil` 2, `dramatic` 2, `enthusiastic` 2 |
| `layla` | 266 | 7 | `civil` 6, `dramatic` 20, `enthusiastic` 15, `political` 10, `sadness` 31, `spiritual` 6, `tranquil` 178 |
| `mansur` | 6 | 5 | `civil` 2, `dramatic` 1, `enthusiastic` 1, `sadness` 1, `tranquil` 1 |
| `mina` | 6 | 4 | `civil` 2, `enthusiastic` 1, `spiritual` 1, `tranquil` 2 |
| `nabil` | 6 | 4 | `civil` 2, `dramatic` 1, `political` 1, `tranquil` 2 |
| `nour` | 6 | 4 | `civil` 2, `enthusiastic` 1, `political` 2, `tranquil` 1 |
| `rashid` | 6 | 4 | `civil` 2, `political` 2, `sadness` 1, `tranquil` 1 |
| `salma` | 6 | 6 | `civil` 1, `dramatic` 1, `enthusiastic` 1, `political` 1, `sadness` 1, `tranquil` 1 |
| `samier` | 6 | 5 | `dramatic` 1, `enthusiastic` 1, `political` 1, `sadness` 1, `tranquil` 2 |
| `soldier` | 6 | 5 | `civil` 1, `dramatic` 1, `sadness` 2, `spiritual` 1, `tranquil` 1 |
| `tarek` | 6 | 4 | `dramatic` 1, `enthusiastic` 1, `political` 3, `tranquil` 1 |
| `zaynab` | 6 | 4 | `civil` 2, `sadness` 1, `spiritual` 2, `tranquil` 1 |

## Checks

```bash
script/audit-event-audio.py
script/build-audio-cue-ledger.py --check
python3 script/audit-audio-palette.py
python3 script/build-audio-palette-ledger.py --check
```
