# V3 Cultures, Religions, and Discrimination

## Key Cultures for Our Mod

### Egypt
- `cu:misri` -- Egyptian (primary)
- `cu:bedouin` -- Bedouin
- Plus: Beja, Sudanese, Dinka, Nuer, Nuba

### Ottoman Empire
- Turkish, Greek, Armenian, Kurdish, Albanian, Bosniak, Serbian, Croatian, Bulgarian, Mashriqi, Bedouin, Georgian, Romanian, Assyrian

### India
- Bengali, Hindi, Punjabi, Tamil, Telugu, Marathi, Gujarati, etc.

### China
- Manchu, Han (primary); Cantonese, Wu, Min, Hakka, Tibetan, Mongol, Uighur

### Japan
- Japanese (Yamato); Ainu

### Russia
- Russian (primary); Ukrainian, Belarusian (accepted); Tatar, Don Cossack, etc.

**Total: 315 cultures in V3, 302 present at game start in 1836**

## Religions

### With Taboos (Important for Events)
| Religion | ID | Taboo Goods |
|----------|----|------------|
| Sunni Islam | `rel:sunni` | Liquor, Wine |
| Shiite Islam | `rel:shiite` | Liquor, Wine |
| Ibadi Islam | `rel:ibadi` | Liquor, Wine |
| Hindu | `rel:hindu` | Meat |
| Jewish | `rel:jewish` | Groceries |

### Without Taboos
- `rel:catholic`, `rel:protestant`, `rel:orthodox`, `rel:oriental_orthodox`
- `rel:sikh`, `rel:theravada`, `rel:mahayana`, `rel:gelugpa`
- `rel:confucian`, `rel:shinto`, `rel:animist`, `rel:atheist`

Taboo mechanic: pops purchase 50% of restricted goods.

## Discrimination System

### Acceptance Levels (0-100 score)
| Status | Score | Effects |
|--------|-------|---------|
| Violent Hostility | 0-19 | Can't vote, work military, or upper jobs |
| Cultural Erasure | 20-39 | Can't vote, work military, or upper jobs |
| Open Prejudice | 40-59 | -20% wages, -20% political strength |
| Second-class Citizen | 60-79 | -10% wages, -10% political strength |
| Full Acceptance | 80-100 | No penalties |

### Modding Checks
```
# Check country's primary culture
country_has_primary_culture = cu:misri

# Check religion
has_state_religion = rel:sunni

# Check discrimination in pop scope
# Lower acceptance = more radicalism, higher emigration desire
```

## Culture Definition Structure
```
culture_name = {
    religion = religion_name
    heritage = heritage_trait
    language = language_trait
    traditions = { tradition_list }
    male_common_first_names = { ... }
    female_common_first_names = { ... }
    common_last_names = { ... }
    ethnicities = { 1 = arab }
    graphics = arabic
}
```

Heritage, language, and tradition traits determine discrimination. Shared traits = higher acceptance.

## Assimilation
- Base: 0.2% monthly
- Public Schools: +12.5% per level
- Cultural Erasure: +5% bonus
- Open Prejudice: +15% bonus
- Cultural Fervor (0-100): higher = lower assimilation
