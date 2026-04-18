# V3 Decisions, Journal Entries, and Game Events

## Key Journal Entries We Can Hook Into

These are base game journal entries. We can check if they're active/completed and have our characters react to them.

### American Civil War
- `je_acw_countdown` -- The Slavery Debate
- `je_acw_war` -- The American Civil War
- `je_acw_reconstruction` -- Reconstruction (12 years)
- `je_acw_equality` -- Equality for All

### Japanese Meiji Restoration
- `je_meiji_restoration` -- Restore Emperor over Shogun
- `je_meiji_main` -- Main modernization journal
- `je_meiji_economy` -- Industrialize Japan
- `je_meiji_army` -- Retire the Samurai
- `je_meiji_diplomacy` -- End Sakoku (isolationism)

### Canal Construction
- Suez Canal: "The Suez Survey" -> "Construct the Suez Canal"
- Panama Canal: "The Panama Survey" -> "Construct the Panama Canal"

### Other Major Entries
- Government Petition -- IG petitions for legislation
- The Great Hunger -- Crop failures and famine
- Springtime of the Peoples -- 1848 liberal movements
- The Red Scare -- Communist threat
- From Farms to Factories -- Industrial peasant decline
- Krakatoa eruption -- volcanic event chain

## Detecting Journal Entry Status

```
# Check if a journal entry is active
has_journal_entry = je_type_name

# On-actions for journal lifecycle
on_journal_entry_activated
on_journal_entry_completed
on_journal_entry_deactivated
on_journal_entry_failed
```

## Decisions

Decisions go in `common/decisions/`. Key existing decisions:
- Ban/remove goods (opium, liquor)
- Hold a Grand Exhibition
- Canal surveys and construction
- Country-specific: British Raj, Canadian confederation, etc.

No direct `on_decision_taken` on_action, but decisions can fire events through their `when_taken` block.

## Diplomatic Play Types

1. Annex Subject
2. Ban Slavery
3. Conquer State
4. Cut Down To Size
5. Humiliate
6. Independence
7. Liberate Subject
8. Return State
9. Take Treaty Port
10. Unify Germany/Italy/etc.

```
# Check diplomatic plays
any_diplomatic_play = { ... }
any_scope_play_involved = { ... }
```

## Revolution Events (33+ types)

The base game has extensive revolution events we can hook into:
- Membership Lists Discovered
- The Infernal Machine (assassination attempt)
- Ersatz Food (shortages)
- Sailors Stay Ashore (mutiny)
- The Mob Approaches
- Stochastic Terror (bombings)
- Under No Pretext (trade union activity)
