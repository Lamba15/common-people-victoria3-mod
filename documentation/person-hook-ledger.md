# Person Hook Surface Ledger

Generated from live Paradox script. Rebuild with `python3 script/build-person-hook-ledger.py`.

This ledger shows what each registered person's standard hook surface actually does. The person contract ledger proves every hook exists; this file makes no-op hooks, maintenance hooks, world responses, law reactions, milestones, and raw triggers reviewable so Layla cannot quietly become a special infrastructure lane again.

Cell key: `noop` means an intentional placeholder, `life` means yearly age/SoL maintenance, `state` means non-popup variable work, `amb:N`, `law:N`, `world:N`, `mile:N`, and `button:N` count unique events fired through the shared gatekeepers, and `raw-hidden:N` is allowed hidden setup plumbing. `raw-visible:N` is a failure because visible event windows must use a gatekeeper.

## Summary

- Registered persons: 16
- Dispatcher hooks inspected: 144
- Active dispatcher hooks: 61
- Intentional no-op dispatcher hooks: 83
- Visible person-owned events: 356
- Layla visible events: 266
- Non-Layla visible events: 90
- Raw visible hook triggers: 0
- Ledger issues: 0

## Hook Matrix

| Person | Startup | Monthly | Yearly | Law | War Start | War End | Tech | Building | Revolution | Ambient Pool | Try Spawn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bey | noop | noop | life | law:1 | noop | noop | world:1 | world:1 | noop | amb:2 | - |
| dawud | noop | noop | life+world:1 | law:1 | noop | noop | world:2 | world:2 | noop | amb:3 | raw-hidden:1 |
| farid | noop | noop | life+world:2 | noop | noop | noop | world:3 | world:2 | noop | amb:3 | raw-hidden:1 |
| huda | noop | noop | life+world:4 | noop | noop | noop | world:3 | world:3 | noop | amb:5 | raw-hidden:1 |
| karim | noop | noop | life+world:2 | noop | noop | noop | world:2 | world:4 | noop | amb:3 | raw-hidden:1 |
| layla | state | state | life+mile:13 | state+law:25 | state+mile:1 | state+mile:2 | state+world:3 | state+world:1 | state+mile:1 | amb:31 | - |
| mansur | noop | noop | life+world:5 | noop | noop | noop | world:2 | world:4 | noop | amb:6 | raw-hidden:1 |
| mina | noop | noop | life | noop | noop | noop | world:1 | world:1 | noop | amb:3 | - |
| nabil | noop | noop | life+world:2 | law:3 | noop | noop | noop | noop | state+world:1 | amb:4 | raw-hidden:1 |
| nour | noop | noop | life+world:1 | noop | noop | noop | world:1 | world:1 | noop | amb:3 | - |
| rashid | noop | noop | life+world:1 | law:1 | noop | noop | world:2 | world:2 | noop | amb:3 | raw-hidden:1 |
| salma | noop | noop | life+world:3 | noop | noop | noop | world:5 | world:3 | noop | amb:4 | raw-hidden:1 |
| samier | noop | noop | life+world:2 | law:1 | noop | noop | world:1 | world:2 | noop | amb:4 | raw-hidden:1 |
| soldier | noop | noop | life+world:1 | noop | state+mile:1 | mile:1 | world:1 | world:1 | noop | amb:3 | - |
| tarek | noop | noop | life+world:2 | law:1 | noop | noop | world:1 | world:2 | noop | amb:4 | raw-hidden:1 |
| zaynab | noop | noop | life+world:1 | noop | noop | noop | world:1 | world:1 | noop | amb:3 | - |

## Content Depth Backlog

This table is deliberately descriptive, not a failing gate: a new person can land with a small scaffold, but the imbalance stays visible until the roster has enough authored beats to feel as grand as Layla's branch.

| Person | Visible Events | Active Hooks | No-op Hooks | Hook Action Score |
|---|---:|---:|---:|---:|
| bey | 6 | 4 | 5 | 6 |
| dawud | 6 | 4 | 5 | 11 |
| farid | 6 | 3 | 6 | 12 |
| huda | 6 | 3 | 6 | 17 |
| karim | 6 | 3 | 6 | 13 |
| layla | 266 | 9 | 0 | 86 |
| mansur | 6 | 3 | 6 | 19 |
| mina | 6 | 3 | 6 | 6 |
| nabil | 6 | 3 | 6 | 13 |
| nour | 6 | 3 | 6 | 7 |
| rashid | 6 | 4 | 5 | 11 |
| salma | 6 | 3 | 6 | 17 |
| samier | 6 | 4 | 5 | 12 |
| soldier | 6 | 5 | 4 | 10 |
| tarek | 6 | 4 | 5 | 12 |
| zaynab | 6 | 3 | 6 | 7 |
