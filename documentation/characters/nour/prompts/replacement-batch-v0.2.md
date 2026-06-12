# Nour replacement image batch v0.2

Date: 2026-05-30

Purpose: replace Nour's remaining vanilla/generic event videos with Common People generated art. This finishes her active slice so all visible Nour events use mod-owned still art centered on household paper, keys, receipts, registers, and accounts.

Generated with: `gpt-image-2`

Shared visual contract for every prompt:

```text
Use case: historical-scene
Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400
Primary request: Generate one painted historical realism event image for Common People.
Subject: Nour, a Misri Sunni woman around 31 in late-19th-century Lower Egypt; practical modest clothing and headscarf, shopkeeper household, composed and intelligent rather than theatrical.
Style/medium: painterly historical realism, textured oil-paint surface, natural anatomy, grounded materials, 19th-century Egypt, quiet human scale.
Composition/framing: close-medium or medium-wide. Put the essential face, action, and required object in the left half or center-left; right half can carry shelves, walls, doorway, or atmosphere.
Constraints: no readable text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no palace grandeur, no decorative atmosphere without the required object.
```

## Batch targets

| Priority | Asset | Active windows | Main event families |
|---:|---|---:|---|
| 1 | `cp_nour_rent_receipt_v02.dds` | 1 | rent receipt with Nour's name |
| 2 | `cp_nour_key_under_pillow_v02.dds` | 1 | private key and cedar chest |
| 3 | `cp_nour_register_shelf_v02.dds` | 1 | government register shelf |
| 4 | `cp_nour_morning_account_v02.dds` | 1 | morning shop account |

## Prompt 1 - The Rent Receipt

```text
Event: cp_nour.30 - "The Rent Receipt"
Narrative function: a receipt with Nour's own name changes the household room more than the rent itself.
Subject: Nour in modest shopkeeper clothing, steady and insistent.
Scene/backdrop: modest market-room or back room above a shop selling cloth and lamp oil; landlord's nephew at a low table, brother-in-law silent near the doorway.
Foreground action: Nour points gently but firmly to where her own name should be written while the young man begins the receipt again.
Required object/gesture: rent receipt paper, pen, ink, and Nour's hand indicating the page, no readable text.
Background detail: cloth shelves, lamp oil jars, doorway, muted household goods.
Lighting/mood: late afternoon shop light, legal power becoming ordinary, quiet tension.
Avoid: business contract scene, modern office, court hearing, readable form, grand legal victory pose.
```

## Prompt 2 - The Key Under the Pillow

```text
Event: cp_nour.40 - "The Key Under the Pillow"
Narrative function: property security is private and tactile, carried by a key warm from her hand.
Subject: Nour in predawn lamplight, composed and watchful.
Scene/backdrop: small room above a shop, cedar chest nearby, folded bedding, plain walls, faint street light through a shutter.
Foreground action: Nour sits at the edge of a low bed or mat and touches the small metal key under her pillow.
Required object/gesture: key half-visible under the pillow and Nour's hand touching it; cedar chest visible nearby.
Background detail: folded cloth, lamp, leaking winter corner or rough plaster wall.
Lighting/mood: predawn lamplight, private security, cautious self-possession, no melodrama.
Avoid: romantic bedroom staging, palace interior, jewelry-box glamour, oversized symbolic key.
```

## Prompt 3 - The Register Shelf

```text
Event: cp_nour.50 - "The Register Shelf"
Narrative function: the state becomes visible as a shelf holding her name where a brother-in-law cannot move it.
Subject: Nour bending close to an opened register, wary but steady.
Scene/backdrop: provincial Egyptian government records office, old plaster wall, tall dusty shelf, heavy ledger volume, clerk's desk, small window.
Foreground action: a clerk opens the register while Nour leans near enough to see the page.
Required object/gesture: large register volume, high dusty shelf, Nour leaning toward the open page, no readable text.
Background detail: stacked records, ink pot, distant clerk, dust in window light.
Lighting/mood: dusty office daylight, official paper as witness, wary relief.
Avoid: telegraph office as the focus, modern files, courtroom, readable labels, heroic bureaucracy scene.
```

## Prompt 4 - The Morning Account

```text
Event: cp_nour.60 - "The Morning Account"
Narrative function: confidence arrives as a clean account line before anyone asks why.
Subject: Nour in a small market-room, quietly confident.
Scene/backdrop: shop before the street fully wakes, shelves of cloth, lamp oil jars, thread, low account table, shutters beginning to lift outside.
Foreground action: Nour balances small money beside an oil lamp and writes numbers slowly in an account paper.
Required object/gesture: coins set in a row, account paper with no readable text, lamp, Nour's hand drawing a line under the account.
Background detail: folded cloth, jars, spools, street doorway, muted early customers outside.
Lighting/mood: early morning lamp and pale street light, ordinary confidence, small exactness, gentle hope.
Avoid: cafe scene, modern cash register, readable account book, abundant wealth, staged portrait.
```

## Built-in image generation output

- `cp_nour_rent_receipt_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a8d8d4b2c819182c0876e2ec35195.png`
- `cp_nour_key_under_pillow_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a8de26e848191b84014be4df1b099.png`
- `cp_nour_register_shelf_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a8e2db454819194762e1be79eb3b2.png`
- `cp_nour_morning_account_v02`: `/home/aboelsoud/.codex/generated_images/019e60b3-1ea6-74b1-aac6-f7bc8ce59ffb/ig_0ff49571cacbebfc016a1a8edae2ec8191a71f29219edc95a4.png`

## Workspace archive

- `image/generated/nour/v0.2/cp_nour_rent_receipt_v02_1536.png`
- `image/generated/nour/v0.2/cp_nour_rent_receipt_v02.dds.png`
- `image/generated/nour/v0.2/cp_nour_key_under_pillow_v02_1536.png`
- `image/generated/nour/v0.2/cp_nour_key_under_pillow_v02.dds.png`
- `image/generated/nour/v0.2/cp_nour_register_shelf_v02_1536.png`
- `image/generated/nour/v0.2/cp_nour_register_shelf_v02.dds.png`
- `image/generated/nour/v0.2/cp_nour_morning_account_v02_1536.png`
- `image/generated/nour/v0.2/cp_nour_morning_account_v02.dds.png`

## Shipped DDS

- `mod/gfx/event_pictures/cp_nour_rent_receipt_v02.dds`
- `mod/gfx/event_pictures/cp_nour_key_under_pillow_v02.dds`
- `mod/gfx/event_pictures/cp_nour_register_shelf_v02.dds`
- `mod/gfx/event_pictures/cp_nour_morning_account_v02.dds`

## Verification commands after generation

```bash
python3 script/export-art-batch-prompts.py --all --check
script/audit-art-batch-plan.py --all
script/build-art-acceptance-ledger.py --check
script/build-image-contact-sheets.py
script/build-image-contact-sheets.py --check
script/audit-event-images.py
script/audit-generic-video-art.py
script/audit-release-readiness.py --mode dev
```
