# Mina

## Profile

Mina is a Misri Orthodox printer's apprentice in Cairo, nineteen in 1836, living between the press, the church courtyard, and the street where news becomes rumor before ink dries. He is not a politician. He knows reform first as paper: primers, notices, petitions, correction slips, and the one backward letter that can shame a whole sentence.

## Mechanical Identity

| Field | Value |
|---|---|
| Token | `mina` |
| Country | `EGY` |
| Culture | `misri` |
| Religion | `orthodox` |
| Home state | `STATE_LOWER_EGYPT` |
| Starting profession | `clerks` |
| Starting age | `19` |
| Entry/routing | Always-on startup person, routed through `cp_shared_startup.1`, `cp_mina.1`, and person-owned dispatchers |

## Current Slice

- `cp_mina.1` hidden setup initializes his country variables and state marker.
- `cp_mina.10` introduces the press, the type case, and the workshop as his baseline ambient beat.
- `cp_mina.20` reacts to `law_public_schools`, sharing the trigger with Layla's school beat so the reform produces one street-level story instead of duplicate popups.
- `cp_mina.30` reacts to modern records technology through his tech dispatcher, turning state paperwork into a print-shop scene.
- `cp_mina.40` adds a quiet ambient proofing beat so his life can surface outside formal reform moments.
- `cp_mina.50` reacts to universities and government offices through the shared world-response lane, making modernization visible as catalogue work instead of another Layla-only popup.
- `cp_mina.60` adds a church-courtyard notice beat to his ambient pool, still spending the global 1-2/year visible-story budget.

## Art Coverage

- `cp_mina.10` and `cp_mina.20` use the v0.1 generated print/education set.
- `cp_mina.30`, `.40`, `.50`, and `.60` use the v0.2 generated replacement set, removing Mina's remaining vanilla/generic event videos.
- All active Mina event art is composed with the essential person/action/object on the left or center-left so the Victoria 3 event text panel can cover the right half without hiding the story.

## Personality Weights

| Topic | Weight | Notes |
|---|---:|---|
| Education | 10 | Letters are craft before doctrine. |
| Work | 8 | He thinks through hands, ink, fatigue, and mistakes. |
| City | 8 | Cairo is opportunity and danger in the same doorway. |
| Religion | 7 | A private grammar of belonging, not a sermon machine. |
| Politics | 5 | Public power arrives as paper someone ordered him to print. |

## Tone

Write Mina through material literacy: lead type, damp paper, ink under nails, shop talk, copied forms, and the unease of being visible as both useful and minor. His scenes should make education and public opinion feel like handmade things.
